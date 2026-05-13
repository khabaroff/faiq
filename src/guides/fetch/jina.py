from __future__ import annotations

import os
import threading
import time
from urllib.parse import quote_plus

JINA_READER_MIN_INTERVAL_SECONDS = 3.0

_reader_throttle_lock = threading.Lock()
_last_reader_request_at: float | None = None


def get_jina_reader_headers() -> dict[str, str]:
    return {"Accept": "text/markdown"}


def get_jina_search_headers(*, respond_with_no_content: bool = False) -> dict[str, str]:
    headers = {"Accept": "text/markdown"}
    token = _get_jina_api_key()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if respond_with_no_content:
        headers["X-Respond-With"] = "no-content"
    return headers


def get_jina_reader_url(url: str) -> str:
    return f"https://r.jina.ai/{url}"


def get_jina_search_url(query: str) -> str:
    return f"https://search.jina.ai/?q={quote_plus(query)}"


def throttle_jina_reader() -> None:
    global _last_reader_request_at

    with _reader_throttle_lock:
        now = time.monotonic()
        if _last_reader_request_at is not None:
            delay = JINA_READER_MIN_INTERVAL_SECONDS - (now - _last_reader_request_at)
            if delay > 0:
                time.sleep(delay)
                now = time.monotonic()
        _last_reader_request_at = now


def _get_jina_api_key() -> str | None:
    env_token = os.getenv("JINA_API_KEY")
    if env_token:
        return env_token

    try:
        from guides.settings import Settings

        return Settings().jina_api_key
    except Exception:
        return None
