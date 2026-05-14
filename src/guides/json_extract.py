"""Centralized JSON extraction from LLM responses."""
from __future__ import annotations

import json
from typing import Any


def extract_json(text: str) -> dict[str, Any]:
    r"""Extract first JSON object from text using bracket counting state machine.

    Supports:
    - Multi-JSON response (takes first)
    - Braces inside strings
    - Escaped braces and quotes inside strings
    - Depth counting to find balanced closure

    More reliable than greedy regex which fails on multiple objects.
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
                    res = json.loads(candidate)
                    if not isinstance(res, dict):
                        # If we found something like "{...}" but it's not a dict 
                        # (unlikely with balanced braces unless it's malformed), 
                        # we should probably continue or raise.
                        # json.loads already handles malformed.
                        raise ValueError("First balanced structure is not a JSON object")
                    return res
                except json.JSONDecodeError as err:
                    raise ValueError(f"Malformed JSON at position {start}: {err}") from err

    raise ValueError(f"Unclosed JSON object in response: {text[:200]}")
