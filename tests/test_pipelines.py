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
        self.assertEqual(b.count_tokens("abcd"), 1)
        self.assertEqual(b.count_tokens("a" * 40), 10)

    def test_parse_front_matter_simple(self):
        text = "---\ntitle: Test\nkey: value\n---\nBody text"
        fm, body = b.parse_front_matter_simple(text)
        self.assertEqual(fm, {"title": "Test", "key": "value"})
        self.assertEqual(body, "Body text")
        self.assertEqual(b.parse_front_matter_simple("No FM"), ({}, "No FM"))

    def test_parse_front_matter_yaml(self):
        text = "---\ntools:\n  - t1\npatterns: []\n---\nBody"
        res = b.parse_front_matter_yaml(text)
        self.assertIsNotNone(res)
        fm, body = res
        self.assertEqual(fm["tools"], ["t1"])
        self.assertIsNone(b.parse_front_matter_yaml("---\n[invalid"))

    def test_validate_summary_md(self):
        self.assertTrue(b._validate_summary_md("---\ntools: []\npatterns: []\n---\nBody"))
        self.assertFalse(b._validate_summary_md("---\ntitle: T\n---\nBody"))

    @patch("guides.pipelines.b_summarize.load_prompt", return_value="{{source_text}}")
    def test_render_summary_prompt(self, mock_load):
        self.assertEqual(b._render_summary_prompt("text", "u", "t", "ru"), "text")

    @patch("guides.pipelines.b_summarize.call_llm")
    @patch("guides.pipelines.b_summarize.get_smart_client")
    def test_call_llm_summary(self, mock_client, mock_call):
        mock_call.return_value = ("---\ntools: []\npatterns: []\n---\nBody", Mock(prompt_tokens=1, completion_tokens=1, cost_usd=0))
        self.assertIn("Body", b.call_llm_summary("s", "src", "u", "t", "ru"))

    @patch("guides.pipelines.b_summarize.call_llm_summary", return_value="---\ntools: []\npatterns: []\n---\nBody")
    def test_summarize_one(self, mock_call):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmpdir:
            tp = Path(tmpdir)
            src_dir = tp / "sources"
            src_dir.mkdir()
            sum_dir = tp / "summaries"
            sum_dir.mkdir()
            with patch("guides.pipelines.b_summarize.SOURCES_DIR", src_dir), \
                 patch("guides.pipelines.b_summarize.SUMMARIES_DIR", sum_dir):
                (src_dir / "s.md").write_text("---\ntitle: T\n---\nBody")
                out = b.summarize_one("s")
                self.assertTrue(out.exists())

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
        self.assertEqual(c.parse_front_matter("---\na: b\n---\nB"), ({"a": "b"}, "B"))

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
    def test_propagate_summary(self, mock_call):
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
                mock_call.return_value = {"action": "create", "page_md": "---\nname: T\n---\n# T"}
                self.assertEqual(c.propagate_summary("s"), 1)

class PipelineETests(unittest.TestCase):
    def test_parse_front_matter_yaml(self):
        self.assertEqual(e.parse_front_matter_yaml("---\na: b\n---\nB"), ({"a": "b"}, "B"))

    def test_extract_json(self):
        self.assertEqual(e._extract_json("{\"a\":1}"), {"a": 1})

    @patch("guides.pipelines.e_seo.load_prompt", return_value="{{title}} {{tldr}}")
    def test_render_seo_prompt(self, mock_load):
        self.assertIn("T", e._render_seo_prompt({"title": "T"}, "## TL;DR\n\nTLDR"))

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
        self.assertEqual(e.call_llm_seo({}, "B"), {"seo_title": "T"})

class PipelineGTests(unittest.TestCase):
    def test_parse_front_matter_yaml(self):
        self.assertEqual(g.parse_front_matter_yaml("---\na: b\n---\nB"), ({"a": "b"}, "B"))

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

class PipelineDTests(unittest.TestCase):
    def test_extract_json(self):
        self.assertEqual(d._extract_json("{\"a\":1}"), {"a": 1})

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
    def test_clean_wiki_pages(self, mock_tech, mock_tools, mock_call):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmpdir:
            tp = Path(tmpdir)
            mock_tools.glob.return_value = [tp / "t1.md"]
            mock_tech.glob.return_value = []
            (tp / "t1.md").write_text("page")
            mock_call.return_value = {"verdict": "ok"}
            res = d.clean_wiki_pages()
            self.assertEqual(len(res), 1)

if __name__ == "__main__":
    unittest.main()
