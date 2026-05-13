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


def test_slugify_unified_underscore_handling():
    """After faiq-h2: both pipelines use guides.utils.slugify — underscores stripped."""
    assert slugify_a("claude_code") == "claude-code"
    assert slugify_c("claude_code") == "claude-code"
    assert slugify_a is slugify_c
