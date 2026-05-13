import shutil
import subprocess
import re
from pathlib import Path

import httpx

from guides.fetch.base import FetchedContent, QueueItem, SourceKind, SourceType
from guides.fetch.jina import get_jina_reader_headers, get_jina_reader_url, throttle_jina_reader


def _extract_source_title(text: str) -> str:
    stripped = text.lstrip()
    if stripped.startswith("---\n"):
        lines = stripped.splitlines()
        in_frontmatter = True
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
    text, fetcher = _try_defuddle(url) or _try_cloudflare_markdown(url) or _try_jina(url) or (None, None)

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
