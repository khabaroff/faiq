from __future__ import annotations

import unittest

from guides.process.wiki import wrap_with_frontmatter


def _frontmatter_map(text: str) -> dict[str, str]:
    lines = text.splitlines()
    assert lines[0] == "---"

    result: dict[str, str] = {}
    for line in lines[1:]:
        if line == "---":
            break
        if ": " not in line:
            continue
        key, value = line.split(": ", 1)
        result[key] = value.strip()
    return result


class WrapWithFrontmatterTests(unittest.TestCase):
    def test_local_placeholder_heading_uses_real_title(self) -> None:
        body = "# Title\n\n07 Prompts\n\n## Назначение\n\nText"

        text = wrap_with_frontmatter(
            body,
            source_type="article",
            source_url="",
            tags=[],
            source_path="data/inbox/04-laai-prd-prompts.md",
            status="needs-review",
        )

        fm = _frontmatter_map(text)
        self.assertEqual(fm["title"], '"07 Prompts"')

    def test_verified_status_updates_review_flags(self) -> None:
        text = wrap_with_frontmatter(
            "# Good Title\n\nBody",
            source_type="article",
            source_url="https://example.com/post",
            tags=["Agent Architecture"],
            status="verified",
        )

        fm = _frontmatter_map(text)
        self.assertEqual(fm["status"], '"active"')
        self.assertEqual(fm["review_required"], "false")
        self.assertEqual(fm["verified"], "true")

    def test_local_file_frontmatter_uses_file_origin(self) -> None:
        text = wrap_with_frontmatter(
            "# Good Title\n\nBody",
            source_type="article",
            source_url="",
            tags=[],
            source_path="data/inbox/local-note.md",
            status="needs-review",
        )

        fm = _frontmatter_map(text)
        self.assertEqual(fm["origin"], '"file"')
        self.assertEqual(fm["url"], '""')
        self.assertEqual(fm["language"], '"ru"')


if __name__ == "__main__":
    unittest.main()
