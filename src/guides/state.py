"""SQLite state management for pipeline articles."""

import json
import sqlite3
import threading
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from guides.atomic_write import atomic_write_text
from guides.models import ArticleState

ROOT = Path(__file__).resolve().parent.parent.parent
STATE_DIR = ROOT / "state"
DB_PATH = STATE_DIR / "articles.db"
JSON_STATE = STATE_DIR / "index.json"

_local = threading.local()


def _get_conn() -> sqlite3.Connection:
    if not hasattr(_local, "conn"):
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH), timeout=5.0)  # 5000ms busy_timeout
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        _local.conn = conn
    return _local.conn


def _sql_type_for_field(field_info) -> str:
    """Map ArticleState field to SQLite column definition."""
    from typing import get_origin, get_args
    annotation = field_info.annotation
    default = field_info.default
    origin = get_origin(annotation)
    if origin is not None:
        args = get_args(annotation)
        annotation = next((a for a in args if a is not type(None)), str)
    if annotation is bool:
        return f"INTEGER DEFAULT {1 if default else 0}"
    if annotation is int:
        return f"INTEGER DEFAULT {default if isinstance(default, int) else 0}"
    if annotation is str and isinstance(default, str):
        return f"TEXT DEFAULT '{default}'"
    return "TEXT"


def _build_alter_columns() -> list[tuple[str, str]]:
    """Generate ALTER TABLE columns from ArticleState."""
    columns: list[tuple[str, str]] = []
    for name, field_info in ArticleState.model_fields.items():
        if name == "slug":
            continue
        columns.append((name, _sql_type_for_field(field_info)))
    return columns


def init_db() -> None:
     conn = _get_conn()
     # Base CREATE TABLE — must match ArticleState fields
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
             quality_checked INTEGER DEFAULT 0,
             qc_hash TEXT,
             status TEXT DEFAULT 'draft',
             revision_count INTEGER DEFAULT 0,
             last_edited_at TEXT,
             last_edited_by TEXT,
             compacted INTEGER DEFAULT 0
         )
         """
     )
     conn.commit()
     # Add columns that may be missing in older DBs (migrations)
     for col, definition in _build_alter_columns():
         try:
             conn.execute(f"ALTER TABLE articles ADD COLUMN {col} {definition}")
             conn.commit()
         except sqlite3.OperationalError:
             pass  # column already exists


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
    return migrated


def _ensure_db() -> None:
    if not DB_PATH.exists():
        init_db()
        migrate_from_json()


def get_state(slug: str) -> dict[str, Any]:
    _ensure_db()
    conn = _get_conn()
    row = conn.execute("SELECT * FROM articles WHERE slug = ?", (slug,)).fetchone()

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
        "qc_hash": row["qc_hash"],
        "status": row["status"],
        "revision_count": row["revision_count"],
        "last_edited_at": row["last_edited_at"],
        "last_edited_by": row["last_edited_by"],
        "compacted": bool(row["compacted"]),
    }


_VALID_FIELDS: frozenset[str] = frozenset(ArticleState.model_fields)

_FIELD_SQL: dict[str, str] = {
    f: f"INSERT INTO articles (slug, {f}) VALUES (?, ?) ON CONFLICT(slug) DO UPDATE SET {f} = ?"
    for f in _VALID_FIELDS
}


def set_state(slug: str, field: str, value: Any) -> None:
    _ensure_db()
    if field not in _VALID_FIELDS:
        raise ValueError(f"Unknown state field: {field!r}")

    conn = _get_conn()

    if field in ("raw", "wiki_propagated", "seo_optimized", "quality_checked", "compacted"):
        value = 1 if value else 0

    conn.execute(_FIELD_SQL[field], (slug, value, value))
    conn.commit()


def find_by_content_hash(content_hash: str) -> str | None:
    _ensure_db()
    conn = _get_conn()
    row = conn.execute("SELECT slug FROM articles WHERE content_hash = ?", (content_hash,)).fetchone()
    return row["slug"] if row else None


def list_pending(stage: str) -> list[str]:
     _ensure_db()
     conn = _get_conn()

     if stage == "raw":
         rows = conn.execute("SELECT slug FROM articles WHERE raw = 0").fetchall()
     elif stage == "summarized":
         rows = conn.execute("SELECT slug FROM articles WHERE raw = 1 AND (summarized_at IS NULL OR summarized_at = '')").fetchall()
     elif stage == "wiki_propagated":
         rows = conn.execute("SELECT slug FROM articles WHERE summarized_at IS NOT NULL AND wiki_propagated = 0").fetchall()
     elif stage == "seo_optimized":
         rows = conn.execute("SELECT slug FROM articles WHERE wiki_propagated = 1 AND seo_optimized = 0").fetchall()
     elif stage == "published":
         rows = conn.execute("SELECT slug FROM articles WHERE seo_optimized = 1 AND published_telegram IS NULL").fetchall()
     else:
         rows = []

     return [row["slug"] for row in rows]


def update_frontmatter(filepath: Path, updates: dict) -> None:
     """Обновляет YAML frontmatter в .md файле, сохраняя тело."""
     text = filepath.read_text(encoding="utf-8")
     if not text.startswith("---"):
         fm_str = "---\n" + yaml.safe_dump(updates, allow_unicode=True, default_flow_style=False) + "---\n\n"
         atomic_write_text(filepath, fm_str + text)
         return

     end = text.index("\n---\n", 4)
     body = text[end + 5:]
     try:
         fm = yaml.safe_load(text[4:end]) or {}
     except yaml.YAMLError:
         fm = {}
     fm.update(updates)
     new_fm = yaml.safe_dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
     atomic_write_text(filepath, f"---\n{new_fm}---\n{body}")


def set_status(slug: str, filepath: Path | None, status: str,
                edited_by: str = "", filepath_for_fm: Path | None = None) -> None:
     """Устанавливает status в SQLite и обновляет frontmatter .md файла."""
     _ensure_db()
     now = datetime.now().isoformat(timespec="seconds")
     conn = _get_conn()
     conn.execute(
         "INSERT INTO articles (slug, status, last_edited_at, last_edited_by) "
         "VALUES (?, ?, ?, ?) "
         "ON CONFLICT(slug) DO UPDATE SET status = ?, last_edited_at = ?, last_edited_by = ?",
         (slug, status, now, edited_by, status, now, edited_by),
     )
     conn.commit()

     target = filepath_for_fm or filepath
     if target:
         update_frontmatter(target, {"status": status, "last_edited_at": now})
         if edited_by:
             # Читаем текущее fm чтобы добавить last_edited_by
             _update_fm_field(target, "last_edited_by", edited_by)


def _update_fm_field(filepath: Path, key: str, value: str) -> None:
     """Обновляет одно поле в frontmatter."""
     update_frontmatter(filepath, {key: value})


def load_state_json() -> dict:
    if JSON_STATE.exists():
        return json.loads(JSON_STATE.read_text())
    return {}


def save_state_json(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    atomic_write_text(JSON_STATE, json.dumps(state, ensure_ascii=False, indent=2))
