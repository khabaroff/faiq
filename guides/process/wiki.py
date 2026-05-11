from __future__ import annotations

import hashlib
from datetime import date as Date


def _quote(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def strip_frontmatter(text: str) -> str:
    stripped = text.lstrip()
    if not stripped.startswith("---\n"):
        return text.strip()

    lines = stripped.splitlines()
    end = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end = idx
            break
    if end is None:
        return text.strip()
    return "\n".join(lines[end + 1 :]).strip()


def _infer_title(body: str, source_url: str) -> str:
    placeholder_seen = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            candidate = stripped[2:].strip()
            if candidate.lower() == "title":
                placeholder_seen = True
                continue
            return candidate
        if placeholder_seen and stripped and not stripped.startswith(("#", "-", "*", "`")):
            return stripped
    tail = source_url.rstrip("/").rsplit("/", 1)[-1] if source_url else ""
    if tail:
        return tail.replace("-", " ").replace("_", " ").title()
    return "Untitled"


def _compute_hash8(source_url: str) -> str:
    return hashlib.sha256(source_url.encode()).hexdigest()[:8]


def _map_content_format(source_type: str) -> str:
    mapping = {
        "reference": "reference",
        "youtube": "transcript",
        "youtube_video": "transcript",
        "github_repo": "reference",
    }
    return mapping.get(source_type, "text")


def _map_origin(source_type: str) -> str:
    mapping = {
        "reference": "github",
        "youtube": "youtube",
        "youtube_video": "youtube",
        "github_repo": "github",
        "telegram": "telegram",
        "pdf": "file",
        "file": "file",
        "note": "file",
    }
    return mapping.get(source_type, "url")


def _bool_str(val: bool) -> str:
    return "true" if val else "false"


def wrap_with_frontmatter(
    body: str,
    source_type: str,
    source_url: str,
    tags: list,
    topics: list | None = None,
    entities: list | None = None,
    concepts: list | None = None,
    date: str | None = None,
    hash8: str | None = None,
    prompt_version: str | None = None,
    source_path: str = "",
    status: str | None = None,
) -> str:
    # Use source_path for title if source_url is empty (common for local files)
    title = _infer_title(body, source_url or source_path)
    date_value = date or Date.today().isoformat()
    # If source_url is empty, use source_path for hash calculation
    h8 = hash8 or _compute_hash8(source_url or source_path)
    st_lower = source_type.lower()

    if st_lower in {"reference", "github_repo"}:
        page_id = f"ref-{date_value}-{h8}"
        page_type = "reference-page"
    else:
        page_id = f"src-{date_value}-{h8}"
        page_type = "source-page"

    if status == "verified":
        fm_status = "active"
        review_required = False
        verified = True
    elif status in {"needs-review", "needs_review"}:
        fm_status = "needs-review"
        review_required = True
        verified = False
    elif status == "active":
        fm_status = "active"
        review_required = False
        verified = False
    else:
        review_required = st_lower in ("telegram", "pdf", "file", "article")
        fm_status = "needs-review" if review_required else "active"
        verified = False

    content_format = _map_content_format(st_lower)
    origin = _map_origin(st_lower)
    
    # Ensure origin is "file" for FILE sources if not already caught by _map_origin
    if not source_url and source_path:
        origin = "file"

    lines: list[str] = [
        "---",
        f'id: "{page_id}"',
        f'title: "{_quote(title)}"',
        f'type: "{page_type}"',
        f'status: "{fm_status}"',
        f'source_type: "{st_lower}"',
        f'content_format: "{content_format}"',
        f'origin: "{origin}"',
        f'url: "{_quote(source_url)}"',
        f'created_at: "{date_value}"',
        f'updated_at: "{date_value}"',
        'language: "ru"', # Default to Russian as per current extracting prompts
    ]

    if tags:
        lines.append("tags:")
        lines.extend(f'  - "{_quote(str(tag))}"' for tag in tags)
    else:
        lines.append("tags: []")

    for key, values in (("topics", topics), ("entities", entities), ("concepts", concepts)):
        if values:
            lines.append(f"{key}:")
            lines.extend(f'  - "{_quote(str(value))}"' for value in values)
        else:
            lines.append(f"{key}: []")

    lines.extend(["related: []", f"review_required: {_bool_str(review_required)}", f"verified: {_bool_str(verified)}", "quality_score: null", "provenance:", "  extracted: 0", "  inferred: 0", "  ambiguous: 0"])

    if source_path:
        lines.append(f'source_paths:\n  - "{_quote(source_path)}"')
    else:
        lines.append("source_paths: []")

    pv = prompt_version or "article_rewrite@v1"
    lines.append(f'prompt_version: "{pv}"')

    lines.append("---")

    frontmatter = "\n".join(lines)
    return f"{frontmatter}\n\n{body.strip()}"
