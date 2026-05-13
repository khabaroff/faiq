import base64
import logging
import mimetypes
from functools import lru_cache
from pathlib import Path
from typing import Sequence, Any, NamedTuple

from openai import OpenAI

from guides.settings import Settings

logger = logging.getLogger(__name__)


class UsageRecord(NamedTuple):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd: float
    deployment: str


def estimate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    # Azure/OpenAI GPT-4o style pricing as reasonable default for gpt-5.4
    # $5.00 / 1M input, $15.00 / 1M output
    if "mini" in model.lower():
        # GPT-4o-mini style: $0.15 / 1M input, $0.60 / 1M output
        return (prompt_tokens * 0.15 / 1_000_000) + (completion_tokens * 0.60 / 1_000_000)
    
    return (prompt_tokens * 5.00 / 1_000_000) + (completion_tokens * 15.00 / 1_000_000)


def extract_usage(response: Any, deployment: str) -> UsageRecord:
    usage = getattr(response, "usage", None)
    prompt_tokens = getattr(usage, "prompt_tokens", 0) or 0
    completion_tokens = getattr(usage, "completion_tokens", 0) or 0
    total_tokens = getattr(usage, "total_tokens", 0) or 0
    cost_usd = estimate_cost(deployment, prompt_tokens, completion_tokens)
    return UsageRecord(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        cost_usd=cost_usd,
        deployment=deployment,
    )


def record_to_log_extra(rec: UsageRecord) -> dict:
    return {
        "deployment": rec.deployment,
        "prompt_tokens": rec.prompt_tokens,
        "completion_tokens": rec.completion_tokens,
        "total_tokens": rec.total_tokens,
        "cost_usd": rec.cost_usd,
    }


@lru_cache(maxsize=1)
def _client() -> OpenAI:
    s = Settings()
    return OpenAI(api_key=s.azure_openai_api_key, base_url=s.azure_openai_endpoint)


def get_smart_client() -> OpenAI:
    return _client()


def get_fast_client() -> OpenAI:
    return _client()


def _record_usage(response, deployment: str) -> UsageRecord:
    rec = extract_usage(response, deployment)
    logger.info("llm_call", extra={"extra": record_to_log_extra(rec)})
    return rec


def _extract_response_text(response) -> str:
    content = response.choices[0].message.content or ""
    if isinstance(content, str):
        return content

    parts: list[str] = []
    for item in content:
        if isinstance(item, str):
            parts.append(item)
            continue
        text = getattr(item, "text", None)
        if text:
            parts.append(text)
            continue
        if isinstance(item, dict) and item.get("type") == "text":
            parts.append(item.get("text", ""))
    return "\n".join(part for part in parts if part)


def call_llm(client: OpenAI, deployment: str, prompt: str, system: str = "") -> tuple[str, UsageRecord]:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(model=deployment, messages=messages)
    usage = _record_usage(response, deployment)
    return _extract_response_text(response), usage


def _image_path_to_data_url(image_path: Path) -> str:
    mime_type = mimetypes.guess_type(image_path.name)[0] or "image/png"
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def call_llm_with_images(
    client: OpenAI, deployment: str, prompt: str, image_paths: Sequence[Path], system: str = ""
) -> tuple[str, UsageRecord]:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})

    content = [{"type": "text", "text": prompt}]
    for image_path in image_paths:
        content.append({"type": "image_url", "image_url": {"url": _image_path_to_data_url(Path(image_path))}})

    messages.append({"role": "user", "content": content})
    response = client.chat.completions.create(model=deployment, messages=messages)
    usage = _record_usage(response, deployment)
    return _extract_response_text(response), usage


def call_smart(prompt: str, system: str = "") -> str:
    s = Settings()
    return call_llm(_client(), s.azure_deployment_smart, prompt, system)


def call_fast(prompt: str, system: str = "") -> str:
    s = Settings()
    deployment = s.azure_deployment_fast or s.azure_deployment_smart
    return call_llm(_client(), deployment, prompt, system)


def call_smart_with_images(
    prompt: str, image_paths: Sequence[Path], system: str = "", return_usage: bool = False
) -> str | tuple[str, UsageRecord]:
    s = Settings()
    text, usage = call_llm_with_images(_client(), s.azure_deployment_smart, prompt, image_paths, system)
    if return_usage:
        return text, usage
    return text


def load_prompt(filename: str) -> str:
    s = Settings()
    return (s.prompts_dir / filename).read_text(encoding="utf-8")
