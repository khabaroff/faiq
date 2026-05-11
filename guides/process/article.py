from __future__ import annotations

import hashlib
from pathlib import Path

from guides.fetch.base import FetchedContent
from guides.llm import call_llm, get_smart_client, load_prompt
from guides.settings import Settings
from guides.process.wiki import wrap_with_frontmatter


def _chunk_text(text: str, limit: int = 50000) -> list[str]:
    if len(text) <= limit:
        return [text]

    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for block in text.split("\n\n"):
        piece = block if not current else f"\n\n{block}"
        if current and current_len + len(piece) > limit:
            chunks.append("".join(current))
            current = [block]
            current_len = len(block)
            continue

        if not current and len(block) > limit:
            start = 0
            while start < len(block):
                chunks.append(block[start : start + limit])
                start += limit
            current = []
            current_len = 0
            continue

        current.append(piece if current else block)
        current_len += len(piece if current_len else block)

    if current:
        chunks.append("".join(current))

    return chunks


def _local_rewrite(content: FetchedContent) -> str:
    source_url = content.source_meta.get("url", "")
    hash8 = hashlib.sha256(source_url.encode()).hexdigest()[:8]
    return wrap_with_frontmatter(
        content.raw_text.strip(),
        source_type="article",
        source_url=source_url,
        tags=[],
        hash8=hash8,
        prompt_version="article_rewrite@v1",
        source_path=content.source_meta.get("source_path", ""),
    )


def _has_azure_config(settings: Settings) -> bool:
    return bool(
        settings.azure_openai_api_key.strip()
        and settings.azure_openai_endpoint.strip()
        and settings.azure_deployment_smart.strip()
    )


def rewrite_article(content: FetchedContent) -> str:
    settings = Settings()

    if not _has_azure_config(settings):
        return _local_rewrite(content)

    try:
        system_prompt = load_prompt("article_rewrite.md")
    except FileNotFoundError:
        system_prompt = ""

    client = get_smart_client()
    deployment = settings.azure_deployment_smart

    if len(content.raw_text) <= 50000:
        body = call_llm(client, deployment, content.raw_text, system_prompt)
    else:
        rewritten_parts = [call_llm(client, deployment, part, system_prompt) for part in _chunk_text(content.raw_text)]
        body = "\n\n".join(part for part in rewritten_parts if part.strip())

    source_url = content.source_meta.get("url", "")
    hash8 = hashlib.sha256(source_url.encode()).hexdigest()[:8]
    return wrap_with_frontmatter(
        body,
        source_type="article",
        source_url=source_url,
        tags=[],
        hash8=hash8,
        prompt_version="article_rewrite@v1",
        source_path=content.source_meta.get("source_path", ""),
    )
