from datetime import datetime
from pathlib import Path

from guides.fetch.base import QueueItem, SourceKind


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
    return [
        QueueItem(source=str(f), source_kind=SourceKind.FILE, received_at=datetime.now(), origin="inbox")
        for f in inbox_dir.iterdir()
        if f.is_file() and not f.name.startswith(".")
    ]
