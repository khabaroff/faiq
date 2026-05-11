import glob
import re
import subprocess
import tempfile

import httpx

from .base import FetchedContent, QueueItem, SourceType


def fetch_youtube(item: QueueItem) -> FetchedContent:
    url = item.source
    source_meta: dict[str, object] = {}
    text = ""

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [
                    "yt-dlp",
                    "--write-auto-sub",
                    "--sub-lang", "ru,en",
                    "--skip-download",
                    "--output", f"{tmpdir}/%(id)s",
                    url,
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )
            if result.returncode != 0:
                source_meta["error"] = f"yt-dlp failed: {result.stderr.strip()}"
                return FetchedContent(raw_text="", source_type=SourceType.YOUTUBE, source_meta=source_meta)

            vtt_files = glob.glob(f"{tmpdir}/*.vtt")
            if vtt_files:
                vtt = vtt_files[0]
                raw = vtt.read_text(encoding="utf-8")
                text = _parse_vtt(raw)

    except Exception as e:
        source_meta["fallback_attempted"] = True

    if not text.strip():
        try:
            resp = httpx.get(f"https://youtubetranscribe.khabaroff.studio/transcript?url={url}", timeout=60)
            if resp.status_code == 200:
                text = resp.text
        except Exception:
            source_meta["error"] = "no_transcript"
            return FetchedContent(raw_text="", source_type=SourceType.YOUTUBE, source_meta=source_meta)

    if not text.strip():
        source_meta["error"] = "no_transcript"
        return FetchedContent(raw_text="", source_type=SourceType.YOUTUBE, source_meta=source_meta)

    return FetchedContent(raw_text=text, source_type=SourceType.YOUTUBE, source_meta=source_meta)


def _parse_vtt(vtt: str) -> str:
    lines = vtt.splitlines()
    cleaned: list[str] = []
    for line in lines:
        if re.match(r"\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}", line):
            continue
        if line.strip() in ("", "WEBVTT", "Kind: captions", "Language: en", "Language: ru"):
            continue
        line = re.sub(r"<[^>]+>", "", line)
        cleaned.append(line)
    return "\n".join(cleaned).strip()