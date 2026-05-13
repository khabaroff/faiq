from __future__ import annotations

import unittest
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from guides.tools.daily_log import append_log_entry


class DailyLogTests(unittest.TestCase):
    def test_creates_file_with_header_on_first_call(self) -> None:
        with TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "2026-05-13.md"

            with patch("guides.tools.daily_log._get_log_path", return_value=log_path):
                append_log_entry("test-slug", "summary", "gpt-5.4", 1000, 500, 0.01)

            self.assertTrue(log_path.exists())
            content = log_path.read_text(encoding="utf-8")
            self.assertIn("# Daily Pipeline Log", content)
            self.assertIn("| slug | action | model | tokens | cost | time |", content)
            self.assertIn("Total cost:", content)

    def test_accumulates_total_cost_on_multiple_calls(self) -> None:
        with TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "2026-05-13.md"

            with patch("guides.tools.daily_log._get_log_path", return_value=log_path):
                append_log_entry("slug-1", "summary", "gpt-5.4", 1000, 500, 0.01)
                append_log_entry("slug-2", "wiki_tool", "azure-mini", 500, 200, 0.005)

            content = log_path.read_text(encoding="utf-8")

            self.assertEqual(content.count("Total cost:"), 1)
            self.assertIn("Total cost: $0.0150", content)
            self.assertIn("| slug-1 |", content)
            self.assertIn("| slug-2 |", content)

    def test_per_day_naming(self) -> None:
        with TemporaryDirectory() as tmpdir:
            log_path_1 = Path(tmpdir) / "2026-05-13.md"
            log_path_2 = Path(tmpdir) / "2026-05-14.md"

            with patch("guides.tools.daily_log._get_log_path") as mock_path:
                mock_path.return_value = log_path_1
                append_log_entry("slug-1", "summary", "gpt-5.4", 1000, 500, 0.01)

                mock_path.return_value = log_path_2
                append_log_entry("slug-2", "summary", "gpt-5.4", 2000, 1000, 0.02)

            self.assertTrue(log_path_1.exists())
            self.assertTrue(log_path_2.exists())

            content_1 = log_path_1.read_text(encoding="utf-8")
            content_2 = log_path_2.read_text(encoding="utf-8")

            self.assertIn("Total cost: $0.0100", content_1)
            self.assertIn("Total cost: $0.0200", content_2)


if __name__ == "__main__":
    unittest.main()