"""Smoke test: runs fixture files through queue classification + one real pipeline call.

Expected outcomes:
  single_url.txt     -> classification: single_url (one URL, nothing else)
  multi_url.txt      -> classification: url_list    (3+ URLs, no extra prose)
  link_list.md       -> classification: url_list    (5 links, minimal prose)
  mixed_note.md      -> classification: mixed       (paragraph + 2 embedded links)
  plain_article.md   -> classification: article     (markdown with no external links)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from guides.queue import _classify_text_file, _extract_urls, pop_pending, scan_inbox
from guides.fetch.base import QueueItem, SourceKind, detect_source_type
from guides.fetch.github import fetch_github_repo
from datetime import datetime


def run() -> None:
    fixtures_dir = Path(__file__).resolve().parent / "tests" / "fixtures"
    print("=" * 60)
    print("FIXTURE CLASSIFICATION TESTS")
    print("=" * 60)

    for fpath in sorted(fixtures_dir.iterdir()):
        if not fpath.is_file() or fpath.name.startswith("."):
            continue
        text = fpath.read_text(encoding="utf-8")
        classification = _classify_text_file(text)
        urls = _extract_urls(text)
        print(f"\n{fpath.name} ({len(text)} chars, {len(urls)} URLs)")
        print(f"  classification -> {classification}")
        print(f"  extracted URLs  -> {urls}")

    print("\n" + "=" * 60)
    print("SCAN_INBOX TEST (no real files -> should be empty)")
    print("=" * 60)
    inbox_items = scan_inbox(fixtures_dir.parent / "fixtures")
    for item in inbox_items:
        src = item.source
        kind = item.source_kind.value
        stype = detect_source_type(item).value
        print(f"  {kind:5} | {stype:12} | {src}")

    print("\n" + "=" * 60)
    print("REAL PIPELINE TEST: fetch_github_repo(simonw/llm)")
    print("=" * 60)
    item = QueueItem(source="https://github.com/simonw/llm", source_kind=SourceKind.URL, received_at=datetime.now())
    fetched = fetch_github_repo(item)
    status = "ok" if len(fetched.raw_text) > 100 else "short"
    stype = detect_source_type(item).value
    print(f"  source_type  -> {stype}")
    print(f"  raw_text len -> {len(fetched.raw_text)}")
    print(f"  meta         -> {fetched.source_meta}")
    print(f"  status       -> {status}")
    print(f"\n  raw_text[:200]:\n  {fetched.raw_text[:200]}")

    print("\n" + "=" * 60)
    print("POP_PENDING from empty inbox.txt -> should be []")
    print("=" * 60)
    pending = pop_pending(fixtures_dir.parent.parent / "data" / "queue" / "inbox.txt")
    print(f"  items -> {pending}")
    print("\nDone.")


if __name__ == "__main__":
    run()