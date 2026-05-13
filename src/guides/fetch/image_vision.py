"""Analyze images (posters, infographics) via LLM vision."""
from __future__ import annotations

import json
import logging
import re
from pathlib import Path

from guides.llm import call_llm_with_images, get_smart_client, load_prompt
from guides.settings import Settings

logger = logging.getLogger(__name__)

_IMAGE_EXTENSIONS = frozenset({".jpg", ".jpeg", ".png", ".gif", ".webp"})


def is_image(path: Path) -> bool:
    return path.suffix.lower() in _IMAGE_EXTENSIONS


def analyze_image(image_path: Path) -> dict:
    """Send image to LLM vision. Returns dict with title, description, extracted_text, concepts."""
    s = Settings()
    prompt = load_prompt("image_analysis.md")
    system = "You are a visual content analyst. Return only valid JSON."

    response, usage = call_llm_with_images(
        get_smart_client(),
        s.azure_deployment_smart,
        prompt,
        [image_path],
        system=system,
    )

    match = re.search(r"\{[\s\S]*\}", response)
    if not match:
        raise ValueError(f"No JSON in vision response: {response[:300]}")

    result = json.loads(match.group())

    logger.info(
        "image_analyzed",
        extra={
            "extra": {
                "path": str(image_path),
                "title": result.get("title", ""),
                "tokens": usage.total_tokens,
                "cost_usd": usage.cost_usd,
            }
        },
    )

    return result
