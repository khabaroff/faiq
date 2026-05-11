import hashlib

from ..fetch.base import FetchedContent
from ..llm import call_llm, get_smart_client, load_prompt
from ..process.wiki import wrap_with_frontmatter
from ..settings import Settings


def build_reference(content: FetchedContent) -> str:
    prompt_template = load_prompt("github_reference.md")
    settings = Settings()
    client = get_smart_client()
    body = call_llm(client, settings.azure_deployment_smart, content.raw_text, system=prompt_template)
    source_url = content.source_meta.get("url", "")
    hash8 = hashlib.sha256(source_url.encode()).hexdigest()[:8]
    return wrap_with_frontmatter(
        body,
        source_type="github_repo",
        source_url=source_url,
        tags=[],
        hash8=hash8,
        prompt_version="github_reference@v1",
        source_path=content.source_meta.get("source_path", ""),
    )
