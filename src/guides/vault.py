import hashlib
import json
import logging
import re
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


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


def _wiki_subfolder(source_type: str, source: str) -> str:
    normalized = source_type.upper()
    lower_source = source.lower()

    if lower_source.endswith(".pdf") or normalized == "PDF":
        return "pdfs"
    if not lower_source.startswith(("http://", "https://")) and Path(source).suffix.lower() in {".md", ".txt"}:
        return "notes"
    if normalized in {"ARTICLE", "TELEGRAM"}:
        return "articles"
    if normalized == "YOUTUBE":
        return "youtubes"
    if normalized == "PDF":
        return "pdfs"
    if normalized == "GITHUB_REPO":
        return "githubs"
    if normalized == "FILE":
        return "notes"
    return "articles"


_PLACEHOLDER_TITLES = {"title", "заголовок", "untitled", "название"}


def _extract_title(output_text: str, source: str) -> str:
    for line in output_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            candidate = stripped[2:].strip()
            if candidate.lower() not in _PLACEHOLDER_TITLES:
                return candidate

    source_path = Path(source)
    if source_path.suffix:
        return source_path.stem

    tail = source.rstrip("/").rsplit("/", 1)[-1]
    return tail or "untitled"


def _slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-") or "untitled"


def _wiki_slug(output_text: str, source: str, wiki_sub: Path) -> tuple[str, str]:
    title = _extract_title(output_text, source)
    slug = _slugify(title)
    slug = f"{slug}-{hash_source(source)[:4]}"
    return title, slug


def _ensure_wiki_layout(wiki_dir: Path) -> None:
    indexes = wiki_dir / "_indexes"
    extracts = wiki_dir / "extracts"
    indexes.mkdir(parents=True, exist_ok=True)
    extracts.mkdir(parents=True, exist_ok=True)

    for sub in ["articles", "youtubes", "pdfs", "githubs", "notes"]:
        (extracts / sub).mkdir(parents=True, exist_ok=True)

    placeholders = {
        indexes / "recent.md": "# Recent",
        indexes / "by-topic.md": "# By Topic",
        indexes / "by-kind.md": "# By Kind",
        indexes / "needs-review.md": "# Needs Review",
        indexes / "githubs.md": "# GitHubs",
        indexes / "entities.md": "# Entities",
        indexes / "concepts.md": "# Concepts",
    }

    for path, content in placeholders.items():
        if not path.exists():
            path.write_text(content + "\n", encoding="utf-8")

    log_path = wiki_dir / "log.md"
    if not log_path.exists():
        log_path.write_text("# Log\n", encoding="utf-8")


def _append_wiki_log(wiki_dir: Path, title: str, source_subfolder: str, slug: str) -> None:
    log_path = wiki_dir / "log.md"
    data_dir = wiki_dir.parent / "data"
    date_str = datetime.utcnow().date().isoformat()
    entry = f"- ingest | {title} -> wiki/extracts/{source_subfolder}/{slug}.md"

    sections = _read_daily_log_sections(log_path)
    day_entries = sections.setdefault(date_str, [])
    if entry not in day_entries:
        day_entries.append(entry)

    daily_spend_by_day = {day: _daily_spend_usd(data_dir, day) for day in sections.keys()}
    _write_daily_log_sections(log_path, sections, daily_spend_by_day=daily_spend_by_day)


def _daily_spend_usd(data_dir: Path, date_str: str) -> float:
    pipeline_log = data_dir / "logs" / "pipeline.log"
    if not pipeline_log.exists():
        return 0.0

    total = 0.0
    prefix = f'"ts": "{date_str}'
    for line in pipeline_log.read_text(encoding="utf-8").splitlines():
        if prefix not in line or '"logger": "guides.llm"' not in line or '"msg": "llm_call"' not in line:
            continue
        try:
            payload = json.loads(line)
        except Exception:
            continue
        if str(payload.get("ts", "")).startswith(date_str):
            try:
                total += float(payload.get("cost_usd") or 0)
            except (TypeError, ValueError):
                continue
    return total


def _read_daily_log_sections(log_path: Path) -> "OrderedDict[str, list[str]]":
    sections: "OrderedDict[str, list[str]]" = OrderedDict()
    if not log_path.exists():
        return sections

    current_day = None
    for raw_line in log_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.startswith("## "):
            current_day = line[3:].split(" | ", 1)[0].strip()
            sections.setdefault(current_day, [])
            continue
        if line.startswith("- ") and current_day:
            sections.setdefault(current_day, []).append(line)
    return sections


def _write_daily_log_sections(log_path: Path, sections: "OrderedDict[str, list[str]]", *, daily_spend_by_day: dict[str, float]) -> None:
    lines = ["# Log", ""]
    for day, entries in sections.items():
        spend = daily_spend_by_day.get(day, 0.0)
        lines.append(f"## {day} | spent: ${spend:.6f}")
        for entry in entries:
            lines.append(entry)
        lines.append("")
    log_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


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
    wiki_dir = data_dir.parent / "wiki"
    _ensure_wiki_layout(wiki_dir)

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

    source_subfolder = _wiki_subfolder(source_type, source)
    wiki_sub = wiki_dir / "extracts" / source_subfolder
    wiki_sub.mkdir(parents=True, exist_ok=True)

    title, slug = _wiki_slug(output_text, source, wiki_sub)
    wiki_path = wiki_sub / f"{slug}.md"

    if wiki_path.exists():
        logger.warning("Wiki page already exists at %s, skipping duplicate", wiki_path)
        return wiki_path

    if status == "failed":
        logger.info("Skipping wiki write for %s — status=%s", source, status)
    else:
        wiki_path.write_text(output_text, encoding="utf-8")
        _append_wiki_log(wiki_dir, title, source_subfolder, slug)

    from guides.enrich.indexes import rebuild_indexes
    rebuild_indexes(wiki_dir)

    return wiki_path
