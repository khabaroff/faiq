#!/usr/bin/env python3
"""Scan wiki extracts for placeholder '# Title' headings and queue for reprocessing."""

import hashlib
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WIKI_DIR = ROOT / "wiki" / "extracts"
SOURCES_DIR = ROOT / "data" / "sources"
INBOX_DIR = ROOT / "data" / "inbox"
QUEUE_FILE = ROOT / "data" / "queue" / "urls.txt"

_FM_RE = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
_SOURCE_PATHS_RE = re.compile(r"source_paths:\s*\n((?:\s+-\s+.*\n)*)", re.MULTILINE)
_URL_RE = re.compile(r"url:\s*\"?(https?://\S+?)\"?\s*$", re.MULTILINE)


def _parse_source_paths(fm_text: str) -> list[str]:
    m = _SOURCE_PATHS_RE.search(fm_text)
    if not m:
        return []
    return [line.strip().strip("-").strip().strip('"') for line in m.group(1).splitlines() if line.strip()]


def _parse_url(fm_text: str) -> str:
    m = _URL_RE.search(fm_text)
    return m.group(1) if m else ""


def _find_source_dir(hash8: str) -> Path | None:
    for d in SOURCES_DIR.iterdir():
        if d.is_dir() and hash8 in d.name:
            return d
    return None


def find_stale_pages() -> list[Path]:
    stale = []
    for fpath in sorted(WIKI_DIR.rglob("*.md")):
        if fpath.parent.name == "_indexes":
            continue
        text = fpath.read_text(encoding="utf-8")
        body = _FM_RE.sub("", text, count=1).lstrip()
        if body.startswith("# Title"):
            stale.append(fpath)
    return stale


def requeue(fpath: Path, dry_run: bool = False) -> str:
    text = fpath.read_text(encoding="utf-8")
    fm_match = _FM_RE.match(text)
    fm_text = fm_match.group(0) if fm_match else ""

    source_paths = _parse_source_paths(fm_text)
    url = _parse_url(fm_text)

    action = "?"
    for sp in source_paths:
        sp_path = Path(sp)
        if sp_path.exists() and sp_path.is_file():
            h8 = hashlib.sha256(str(sp_path).encode()).hexdigest()[:8]
            src_dir = _find_source_dir(h8)
            if src_dir and not dry_run:
                shutil.rmtree(src_dir)
                print(f"  deleted source dir: {src_dir.name}")
            dest = INBOX_DIR / sp_path.name
            if not dry_run:
                shutil.copy2(sp_path, dest)
                print(f"  copied to inbox: {dest.name}")
            action = f"file→inbox:{dest.name}"
            break
    else:
        if url:
            h8 = hashlib.sha256(url.encode()).hexdigest()[:8]
            src_dir = _find_source_dir(h8)
            if src_dir and not dry_run:
                shutil.rmtree(src_dir)
                print(f"  deleted source dir: {src_dir.name}")
            if not dry_run:
                with open(QUEUE_FILE, "a", encoding="utf-8") as f:
                    f.write(url + "\n")
                print(f"  queued URL: {url}")
            action = f"url→queue:{url}"

    if not dry_run:
        fpath.unlink()
        print(f"  deleted wiki page: {fpath.name}")

    return action


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    stale = find_stale_pages()
    if not stale:
        print("No stale pages with '# Title' found.")
        return

    print(f"Found {len(stale)} stale page(s){'  [DRY RUN]' if dry_run else ''}:")
    for fpath in stale:
        print(f"\n{fpath.relative_to(ROOT)}")
        action = requeue(fpath, dry_run=dry_run)
        if dry_run:
            print(f"  would: {action}")

    if not dry_run:
        print(f"\nDone. Run: uv run python -m process_stream")


if __name__ == "__main__":
    main()
