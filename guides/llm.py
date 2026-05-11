import logging
from functools import lru_cache

from openai import OpenAI

from guides.settings import Settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _client() -> OpenAI:
    s = Settings()
    return OpenAI(api_key=s.azure_openai_api_key, base_url=s.azure_openai_endpoint)


def get_smart_client() -> OpenAI:
    return _client()


def get_fast_client() -> OpenAI:
    return _client()


def call_llm(client: OpenAI, deployment: str, prompt: str, system: str = "") -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(model=deployment, messages=messages)

    from guides.enrich.accounting import extract_usage, record_to_log_extra

    rec = extract_usage(response, deployment)
    logger.info("llm_call", extra={"extra": record_to_log_extra(rec)})

    return response.choices[0].message.content or ""


def call_smart(prompt: str, system: str = "") -> str:
    s = Settings()
    return call_llm(_client(), s.azure_deployment_smart, prompt, system)


def call_fast(prompt: str, system: str = "") -> str:
    s = Settings()
    deployment = s.azure_deployment_fast or s.azure_deployment_smart
    return call_llm(_client(), deployment, prompt, system)


def load_prompt(filename: str) -> str:
    s = Settings()
    return (s.prompts_dir / filename).read_text(encoding="utf-8")
