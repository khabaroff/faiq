from __future__ import annotations

import unittest
from unittest.mock import patch

from guides.enrich.tags import extract_tags


class ExtractTagsFallbackTests(unittest.TestCase):
    def test_falls_back_to_heuristics_when_llm_output_is_invalid(self) -> None:
        text = """# Building Effective Agents

## Ключевая идея

Anthropic argues for simple, composable patterns.

## Key concepts

Agent orchestration, tool use, workflows.
"""

        with patch("guides.enrich.tags.call_llm", return_value="not json"):
            result = extract_tags(text)

        self.assertTrue(result["tags"])
        self.assertTrue(result["topics"])
        self.assertTrue(result["entities"])
        self.assertTrue(result["concepts"])


if __name__ == "__main__":
    unittest.main()
