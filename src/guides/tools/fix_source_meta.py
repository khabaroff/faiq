"""Fix metadata in public/sources/*.md.

Problems to fix:
  1. source_url is empty — URL is in body as plain text line
  2. title = slug — derive from first H1 or slug
  3. Stale timestamp header ## 2026-... at start of body

Usage:
  python -m guides.tools.fix_source_meta [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
SOURCES_DIR = ROOT / "public" / "sources"


_UPPER_WORDS = {"ai", "llm", "api", "ux", "ui", "seo", "vs", "rss", "sdk"}


def slugify_to_title(slug: str) -> str:
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", slug)
    slug = re.sub(r"[_]", " ", slug)
    words = slug.replace("-", " ").strip().split()
    result = []
    for w in words:
        if w.lower() in _UPPER_WORDS:
            result.append(w.upper())
        else:
            result.append(w.capitalize())
    return " ".join(result)


def parse_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        return {}, text
    fm_raw = text[4:end]
    body = text[end + 5:]
    fm: dict[str, str] = {}
    for line in fm_raw.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm, body


def build_front_matter(fm: dict) -> str:
    lines = ["---"]
    for k, v in fm.items():
        lines.append(f"{k}: {v}")
    lines.append("---\n\n")
    return "\n".join(lines)


def fix_source_file(path: Path, dry_run: bool = False) -> bool:
    text = path.read_text()
    fm, body = parse_front_matter(text)

    changed = False
    slug = path.stem

    # Fix title
    if not fm.get("title") or fm.get("title") == slug:
        h1_match = re.search(r"^# (.+)$", body, re.MULTILINE)
        if h1_match:
            fm["title"] = h1_match.group(1).strip()
        else:
            fm["title"] = slugify_to_title(slug)
        changed = True

    # Remove timestamp header + extract URL from body
    lines = body.splitlines()
    new_lines = []
    url_found = ""
    skip_next_blank = False

    for i, line in enumerate(lines):
        # Skip timestamp header (## 2026-...)
        if re.match(r"^## \d{4}-\d{2}-\d{2}T", line):
            skip_next_blank = True
            changed = True
            continue

        # Skip blank line after timestamp
        if skip_next_blank and line.strip() == "":
            skip_next_blank = False
            continue
        skip_next_blank = False

        # Extract URL if source_url empty
        if not fm.get("source_url") and re.match(r"^https?://\S+$", line.strip()):
            url_found = line.strip()
            changed = True
            continue  # remove URL from body

        new_lines.append(line)

    if url_found:
        fm["source_url"] = url_found

    # Fix source_type: "md" → "article" if URL is now known
    if fm.get("source_type") == "md" and fm.get("source_url"):
        url = fm["source_url"]
        if "youtube.com" in url or "youtu.be" in url:
            fm["source_type"] = "youtube"
        elif "github.com" in url:
            fm["source_type"] = "repo"
        else:
            fm["source_type"] = "article"
        changed = True

    if not changed:
        return False

    new_body = "\n".join(new_lines).lstrip("\n")
    new_text = build_front_matter(fm) + new_body

    if dry_run:
        print(f"  [dry-run] {path.name}")
        print(f"    title: {fm.get('title')}")
        print(f"    source_url: {fm.get('source_url')}")
        print(f"    source_type: {fm.get('source_type')}")
    else:
        path.write_text(new_text)
        print(f"  fixed: {path.name}")

    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--file", help="fix single file by name")
    args = ap.parse_args()

    if args.file:
        paths = [SOURCES_DIR / args.file]
    else:
        paths = sorted(SOURCES_DIR.glob("*.md"))

    fixed = 0
    for p in paths:
        if p.name == ".gitkeep":
            continue
        if fix_source_file(p, dry_run=args.dry_run):
            fixed += 1

    print(f"{'Would fix' if args.dry_run else 'Fixed'} {fixed}/{len(paths)-1} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
