import asyncio
import logging
import re
import tempfile
import time
from inspect import isawaitable
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import httpx

from guides.fetch.base import FetchedContent, QueueItem, SourceType, Fetcher
from guides.security.url_safety import validate_url
from guides.utils.fetch_cache import cache_failure, get_cached_failure

logger = logging.getLogger(__name__)

_TOTAL_BUDGET_SECONDS = 120
_UNAVAILABLE_PATTERNS = [
    "403",
    "Forbidden",
    "410",
    "Gone",
    "Video unavailable",
    "This video has been removed",
    "Private video",
    "This video is private",
    "This video is not available",
]
_TRANSCRIBE_BASE = "https://youtubetranscribe.khabaroff.studio"


def _cache_key_for_url(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()

    if host == "youtu.be":
        video_id = parsed.path.strip("/")
        if video_id:
            return f"youtube:{video_id}"

    if "youtube.com" in host:
        video_id = parse_qs(parsed.query).get("v", [""])[0]
        if video_id:
            return f"youtube:{video_id}"

    return url


async def _terminate_process(proc: asyncio.subprocess.Process) -> None:
    try:
        result = proc.kill()
        if isawaitable(result):
            await result
    except Exception:
        pass


class YouTubeFetcher:
    def can_fetch(self, item: QueueItem) -> bool:
        url = item.source.lower()
        return "youtube.com" in url or "youtu.be" in url

    def fetch(self, item: QueueItem) -> FetchedContent:
        """Synchronous wrapper for async fetch_youtube."""
        return asyncio.run(fetch_youtube(item))


async def fetch_youtube(item: QueueItem) -> FetchedContent:
    url = item.source
    validate_url(url)
    cache_key = _cache_key_for_url(url)
    deadline = time.monotonic() + _TOTAL_BUDGET_SECONDS

    cached_code = get_cached_failure(cache_key)
    if cached_code:
        logger.info("YouTube cache hit for %s (code %s)", url, cached_code)
        return FetchedContent(
            raw_text="",
            source_type=SourceType.YOUTUBE,
            source_meta={"url": url, "error": f"cached_{cached_code}"},
        )

    transcript = await _try_ytdlp(url, cache_key, deadline)
    cached_code = get_cached_failure(cache_key)
    if not transcript and cached_code:
        return FetchedContent(
            raw_text="",
            source_type=SourceType.YOUTUBE,
            source_meta={"url": url, "error": f"fail_fast_{cached_code}"},
        )

    if not transcript:
        transcript = await _try_transcribe_service(url, cache_key, deadline)

    meta: dict = {"url": url}
    if not transcript:
        meta["error"] = "no_transcript"
        transcript = ""

    return FetchedContent(raw_text=transcript, source_type=SourceType.YOUTUBE, source_meta=meta)


async def _try_ytdlp(url: str, cache_key: str, deadline: float) -> str | None:
    attempts = [
        ["--write-auto-sub", "--sub-lang", "en"],
        ["--write-auto-sub", "--sub-lang", "ru"],
        ["--write-auto-sub", "--all-subs"],
    ]
    for args in attempts:
        if time.monotonic() >= deadline:
            logger.warning("YouTube fetch budget exhausted before yt-dlp attempt for %s", url)
            return None
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                cmd = [
                    "yt-dlp",
                    *args,
                    "--skip-download",
                    "--socket-timeout",
                    "10",
                    "--no-warnings",
                    "--output",
                    f"{tmpdir}/yt",
                    "--",
                    url,
                ]
                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                try:
                    _stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=10)
                except asyncio.TimeoutError:
                    if proc.returncode is None:
                        await _terminate_process(proc)
                    logger.warning("yt-dlp timeout for %s — trying next attempt within budget", url)
                    continue

                stderr_text = stderr.decode()
                for pattern in _UNAVAILABLE_PATTERNS:
                    if pattern in stderr_text:
                        logger.warning("YouTube non-retryable error for %s (pattern: %s)", url, pattern)
                        cache_code = 404
                        if "403" in stderr_text or "Forbidden" in stderr_text:
                            cache_code = 403
                        elif "410" in stderr_text or "Gone" in stderr_text:
                            cache_code = 410
                        cache_failure(cache_key, cache_code)
                        return None

                vtt_files = list(Path(tmpdir).glob("*.vtt"))
                if vtt_files:
                    raw = vtt_files[0].read_text(encoding="utf-8")
                    return _parse_vtt(raw)
        except Exception as exc:
            logger.debug("yt-dlp attempt failed: %s", exc)
            continue
    return None


def _parse_vtt(vtt: str) -> str:
    lines = []
    seen: set[str] = set()
    for line in vtt.splitlines():
        if re.match(r"^\d{2}:\d{2}", line) or line.startswith("WEBVTT") or "-->" in line or not line.strip():
            continue
        clean = re.sub(r"<[^>]+>", "", line).strip()
        if clean and clean not in seen:
            seen.add(clean)
            lines.append(clean)
    return " ".join(lines)


async def _try_transcribe_service(url: str, cache_key: str, deadline: float) -> str | None:
    remaining = max(1.0, deadline - time.monotonic())
    async with httpx.AsyncClient(timeout=min(10.0, remaining)) as client:
        for endpoint in [f"{_TRANSCRIBE_BASE}/transcript", f"{_TRANSCRIBE_BASE}/"]:
            if time.monotonic() >= deadline:
                return None
            try:
                resp = await client.get(endpoint, params={"url": url})
                if resp.status_code == 200 and resp.text.strip():
                    text = resp.text.strip()
                    if text.startswith("<!DOCTYPE html>") or "<html" in text.lower():
                        continue
                    return text
                if resp.status_code in (403, 410):
                    cache_failure(cache_key, resp.status_code)
                    return None
            except Exception:
                continue
    return None
