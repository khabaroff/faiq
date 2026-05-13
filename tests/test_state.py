import pytest
from pathlib import Path


def test_set_get_state(isolated_state_db):
    from guides.state import set_state, get_state
    set_state("slug-a", "raw", True)
    result = get_state("slug-a")
    assert result["raw"] in (1, True)


def test_get_state_missing_slug(isolated_state_db):
    from guides.state import get_state
    result = get_state("nonexistent")
    assert result == {}


def test_find_by_content_hash(isolated_state_db):
    from guides.state import set_state, find_by_content_hash
    set_state("slug-b", "content_hash", "abc123")
    assert find_by_content_hash("abc123") == "slug-b"
    assert find_by_content_hash("unknown") is None


def test_update_frontmatter_creates_if_missing(isolated_state_db, tmp_path):
    from guides.state import update_frontmatter
    f = tmp_path / "test.md"
    f.write_text("Body text")
    update_frontmatter(f, {"status": "draft"})
    assert "status: draft" in f.read_text()


def test_update_frontmatter_updates_existing(isolated_state_db, tmp_path):
    from guides.state import update_frontmatter
    f = tmp_path / "test.md"
    f.write_text("---\nslug: foo\n---\n\nBody")
    update_frontmatter(f, {"status": "reviewed"})
    text = f.read_text()
    assert "status: reviewed" in text
    assert "slug: foo" in text


def test_update_frontmatter_preserves_body(isolated_state_db, tmp_path):
    from guides.state import update_frontmatter
    f = tmp_path / "test.md"
    f.write_text("---\nslug: foo\n---\n\n# Title\n\nBody paragraph.")
    update_frontmatter(f, {"status": "reviewed"})
    assert "# Title" in f.read_text()
    assert "Body paragraph." in f.read_text()
