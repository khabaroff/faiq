import hashlib

from ..fetch.base import FetchedContent
from ..llm import call_llm, get_smart_client, load_prompt
from ..process.wiki import wrap_with_frontmatter
from ..settings import Settings

CHUNK_SIZE = 25000


def summarize_youtube(content: FetchedContent) -> str:
    prompt_template = load_prompt("youtube_summary.md")
    settings = Settings()
    client = get_smart_client()
    raw = content.raw_text

    if len(raw) <= CHUNK_SIZE:
        body = call_llm(client, settings.azure_deployment_smart, raw, system=prompt_template)
    else:
        chunks = [raw[i : i + CHUNK_SIZE] for i in range(0, len(raw), CHUNK_SIZE)]
        results = []
        for i, chunk in enumerate(chunks):
            header = f"[Part {i + 1}/{len(chunks)}]\n\n"
            summary = call_llm(client, settings.azure_deployment_smart, header + chunk, system=prompt_template)
            results.append(summary)

        body = "\n\n---\n\n".join(results)
        if len(chunks) > 1:
            body = call_llm(client, settings.azure_deployment_smart, body, system="Merge these partial summaries into one coherent document. Remove duplicate information.")

    source_url = content.source_meta.get("url", "")
    hash8 = hashlib.sha256(source_url.encode()).hexdigest()[:8]
    return wrap_with_frontmatter(
        body,
        source_type="youtube",
        source_url=source_url,
        tags=[],
        hash8=hash8,
        prompt_version="youtube_summary@v1",
        source_path=content.source_meta.get("source_path", ""),
    )
