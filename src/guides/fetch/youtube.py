import asyncio
import logging
import re
import tempfile
from pathlib import Path

import httpx

from guides.fetch.base import FetchedContent, QueueItem, SourceType
from guides.security.url_safety import validate_url
from guides.utils.fetch_cache import cache_failure, get_cached_failure

logger = logging.getLogger(__name__)

async def fetch_youtube(item: QueueItem) -> FetchedContent:
    url = item.source
    validate_url(url)
    
    # Check cache
    cached_code = get_cached_failure(url)
    if cached_code:
        logger.info("YouTube cache hit for %s (code %s)", url, cached_code)
        return FetchedContent(raw_text="", source_type=SourceType.YOUTUBE, source_meta={"url": url, "error": f"cached_{cached_code}"})

    transcript = await _try_ytdlp(url)
    
    # If identified as 403/410 during ytdlp, it's now in cache
    cached_code = get_cached_failure(url)
    if not transcript and cached_code:
        return FetchedContent(raw_text="", source_type=SourceType.YOUTUBE, source_meta={"url": url, "error": f"fail_fast_{cached_code}"})

    if not transcript:
        transcript = await _try_transcribe_service(url)

    meta: dict = {"url": url}
    if not transcript:
        meta["error"] = "no_transcript"
        transcript = ""

    return FetchedContent(raw_text=transcript, source_type=SourceType.YOUTUBE, source_meta=meta)


async def _try_ytdlp(url: str) -> str | None:
    for args in [
        ["--write-auto-sub", "--sub-lang", "en"],
        ["--write-auto-sub", "--sub-lang", "ru"],
        ["--write-auto-sub", "--all-subs"],
    ]:
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                # --socket-timeout 10 for fail-fast on network issues
                cmd = ["yt-dlp", *args, "--skip-download", "--socket-timeout", "10", "--no-warnings", "--output", f"{tmpdir}/yt", "--", url]
                
                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                try:
                    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=15)
                except asyncio.TimeoutError:
                    if proc.returncode is None:
                        try:
                            # Use kill() directly, don't await (it's not a coroutine in Process)
                            # Actually, it's a method on Process.
                            proc.kill()
                        except Exception:
                            pass
                    logger.warning("yt-dlp timeout for %s", url)
                    continue

                stderr_text = stderr.decode()
                if "403" in stderr_text or "Forbidden" in stderr_text:
                    logger.warning("YouTube 403 for %s, fail-fast", url)
                    cache_failure(url, 403)
                    return None
                if "410" in stderr_text or "Gone" in stderr_text:
                    logger.warning("YouTube 410 for %s, fail-fast", url)
                    cache_failure(url, 410)
                    return None

                vtt_files = list(Path(tmpdir).glob("*.vtt"))
                if vtt_files:
                    raw = vtt_files[0].read_text(encoding="utf-8")
                    return _parse_vtt(raw)
        except Exception as e:
            logger.debug("yt-dlp attempt failed: %s", e)
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


_TRANSCRIBE_BASE = "https://youtubetranscribe.khabaroff.studio"

async def _try_transcribe_service(url: str) -> str | None:
    async with httpx.AsyncClient(timeout=30) as client:
        for endpoint in [f"{_TRANSCRIBE_BASE}/transcript", f"{_TRANSCRIBE_BASE}/"]:
            try:
                resp = await client.get(endpoint, params={"url": url})
                if resp.status_code == 200 and resp.text.strip():
                    text = resp.text.strip()
                    # Ignore HTML responses (landing pages/error pages)
                    if text.startswith("<!DOCTYPE html>") or "<html" in text.lower():
                        continue
                    return text
                if resp.status_code in (403, 410):
                    cache_failure(url, resp.status_code)
                    return None
            except Exception:
                continue
    return None
