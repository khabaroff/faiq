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
from guides.fetch.url import _try_jina, fetch_url


class FetchUrlTests(unittest.TestCase):
    def test_trafilatura_is_used_first(self) -> None:
        item = QueueItem(source="https://example.com/post", source_kind=SourceKind.URL, received_at=datetime.now())

        with patch("guides.fetch.url.trafilatura.fetch_url", return_value="<html>body</html>"), patch(
            "guides.fetch.url.trafilatura.extract", return_value="extracted body " + ("x" * 200)
        ) as extract_mock:
            fetch_url(item)

        self.assertTrue(extract_mock.called)

    def test_cloudflare_markdown_is_preferred_before_jina(self) -> None:
        item = QueueItem(source="https://example.com/post", source_kind=SourceKind.URL, received_at=datetime.now())

        with patch("guides.fetch.url._try_trafilatura", return_value=None), patch(
            "guides.fetch.url._try_cloudflare_markdown", return_value=("cloudflare body", "cloudflare-markdown")
        ) as cloudflare_mock, patch("guides.fetch.url._try_jina") as jina_mock:
            jina_mock.side_effect = AssertionError("jina should not be called when cloudflare succeeds")

            content = fetch_url(item)

        self.assertEqual(content.raw_text, "cloudflare body")
        self.assertEqual(content.source_meta["fetcher"], "cloudflare-markdown")
        self.assertTrue(cloudflare_mock.called)

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

    def test_jina_reader_does_not_use_bearer_auth(self) -> None:
        response = Mock(status_code=200, text="x" * 250)

        with patch.dict("os.environ", {"JINA_API_KEY": "jina-test-token"}, clear=False), patch(
            "guides.fetch.url.httpx.get", return_value=response
        ) as get_mock:
            content = _try_jina("https://www.example.com")

        self.assertEqual(content, ("x" * 250, "jina"))
        self.assertEqual(get_mock.call_args.args[0], "https://r.jina.ai/https://www.example.com")
        self.assertEqual(get_mock.call_args.kwargs["headers"]["Accept"], "text/markdown")
        self.assertNotIn("Authorization", get_mock.call_args.kwargs["headers"])


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
