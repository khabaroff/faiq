import json
import re

from guides.llm import call_llm, get_fast_client, load_prompt
from guides.settings import Settings


def _dedupe(items: list[str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()

    for item in items:
        value = item.strip()
        if not value or value in seen:
            continue
        seen.add(value)
        normalized.append(value)

    return normalized


def _normalize_tags(tags: list[object]) -> list[str]:
    values = []
    for tag in tags:
        if isinstance(tag, str):
            values.append(tag.strip())
    return _dedupe(values)


def _normalize_topics(topics: list[object]) -> list[str]:
    values = []
    for topic in topics:
        if isinstance(topic, str):
            value = re.sub(r"[^a-z0-9]+", "-", topic.strip().lower()).strip("-")
            if value:
                values.append(value)
    return _dedupe(values)


def _normalize_entities(entities: list[object]) -> list[str]:
    values = []
    for entity in entities:
        if isinstance(entity, str):
            values.append(entity.strip())
    return _dedupe(values)


def _normalize_concepts(concepts: list[object]) -> list[str]:
    values = []
    for concept in concepts:
        if isinstance(concept, str):
            value = concept.strip().lower()
            if value:
                values.append(value)
    return _dedupe(values)


def extract_tags(text: str) -> dict[str, list[str]]:
    try:
        system_prompt = load_prompt("tags_extract.md")
    except FileNotFoundError:
        system_prompt = ""

    settings = Settings()
    deployment = settings.azure_deployment_fast or settings.azure_deployment_smart

    empty = {"tags": [], "topics": [], "entities": [], "concepts": []}

    try:
        raw = call_llm(get_fast_client(), deployment, text, system_prompt)
        parsed = json.loads(raw)
    except (json.JSONDecodeError, TypeError, ValueError):
        return empty

    if not isinstance(parsed, dict):
        return empty

    tags = _normalize_tags(parsed.get("tags", []))
    topics = _normalize_topics(parsed.get("topics", []))
    entities = _normalize_entities(parsed.get("entities", []))[:5]
    concepts = _normalize_concepts(parsed.get("concepts", []))[:4]

    return {
        "tags": tags,
        "topics": topics,
        "entities": entities,
        "concepts": concepts,
    }
