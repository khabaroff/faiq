import unittest
from pathlib import Path
from unittest.mock import patch, Mock
import json

import guides.pipelines.b_summarize as b
import guides.pipelines.c_wiki_update as c
import guides.pipelines.e_seo as e
import guides.pipelines.g_telegram as g
import guides.pipelines.d_quality_check as d

class PipelineBTests(unittest.TestCase):
    def test_count_tokens(self):
        self.assertGreater(b.count_tokens("abcd"), 0)
        # tiktoken: "a"*40 is a few tokens, not exactly len//4
        self.assertGreater(b.count_tokens("a" * 40), 0)
        # Cyrillic should count more tokens than ASCII of same char count
        ru = "а" * 40
        en = "a" * 40
        self.assertGreater(b.count_tokens(ru), b.count_tokens(en))

    def test_parse_front_matter_simple(self):
        text = "---\ntitle: Test\nkey: value\n---\nBody text"
        fm, body = b.parse_front_matter_simple(text)
        self.assertEqual(fm, {"title": "Test", "key": "value"})
        self.assertEqual(body, "Body text")
        self.assertEqual(b.parse_front_matter_simple("No FM"), ({}, "No FM"))

    def test_parse_front_matter_yaml(self):
        from guides.frontmatter import parse_frontmatter
        text = "---\ntools:\n  - t1\npatterns: []\n---\nBody"
        fm, body = parse_frontmatter(text)
        self.assertEqual(fm["tools"], ["t1"])
        fm_bad, _ = parse_frontmatter("---\n[invalid")
        self.assertEqual(fm_bad, {})

    def test_validate_summary_md(self):
        self.assertTrue(b._validate_summary_md("---\ntools: []\npatterns: []\n---\nBody"))
        self.assertFalse(b._validate_summary_md("---\ntitle: T\n---\nBody"))

    @patch("guides.pipelines.b_summarize.load_prompt", return_value="{{source_text}}")
    def test_render_summary_prompt(self, mock_load):
        self.assertEqual(b._render_summary_prompt("text", "u", "t", "ru"), "text")

    @patch("guides.pipelines.b_summarize.call_llm_messages")
    @patch("guides.pipelines.b_summarize.get_smart_client")
    def test_call_llm_summary(self, mock_client, mock_call):
        mock_call.return_value = ("---\ntools: []\npatterns: []\n---\nBody", Mock(prompt_tokens=1, completion_tokens=1, cost_usd=0))
        self.assertIn("Body", b.call_llm_summary("s", "src", "u", "t", "ru"))

    @patch("guides.pipelines.b_summarize.call_llm_messages")
    @patch("guides.pipelines.b_summarize.get_smart_client")
    def test_call_llm_summary_retry(self, mock_client, mock_call):
        mock_call.side_effect = [
            ("Bad Response", Mock(prompt_tokens=1, completion_tokens=1, cost_usd=0)),
            ("---\ntools: []\npatterns: []\n---\nGood", Mock(prompt_tokens=1, completion_tokens=1, cost_usd=0))
        ]
        res = b.call_llm_summary("s", "src", "u", "t", "ru")
        self.assertIn("Good", res)
        self.assertEqual(mock_call.call_count, 2)

class PipelineCTests(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(c.slugify("Hello World"), "hello-world")

    def test_canonicalize_slug(self):
        self.assertEqual(c.canonicalize_slug("Claude Code", ["claude-code"]), "claude-code")
        self.assertEqual(c.canonicalize_slug("New", []), "new")

    def test_extract_summary_fm(self):
        text = "---\ntools: [T1]\npatterns: [P1]\nsource_url: u\n---\nBody"
        self.assertEqual(c.extract_summary_fm(text), (["T1"], ["P1"], "u"))

    def test_parse_front_matter(self):
        from guides.frontmatter import parse_frontmatter
        self.assertEqual(parse_frontmatter("---\na: b\n---\nB"), ({"a": "b"}, "B"))

    def test_append_mention_to_page(self):
        from tempfile import NamedTemporaryFile
        with NamedTemporaryFile(mode="w+", suffix=".md") as tmp:
            tmp.write("---\nname: T\n---\n## Упоминания\n\n- [o](../summaries/o.md)\n")
            tmp.flush()
            c.append_mention_to_page(Path(tmp.name), {"source_slug": "n"})
            self.assertIn("- [n]", Path(tmp.name).read_text())

    def test_append_mention_no_section(self):
        from tempfile import NamedTemporaryFile
        with NamedTemporaryFile(mode="w+", suffix=".md") as tmp:
            tmp.write("---\nname: T\n---\nBody")
            tmp.flush()
            c.append_mention_to_page(Path(tmp.name), {"source_slug": "n"})
            self.assertIn("## Упоминания", Path(tmp.name).read_text())

    def test_write_wiki_page(self):
        from tempfile import NamedTemporaryFile
        with NamedTemporaryFile(mode="w+", suffix=".md") as tmp:
            c.write_wiki_page(Path(tmp.name), "N", "s", "t", "u", "D", [{"source_slug": "s1"}])
            self.assertIn("# N", Path(tmp.name).read_text())

    @patch("guides.pipelines.c_wiki_update.call_llm_update")
    def test_propagate_summary_rewrite_description(self, mock_call):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmpdir:
            tp = Path(tmpdir)
            sum_dir = tp / "summaries"
            sum_dir.mkdir()
            tools_dir = tp / "tools"
            tools_dir.mkdir()
            tech_dir = tp / "tech"
            tech_dir.mkdir()
            with patch("guides.pipelines.c_wiki_update.SUMMARIES_DIR", sum_dir), \
                 patch("guides.pipelines.c_wiki_update.WIKI_TOOLS_DIR", tools_dir), \
                 patch("guides.pipelines.c_wiki_update.WIKI_TECH_DIR", tech_dir):
                (sum_dir / "s.md").write_text("---\ntools: [T]\n---\nB")
                (tools_dir / "t.md").write_text("---\nname: T\n---\n# T\n\n## Что это\n\nOld")
                mock_call.return_value = {
                    "action": "rewrite_description",
                    "page_md": "---\nname: T\n---\n# T\n\n## Что это\n\nNew\n\n## Упоминания\n\n- [s](../summaries/s.md)"
                }
                self.assertEqual(c.propagate_summary("s"), 1)
                self.assertIn("New", (tools_dir / "t.md").read_text())

    def test_canonicalize_slug_fuzzy(self):
        # 85+ score token_sort_ratio
        self.assertEqual(c.canonicalize_slug("Claude 3.5 Sonnet", ["claude-35-sonnet"]), "claude-35-sonnet")
        self.assertEqual(c.canonicalize_slug("Brand New Tool", ["other"]), "brand-new-tool")

    def test_extract_summary_fm_edge_cases(self):
        self.assertEqual(c.extract_summary_fm("no fm"), ([], [], ""))
        self.assertEqual(c.extract_summary_fm("---\ntools: [\"T1\"]\npatterns: [{\"name\": \"P1\"}]\nsource_url: u\n---\nBody"), (["T1"], ["P1"], "u"))

    def test_backup_page(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmpdir:
            tp = Path(tmpdir)
            p = tp / "page.md"
            p.write_text("content")
            c._backup_page(p)
            self.assertTrue((tp / ".backups").exists())
            self.assertEqual(len(list((tp / ".backups").glob("*.bak"))), 1)

class PipelineETests(unittest.TestCase):
    def test_parse_front_matter_yaml(self):
        from guides.frontmatter import parse_frontmatter
        self.assertEqual(parse_frontmatter("---\na: b\n---\nB"), ({"a": "b"}, "B"))

    def test_extract_json(self):
        self.assertEqual(e._extract_json("{\"a\":1}"), {"a": 1})

    @patch("guides.pipelines.e_seo.load_prompt", return_value="{{title}} {{tldr}}")
    def test_render_seo_prompt(self, mock_load):
        self.assertIn("T", e._render_seo_prompt({"title": "T"}, "## TL;DR\n\nTLDR text\n## Next"))
        self.assertIn("TLDR text", e._render_seo_prompt({"title": "T"}, "## TL;DR\n\nTLDR text"))

    @patch("guides.pipelines.e_seo.call_llm_seo")
    @patch("guides.pipelines.e_seo.SUMMARIES_DIR")
    def test_optimize_one(self, mock_sum_dir, mock_call):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmpdir:
            tp = Path(tmpdir)
            mock_sum_dir.__truediv__.side_effect = lambda x: tp / x
            (tp / "s.md").write_text("---\ntitle: T\n---\nB")
            mock_call.return_value = {"seo_title": "ST"}
            self.assertTrue(e.optimize_one("s"))

    @patch("guides.pipelines.e_seo.call_llm")
    @patch("guides.pipelines.e_seo.get_smart_client")
    @patch("guides.pipelines.e_seo.load_prompt", return_value="prompt")
    def test_call_llm_seo(self, mock_load, mock_client, mock_call):
        mock_call.return_value = ("{\"seo_title\": \"T\"}", None)
        result = e.call_llm_seo({}, "B")
        self.assertEqual(result["seo_title"], "T")

class PipelineGTests(unittest.TestCase):
    def test_parse_front_matter_yaml(self):
        from guides.frontmatter import parse_frontmatter
        self.assertEqual(parse_frontmatter("---\na: b\n---\nB"), ({"a": "b"}, "B"))

    def test_escape_markdown_v2(self):
        self.assertEqual(g._escape_markdown_v2("!"), "\\!")

    @patch("guides.pipelines.g_telegram.load_prompt", return_value="{{title}}")
    def test_render_telegram_prompt(self, mock_load):
        self.assertEqual(g._render_telegram_prompt({"title": "T"}), "T")

    @patch("guides.pipelines.g_telegram.call_llm_telegram", return_value="Post")
    @patch("guides.pipelines.g_telegram.SUMMARIES_DIR")
    def test_publish_one_dry_run(self, mock_sum_dir, mock_call):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmpdir:
            tp = Path(tmpdir)
            mock_sum_dir.__truediv__.side_effect = lambda x: tp / x
            (tp / "s.md").write_text("---\ntitle: T\n---\nB")
            self.assertTrue(g.publish_one("s", dry_run=True))

    @patch("guides.pipelines.g_telegram.send_telegram_message", return_value=True)
    @patch("guides.pipelines.g_telegram.call_llm_telegram", return_value="Post")
    @patch("guides.pipelines.g_telegram.SUMMARIES_DIR")
    @patch("guides.pipelines.g_telegram.set_state")
    @patch("guides.pipelines.g_telegram.update_frontmatter")
    def test_publish_one_real(self, mock_fm, mock_state, mock_sum_dir, mock_call, mock_send):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmpdir:
            tp = Path(tmpdir)
            mock_sum_dir.__truediv__.side_effect = lambda x: tp / x
            (tp / "s.md").write_text("---\ntitle: T\n---\nB")
            self.assertTrue(g.publish_one("s", dry_run=False))

    @patch("guides.pipelines.g_telegram.SUMMARIES_DIR")
    @patch("guides.pipelines.g_telegram.get_state", return_value={})
    @patch("guides.pipelines.g_telegram.publish_one", return_value=True)
    def test_main(self, mock_pub, mock_state, mock_sum_dir):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmpdir:
            tp = Path(tmpdir)
            mock_sum_dir.exists.return_value = True
            mock_sum_dir.glob.return_value = [tp / "s.md"]
            self.assertEqual(g.main(["--slug", "s"]), 0)

class PipelineDTests(unittest.TestCase):
    def test_extract_json(self):
        self.assertEqual(d._extract_json("{\"a\":1}"), {"a": 1})
        with self.assertRaises(ValueError):
            d._extract_json("no json")

    @patch("guides.pipelines.d_quality_check.call_llm_summary_check")
    @patch("guides.pipelines.d_quality_check.SUMMARIES_DIR")
    @patch("guides.pipelines.d_quality_check.SOURCES_DIR")
    def test_check_summaries(self, mock_src, mock_sum, mock_call):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmpdir:
            tp = Path(tmpdir)
            mock_sum.glob.return_value = [tp / "s.md"]
            (tp / "s.md").write_text("sum")
            with patch.object(Path, "exists", return_value=True):
                mock_call.return_value = {"verdict": "ok"}
                res = d.check_summaries()
                self.assertEqual(len(res), 1)

    @patch("guides.pipelines.d_quality_check.call_llm_wiki_clean")
    @patch("guides.pipelines.d_quality_check.TOOLS_DIR")
    @patch("guides.pipelines.d_quality_check.TECH_DIR")
    def test_clean_wiki_pages_cleanup(self, mock_tech, mock_tools, mock_call):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmpdir:
            tp = Path(tmpdir)
            mock_tools.glob.return_value = [tp / "t1.md"]
            mock_tech.glob.return_value = []
            p = tp / "t1.md"
            p.write_text("page")
            mock_call.return_value = {"verdict": "needs_cleanup", "cleaned_page_md": "clean"}
            with patch("guides.pipelines.d_quality_check.ROOT", tp):
                res = d.clean_wiki_pages()
                self.assertEqual(res[0]["verdict"], "needs_cleanup")
                self.assertEqual(p.read_text(), "clean")

    @patch("guides.pipelines.d_quality_check.check_summaries", return_value=[{"slug": "s", "verdict": "ok"}])
    @patch("guides.pipelines.d_quality_check.clean_wiki_pages", return_value=[])
    @patch("guides.pipelines.d_quality_check.set_state")
    @patch("guides.pipelines.d_quality_check.update_frontmatter")
    @patch("guides.pipelines.d_quality_check.SUMMARIES_DIR")
    def test_main(self, mock_sum_dir, mock_fm, mock_state, mock_clean, mock_check):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmpdir:
            tp = Path(tmpdir)
            report_file = tp / "report.json"
            mock_sum_dir.__truediv__.side_effect = lambda x: tp / x
            with patch.object(Path, "exists", return_value=True), \
                 patch("guides.pipelines.d_quality_check.QC_REPORT", report_file):
                self.assertEqual(d.main(["--mode", "summary"]), 0)
                self.assertTrue(report_file.exists())

    @patch("guides.pipelines.b_summarize.call_llm_messages")
    @patch("guides.pipelines.b_summarize.get_smart_client")
    def test_call_llm_summary_uses_conversation_history(self, mock_client, mock_call):
        """Retry should append assistant + correction, not resend full body."""
        mock_call.side_effect = [
            ("Bad", Mock(prompt_tokens=100, completion_tokens=50, cost_usd=0.001)),
            ("---\ntools: []\npatterns: []\n---\nGood", Mock(prompt_tokens=120, completion_tokens=50, cost_usd=0.001))
        ]
        res = b.call_llm_summary("s", "src", "u", "t", "ru")
        self.assertIn("Good", res)
        self.assertEqual(mock_call.call_count, 2)
        # messages list is mutated in place; final state after two calls
        final_messages = mock_call.call_args_list[1][0][2]
        self.assertEqual(len(final_messages), 4)
        self.assertEqual(final_messages[0]["role"], "system")
        self.assertEqual(final_messages[1]["role"], "user")
        self.assertEqual(final_messages[2]["role"], "assistant")
        self.assertEqual(final_messages[3]["role"], "user")
        self.assertIn("ВАЖНО", final_messages[3]["content"])


if __name__ == "__main__":
    unittest.main()
