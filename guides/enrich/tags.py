import json

from guides.llm import call_llm, get_fast_client, load_prompt
from guides.settings import Settings


def _normalize_tags(tags: list[object]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()

    for tag in tags:
        if not isinstance(tag, str):
            continue
        value = tag.strip().lower()
        if not value or value in seen:
            continue
        seen.add(value)
        normalized.append(value)

    return normalized


def extract_tags(text: str) -> list[str]:
    try:
        system_prompt = load_prompt("tags_extract.md")
    except FileNotFoundError:
        system_prompt = ""

    settings = Settings()
    deployment = settings.azure_deployment_fast or settings.azure_deployment_smart

    try:
        raw = call_llm(get_fast_client(), deployment, text, system_prompt)
        parsed = json.loads(raw)
    except (json.JSONDecodeError, TypeError, ValueError):
        return []

    if not isinstance(parsed, list):
        return []

    return _normalize_tags(parsed)
