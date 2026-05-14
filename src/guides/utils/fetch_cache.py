import sqlite3
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from guides.settings import get_settings

_local = threading.local()

def _get_conn() -> sqlite3.Connection:
    if not hasattr(_local, "conn"):
        settings = get_settings()
        db_path = settings.state_dir / "fetch_cache.sqlite"
        settings.state_dir.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(db_path), timeout=5.0)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS fetch_failures (
                url TEXT PRIMARY KEY,
                code INTEGER,
                expires_at TEXT
            )
            """
        )
        conn.commit()
        _local.conn = conn
    return _local.conn

def get_cached_failure(url: str) -> Optional[int]:
    """Return error code if failure is cached and not expired, else None."""
    conn = _get_conn()
    now = datetime.now().isoformat()
    row = conn.execute(
        "SELECT code FROM fetch_failures WHERE url = ? AND expires_at > ?",
        (url, now)
    ).fetchone()
    if row:
        return row[0]
    return None

def cache_failure(url: str, code: int, ttl_hours: int = 1) -> None:
    """Cache failure for a specific URL."""
    conn = _get_conn()
    expires_at = (datetime.now() + timedelta(hours=ttl_hours)).isoformat()
    conn.execute(
        "INSERT OR REPLACE INTO fetch_failures (url, code, expires_at) VALUES (?, ?, ?)",
        (url, code, expires_at)
    )
    conn.commit()
