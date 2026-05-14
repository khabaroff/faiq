from __future__ import annotations

import re
import importlib
import subprocess
import unittest
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

from guides.fetch.base import QueueItem, SourceKind
from guides.fetch.url import JinaFetcher, fetch_url
from guides.fetch.youtube import fetch_youtube


class FetchUrlTests(unittest.TestCase):
    def test_trafilatura_is_used_first(self) -> None:
        item = QueueItem(source="https://example.com/post", source_kind=SourceKind.URL, received_at=datetime.now())

        with patch("guides.fetch.url.validate_url", side_effect=lambda url: url), patch(
            "guides.fetch.url.trafilatura.fetch_url", return_value="<html>body</html>"
        ), patch("guides.fetch.url.trafilatura.extract", return_value="extracted body " + ("x" * 200)) as extract_mock:
            fetch_url(item)

        self.assertTrue(extract_mock.called)

    def test_jina_is_used_after_trafilatura_failure(self) -> None:
        item = QueueItem(source="https://example.com/post", source_kind=SourceKind.URL, received_at=datetime.now())

        with patch("guides.fetch.url.validate_url", side_effect=lambda url: url), patch(
            "guides.fetch.url.trafilatura.fetch_url", return_value=None
        ), patch("guides.fetch.url.trafilatura.extract", return_value=None), patch(
            "guides.fetch.url.get_http_client"
        ) as client_mock, patch("guides.fetch.url.throttle_jina_reader"):
            client = Mock()
            client.get.return_value = Mock(status_code=200, text="jina body " + ("x" * 220))
            client_mock.return_value = client

            content = fetch_url(item)

        self.assertIn("jina body", content.raw_text)
        self.assertEqual(content.source_meta["fetcher"], "jina")

    def test_local_file_source_uses_source_frontmatter_title(self) -> None:
        with TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "05-alf-implementing-claude-code-skills-from-scratch.md"
            source.write_text(
                """---
title: Implementing Claude Code Skills from Scratch
---

## Core idea

Body text
""",
                encoding="utf-8",
            )
            item = QueueItem(source=str(source), source_kind=SourceKind.FILE, received_at=datetime.now())

            content = fetch_url(item)

        self.assertEqual(content.source_meta["title"], "Implementing Claude Code Skills from Scratch")
        self.assertTrue(re.search(r"Implementing Claude Code Skills from Scratch", content.raw_text))

    def test_youtube_rejects_file_scheme(self) -> None:
        item = QueueItem(source="file:///etc/passwd", source_kind=SourceKind.URL, received_at=datetime.now())
        with self.assertRaises(ValueError):
            import asyncio

            asyncio.run(fetch_youtube(item))

    def test_jina_reader_does_not_use_bearer_auth(self) -> None:
        response = Mock(status_code=200, text="x" * 250)

        with patch.dict("os.environ", {"JINA_API_KEY": "jina-test-token"}, clear=False), patch(
            "guides.fetch.url.get_http_client"
        ) as client_mock, patch("guides.fetch.url.validate_url", side_effect=lambda url: url), patch(
            "guides.fetch.url.throttle_jina_reader"
        ):
            client = Mock()
            client.get.return_value = response
            client_mock.return_value = client
            content = JinaFetcher().fetch(
                QueueItem(source="https://www.example.com", source_kind=SourceKind.URL, received_at=datetime.now())
            )

        self.assertEqual(content.raw_text, "x" * 250)
        self.assertEqual(client.get.call_args.args[0], "https://r.jina.ai/https://www.example.com")
        self.assertEqual(client.get.call_args.kwargs["headers"]["Accept"], "text/markdown")
        self.assertNotIn("Authorization", client.get.call_args.kwargs["headers"])

    @patch("guides.fetch.github.validate_url")
    def test_github_blocks_internal_url(self, mock_validate_url) -> None:
        from guides.fetch.github import fetch_github_repo

        mock_validate_url.side_effect = ValueError("Host blocked")
        item = QueueItem(
            source="http://169.254.169.254/root/repo",
            source_kind=SourceKind.URL,
            received_at=datetime.now(),
        )
        with self.assertRaisesRegex(ValueError, "Host blocked"):
            fetch_github_repo(item)


class JinaHelpersTests(unittest.TestCase):
    def test_jina_helpers_build_reader_and_search_headers(self) -> None:
        self.assertIsNotNone(importlib.util.find_spec("guides.fetch.jina"))
        jina = importlib.import_module("guides.fetch.jina")

        with patch.dict("os.environ", {"JINA_API_KEY": "jina-test-token"}, clear=False):
            reader_headers = jina.get_jina_reader_headers()
            search_headers = jina.get_jina_search_headers(respond_with_no_content=True)

        self.assertEqual(reader_headers["Accept"], "text/markdown")
        self.assertNotIn("Authorization", reader_headers)
        self.assertEqual(search_headers["Authorization"], "Bearer jina-test-token")
        self.assertEqual(search_headers["X-Respond-With"], "no-content")

    def test_jina_reader_throttle_waits_for_free_tier_interval(self) -> None:
        jina = importlib.import_module("guides.fetch.jina")
        original_last_request_at = jina._last_reader_request_at

        try:
            jina._last_reader_request_at = 10.0
            monotonic_values = iter([11.5, 13.1])

            with patch("guides.fetch.jina.time.monotonic", side_effect=lambda: next(monotonic_values)), patch(
                "guides.fetch.jina.time.sleep"
            ) as sleep_mock:
                jina.throttle_jina_reader()

            sleep_mock.assert_called_once_with(1.5)
            self.assertEqual(jina._last_reader_request_at, 13.1)
        finally:
            jina._last_reader_request_at = original_last_request_at


if __name__ == "__main__":
    unittest.main()
