from ..fetch.base import FetchedContent
from ..llm import call_llm, get_smart_client, load_prompt
from ..settings import Settings


def build_reference(content: FetchedContent) -> str:
    prompt_template = load_prompt("github_reference.md")
    settings = Settings()
    client = get_smart_client()
    return call_llm(client, settings.azure_deployment_smart, content.raw_text, system=prompt_template)