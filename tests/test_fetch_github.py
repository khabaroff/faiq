from __future__ import annotations

import unittest
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

from guides.fetch.base import QueueItem, SourceKind
from guides.fetch.github import fetch_github_repo
from guides.queue import clear_quarantine


class FetchGithubTests(unittest.TestCase):
    def test_repo_fetch_falls_back_to_master_readme(self) -> None:
        item = QueueItem(
            source="https://github.com/example/project",
            source_kind=SourceKind.URL,
            received_at=datetime.now(),
        )

        def fake_get(url: str, **kwargs):
            if url == "https://api.github.com/repos/example/project":
                raise RuntimeError("api down")
            if url == "https://raw.githubusercontent.com/example/project/main/README.md":
                return Mock(status_code=404, text="")
            if url == "https://raw.githubusercontent.com/example/project/master/README.md":
                return Mock(status_code=200, text="# Project\n\nMaster README")
            if url == "https://raw.githubusercontent.com/example/project/HEAD/README.md":
                return Mock(status_code=404, text="")
            raise AssertionError(f"unexpected url: {url}")

        with patch("guides.fetch.github._get_headers", return_value={}), patch("guides.fetch.github.httpx.get", side_effect=fake_get):
            content = fetch_github_repo(item)

        self.assertIn("Master README", content.raw_text)
        self.assertEqual(content.source_meta["fetcher"], "fallback+readme:master")

    def test_clear_quarantine_removes_failed_entry(self) -> None:
        with TemporaryDirectory() as tmpdir:
            quarantine_file = Path(tmpdir) / "needs_review.txt"
            quarantine_file.write_text(
                "#failed# 2026-05-11T10:00:00 boom | https://example.com/post\n#failed# 2026-05-11T10:01:00 boom | https://example.com/other\n",
                encoding="utf-8",
            )
            item = QueueItem(source="https://example.com/post", source_kind=SourceKind.URL, received_at=datetime.now())

            clear_quarantine(quarantine_file, item)

            text = quarantine_file.read_text(encoding="utf-8")
            self.assertNotIn("https://example.com/post", text)
            self.assertIn("https://example.com/other", text)


if __name__ == "__main__":
    unittest.main()
