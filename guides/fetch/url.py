import shutil
import subprocess
from pathlib import Path

import httpx

from guides.fetch.base import FetchedContent, QueueItem, SourceKind, SourceType


def fetch_url(item: QueueItem) -> FetchedContent:
    if item.source_kind == SourceKind.FILE:
        text = Path(item.source).read_text(encoding="utf-8")
        return FetchedContent(raw_text=text, source_type=SourceType.ARTICLE, source_meta={"path": item.source, "fetcher": "local"})

    url = item.source
    text, fetcher = _try_defuddle(url) or _try_jina(url) or _try_http_markdown(url) or (None, None)

    if not text:
        raise RuntimeError(f"Cannot fetch: {url}")

    return FetchedContent(
        raw_text=text,
        source_type=SourceType.ARTICLE,
        source_meta={"url": url, "fetcher": fetcher},
    )


def _try_defuddle(url: str) -> tuple[str, str] | None:
    cmd = shutil.which("defuddle") or shutil.which("defuddle-cli")
    if not cmd:
        try:
            result = subprocess.run(["npx", "-y", "defuddle-cli", "parse", url], capture_output=True, text=True, timeout=60)
            if result.returncode == 0 and len(result.stdout.strip()) > 200:
                return result.stdout.strip(), "defuddle-npx"
        except Exception:
            pass
        return None
    try:
        result = subprocess.run([cmd, "parse", url], capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and len(result.stdout.strip()) > 200:
            return result.stdout.strip(), "defuddle"
    except Exception:
        pass
    return None


def _try_jina(url: str) -> tuple[str, str] | None:
    try:
        resp = httpx.get(f"https://r.jina.ai/{url}", headers={"Accept": "text/markdown"}, timeout=30, follow_redirects=True)
        if resp.status_code == 200 and len(resp.text.strip()) > 200:
            return resp.text.strip(), "jina"
    except Exception:
        pass
    return None


def _try_http_markdown(url: str) -> tuple[str, str] | None:
    try:
        resp = httpx.get(url, headers={"Accept": "text/markdown", "User-Agent": "Mozilla/5.0"}, timeout=30, follow_redirects=True)
        ct = resp.headers.get("content-type", "")
        if resp.status_code == 200 and "html" not in ct and len(resp.text.strip()) > 200:
            return resp.text.strip(), "http-markdown"
    except Exception:
        pass
    return None
