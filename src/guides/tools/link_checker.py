"""Link checker — scans wikilinks [[Name]] across public summaries/tools/techniques.

Reports broken links:  file:line -> [[target]]
Option --create-stubs  creates empty stub pages for broken links.

Usage:
  python -m guides.tools.link_checker
  python -m guides.tools.link_checker --create-stubs
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent

SOURCES_DIR = ROOT / "public" / "sources"
SUMMARIES_DIR = ROOT / "public" / "summaries"
TOOLS_DIR = ROOT / "public" / "tools"
TECH_DIR = ROOT / "public" / "techniques"

TARGET_DIRS = (SUMMARIES_DIR, TOOLS_DIR, TECH_DIR)

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def slugify(name: str) -> str:
    """Convert a wikilink target to a file slug."""
    s = name.strip().lower()
    s = re.sub(r"[_\s]+", "-", s)
    s = re.sub(r"-{2,}", "-", s)
    return s.strip("-")


def resolve_link(target: str) -> Path | None:
    """Return the first existing file for the wikilink target, or None."""
    slug = slugify(target)
    for d in TARGET_DIRS:
        p = d / f"{slug}.md"
        if p.exists():
            return p
    return None


def scan_file(filepath: Path) -> list[tuple[int, str]]:
    """Return list of (line_number, wikilink_target) for broken links."""
    broken: list[tuple[int, str]] = []
    try:
        lines = filepath.read_text(encoding="utf-8").splitlines()
    except Exception:
        return broken

    for lineno, line in enumerate(lines, start=1):
        for m in WIKILINK_RE.finditer(line):
            target = m.group(1)
            if resolve_link(target) is None:
                broken.append((lineno, target))
    return broken


def create_stub(target: str, dest_dir: Path) -> Path:
    """Create an empty stub page for a broken wikilink target."""
    slug = slugify(target)
    dest = dest_dir / f"{slug}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(f"---\ntitle: {target}\nslug: {slug}\n---\n\n", encoding="utf-8")
    return dest


def main() -> int:
    ap = argparse.ArgumentParser(description="Check wikilinks for broken references")
    ap.add_argument("--create-stubs", action="store_true",
                    help="create empty stub pages for broken links")
    args = ap.parse_args()

    all_broken: list[tuple[Path, int, str]] = []  # (file, line, target)

    for d in TARGET_DIRS:
        if not d.exists():
            continue
        for f in sorted(d.glob("*.md")):
            for lineno, target in scan_file(f):
                all_broken.append((f, lineno, target))

    if not all_broken:
        print("No broken wikilinks found.")
        return 0

    for f, lineno, target in all_broken:
        rel = f.relative_to(ROOT)
        print(f"{rel}:{lineno} -> [[{target}]]")

    if args.create_stubs:
        created = 0
        for _, _, target in all_broken:
            # Place stubs in summaries/ by default
            dest = create_stub(target, SUMMARIES_DIR)
            print(f"  created stub: {dest.relative_to(ROOT)}")
            created += 1
        print(f"\nCreated {created} stub pages.")

    print(f"\nTotal broken links: {len(all_broken)}")
    return 1


if __name__ == "__main__":
    sys.exit(main())