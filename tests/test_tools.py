import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock
import json
import argparse
from datetime import datetime

import guides.tools.daily_log as daily_log
import guides.tools.cost_report as cost_report
import guides.tools.link_checker as link_checker
import guides.tools.build_indexes as build_indexes

class ToolTests(unittest.TestCase):
    def test_daily_log_append(self):
        with TemporaryDirectory() as tmpdir:
            tp = Path(tmpdir)
            log_dir = tp / "logs"
            log_dir.mkdir()
            
            with patch("guides.tools.daily_log._get_log_path") as mock_path:
                log_file = log_dir / "2026-05-13.jsonl"
                mock_path.return_value = log_file
                
                daily_log.append_log_entry("s1", "action1", "gpt-4", 100, 50, 0.01)
                lines = log_file.read_text().strip().splitlines()
                self.assertEqual(len(lines), 1)
                entry = json.loads(lines[0])
                self.assertEqual(entry["slug"], "s1")
                self.assertEqual(entry["action"], "action1")
                self.assertEqual(entry["deployment"], "gpt-4")
                self.assertEqual(entry["total_tokens"], 150)
                self.assertEqual(entry["cost_usd"], 0.01)
                self.assertEqual(entry["msg"], "llm_call")
                
                daily_log.append_log_entry("s2", "action2", "gpt-4", 200, 100, 0.02)
                lines = log_file.read_text().strip().splitlines()
                self.assertEqual(len(lines), 2)
                entry2 = json.loads(lines[1])
                self.assertEqual(entry2["slug"], "s2")
                self.assertEqual(entry2["total_tokens"], 300)
                self.assertEqual(entry2["cost_usd"], 0.02)

    def test_daily_log_performance(self):
        """Bench: 1000 entries append-only JSONL < 200ms."""
        import time
        with TemporaryDirectory() as tmpdir:
            tp = Path(tmpdir)
            log_file = tp / "bench.jsonl"
            with patch("guides.tools.daily_log._get_log_path", return_value=log_file):
                start = time.perf_counter()
                for i in range(1000):
                    daily_log.append_log_entry(f"s{i}", "action", "gpt-4", 100, 50, 0.01)
                elapsed = time.perf_counter() - start
                self.assertLess(elapsed, 0.2, f"1000 appends took {elapsed:.3f}s, expected < 0.2s")

    def test_cost_report_collect_and_aggregate(self):
        with TemporaryDirectory() as tmpdir:
            tp = Path(tmpdir)
            log_file = tp / "2026-05-13.jsonl"
            log_file.write_text(json.dumps({
                "ts": "2026-05-13T12:00:00Z",
                "msg": "llm_call",
                "deployment": "gpt-4",
                "total_tokens": 100,
                "cost_usd": 0.01
            }) + "\n")
            
            entries = list(cost_report._iter_entries([log_file], days=None))
            self.assertEqual(len(entries), 1)
            
            by_model, by_date, grand = cost_report._aggregate(entries)
            self.assertEqual(grand.calls, 1)
            self.assertEqual(grand.tokens, 100)
            self.assertAlmostEqual(grand.cost_usd, 0.01)
            self.assertIn("gpt-4", by_model)
            self.assertIn("2026-05-13", by_date)

    @patch("guides.tools.cost_report._log_dir")
    @patch("argparse.ArgumentParser.parse_args")
    def test_cost_report_main(self, mock_args, mock_log_dir):
        with TemporaryDirectory() as tmpdir:
            tp = Path(tmpdir)
            mock_log_dir.return_value = tp
            mock_args.return_value = argparse.Namespace(days=None)
            
            log_file = tp / "2026-05-13.jsonl"
            log_file.write_text(json.dumps({
                "ts": "2026-05-13T12:00:00Z",
                "msg": "llm_call",
                "deployment": "gpt-4",
                "total_tokens": 100,
                "cost_usd": 0.01
            }) + "\n")
            
            with patch("sys.stdout", new_callable=MagicMock()):
                self.assertEqual(cost_report.main(), 0)

    def test_link_checker_slugify(self):
        self.assertEqual(link_checker.slugify("Claude Code"), "claude-code")
        self.assertEqual(link_checker.slugify("Multi  Space"), "multi-space")

    def test_link_checker_scan_and_resolve(self):
        with TemporaryDirectory() as tmpdir:
            tp = Path(tmpdir)
            sum_dir = tp / "summaries"
            sum_dir.mkdir(parents=True)
            (sum_dir / "target.md").write_text("target content")
            
            with patch("guides.tools.link_checker.TARGET_DIRS", [sum_dir]):
                self.assertIsNotNone(link_checker.resolve_link("Target"))
                self.assertIsNone(link_checker.resolve_link("Missing"))
                
                f = tp / "source.md"
                f.write_text("Link [[Target]] and [[Missing]]")
                broken = link_checker.scan_file(f)
                self.assertEqual(len(broken), 1)
                self.assertEqual(broken[0][1], "Missing")

    def test_build_indexes_parse_fm(self):
        fm = build_indexes.parse_front_matter_yaml("---\ntools: [T1]\n---\nBody")
        self.assertEqual(fm["tools"], ["T1"])
        self.assertEqual(build_indexes.parse_front_matter_yaml("No FM"), {})

    @patch("guides.tools.build_indexes.SUMMARIES_DIR")
    @patch("guides.tools.build_indexes.INDEX_DIR")
    def test_build_indexes_main(self, mock_index, mock_sum):
        with TemporaryDirectory() as tmpdir:
            tp = Path(tmpdir)
            mock_sum.exists.return_value = True
            sum_file = tp / "s1.md"
            sum_file.write_text("---\ntitle: T1\ntools: [Tool1]\n---\nBody")
            mock_sum.glob.return_value = [sum_file]
            
            out_dir = tp / "index"
            out_dir.mkdir() # Actually create it
            mock_index.mkdir.return_value = None
            mock_index.__truediv__.side_effect = lambda x: out_dir / x
            
            with patch("guides.tools.build_indexes.TOOLS_DIR", tp / "tools"):
                self.assertEqual(build_indexes.main([]), 0)
                self.assertTrue((out_dir / "tools.md").exists())

if __name__ == "__main__":
    unittest.main()
