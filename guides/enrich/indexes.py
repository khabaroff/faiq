import re
from datetime import datetime
from pathlib import Path


def _parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    result: dict[str, object] = {}
    current_key = None
    for line in block.splitlines():
        list_item = re.match(r"^\s+-\s+(.*)", line)
        if list_item and current_key:
            val = list_item.group(1).strip().strip('"').strip("'")
            if isinstance(result.get(current_key), list):
                result[current_key].append(val)
            else:
                result[current_key] = [val]
            continue
        m = re.match(r"^(\w+):\s*(.*)", line)
        if m:
            current_key = m.group(1)
            val = m.group(2).strip().strip('"').strip("'")
            result[current_key] = val if val else None
    return result


def _read_wiki_md_files(wiki_dir: Path) -> list[dict]:
    entries: list[dict] = []
    for fpath in wiki_dir.rglob("*.md"):
        if fpath.parent.name == "_indexes" or fpath.name == "log.md":
            continue
        text = fpath.read_text(encoding="utf-8")
        fm = _parse_frontmatter(text)
        if not fm:
            continue

        slug = fpath.stem
        qs_raw = fm.get("quality_score")
        try:
            quality_score: float | None = float(qs_raw) if qs_raw not in (None, "null", "") else None
        except (ValueError, TypeError):
            quality_score = None
        entry = {
            "slug": slug,
            "title": fm.get("title", slug),
            "source_type": fm.get("source_type", "unknown"),
            "url": fm.get("url", ""),
            "created_at": fm.get("created_at", ""),
            "status": fm.get("status", "active"),
            "review_required": str(fm.get("review_required", "false")).lower() == "true",
            "verified": str(fm.get("verified", "true")).lower() == "true",
            "topics": fm.get("topics", []) if isinstance(fm.get("topics"), list) else [],
            "quality_score": quality_score,
        }
        entries.append(entry)
    return entries


def rebuild_indexes(wiki_dir: Path) -> None:
    indexes_dir = wiki_dir / "_indexes"
    indexes_dir.mkdir(parents=True, exist_ok=True)

    entries = _read_wiki_md_files(wiki_dir)
    if not entries:
        for name in ("recent", "needs-review", "githubs", "by-topic", "by-kind", "prompts"):
            (indexes_dir / f"{name}.md").write_text(f"# {name}\n\n_(no entries yet)_\n", encoding="utf-8")
        return

    # 1) recent.md — last 20 by created_at desc
    sorted_recent = sorted(entries, key=lambda e: e["created_at"], reverse=True)[:20]
    lines = ["# Recent\n"]
    for e in sorted_recent:
        lines.append(f"## {e['created_at']} | [[{e['slug']}]] - {e['title']} ({e['source_type']})\n")
    (indexes_dir / "recent.md").write_text("".join(lines), encoding="utf-8")

    # 2) needs-review.md — low quality_score (<0.7) or explicitly flagged
    def _needs_review(e: dict) -> bool:
        qs = e["quality_score"]
        if qs is not None and qs < 0.7:
            return True
        return e["review_required"] or not e["verified"] or e["status"] == "needs-review"

    flagged = sorted([e for e in entries if _needs_review(e)], key=lambda e: e.get("quality_score") or 1.0)
    lines = ["# Needs Review\n"]
    for e in flagged:
        qs = e["quality_score"]
        qs_str = f" quality_score: {qs:.2f}" if qs is not None else ""
        lines.append(f"## {e['created_at']} | [[{e['slug']}]] - {e['title']} ({e['source_type']}){qs_str}\n")
    (indexes_dir / "needs-review.md").write_text("".join(lines), encoding="utf-8")

    # 3) githubs.md
    githubs = [e for e in entries if e["source_type"] == "github_repo"]
    lines = ["# GitHubs\n"]
    for e in githubs:
        lines.append(f"## [[{e['slug']}]] - {e['title']} | {e['url']}\n")
    (indexes_dir / "githubs.md").write_text("".join(lines), encoding="utf-8")

    # 4) by-topic.md
    topic_map: dict[str, list[dict]] = {}
    for e in entries:
        for topic in e["topics"]:
            topic_map.setdefault(topic, []).append(e)
    lines = ["# By Topic\n"]
    for topic in sorted(topic_map):
        lines.append(f"## {topic}\n")
        for e in topic_map[topic]:
            lines.append(f"- [[{e['slug']}]] - {e['title']}\n")
    (indexes_dir / "by-topic.md").write_text("".join(lines), encoding="utf-8")

    # 5) by-kind.md
    kind_map: dict[str, list[dict]] = {}
    for e in entries:
        kind_map.setdefault(e["source_type"], []).append(e)
    lines = ["# By Kind\n"]
    for kind in sorted(kind_map):
        lines.append(f"## {kind}\n")
        for e in kind_map[kind]:
            lines.append(f"- [[{e['slug']}]] - {e['title']}\n")
    (indexes_dir / "by-kind.md").write_text("".join(lines), encoding="utf-8")

    # 6) prompts.md — entries where source_type=article or youtube, sorted by created_at desc
    prompts = [e for e in entries if e["source_type"] in ("article", "youtube")]
    prompts.sort(key=lambda e: e["created_at"], reverse=True)
    lines = ["# Prompts\n"]
    for e in prompts:
        lines.append(f"## [[{e['slug']}]] - {e['title']} | {e['created_at']}\n")
    (indexes_dir / "prompts.md").write_text("".join(lines), encoding="utf-8")