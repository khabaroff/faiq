import base64
import logging
import mimetypes
from collections.abc import Sequence
from functools import lru_cache
from pathlib import Path
from typing import Any, NamedTuple

from openai import APIError, APIStatusError, APITimeoutError, AzureOpenAI, OpenAI, RateLimitError
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)
from tenacity.wait import wait_base

from guides.settings import Settings

logger = logging.getLogger(__name__)


def count_tokens(text: str, model: str = "gpt-4o") -> int:
    try:
        import tiktoken
        try:
            enc = tiktoken.encoding_for_model(model)
        except KeyError:
            logger.warning("No encoding found for model %s, using cl100k_base", model)
            enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception as e:
        logger.warning("tiktoken failed: %s. Falling back to length-based estimation.", e)
        # 1 token ~= 4 chars for EN, but for RU it's closer to 2 chars.
        # Using a conservative 2 to avoid 429 storms.
        return len(text) // 2


def truncate_to_tokens(text: str, max_tokens: int, model: str = "gpt-4o") -> str:
    try:
        import tiktoken
        try:
            enc = tiktoken.encoding_for_model(model)
        except KeyError:
            enc = tiktoken.get_encoding("cl100k_base")
        tokens = enc.encode(text)
        if len(tokens) <= max_tokens:
            return text
        return enc.decode(tokens[:max_tokens])
    except Exception:
        # Fallback to rough char truncation
        return text[:max_tokens * 2]


@lru_cache(maxsize=1)
def _get_settings() -> Settings:
    return Settings()


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
def _client() -> AzureOpenAI:
    s = Settings()
    return AzureOpenAI(
        api_key=s.azure_openai_api_key,
        azure_endpoint=s.azure_openai_endpoint,
        api_version=s.azure_openai_api_version,
        timeout=120.0,
        max_retries=0,
    )


def _should_retry(exc: BaseException) -> bool:
    if isinstance(exc, RateLimitError):
        return True
    if isinstance(exc, APITimeoutError):
        return True
    if isinstance(exc, APIStatusError):
        return exc.status_code in {500, 502, 503, 504}
    return False


class _WaitWithRetryAfter(wait_base):
    """Respects Retry-After header on 429; falls back to exponential backoff."""

    def __call__(self, retry_state):
        exc = retry_state.outcome.exception()
        if isinstance(exc, RateLimitError):
            response = getattr(exc, "response", None)
            if response is not None:
                retry_after = response.headers.get("retry-after") or response.headers.get("Retry-After")
                if retry_after:
                    try:
                        return float(retry_after)
                    except (ValueError, TypeError):
                        pass
        return wait_exponential(multiplier=1, min=2, max=30)(retry_state)


def _before_sleep_log(retry_state):
    exc = retry_state.outcome.exception()
    reason = f"{type(exc).__name__}_{getattr(exc, 'status_code', 'N/A')}"
    try:
        from guides.tools.daily_log import append_log_entry

        append_log_entry(
            slug="llm_retry",
            action=f"retry_{reason}",
            model="",
            tokens_in=0,
            tokens_out=0,
            cost_usd=0.0,
        )
    except Exception:
        logger.warning("Failed to log retry to daily_log", exc_info=True)


def get_smart_client() -> AzureOpenAI:
    return _client()


def get_fast_client() -> AzureOpenAI:
    return _client()


def _record_usage(response, deployment: str) -> UsageRecord:
    rec = extract_usage(response, deployment)
    logger.info("llm_call", extra={"extra": record_to_log_extra(rec)})
    return rec


def _extract_response_text(response) -> str:
    content = response.choices[0].message.content or ""
    if isinstance(content, str):
        text = content
    else:
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
                continue
            t = getattr(item, "text", None)
            if t:
                parts.append(t)
                continue
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
        text = "\n".join(part for part in parts if part)
    if not text.strip():
        raise ValueError("LLM returned empty response")
    return text


@retry(
    retry=retry_if_exception(_should_retry),
    wait=_WaitWithRetryAfter(),
    stop=stop_after_attempt(4),
    reraise=True,
    before_sleep=_before_sleep_log,
)
def _chat_create(client: OpenAI, deployment: str, messages: list) -> Any:
    return client.chat.completions.create(model=deployment, messages=messages, timeout=120.0)


def _check_cost_spike(usage: UsageRecord, deployment: str, estimated_input_tokens: int) -> None:
    estimated_completion_tokens = max(1, estimated_input_tokens // 4)
    estimated_cost = estimate_cost(deployment, estimated_input_tokens, estimated_completion_tokens)
    if usage.cost_usd > estimated_cost * 2:
        logger.critical(
            "LLM cost spike: actual_cost=%.4f, estimated_cost=%.4f, deployment=%s",
            usage.cost_usd,
            estimated_cost,
            deployment,
        )


def _estimate_message_tokens(messages: list) -> int:
    total = 0
    for m in messages:
        content = m.get("content", "")
        if isinstance(content, str):
            total += count_tokens(content)
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    total += count_tokens(item.get("text", ""))
    return total


def call_llm_messages(client: OpenAI, deployment: str, messages: list) -> tuple[str, UsageRecord]:
    response = _chat_create(client, deployment, messages)
    usage = _record_usage(response, deployment)
    _check_cost_spike(usage, deployment, _estimate_message_tokens(messages))
    return _extract_response_text(response), usage


def call_llm(client: OpenAI, deployment: str, prompt: str, system: str = "") -> tuple[str, UsageRecord]:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = _chat_create(client, deployment, messages)
    usage = _record_usage(response, deployment)
    _check_cost_spike(usage, deployment, count_tokens(prompt) + (count_tokens(system) if system else 0))
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


def call_smart(prompt: str, system: str = "") -> tuple[str, UsageRecord]:
    s = _get_settings()
    return call_llm(_client(), s.azure_deployment_smart, prompt, system)


def call_fast(prompt: str, system: str = "") -> tuple[str, UsageRecord]:
    s = _get_settings()
    deployment = s.azure_deployment_fast or s.azure_deployment_smart
    return call_llm(_client(), deployment, prompt, system)


def call_smart_with_images(
    prompt: str, image_paths: Sequence[Path], system: str = "", return_usage: bool = False
) -> str | tuple[str, UsageRecord]:
    s = _get_settings()
    text, usage = call_llm_with_images(_client(), s.azure_deployment_smart, prompt, image_paths, system)
    if return_usage:
        return text, usage
    return text


@lru_cache(maxsize=64)
def load_prompt(filename: str) -> str:
    s = _get_settings()
    return (s.prompts_dir / filename).read_text(encoding="utf-8")
