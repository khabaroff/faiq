import hashlib
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Literal

from guides.fetch.base import QueueItem, SourceKind
from guides.settings import Settings

logger = logging.getLogger(__name__)

_TEXT_EXTENSIONS = {".md", ".txt", ".pdf", ".rst", ".markdown", ".org", ""}
_URL_RE = re.compile(r"https?://\S+")


def _is_valid_line(stripped: str) -> bool:
    if stripped.startswith(("http://", "https://")):
        return True
    path = Path(stripped)
    if path.exists():
        return True
    inbox_prefix = Path("data/inbox/")
    full = inbox_prefix / stripped if not stripped.startswith("data/inbox") else Path(stripped)
    return full.exists()


def already_processed(source: str, sources_dir: Path) -> bool:
    hash8 = hashlib.sha256(source.encode()).hexdigest()[:8]
    for entry in sources_dir.iterdir():
        if entry.is_dir() and hash8 in entry.name:
            return True
    return False


def _extract_urls(text: str) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    for match in _URL_RE.findall(text):
        url = match.rstrip(")].,;:!?'\"")
        if url in seen:
            continue
        seen.add(url)
        urls.append(url)
    return urls


def _classify_text_file(text: str) -> Literal["single_url", "url_list", "mixed", "article"]:
    stripped = text.strip()
    if not stripped:
        return "article"

    urls = _extract_urls(text)
    non_empty_lines = [line.strip() for line in text.splitlines() if line.strip()]

    if len(urls) == 1 and _URL_RE.sub("", text).strip() == "":
        return "single_url"

    if len(urls) >= 3 and non_empty_lines:
        url_lines = sum(1 for line in non_empty_lines if _URL_RE.search(line))
        if url_lines / len(non_empty_lines) > 0.5:
            return "url_list"

    text_without_urls = _URL_RE.sub("", text)
    text_chars = sum(1 for ch in text_without_urls if not ch.isspace())
    url_chars = sum(len(url) for url in urls)

    if urls and (len(non_empty_lines) >= 3 or text_chars >= 20):
        return "mixed"

    return "article"


def pop_pending(queue_file: Path) -> list[QueueItem]:
    if not queue_file.exists():
        return []
    seen: set[str] = set()
    items: list[QueueItem] = []
    for line in queue_file.read_text(encoding="utf-8").splitlines():
        try:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped in seen:
                continue
            if not _is_valid_line(stripped):
                logger.warning("Skipping malformed line: %s", stripped)
                continue
            seen.add(stripped)
            kind = SourceKind.URL if stripped.startswith("http") else SourceKind.FILE
            items.append(QueueItem(source=stripped, source_kind=kind, received_at=datetime.now(), origin="queue"))
        except Exception as e:
            logger.warning("Error processing queue line '%s': %s", line, e)
            continue
    return items


def quarantine(item: QueueItem, reason: str, quarantine_file: Path) -> None:
    line = f"#failed# {datetime.now().isoformat()} {reason} | {item.source}\n"
    with open(quarantine_file, "a", encoding="utf-8") as f:
        f.write(line)


def mark_done(queue_file: Path, item: QueueItem) -> None:
    if not queue_file.exists():
        return
    lines = queue_file.read_text(encoding="utf-8").splitlines(keepends=True)
    result = []
    for line in lines:
        if line.strip() == item.source:
            result.append(f"#done# {line}" if not line.startswith("#done#") else line)
        else:
            result.append(line)
    queue_file.write_text("".join(result), encoding="utf-8")


def scan_inbox(inbox_dir: Path) -> list[QueueItem]:
    if not inbox_dir.exists():
        return []
    settings = Settings()
    items: list[QueueItem] = []
    for f in sorted(inbox_dir.iterdir()):
        try:
            if not f.is_file() or f.name.startswith("."):
                continue
            if f.name.startswith("#done#"):
                continue

            if f.stat().st_size == 0:
                logger.warning("Skipping empty file: %s", f.name)
                continue

            ext = f.suffix.lower()
            if ext not in _TEXT_EXTENSIONS:
                logger.warning("Unsupported file type '%s': %s", ext, f.name)
                continue

            source = str(f)
            if already_processed(source, settings.data_dir / "sources"):
                continue

            if ext in {".txt", ".md", ""}:
                content = f.read_text(encoding="utf-8")
                classification = _classify_text_file(content)
                urls = _extract_urls(content)

                if classification == "single_url" and urls:
                    url = urls[0]
                    if already_processed(url, settings.data_dir / "sources"):
                        continue
                    items.append(
                        QueueItem(source=url, source_kind=SourceKind.URL, received_at=datetime.now(), origin="inbox")
                    )
                    continue

                if classification == "url_list" and urls:
                    for url in urls:
                        if already_processed(url, settings.data_dir / "sources"):
                            continue
                        items.append(
                            QueueItem(source=url, source_kind=SourceKind.URL, received_at=datetime.now(), origin="inbox")
                        )
                    continue

                if classification == "mixed" and urls:
                    for url in urls:
                        if already_processed(url, settings.data_dir / "sources"):
                            continue
                        items.append(
                            QueueItem(source=url, source_kind=SourceKind.URL, received_at=datetime.now(), origin="inbox")
                        )
                    # For 'mixed', we don't 'continue' - we also fall through to add the file itself

            items.append(QueueItem(source=source, source_kind=SourceKind.FILE, received_at=datetime.now(), origin="inbox"))
        except Exception as e:
            logger.warning("Error processing inbox file %s: %s", f.name, e)
            continue
    return items
