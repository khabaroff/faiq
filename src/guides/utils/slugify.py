from __future__ import annotations

import re


def slugify(text: str, max_len: int = 80) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[-\s_]+", "-", text).strip("-")
    return text[:max_len]
