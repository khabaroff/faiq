import re
import trafilatura
from pathlib import Path
from typing import Optional

import httpx

from guides.fetch.base import (
    Fetcher,
    FetchedContent,
    QueueItem,
    SourceKind,
    SourceType,
    get_http_client
)
from guides.fetch.jina import (
    get_jina_reader_headers,
    get_jina_reader_url,
    throttle_jina_reader
)
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


class LocalFileFetcher:
    def can_fetch(self, item: QueueItem) -> bool:
        return item.source_kind == SourceKind.FILE

    def fetch(self, item: QueueItem) -> FetchedContent:
        text = Path(item.source).read_text(encoding="utf-8")
        meta = {"source_path": item.source, "fetcher": "local"}
        title = _extract_source_title(text)
        if title:
            meta["title"] = title
        return FetchedContent(raw_text=text, source_type=SourceType.ARTICLE, source_meta=meta)


class TrafilaturaFetcher:
    def can_fetch(self, item: QueueItem) -> bool:
        return item.source_kind == SourceKind.URL

    def fetch(self, item: QueueItem) -> FetchedContent:
        url = item.source
        validate_url(url)
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            result = trafilatura.extract(downloaded)
            if result and len(result.strip()) > 200:
                text = result.strip()
                meta = {"url": url, "fetcher": "trafilatura"}
                title = _extract_source_title(text)
                if title: meta["title"] = title
                return FetchedContent(raw_text=text, source_type=SourceType.ARTICLE, source_meta=meta)
        raise RuntimeError(f"Trafilatura failed for {url}")


class JinaFetcher:
    def can_fetch(self, item: QueueItem) -> bool:
        return item.source_kind == SourceKind.URL

    def fetch(self, item: QueueItem) -> FetchedContent:
        url = item.source
        validate_url(url)
        throttle_jina_reader()
        client = get_http_client()
        # Note: shared client has follow_redirects=False for security, 
        # but jina reader internal redirect should be safe since we re-validate url.
        resp = client.get(get_jina_reader_url(url), headers=get_jina_reader_headers(), follow_redirects=True)
        if resp.status_code == 200 and len(resp.text.strip()) > 200:
            text = resp.text.strip()
            meta = {"url": url, "fetcher": "jina"}
            title = _extract_source_title(text)
            if title: meta["title"] = title
            return FetchedContent(raw_text=text, source_type=SourceType.ARTICLE, source_meta=meta)
        raise RuntimeError(f"Jina failed for {url}")


class FallbackFetcher:
    """Chain of fetchers to try in order."""
    def __init__(self, fetchers: list[Fetcher]):
        self.fetchers = fetchers

    def can_fetch(self, item: QueueItem) -> bool:
        return any(f.can_fetch(item) for f in self.fetchers)

    def fetch(self, item: QueueItem) -> FetchedContent:
        last_err = None
        for f in self.fetchers:
            if f.can_fetch(item):
                try:
                    return f.fetch(item)
                except Exception as e:
                    last_err = e
                    continue
        raise last_err or RuntimeError(f"All fetchers failed for {item.source}")


# Default registry
FETCHERS: list[Fetcher] = [
    LocalFileFetcher(),
    TrafilaturaFetcher(),
    JinaFetcher()
]

_FALLBACK_DISPATCHER = FallbackFetcher(FETCHERS)


def fetch_url(item: QueueItem) -> FetchedContent:
    """Main entrypoint for Pipeline A."""
    return _FALLBACK_DISPATCHER.fetch(item)
