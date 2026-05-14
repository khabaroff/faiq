import unittest
import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from guides.state import (
    init_db, migrate_from_json, get_state, set_state,
    find_by_content_hash, list_pending, update_frontmatter,
    set_status, _VALID_FIELDS, _build_alter_columns
)
from guides.models import ArticleState
from guides.frontmatter import VALID_STATE_KEYS, filter_state_keys

class StateTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = TemporaryDirectory()
        self.state_path = Path(self.tmpdir.name)
        self.db_path = self.state_path / "articles.db"
        self.json_path = self.state_path / "index.json"

        # Patch paths in the module
        self.patches = [
            patch("guides.state.STATE_DIR", self.state_path),
            patch("guides.state.DB_PATH", self.db_path),
            patch("guides.state.JSON_STATE", self.json_path),
        ]
        for p in self.patches:
            p.start()

        # Reset connection cache so each test gets its own DB
        import guides.state
        if hasattr(guides.state._local, "conn"):
            try:
                guides.state._local.conn.close()
            except Exception:
                pass
            delattr(guides.state._local, "conn")

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.tmpdir.cleanup()

    def test_schema_invariant(self):
        """Property: ArticleState fields == _VALID_FIELDS == DB columns == frontmatter state keys."""
        model_fields = set(ArticleState.model_fields)
        valid_fields = set(_VALID_FIELDS)
        frontmatter_state_keys = VALID_STATE_KEYS

        # 1. Pydantic model == _VALID_FIELDS
        self.assertEqual(model_fields, valid_fields)
        self.assertEqual(model_fields, frontmatter_state_keys)

        # 2. SQLite schema includes all ArticleState fields (plus slug PK)
        init_db()
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.execute("PRAGMA table_info(articles)")
        db_columns = {row[1] for row in cursor.fetchall()}
        conn.close()

        self.assertIn("slug", db_columns)
        for field in model_fields:
            self.assertIn(field, db_columns, f"DB missing column for {field}")

        # 3. ALTER TABLE columns derived from ArticleState
        alter_cols = {name for name, _ in _build_alter_columns()}
        self.assertEqual(alter_cols, model_fields)

        # 4. filter_state_keys only keeps ArticleState fields
        mixed = {"status": "ok", "tools": ["x"], "slug": "s", "raw": True}
        filtered = filter_state_keys(mixed)
        self.assertEqual(filtered, {"status": "ok", "raw": True})

    def test_init_db_and_idempotency(self):
        init_db()
        self.assertTrue(self.db_path.exists())

        # Verify columns
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.execute("PRAGMA table_info(articles)")
        cols = {row[1] for row in cursor.fetchall()}
        self.assertIn("content_hash", cols)
        self.assertIn("compacted", cols)
        conn.close()

        # Run again to test ALTER TABLE idempotency
        init_db()

    def test_migrate_from_json(self):
        data = {
            "test-slug": {
                "raw": True,
                "ingested_at": "2026-05-13T10:00:00",
                "wiki_propagated": False,
                "quality": "ok"
            }
        }
        self.json_path.write_text(json.dumps(data))

        init_db()
        count = migrate_from_json()
        self.assertEqual(count, 1)

        state = get_state("test-slug")
        self.assertTrue(state["raw"])
        self.assertEqual(state["summarized_at"], "2026-05-13T10:00:00")
        self.assertEqual(state["quality"], "ok")

    def test_get_set_state(self):
        init_db()
        set_state("slug1", "content_hash", "abc123")
        set_state("slug1", "raw", True)

        state = get_state("slug1")
        self.assertEqual(state["content_hash"], "abc123")
        self.assertTrue(state["raw"])
        self.assertFalse(state["wiki_propagated"])

        # Unknown field
        with self.assertRaises(ValueError):
            set_state("slug1", "unknown_field", "val")

    def test_find_by_content_hash(self):
        init_db()
        set_state("slug-h", "content_hash", "hash-val")
        self.assertEqual(find_by_content_hash("hash-val"), "slug-h")
        self.assertIsNone(find_by_content_hash("nonexistent"))

    def test_list_pending(self):
        init_db()
        # Ensure clean state by deleting all rows first
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("DELETE FROM articles")
        conn.commit()
        conn.close()
        # Clear cache so _ensure_db picks up the clean DB
        import guides.state
        if hasattr(guides.state._local, "conn"):
            delattr(guides.state._local, "conn")

        set_state("s1", "raw", False)
        set_state("s2", "raw", True)
        set_state("s2", "summarized_at", None)
        set_state("s3", "raw", True)
        set_state("s3", "summarized_at", "2026-05-13")
        set_state("s3", "wiki_propagated", False)

        self.assertEqual(list_pending("raw"), ["s1"])
        self.assertEqual(list_pending("summarized"), ["s2"])
        self.assertEqual(list_pending("wiki_propagated"), ["s3"])
        self.assertEqual(list_pending("unknown"), [])

    def test_update_frontmatter(self):
        md_file = Path(self.tmpdir.name) / "test.md"
        md_file.write_text("# Title\n\nBody")

        update_frontmatter(md_file, {"status": "active", "slug": "test"})
        content = md_file.read_text()
        self.assertTrue(content.startswith("---"))
        self.assertIn("status: active", content)
        self.assertIn("# Title", content)

        # Update existing
        update_frontmatter(md_file, {"status": "reviewed"})
        content = md_file.read_text()
        self.assertIn("status: reviewed", content)
        self.assertIn("slug: test", content)

    def test_set_status(self):
        init_db()
        md_file = Path(self.tmpdir.name) / "test.md"
        md_file.write_text("---\nstatus: draft\n---\nBody")

        set_status("slug1", md_file, "active", edited_by="test-user")

        state = get_state("slug1")
        self.assertEqual(state["status"], "active")
        self.assertEqual(state["last_edited_by"], "test-user")

        content = md_file.read_text()
        self.assertIn("status: active", content)
        self.assertIn("last_edited_by: test-user", content)

    def test_migrate_from_json_empty(self):
        init_db()
        # No file
        self.assertEqual(migrate_from_json(), 0)
        # Empty file
        self.json_path.write_text("{}")
        self.assertEqual(migrate_from_json(), 0)

    def test_get_state_nonexistent(self):
        init_db()
        self.assertEqual(get_state("nonexistent"), {})

    def test_list_pending_more_stages(self):
        init_db()
        # Clean state first
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("DELETE FROM articles")
        conn.commit()
        conn.close()
        import guides.state
        if hasattr(guides.state._local, "conn"):
            delattr(guides.state._local, "conn")

        set_state("s1", "wiki_propagated", True)
        set_state("s1", "seo_optimized", False)
        set_state("s2", "seo_optimized", True)
        set_state("s2", "published_telegram", None)

        self.assertEqual(list_pending("seo_optimized"), ["s1"])
        self.assertEqual(list_pending("published"), ["s2"])

    def test_update_frontmatter_corrupt_yaml(self):
        md_file = Path(self.tmpdir.name) / "corrupt.md"
        md_file.write_text("---\n[corrupt: yaml\n---\nBody")
        # Should handle error and continue with empty dict
        update_frontmatter(md_file, {"status": "fixed"})
        self.assertIn("status: fixed", md_file.read_text())

    def test_save_load_state_json(self):
        from guides.state import save_state_json, load_state_json
        data = {"a": 1}
        save_state_json(data)
        self.assertEqual(load_state_json(), data)
        # Non-existent
        self.json_path.unlink()
        self.assertEqual(load_state_json(), {})

    def test_concurrent_set_state_no_loss(self):
        init_db()

        def write_one(i: int):
            import guides.state

            if hasattr(guides.state._local, "conn"):
                try:
                    guides.state._local.conn.close()
                except Exception:
                    pass
                delattr(guides.state._local, "conn")
            set_state(f"slug-{i}", "content_hash", f"hash-{i}")

        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(write_one, range(20)))

        for i in range(20):
            self.assertEqual(get_state(f"slug-{i}")["content_hash"], f"hash-{i}")

    def test_query_plan_uses_index(self):
        init_db()
        conn = sqlite3.connect(str(self.db_path))
        rows = conn.execute(
            "EXPLAIN QUERY PLAN SELECT slug FROM articles WHERE content_hash = ?",
            ("hash",),
        ).fetchall()
        conn.close()
        plan_text = " ".join(str(row) for row in rows).lower()
        self.assertIn("index", plan_text)

if __name__ == "__main__":
    unittest.main()
