import pytest
from guides.pipelines.a_ingest import slugify as slugify_a
from guides.pipelines.c_wiki_update import slugify as slugify_c


@pytest.mark.parametrize("text,expected_a,expected_c", [
    ("Claude Code", "claude-code", "claude-code"),
    ("GPT-4o mini", "gpt-4o-mini", "gpt-4o-mini"),
    ("", "", ""),
    ("   ", "", ""),
    ("A" * 100, "a" * 80, "a" * 80),
])
def test_slugify_agree_on_common_cases(text, expected_a, expected_c):
    assert slugify_a(text) == expected_a
    assert slugify_c(text) == expected_c


def test_slugify_underscore_divergence():
    """Document known divergence: a_ingest strips _, c_wiki_update preserves."""
    # This test documents the current behavior (NOT the desired behavior)
    # Fix: unify into guides/utils/slugify.py (faiq-h2)
    assert slugify_a("claude_code") == "claude-code"   # strips underscore
    assert slugify_c("claude_code") == "claude_code"   # preserves underscore
    # These should be the same after faiq-h2 is resolved
