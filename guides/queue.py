import hashlib
import logging
from datetime import datetime
from pathlib import Path

from guides.fetch.base import QueueItem, SourceKind
from guides.settings import Settings

logger = logging.getLogger(__name__)


def _is_valid_line(stripped: str) -> bool:
    if stripped.startswith(("http://", "https://")):
        return True
    path = Path(stripped)
    if path.exists():
        return True
    inbox_prefix = Path("data/inbox/")
    full = inbox_prefix / stripped if not stripped.startswith("data/inbox") else Path(stripped)
    return full.exists()


def _already_processed(source: str, sources_dir: Path) -> bool:
    hash8 = hashlib.sha256(source.encode()).hexdigest()[:8]
    for entry in sources_dir.iterdir():
        if entry.is_dir() and hash8 in entry.name:
            return True
    return False


def pop_pending(queue_file: Path) -> list[QueueItem]:
    if not queue_file.exists():
        return []
    seen: set[str] = set()
    items: list[QueueItem] = []
    for line in queue_file.read_text(encoding="utf-8").splitlines():
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
    return items


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
        if not f.is_file() or f.name.startswith("."):
            continue
        if f.name.startswith("#done#"):
            continue
        source = str(f)
        if _already_processed(source, settings.data_dir / "sources"):
            continue
        items.append(QueueItem(source=source, source_kind=SourceKind.FILE, received_at=datetime.now(), origin="inbox"))
    return items