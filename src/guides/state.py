"""SQLite state management for pipeline articles."""

import json
import sqlite3
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
STATE_DIR = ROOT / "state"
DB_PATH = STATE_DIR / "articles.db"
JSON_STATE = STATE_DIR / "index.json"


def _get_conn() -> sqlite3.Connection:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = _get_conn()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            slug TEXT PRIMARY KEY,
            raw INTEGER DEFAULT 0,
            content_hash TEXT,
            summarized_at TEXT,
            wiki_propagated INTEGER DEFAULT 0,
            wiki_propagated_at TEXT,
            seo_optimized INTEGER DEFAULT 0,
            published_telegram TEXT,
            quality TEXT,
            quality_checked INTEGER DEFAULT 0
        )
        """
    )
    conn.commit()
    # add columns that may be missing in older DBs
    for col, definition in [("content_hash", "TEXT"), ("quality_checked", "INTEGER DEFAULT 0")]:
        try:
            conn.execute(f"ALTER TABLE articles ADD COLUMN {col} {definition}")
            conn.commit()
        except sqlite3.OperationalError:
            pass  # column already exists
    conn.close()


def migrate_from_json() -> int:
    if not JSON_STATE.exists():
        return 0

    data = json.loads(JSON_STATE.read_text())
    if not data:
        return 0

    conn = _get_conn()
    migrated = 0
    for slug, fields in data.items():
        raw = 1 if fields.get("raw") else 0
        summarized_at = fields.get("summarized_at") or fields.get("ingested_at")
        wiki_propagated = 1 if fields.get("wiki_propagated") else 0
        wiki_propagated_at = fields.get("wiki_propagated_at")
        quality = fields.get("quality")

        conn.execute(
            """
            INSERT OR REPLACE INTO articles (slug, raw, summarized_at, wiki_propagated, wiki_propagated_at, quality)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (slug, raw, summarized_at, wiki_propagated, wiki_propagated_at, quality),
        )
        migrated += 1

    conn.commit()
    conn.close()
    return migrated


def get_state(slug: str) -> dict[str, Any]:
    conn = _get_conn()
    row = conn.execute("SELECT * FROM articles WHERE slug = ?", (slug,)).fetchone()
    conn.close()

    if row is None:
        return {}

    return {
        "raw": bool(row["raw"]),
        "content_hash": row["content_hash"],
        "summarized_at": row["summarized_at"],
        "wiki_propagated": bool(row["wiki_propagated"]),
        "wiki_propagated_at": row["wiki_propagated_at"],
        "seo_optimized": bool(row["seo_optimized"]),
        "published_telegram": row["published_telegram"],
        "quality": row["quality"],
        "quality_checked": bool(row["quality_checked"]),
    }


def set_state(slug: str, field: str, value: Any) -> None:
    conn = _get_conn()

    if field in ("raw", "wiki_propagated", "seo_optimized", "quality_checked"):
        value = 1 if value else 0

    conn.execute(
        f"INSERT INTO articles (slug, {field}) VALUES (?, ?) ON CONFLICT(slug) DO UPDATE SET {field} = ?",
        (slug, value, value),
    )
    conn.commit()
    conn.close()


def list_pending(stage: str) -> list[str]:
    conn = _get_conn()

    if stage == "raw":
        rows = conn.execute("SELECT slug FROM articles WHERE raw = 0").fetchall()
    elif stage == "summarized":
        rows = conn.execute("SELECT slug FROM articles WHERE raw = 1 AND (summarized_at IS NULL OR summarized_at = '')").fetchall()
    elif stage == "wiki_propagated":
        rows = conn.execute("SELECT slug FROM articles WHERE summarized_at IS NOT NULL AND wiki_propagated = 0").fetchall()
    elif stage == "seo_optimized":
        rows = conn.execute("SELECT slug FROM articles WHERE wiki_propagated = 1 AND seo_optimized = 0").fetchall()
    else:
        rows = []

    conn.close()
    return [row["slug"] for row in rows]


def load_state_json() -> dict:
    if JSON_STATE.exists():
        return json.loads(JSON_STATE.read_text())
    return {}


def save_state_json(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    JSON_STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


init_db()

if not DB_PATH.exists() or DB_PATH.stat().st_size == 0:
    init_db()

migrated = migrate_from_json()
if migrated > 0:
    print(f"Migrated {migrated} entries from JSON to SQLite")