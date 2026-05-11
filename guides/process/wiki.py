from __future__ import annotations

import hashlib
from datetime import date as Date


def _quote(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _infer_title(body: str, source_url: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    tail = source_url.rstrip("/").rsplit("/", 1)[-1] if source_url else ""
    if tail:
        return tail.replace("-", " ").replace("_", " ").title()
    return "Untitled"


def _compute_hash8(source_url: str) -> str:
    return hashlib.sha256(source_url.encode()).hexdigest()[:8]


def _map_content_format(source_type: str) -> str:
    mapping = {
        "youtube": "transcript",
        "youtube_video": "transcript",
        "github_repo": "reference",
    }
    return mapping.get(source_type, "text")


def _map_origin(source_type: str) -> str:
    mapping = {
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
    date: str | None = None,
    hash8: str | None = None,
    prompt_version: str | None = None,
    source_path: str = "",
) -> str:
    title = _infer_title(body, source_url)
    date_value = date or Date.today().isoformat()
    h8 = hash8 or _compute_hash8(source_url)
    st_lower = source_type.lower()

    if st_lower == "github_repo":
        page_id = f"ref-{date_value}-{h8}"
        page_type = "reference-page"
    else:
        page_id = f"src-{date_value}-{h8}"
        page_type = "source-page"

    needs_review = st_lower in ("telegram", "pdf")
    status = "needs-review" if needs_review else "active"

    content_format = _map_content_format(st_lower)
    origin = _map_origin(st_lower)

    lines: list[str] = [
        "---",
        f'id: "{page_id}"',
        f'title: "{_quote(title)}"',
        f'type: "{page_type}"',
        f"status: \"{status}\"",
        f'source_type: "{st_lower}"',
        f'content_format: "{content_format}"',
        f'origin: "{origin}"',
        f'url: "{_quote(source_url)}"',
        f'created_at: "{date_value}"',
        f'updated_at: "{date_value}"',
        'language: "en"',
    ]

    if tags:
        lines.append("tags:")
        lines.extend(f'  - "{_quote(str(tag))}"' for tag in tags)
    else:
        lines.append("tags: []")

    lines.extend([
        "topics: []",
        "entities: []",
        "concepts: []",
        "related: []",
        f"review_required: {_bool_str(needs_review)}",
        "verified: false",
        "quality_score: null",
        "provenance:",
        "  extracted: 0",
        "  inferred: 0",
        "  ambiguous: 0",
    ])

    if source_path:
        lines.append(f'source_paths:\n  - "{_quote(source_path)}"')
    else:
        lines.append("source_paths: []")

    pv = prompt_version or "article_rewrite@v1"
    lines.append(f'prompt_version: "{pv}"')

    lines.append("---")

    frontmatter = "\n".join(lines)
    return f"{frontmatter}\n\n{body.strip()}"