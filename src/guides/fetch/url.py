import re
import trafilatura
from pathlib import Path

import httpx

from guides.fetch.base import FetchedContent, QueueItem, SourceKind, SourceType
from guides.fetch.jina import get_jina_reader_headers, get_jina_reader_url, throttle_jina_reader
from guides.security.url_safety import validate_url


def _extract_source_title(text: str) -> str:
    stripped = text.lstrip()
    if stripped.startswith("---\n"):
        lines = stripped.splitlines()
        for line in lines[1:]:
            if line.strip() == "---":
                break
            match = re.match(r'^title:\s*"?(.+?)"?\s*$', line)
            if match:
                return match.group(1).strip()

    for line in stripped.splitlines():
        candidate = line.strip()
        if candidate.startswith("# "):
            return candidate[2:].strip()
    return ""


def fetch_url(item: QueueItem) -> FetchedContent:
    if item.source_kind == SourceKind.FILE:
        text = Path(item.source).read_text(encoding="utf-8")
        meta = {"source_path": item.source, "fetcher": "local"}
        title = _extract_source_title(text)
        if title:
            meta["title"] = title
        return FetchedContent(raw_text=text, source_type=SourceType.ARTICLE, source_meta=meta)

    url = item.source
    validate_url(url)
    text, fetcher = _try_trafilatura(url) or _try_cloudflare_markdown(url) or _try_jina(url) or (None, None)

    if not text:
        raise RuntimeError(f"Cannot fetch: {url}")

    source_meta = {"url": url, "fetcher": fetcher}
    title = _extract_source_title(text)
    if title:
        source_meta["title"] = title

    return FetchedContent(
        raw_text=text,
        source_type=SourceType.ARTICLE,
        source_meta=source_meta,
    )


def _try_trafilatura(url: str) -> tuple[str, str] | None:
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            result = trafilatura.extract(downloaded)
            if result and len(result.strip()) > 200:
                return result.strip(), "trafilatura"
    except Exception:
        pass
    return None


def _try_cloudflare_markdown(url: str) -> tuple[str, str] | None:
    try:
        resp = httpx.get(url, headers={"Accept": "text/markdown", "User-Agent": "Mozilla/5.0"}, timeout=30, follow_redirects=True)
        ct = resp.headers.get("content-type", "")
        if resp.status_code == 200 and "html" not in ct and len(resp.text.strip()) > 200:
            return resp.text.strip(), "cloudflare-markdown"
    except Exception:
        pass
    return None


def _try_jina(url: str) -> tuple[str, str] | None:
    try:
        throttle_jina_reader()
        resp = httpx.get(get_jina_reader_url(url), headers=get_jina_reader_headers(), timeout=30, follow_redirects=True)
        if resp.status_code == 200 and len(resp.text.strip()) > 200:
            return resp.text.strip(), "jina"
    except Exception:
        pass
    return None
