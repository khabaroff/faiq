"""Centralized JSON extraction from LLM responses."""
from __future__ import annotations

import json


def extract_first_json(text: str) -> dict:
    r"""Extract first JSON object from text using bracket counting.

    More reliable than greedy r'{[\s\S]*}' which fails on multi-object responses.
    Raises ValueError if no valid JSON object found.
    """
    start = text.find("{")
    if start == -1:
        raise ValueError(f"No JSON object found in response: {text[:200]}")

    depth = 0
    in_string = False
    escape_next = False

    for i, ch in enumerate(text[start:], start):
        if escape_next:
            escape_next = False
            continue
        if ch == "\\" and in_string:
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                candidate = text[start : i + 1]
                try:
                    return json.loads(candidate)
                except json.JSONDecodeError as err:
                    raise ValueError(f"Malformed JSON at position {start}: {err}") from err

    raise ValueError(f"Unclosed JSON object in response: {text[:200]}")
