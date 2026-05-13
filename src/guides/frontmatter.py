from __future__ import annotations
import yaml


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
