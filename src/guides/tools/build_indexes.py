"""Tool to build semantic indexes for tools and patterns.

Reads public/summaries/*.md, extracts 'tools' and 'patterns' from frontmatter,
and generates public/index/tools.md and public/index/patterns.md.
"""
from __future__ import annotations

import argparse
import logging
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

from guides.atomic_write import atomic_write_text

logger = logging.getLogger(__name__)

from guides.settings import get_settings


def slugify(name: str) -> str:
    s = re.sub(r"[^\w\s-]", "", name.lower())
    return re.sub(r"[-\s]+", "-", s).strip("-")[:80]


def parse_front_matter_yaml(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        return {}
    fm_raw = text[4:end]
    try:
        return yaml.safe_load(fm_raw) or {}
    except yaml.YAMLError:
        return {}


def main(argv: list[str] | None = None) -> int:
    settings = get_settings()
    parser = argparse.ArgumentParser(description="Build semantic indexes")
    parser.add_argument("--summaries", help="Path to summaries directory")
    parser.add_argument("--index-dir", help="Path to index output directory")
    parser.add_argument("--tools-dir", help="Path to tools directory")
    parser.add_argument("--tech-dir", help="Path to techniques directory")
    args = parser.parse_args(argv)

    summaries_dir = Path(args.summaries) if args.summaries else settings.summaries_dir
    index_dir = Path(args.index_dir) if args.index_dir else settings.public_dir / "index"
    tools_dir = Path(args.tools_dir) if args.tools_dir else settings.tools_dir
    tech_dir = Path(args.tech_dir) if args.tech_dir else settings.techniques_dir

    if not summaries_dir.exists():
        logger.error(f"Summaries directory not found: {summaries_dir}")
        return 1

    data_maps = {
        "tools": defaultdict(list),
        "patterns": defaultdict(list),
        "concepts": defaultdict(list),
        "entities": defaultdict(list),
        "topics": defaultdict(list),
    }

    summary_files = sorted(summaries_dir.glob("*.md"))
    for f in summary_files:
        if f.name.startswith("."):
            continue
        try:
            text = f.read_text(encoding="utf-8")
            fm = parse_front_matter_yaml(text)

            title = fm.get("title") or fm.get("slug") or f.stem
            rel_link = f"../summaries/{f.name}"

            for key in data_maps.keys():
                items = fm.get(key) or []
                if isinstance(items, str):
                    items = [items]
                for item in items:
                    name = item if isinstance(item, str) else item.get("name")
                    if name:
                        data_maps[key][name].append((title, rel_link))
        except Exception as e:
            logger.error(f"Failed to process {f}: {e}")

    index_dir.mkdir(parents=True, exist_ok=True)

    def write_index(data_map, filename, title_text, wiki_dir=None, wiki_rel_path=None):
        lines = [f"# {title_text}\n"]
        if not data_map:
            lines.append("_No entries found._")
        for name in sorted(data_map.keys(), key=lambda s: s.lower()):
            mentions = data_map[name]
            count = len(mentions)

            # Link to tool/technique page if it exists
            if wiki_dir and wiki_rel_path:
                slug = slugify(name)
                wiki_file = wiki_dir / f"{slug}.md"
                if wiki_file.exists():
                    lines.append(f"- **[{name}](../{wiki_rel_path}/{slug}.md)** ({count} mentions)")
                else:
                    lines.append(f"- **{name}** ({count} mentions)")
            else:
                lines.append(f"- **{name}** ({count} mentions)")

            # List summaries where mentioned
            for m_title, m_link in sorted(mentions):
                lines.append(f"  - [{m_title}]({m_link})")

            lines.append("")

        out_path = index_dir / filename
        atomic_write_text(out_path, "\n".join(lines))
        logger.info(f"Generated {out_path} with {len(data_map)} entries")

    write_index(data_maps["tools"], "tools.md", "Tools Index", tools_dir, "tools")
    write_index(data_maps["patterns"], "patterns.md", "Patterns Index", tech_dir, "techniques")
    write_index(data_maps["concepts"], "concepts.md", "Concepts Index")
    write_index(data_maps["entities"], "entities.md", "Entities Index")
    write_index(data_maps["topics"], "topics.md", "Topics Index")

    return 0


if __name__ == "__main__":
    sys.exit(main())
