from __future__ import annotations

import yaml

from guides.models import ArticleState

VALID_STATE_KEYS: set[str] = set(ArticleState.model_fields)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """YAML-aware parser. Returns ({}, original_text) on any parse failure."""
    if not text.startswith("---\n"):
        return {}, text
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        return {}, text
    try:
        fm = yaml.safe_load(text[4:end]) or {}
        if not isinstance(fm, dict):
            return {}, text
    except yaml.YAMLError:
        return {}, text
    return fm, text[end + 5:]


def filter_state_keys(frontmatter: dict) -> dict:
    """Return only keys that belong to ArticleState (pipeline state fields)."""
    return {k: v for k, v in frontmatter.items() if k in VALID_STATE_KEYS}
