from __future__ import annotations

import unittest

from guides.verify import run_verify


class VerifyThresholdTests(unittest.TestCase):
    def test_high_quality_page_with_soft_warning_can_be_verified(self) -> None:
        source = "# Original\n\nBody"
        output = """---
id: "src-2026-05-11-abcd1234"
title: "Good Page"
type: "source-page"
status: "active"
source_type: "article"
content_format: "text"
origin: "file"
url: ""
created_at: "2026-05-11"
updated_at: "2026-05-11"
language: "ru"
tags:
  - "Agent Architecture"
topics: []
entities: []
concepts: []
related: []
review_required: false
verified: false
quality_score: 0.0
provenance:
  extracted: 0.9
  inferred: 0.08
  ambiguous: 0.02
source_paths: []
prompt_version: "article_rewrite@v1"
---

# Good Page

## Краткое изложение

Text

## Core idea

Text
"""

        status, result, score = run_verify(source, output, ["Agent Architecture"], source_type="article")

        self.assertEqual(status, "verified")
        self.assertTrue(result["passed"])
        self.assertGreaterEqual(score, 0.80)
        self.assertFalse(result["checks"]["no_english_section_headers"])

    def test_low_quality_page_stays_needs_review(self) -> None:
        source = "Body"
        output = """---
id: "src-2026-05-11-abcd1234"
title: "Good Page"
type: "source-page"
status: "active"
source_type: "article"
content_format: "text"
origin: "file"
url: ""
created_at: "2026-05-11"
updated_at: "2026-05-11"
language: "ru"
tags: []
topics: []
entities: []
concepts: []
related: []
review_required: false
verified: false
quality_score: 0.0
provenance:
  extracted: 0.9
  inferred: 0.08
  ambiguous: 0.02
source_paths: []
prompt_version: "article_rewrite@v1"
---

# Good Page

## Краткое изложение

Text
"""

        status, result, score = run_verify(source, output, [], source_type="article")

        self.assertEqual(status, "needs_review")
        self.assertFalse(result["passed"])
        self.assertGreaterEqual(score, 0.80)


if __name__ == "__main__":
    unittest.main()
