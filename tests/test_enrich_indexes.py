from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from guides.enrich.indexes import rebuild_indexes


class RebuildIndexesTests(unittest.TestCase):
    def test_entities_and_concepts_indexes_are_generated(self) -> None:
        with TemporaryDirectory() as tmpdir:
            wiki_dir = Path(tmpdir) / "wiki"
            (wiki_dir / "extracts" / "notes").mkdir(parents=True, exist_ok=True)
            (wiki_dir / "_indexes").mkdir(parents=True, exist_ok=True)

            (wiki_dir / "extracts" / "notes" / "first.md").write_text(
                """---
title: "First Page"
source_type: "article"
status: "active"
review_required: false
verified: true
topics:
  - "prompt-engineering"
entities:
  - "Anthropic"
  - "Claude"
concepts:
  - "prompt chaining"
  - "tool use"
quality_score: 0.9
---

# First Page
""",
                encoding="utf-8",
            )

            (wiki_dir / "extracts" / "notes" / "second.md").write_text(
                """---
title: "Second Page"
source_type: "youtube"
status: "active"
review_required: false
verified: true
topics:
  - "agent-architecture"
entities:
  - "Anthropic"
concepts:
  - "prompt chaining"
quality_score: 0.8
---

# Second Page
""",
                encoding="utf-8",
            )

            rebuild_indexes(wiki_dir)

            entities = (wiki_dir / "_indexes" / "entities.md").read_text(encoding="utf-8")
            concepts = (wiki_dir / "_indexes" / "concepts.md").read_text(encoding="utf-8")

            self.assertIn("# Entities", entities)
            self.assertIn("## Anthropic", entities)
            self.assertIn("[[first]] - First Page", entities)
            self.assertIn("[[second]] - Second Page", entities)

            self.assertIn("# Concepts", concepts)
            self.assertIn("## prompt chaining", concepts)
            self.assertIn("[[first]] - First Page", concepts)
            self.assertIn("[[second]] - Second Page", concepts)


if __name__ == "__main__":
    unittest.main()
