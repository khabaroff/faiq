"""Pipeline A — Ingest+Format.

Input: URL, local file (.md, .pdf), or GitHub repo URL from inbox/.
Output: public/sources/<slug>.md with YAML frontmatter.

Workflow:
  1. Detect source type.
  2. Fetch content (clean MD, metadata).
  3. OCR remote images (if article).
  4. Save as public/sources/<slug>.md.
  5. Move inbox file to inbox/done/.
  6. Update state DB.
"""
from __future__ import annotations

import argparse
import hashlib
import logging
import re
import sys
from datetime import datetime
from pathlib import Path

from guides.atomic_write import atomic_write_text
from guides.fetch.base import QueueItem, SourceKind, SourceType, detect_source_type
from guides.fetch.github import fetch_github_gist, fetch_github_repo
from guides.fetch.image_ocr import process_markdown_file
from guides.fetch.image_vision import analyze_image, is_image
from guides.fetch.pdf import fetch_pdf
from guides.fetch.url import fetch_url
from guides.security.fs_safety import assert_safe_slug, safe_join
from guides.settings import Settings
from guides.state import find_by_content_hash, set_state
from guides.utils.slugify import slugify

logger = logging.getLogger(__name__)


_URL_RE = re.compile(r'^https?://\S+$')


def _expand_file(f: Path) -> list[QueueItem]:
    """Return URL QueueItems if file is URL list, else single FILE item."""
    if f.suffix.lower() == ".pdf":
        return [QueueItem(source=str(f), source_kind=SourceKind.FILE, received_at=datetime.now(), origin="inbox")]

    try:
        text = f.read_text(encoding="utf-8")
    except Exception:
        return [QueueItem(source=str(f), source_kind=SourceKind.FILE, received_at=datetime.now(), origin="inbox")]

    urls = [line.strip() for line in text.splitlines() if _URL_RE.match(line.strip())]
    non_url_lines = [line for line in text.splitlines() if line.strip() and not _URL_RE.match(line.strip())]

    if urls and not non_url_lines:
        # Pure URL list — one item per URL, archive source file after first
        return [QueueItem(source=url, source_kind=SourceKind.URL, received_at=datetime.now(), origin=str(f)) for url in urls]

    # Mixed or pure content — treat as file
    return [QueueItem(source=str(f), source_kind=SourceKind.FILE, received_at=datetime.now(), origin="inbox")]


_IMAGE_EXTENSIONS = frozenset({".jpg", ".jpeg", ".png", ".gif", ".webp"})
_TEXT_EXTENSIONS = frozenset({".md", ".txt", ".pdf"})


def scan_inbox(inbox_dir: Path) -> list[QueueItem]:
    if not inbox_dir.exists():
        return []
    items: list[QueueItem] = []
    for f in sorted(inbox_dir.iterdir()):
        if not f.is_file() or f.name.startswith("."):
            continue
        ext = f.suffix.lower()
        if ext in _IMAGE_EXTENSIONS:
            items.append(QueueItem(source=str(f), source_kind=SourceKind.FILE, received_at=datetime.now(), origin="inbox"))
        elif ext in _TEXT_EXTENSIONS:
            items.extend(_expand_file(f))
    return items


def _archive_file(source_path: Path, done_dir: Path) -> Path:
    done_dir.mkdir(parents=True, exist_ok=True)
    target = done_dir / source_path.name
    counter = 1
    while target.exists():
        target = done_dir / f"{source_path.stem}_{counter}{source_path.suffix}"
        counter += 1
    source_path.rename(target)
    return target


def _process_image(item: QueueItem, settings: Settings) -> dict | None:
    """Process image file through LLM vision → public/images/<slug>.md."""
    image_path = Path(item.source)
    try:
        result = analyze_image(image_path)
    except Exception as e:
        logger.exception("Image analysis failed for %s: %s", item.source, e)
        return None

    title = result.get("title") or image_path.stem
    slug = slugify(title) or hashlib.md5(item.source.encode()).hexdigest()[:8]

    images_dir = settings.inbox_dir.parent / "public" / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    # Copy original image alongside markdown
    dest_image = images_dir / f"{slug}{image_path.suffix.lower()}"
    dest_image.write_bytes(image_path.read_bytes())

    description = result.get("description", "")
    extracted_text = result.get("extracted_text", "")
    concepts = result.get("concepts", [])
    visual_type = result.get("visual_type", "image")

    concepts_yaml = "\n".join(f"  - {c}" for c in concepts)
    frontmatter = (
        "---\n"
        f"title: {title}\n"
        f"slug: {slug}\n"
        f"source_type: image\n"
        f"visual_type: {visual_type}\n"
        f"source_image: {dest_image.name}\n"
        f"fetched_at: {datetime.now().date().isoformat()}\n"
        f"concepts:\n{concepts_yaml}\n"
        "---\n\n"
    )

    body = f"![{title}]({dest_image.name})\n\n# {title}\n\n{description}\n\n"
    if extracted_text:
        body += f"## Extracted Text\n\n{extracted_text}\n"

    out_path = images_dir / f"{slug}.md"
    atomic_write_text(out_path, frontmatter + body)

    _archive_file(image_path, settings.inbox_dir / "done")
    return {"slug": slug, "source_type": "image", "path": out_path, "content_hash": None}


def process_item(item: QueueItem, settings: Settings) -> dict | None:
    try:
        if is_image(Path(item.source)):
            return _process_image(item, settings)

        source_type = detect_source_type(item)
        is_pdf = item.source.lower().endswith(".pdf")

        # 1. Fetch
        if is_pdf:
            fetched = fetch_pdf(item)
            actual_type = "pdf"
        elif source_type == SourceType.GITHUB_REPO:
            fetched = fetch_github_repo(item)
            actual_type = "repo"
        elif source_type == SourceType.GITHUB_GIST:
            fetched = fetch_github_gist(item)
            actual_type = "gist"
        else:
            fetched = fetch_url(item)
            actual_type = "article"

        if not fetched.raw_text.strip():
            logger.warning("Empty content for %s", item.source)
            return None

        # 1a. Content Dedup (SHA256)
        content_hash = hashlib.sha256(fetched.raw_text.encode("utf-8")).hexdigest()
        existing_slug = find_by_content_hash(content_hash)
        if existing_slug:
            print(f"skip (already ingested): {item.source} -> content_hash matches {existing_slug}")
            if item.source_kind == SourceKind.FILE:
                _archive_file(Path(item.source), settings.inbox_dir / "done")
            return None

        # 2. Slug & Title
        title = fetched.source_meta.get("title") or Path(item.source).stem or "untitled"
        slug = slugify(title)
        if not slug:
            slug = hashlib.md5(item.source.encode()).hexdigest()[:8]
        try:
            assert_safe_slug(slug)
        except ValueError:
            slug = hashlib.md5(item.source.encode()).hexdigest()[:16]

        # 3. Save temp for OCR
        content_sources_dir = settings.sources_dir
        content_sources_dir.mkdir(parents=True, exist_ok=True)
        out_path = safe_join(content_sources_dir, f"{slug}.md")

        # Initial write
        atomic_write_text(out_path, fetched.raw_text)

        # 4. OCR images (only for articles/gists, repos usually have internal images)
        if actual_type in ("article", "gist"):
            process_markdown_file(out_path)

        # 5. Add YAML Frontmatter
        raw_content = out_path.read_text(encoding="utf-8")
        # Remove any existing frontmatter if fetcher added it (like defuddle might)
        if raw_content.startswith("---"):
            match = re.match(r"^---.*?---\n", raw_content, re.DOTALL)
            if match:
                raw_content = raw_content[match.end():].lstrip()

        # source_url: prefer fetched meta url, then item URL, then frontmatter of original file
        source_url = fetched.source_meta.get("url", "")
        if not source_url and item.source_kind == SourceKind.URL:
            source_url = item.source
        if not source_url and item.source_kind == SourceKind.FILE:
            # Try reading source_url from frontmatter of the dropped .md
            try:
                _fm_match = re.search(r'^source_url:\s*(\S+)', Path(item.source).read_text(encoding="utf-8"), re.MULTILINE)
                if _fm_match:
                    source_url = _fm_match.group(1)
            except Exception:
                pass

        frontmatter = {
            "title": title,
            "slug": slug,
            "source_url": source_url,
            "source_type": actual_type,
            "fetched_at": datetime.now().date().isoformat(),
            "lang": fetched.source_meta.get("lang", "en"),
            "status": "draft",
        }
        yaml_block = "---\n" + "\n".join(f"{k}: {v}" for k, v in frontmatter.items()) + "\n---\n\n"
        atomic_write_text(out_path, yaml_block + raw_content)

        # 6. Archive
        if item.source_kind == SourceKind.FILE:
            _archive_file(Path(item.source), settings.inbox_dir / "done")

        return {"slug": slug, "source_type": actual_type, "path": out_path, "content_hash": content_hash}

    except Exception as e:
        logger.exception("Failed to ingest %s: %s", item.source, e)
        return None


def main(argv=None) -> int:

    parser = argparse.ArgumentParser(description="Pipeline A: Ingest")
    parser.add_argument("--url", help="URL to ingest")
    parser.add_argument("--file", help="Local file to ingest")
    parser.add_argument("--repo", help="GitHub repo to ingest")
    args = parser.parse_args(argv)

    settings = Settings()

    items = []
    if args.url:
        items.append(QueueItem(source=args.url, source_kind=SourceKind.URL, received_at=datetime.now(), origin="cli"))
    elif args.file:
        items.append(QueueItem(source=args.file, source_kind=SourceKind.FILE, received_at=datetime.now(), origin="cli"))
    elif args.repo:
        items.append(QueueItem(source=args.repo, source_kind=SourceKind.URL, received_at=datetime.now(), origin="cli"))
    else:
        # Batch mode: scan inbox
        inbox_dir = settings.inbox_dir
        items = scan_inbox(inbox_dir)

    # Track which source files (URL-lists) to archive after all their URLs are processed
    url_list_files: set[str] = set()
    for item in items:
        if item.source_kind == SourceKind.URL and item.origin not in ("cli", "inbox"):
            url_list_files.add(item.origin)

    processed_count = 0
    for item in items:
        res = process_item(item, settings)
        if res:
            slug = res["slug"]
            set_state(slug, "raw", True)
            if res.get("content_hash"):
                set_state(slug, "content_hash", res["content_hash"])
            if res.get("source_type") == "image":
                # Images are fully processed in A — skip Pipeline B
                set_state(slug, "summarized_at", datetime.now().date().isoformat())
            processed_count += 1
            print(f"Ingested: {slug} -> {res['path']}")

    # Archive URL-list source files after all items processed
    done_dir = settings.inbox_dir / "done"
    for src_path in url_list_files:
        p = Path(src_path)
        if p.exists():
            _archive_file(p, done_dir)

    print(f"Done. Processed {processed_count} items.")
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    sys.exit(main())
