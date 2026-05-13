from __future__ import annotations

import unittest

from guides.process.wiki import _enforce_h1, _infer_title, _slug_to_title, wrap_with_frontmatter


def _body(text: str) -> str:
    """Extract body after frontmatter."""
    lines = text.splitlines()
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    return "\n".join(lines[end + 1 :]).strip() if end else text.strip()


def _fm_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("title: "):
            return line[len("title: "):].strip().strip('"')
    return ""


class SlugToTitleTests(unittest.TestCase):
    def test_strips_query_params(self) -> None:
        result = _slug_to_title("the-wiki-that-thinks?utm_source=substack&utm_campaign=post")
        self.assertEqual(result, "The Wiki That Thinks")

    def test_strips_file_extension(self) -> None:
        result = _slug_to_title("05-alf-implementing-claude-code-skills-from-scratch.md")
        self.assertEqual(result, "Alf Implementing Claude Code Skills From Scratch")

    def test_strips_date_prefix(self) -> None:
        result = _slug_to_title("2026-04-12-knowledge-unit-specification.md")
        self.assertEqual(result, "Knowledge Unit Specification")

    def test_strips_leading_number_prefix(self) -> None:
        result = _slug_to_title("01-laai-building-effective-ai-agents.txt")
        self.assertEqual(result, "Laai Building Effective Ai Agents")

    def test_plain_slug_unchanged(self) -> None:
        result = _slug_to_title("building-effective-agents")
        self.assertEqual(result, "Building Effective Agents")


class InferTitleTests(unittest.TestCase):
    def test_uses_h1_when_present(self) -> None:
        body = "# Building Effective Agents\n\n## Краткое изложение\n\nText"
        self.assertEqual(_infer_title(body, "https://example.com/building-effective-agents"), "Building Effective Agents")

    def test_url_fallback_strips_query_params(self) -> None:
        body = "Some text without H1"
        url = "https://example.com/the-wiki-that-thinks?utm_source=substack"
        self.assertEqual(_infer_title(body, url), "The Wiki That Thinks")

    def test_filepath_fallback_strips_extension_and_prefix(self) -> None:
        body = "Some text without H1"
        self.assertEqual(_infer_title(body, "data/inbox/05-alf-skills.md"), "Alf Skills")

    def test_date_filepath_fallback(self) -> None:
        body = "Some text"
        self.assertEqual(_infer_title(body, "data/inbox/2026-04-12-knowledge-unit-specification.md"), "Knowledge Unit Specification")


class EnforceH1Tests(unittest.TestCase):
    def test_prepends_h1_when_missing(self) -> None:
        body = "## Краткое изложение\n\nText here"
        result = _enforce_h1(body, "My Title")
        self.assertTrue(result.startswith("# My Title\n"))

    def test_leaves_body_unchanged_when_h1_present(self) -> None:
        body = "# Existing Title\n\n## Краткое изложение\n\nText"
        result = _enforce_h1(body, "Other Title")
        self.assertEqual(result, body)

    def test_prepends_when_body_starts_with_prose(self) -> None:
        body = "Here's a summary of the article:\n\n## Core idea\n\nText"
        result = _enforce_h1(body, "Fallback Title")
        self.assertTrue(result.startswith("# Fallback Title\n"))


class WrapWithFrontmatterH1Tests(unittest.TestCase):
    def test_body_gets_h1_when_missing(self) -> None:
        body = "## Краткое изложение\n\nSome text"
        result = wrap_with_frontmatter(
            body,
            source_type="article",
            source_url="https://example.com/my-article",
            tags=[],
        )
        extracted = _body(result)
        self.assertTrue(extracted.startswith("# My Article\n"), f"Got: {extracted[:60]!r}")

    def test_body_h1_preserved_when_present(self) -> None:
        body = "# Real Title\n\n## Краткое изложение\n\nText"
        result = wrap_with_frontmatter(
            body,
            source_type="article",
            source_url="https://example.com/some-slug",
            tags=[],
        )
        extracted = _body(result)
        self.assertTrue(extracted.startswith("# Real Title\n"))

    def test_file_source_gets_clean_title(self) -> None:
        body = "Here's a concise summary.\n\n## Core idea\n\nText"
        result = wrap_with_frontmatter(
            body,
            source_type="article",
            source_url="",
            tags=[],
            source_path="data/inbox/05-alf-implementing-skills.md",
        )
        title = _fm_title(result)
        self.assertNotIn(".Md", title)
        self.assertNotIn("05 ", title)
        self.assertNotIn("05-", title)

    def test_url_with_query_params_gets_clean_title(self) -> None:
        body = "Some text"
        result = wrap_with_frontmatter(
            body,
            source_type="article",
            source_url="https://example.com/the-wiki-that-thinks?utm_source=substack",
            tags=[],
        )
        title = _fm_title(result)
        self.assertNotIn("utm", title.lower())
        self.assertNotIn("?", title)


if __name__ == "__main__":
    unittest.main()
