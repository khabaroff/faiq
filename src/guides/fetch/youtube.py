import re
import subprocess
import tempfile
from pathlib import Path

import httpx

from guides.fetch.base import FetchedContent, QueueItem, SourceType
from guides.security.url_safety import validate_url


def fetch_youtube(item: QueueItem) -> FetchedContent:
    url = item.source
    transcript = _try_ytdlp(url) or _try_transcribe_service(url)

    meta: dict = {"url": url}
    if not transcript:
        meta["error"] = "no_transcript"
        transcript = ""

    return FetchedContent(raw_text=transcript, source_type=SourceType.YOUTUBE, source_meta=meta)


def _try_ytdlp(url: str) -> str | None:
    for args in [
        ["--write-auto-sub", "--sub-lang", "en"],
        ["--write-auto-sub", "--sub-lang", "ru"],
        ["--write-auto-sub", "--all-subs"],
    ]:
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                subprocess.run(
                    [*["yt-dlp"], *args, "--skip-download", "--output", f"{tmpdir}/yt", "--", url],
                    capture_output=True, text=True, timeout=60,
                )
                vtt_files = list(Path(tmpdir).glob("*.vtt"))
                if vtt_files:
                    raw = vtt_files[0].read_text(encoding="utf-8")
                    return _parse_vtt(raw)
        except Exception:
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
# TODO: verify exact endpoint from /docs — current guess is GET /?url=<url>
# returning plain text transcript

def _try_transcribe_service(url: str) -> str | None:
    try:
        validate_url(url)
    except ValueError:
        return None
    try:
        resp = httpx.get(f"{_TRANSCRIBE_BASE}/transcript", params={"url": url}, timeout=120)
        if resp.status_code == 200 and resp.text.strip():
            return resp.text.strip()
    except Exception:
        pass
    try:
        resp = httpx.get(f"{_TRANSCRIBE_BASE}/", params={"url": url}, timeout=120)
        if resp.status_code == 200 and resp.text.strip():
            return resp.text.strip()
    except Exception:
        pass
    return None
