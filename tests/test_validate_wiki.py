from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from guides.process.validate import autofix, check
from guides.tools.validate_wiki import main


class ValidateWikiTests(unittest.TestCase):
    def test_check_flags_expected_format_violations(self) -> None:
        text = """---
title: "05-alf-implementing-claude-code-skills-from-scratch.md"
quality_score: 0.56
---

Here’s a concise summary of the article:

## Core idea

Text
"""

        result = check(text, "wiki/extracts/notes/example.md")
        rules = {v.rule for v in result.violations}

        self.assertIn("missing_h1", rules)
        self.assertIn("english_sections", rules)
        self.assertIn("placeholder_title", rules)

    def test_autofix_adds_h1_and_localizes_sections(self) -> None:
        text = """---
title: "Implementing Claude Code Skills from Scratch"
quality_score: 0.56
---

Here’s a concise summary of the article:

## Core idea

Text
"""

        fixed, applied = autofix(text, source_path="data/inbox_done/05-alf-implementing-claude-code-skills-from-scratch.md")

        self.assertIn("stripped intro preamble", applied)
        self.assertIn("localized section headings to Russian", applied)
        self.assertIn("added H1: 'Implementing Claude Code Skills from Scratch'", applied)
        self.assertIn("# Implementing Claude Code Skills from Scratch", fixed)
        self.assertIn("## Ключевая идея", fixed)
        self.assertNotIn("## Core idea", fixed)

    def test_cli_skips_index_and_log_files(self) -> None:
        with TemporaryDirectory() as tmpdir:
            wiki = Path(tmpdir) / "wiki"
            extracts = wiki / "extracts" / "notes"
            indexes = wiki / "_indexes"
            extracts.mkdir(parents=True)
            indexes.mkdir(parents=True)

            (extracts / "page.md").write_text(
                """---
title: "Good Page"
quality_score: 0.9
---

# Good Page

## Краткое изложение

Text
""",
                encoding="utf-8",
            )
            (indexes / "bad.md").write_text("no frontmatter", encoding="utf-8")
            (wiki / "log.md").write_text("# Log\n", encoding="utf-8")

            exit_code = main([str(wiki)])

        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
