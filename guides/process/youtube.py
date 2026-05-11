from ..fetch.base import FetchedContent
from ..llm import call_llm, get_smart_client, load_prompt
from ..settings import Settings

CHUNK_SIZE = 25000


def summarize_youtube(content: FetchedContent) -> str:
    prompt_template = load_prompt("youtube_summary.md")
    settings = Settings()
    client = get_smart_client()
    raw = content.raw_text

    if len(raw) <= CHUNK_SIZE:
        return call_llm(client, settings.azure_deployment_smart, raw, system=prompt_template)

    chunks = [raw[i : i + CHUNK_SIZE] for i in range(0, len(raw), CHUNK_SIZE)]
    results = []
    for i, chunk in enumerate(chunks):
        header = f"[Part {i + 1}/{len(chunks)}]\n\n"
        summary = call_llm(client, settings.azure_deployment_smart, header + chunk, system=prompt_template)
        results.append(summary)

    combined = "\n\n---\n\n".join(results)
    if len(chunks) > 1:
        combined = call_llm(client, settings.azure_deployment_smart, combined, system="Merge these partial summaries into one coherent document. Remove duplicate information.")

    return combined