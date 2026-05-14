import pytest
from guides.pipelines.a_ingest import slugify as slugify_a
from guides.pipelines.c_wiki_update import slugify as slugify_c
from guides.slugify import short_hash_slug, slugify


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


@pytest.mark.parametrize("text,expected", [
    ("Claude Code", "claude-code"),
    ("GPT-4o mini", "gpt-4o-mini"),
    ("Привет, мир!", "привет-мир"),
    ("a" * 120, "a" * 80),
    ("___", ""),
])
def test_canonical_slugify_corpus(text, expected):
    assert slugify(text) == expected


def test_short_hash_slug_is_stable_and_8_chars():
    result = short_hash_slug("same-input")
    assert result == short_hash_slug("same-input")
    assert len(result) == 8
    assert result != short_hash_slug("other-input")
