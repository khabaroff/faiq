from functools import lru_cache

from openai import AzureOpenAI

from guides.settings import Settings


@lru_cache(maxsize=1)
def get_smart_client() -> AzureOpenAI:
    s = Settings()
    return AzureOpenAI(
        api_key=s.azure_openai_api_key,
        azure_endpoint=s.azure_openai_endpoint,
        api_version=s.azure_openai_api_version,
    )


@lru_cache(maxsize=1)
def get_fast_client() -> AzureOpenAI:
    s = Settings()
    return AzureOpenAI(
        api_key=s.azure_openai_api_key,
        azure_endpoint=s.azure_openai_endpoint,
        api_version=s.azure_openai_api_version,
    )


def call_llm(client: AzureOpenAI, deployment: str, prompt: str, system: str = "") -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(model=deployment, messages=messages)
    return response.choices[0].message.content or ""


def load_prompt(filename: str) -> str:
    s = Settings()
    return (s.prompts_dir / filename).read_text(encoding="utf-8")
