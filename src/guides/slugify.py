from __future__ import annotations

import hashlib
import re


def slugify(text: str, max_len: int = 80) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[-\s_]+", "-", text).strip("-")
    return text[:max_len]


def short_hash_slug(value: str, length: int = 8) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:length]


def canonicalize_slug(name: str, existing_slugs: list[str], item_type: str = "") -> str:
    """Map a name to existing slug using fuzzy match; LLM fallback only on near-collision."""
    from rapidfuzz import fuzz
    from rapidfuzz import process as fuzz_process

    candidate = slugify(name)
    if not candidate:
        return short_hash_slug(name or item_type or "slug")

    if candidate in existing_slugs:
        return candidate

    if not existing_slugs:
        return candidate

    result = fuzz_process.extractOne(
        candidate,
        existing_slugs,
        scorer=fuzz.token_sort_ratio,
        score_cutoff=85,
    )
    if result is not None:
        matched_slug, _score, _ = result
        return matched_slug

    return candidate
