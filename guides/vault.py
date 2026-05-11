import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def hash_source(source: str) -> str:
    return hashlib.sha256(source.encode()).hexdigest()[:8]


def make_source_dir(data_dir: Path, source: str, date: datetime | None = None) -> Path:
    if date is None:
        date = datetime.now()

    date_str = date.strftime("%Y-%m-%d")
    hash8 = hash_source(source)
    base_name = f"{date_str}_{hash8}"
    dir_path = data_dir / "sources" / base_name

    if dir_path.exists():
        counter = 2
        while (data_dir / "sources" / f"{base_name}-{counter}").exists():
            counter += 1
        dir_path = data_dir / "sources" / f"{base_name}-{counter}"

    dir_path.mkdir(parents=True, exist_ok=True)
    (dir_path / "images").mkdir(exist_ok=True)
    return dir_path


def store(
    source: str,
    raw_text: str,
    output_text: str,
    output_filename: str,
    tags: list[str],
    source_type: str,
    status: str,
    data_dir: Path | None = None,
) -> Path:
    from guides.settings import Settings
    if data_dir is None:
        data_dir = Settings().data_dir

    dir_path = make_source_dir(data_dir, source)

    source_path = dir_path / "source.md"
    if not source_path.exists():
        source_path.write_text(raw_text, encoding="utf-8")

    output_path = dir_path / output_filename
    output_path.write_text(output_text, encoding="utf-8")

    meta: dict[str, Any] = {
        "source": source,
        "source_type": source_type,
        "tags": tags,
        "status": status,
        "output_file": output_filename,
        "created_at": datetime.now().isoformat(),
    }
    (dir_path / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    return dir_path
