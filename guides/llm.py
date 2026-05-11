from functools import lru_cache
from openai import AzureOpenAI

from guides.settings import Settings


@lru_cache(maxsize=1)
def get_smart_client() -> AzureOpenAI:
    settings = Settings()
    return AzureOpenAI(
        api_key=settings.azure_openai_api_key,
        azure_endpoint=settings.azure_openai_endpoint,
        api_version=settings.azure_openai_api_version,
        azure_deployment=settings.azure_deployment_smart,
    )


@lru_cache(maxsize=1)
def get_fast_client() -> AzureOpenAI:
    settings = Settings()
    deployment = settings.azure_deployment_fast or settings.azure_deployment_smart
    return AzureOpenAI(
        api_key=settings.azure_openai_api_key,
        azure_endpoint=settings.azure_openai_endpoint,
        api_version=settings.azure_openai_api_version,
        azure_deployment=deployment,
    )


def load_prompt(filename: str) -> str:
    settings = Settings()
    prompt_path = settings.prompts_dir / filename
    return prompt_path.read_text(encoding="utf-8")
