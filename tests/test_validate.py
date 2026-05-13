from __future__ import annotations

import textwrap
import unittest

from guides.process.validate import PageViolation, autofix, check


def _page(frontmatter: str, body: str) -> str:
    return f"---\n{frontmatter.strip()}\n---\n\n{body.strip()}"


GOOD_FM = textwrap.dedent("""\
    id: "src-2026-05-11-abc12345"
    title: "Building Effective Agents"
    type: "source-page"
    status: "needs-review"
    quality_score: 0.72
""")

GOOD_BODY = textwrap.dedent("""\
    # Building Effective Agents

    ## Краткое изложение

    Agents compose simple patterns.

    ## Ключевые идеи

    - Keep it simple.
""")


class CheckValidPageTests(unittest.TestCase):
    def test_valid_page_has_no_errors(self) -> None:
        text = _page(GOOD_FM, GOOD_BODY)
        result = check(text, "fake.md")
        self.assertTrue(result.is_valid, result.violations)
        self.assertEqual(result.errors, [])

    def test_valid_page_path_stored(self) -> None:
        text = _page(GOOD_FM, GOOD_BODY)
        result = check(text, "some/path.md")
        self.assertEqual(result.path, "some/path.md")


class CheckMissingH1Tests(unittest.TestCase):
    def test_missing_h1_is_error(self) -> None:
        body = "## Краткое изложение\n\nSome text"
        text = _page(GOOD_FM, body)
        result = check(text)
        rules = [v.rule for v in result.violations]
        self.assertIn("missing_h1", rules)
        self.assertIn("error", [v.severity for v in result.violations if v.rule == "missing_h1"])

    def test_h1_present_no_missing_h1_violation(self) -> None:
        text = _page(GOOD_FM, GOOD_BODY)
        result = check(text)
        self.assertNotIn("missing_h1", [v.rule for v in result.violations])


class CheckIntroPreambleTests(unittest.TestCase):
    def test_intro_preamble_is_warning(self) -> None:
        body = "Here's a summary of the article:\n\n## Краткое изложение\n\nText"
        text = _page(GOOD_FM, body)
        result = check(text)
        rules = [v.rule for v in result.violations]
        self.assertIn("intro_preamble", rules)
        preamble_v = next(v for v in result.violations if v.rule == "intro_preamble")
        self.assertEqual(preamble_v.severity, "warning")

    def test_no_preamble_no_violation(self) -> None:
        text = _page(GOOD_FM, GOOD_BODY)
        result = check(text)
        self.assertNotIn("intro_preamble", [v.rule for v in result.violations])


class CheckEnglishSectionsTests(unittest.TestCase):
    def test_english_sections_is_warning(self) -> None:
        body = "# Title\n\n## Core idea\n\nSome text\n\n## Summary\n\nMore text"
        text = _page(GOOD_FM, body)
        result = check(text)
        rules = [v.rule for v in result.violations]
        self.assertIn("english_sections", rules)
        eng_v = next(v for v in result.violations if v.rule == "english_sections")
        self.assertEqual(eng_v.severity, "warning")

    def test_russian_sections_no_violation(self) -> None:
        text = _page(GOOD_FM, GOOD_BODY)
        result = check(text)
        self.assertNotIn("english_sections", [v.rule for v in result.violations])

    def test_technical_term_heading_not_flagged(self) -> None:
        # headings with Russian chars are not flagged even if they contain English words
        body = "# Заголовок\n\n## API и инструменты\n\nText"
        text = _page(GOOD_FM, body)
        result = check(text)
        self.assertNotIn("english_sections", [v.rule for v in result.violations])


class CheckPlaceholderTitleTests(unittest.TestCase):
    def test_filename_title_is_error(self) -> None:
        fm = GOOD_FM.replace("Building Effective Agents", "05-alf-skills.md")
        text = _page(fm, GOOD_BODY)
        result = check(text)
        self.assertIn("placeholder_title", [v.rule for v in result.violations])

    def test_numeric_title_is_error(self) -> None:
        fm = GOOD_FM.replace("Building Effective Agents", "2026 04 12")
        text = _page(fm, GOOD_BODY)
        result = check(text)
        self.assertIn("placeholder_title", [v.rule for v in result.violations])

    def test_real_title_no_violation(self) -> None:
        text = _page(GOOD_FM, GOOD_BODY)
        result = check(text)
        self.assertNotIn("placeholder_title", [v.rule for v in result.violations])


class CheckNullQualityScoreTests(unittest.TestCase):
    def test_null_quality_score_is_warning(self) -> None:
        fm = GOOD_FM.replace("quality_score: 0.72", "quality_score: null")
        text = _page(fm, GOOD_BODY)
        result = check(text)
        self.assertIn("null_quality_score", [v.rule for v in result.violations])

    def test_scored_page_no_violation(self) -> None:
        text = _page(GOOD_FM, GOOD_BODY)
        result = check(text)
        self.assertNotIn("null_quality_score", [v.rule for v in result.violations])


class AutofixTests(unittest.TestCase):
    def test_autofix_strips_preamble(self) -> None:
        body = "Here's a summary:\n\n## Краткое изложение\n\nText"
        text = _page(GOOD_FM, body)
        fixed, applied = autofix(text)
        self.assertTrue(any("preamble" in a for a in applied))
        self.assertNotIn("Here's", fixed.split("---")[-1][:50])

    def test_autofix_localizes_english_headings(self) -> None:
        body = "# Title\n\n## Summary\n\nText\n\n## Entities\n\nFoo"
        text = _page(GOOD_FM, body)
        fixed, applied = autofix(text)
        self.assertTrue(any("localized" in a for a in applied))
        self.assertIn("## Краткое изложение", fixed)
        self.assertIn("## Сущности", fixed)

    def test_autofix_adds_h1_when_missing(self) -> None:
        body = "## Краткое изложение\n\nSome text"
        fm = GOOD_FM  # title = "Building Effective Agents"
        text = _page(fm, body)
        fixed, applied = autofix(text, source_url="https://example.com/building-effective-agents")
        self.assertTrue(any("H1" in a for a in applied))
        body_part = fixed.split("---\n\n", 1)[-1]
        self.assertTrue(body_part.startswith("# "))

    def test_autofix_returns_original_when_clean(self) -> None:
        text = _page(GOOD_FM, GOOD_BODY)
        fixed, applied = autofix(text)
        self.assertEqual(applied, [])
        self.assertEqual(fixed, text)

    def test_autofix_preserves_frontmatter(self) -> None:
        body = "## Summary\n\nText"
        text = _page(GOOD_FM, body)
        fixed, _ = autofix(text)
        self.assertIn('id: "src-2026-05-11-abc12345"', fixed)
        self.assertIn('title: "Building Effective Agents"', fixed)


if __name__ == "__main__":
    unittest.main()
