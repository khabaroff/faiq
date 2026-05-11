from __future__ import annotations

import subprocess
from pathlib import Path

import httpx

from guides.fetch.base import FetchedContent, QueueItem, SourceKind, SourceType


def _fetch_with_defuddle(url: str) -> str:
    try:
        result = subprocess.run(
            ["defuddle", url],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return ""

    if result.returncode != 0:
        return ""

    return result.stdout.strip()


def _fetch_with_http(url: str) -> str:
    response = httpx.get(
        url,
        headers={"Accept": "text/markdown", "User-Agent": "Mozilla/5.0"},
        follow_redirects=True,
        timeout=30,
    )
    return response.text.strip()


def fetch_url(item: QueueItem) -> FetchedContent:
    if item.source_kind == SourceKind.FILE:
        raw_text = Path(item.source).read_text(encoding="utf-8").strip()
        if not raw_text:
            raise ValueError("Cannot fetch: url")
        return FetchedContent(
            raw_text=raw_text,
            source_type=SourceType.ARTICLE,
            source_meta={"path": item.source, "fetcher": "file"},
        )

    raw_text = _fetch_with_defuddle(item.source)
    fetcher = "defuddle"

    if not raw_text:
        raw_text = _fetch_with_http(item.source)
        fetcher = "http"

    if not raw_text:
        raise ValueError("Cannot fetch: url")

    return FetchedContent(
        raw_text=raw_text,
        source_type=SourceType.ARTICLE,
        source_meta={"url": item.source, "fetcher": fetcher},
    )
