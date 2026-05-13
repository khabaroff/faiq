import pytest
from pathlib import Path
from guides.security.fs_safety import safe_join, assert_safe_slug


def test_safe_join_allows_normal(tmp_path):
    result = safe_join(tmp_path, "my-article.md")
    assert result == tmp_path / "my-article.md"


def test_safe_join_blocks_traversal(tmp_path):
    with pytest.raises(ValueError, match="[Pp]ath traversal|escapes"):
        safe_join(tmp_path, "../etc/passwd")


def test_safe_join_blocks_double_traversal(tmp_path):
    with pytest.raises(ValueError):
        safe_join(tmp_path, "../../etc/shadow")


@pytest.mark.parametrize("slug,should_raise", [
    ("valid-slug-123", False),
    ("a", False),
    ("abc123", False),
    ("a" * 80, False),        # max length
    ("a" * 81, True),         # exceeds 80
    ("-starts-with-dash", True),
    ("UPPERCASE", True),
    ("has space", True),
    ("has.dot", True),
    ("../etc/passwd", True),
])
def test_assert_safe_slug(slug, should_raise):
    if should_raise:
        with pytest.raises(ValueError):
            assert_safe_slug(slug)
    else:
        assert assert_safe_slug(slug) == slug
