"""Filesystem safety utilities to prevent path traversal."""
from __future__ import annotations

import re
from pathlib import Path

SAFE_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,79}$")


def safe_join(base: Path, name: str) -> Path:
    """Join base/name, raising ValueError if result escapes base."""
    candidate = (base / name).resolve()
    try:
        candidate.relative_to(base.resolve())
    except ValueError as err:
        raise ValueError(f"Path traversal detected: {name!r} escapes {base}") from err
    return candidate


def assert_safe_slug(slug: str) -> str:
    """Validate slug contains only safe characters. Returns slug or raises."""
    if not SAFE_SLUG_RE.match(slug):
        raise ValueError(f"Unsafe slug: {slug!r} — must match [a-z0-9][a-z0-9-]{{0,79}}")
    return slug
