from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

COST_PER_1K = {
    "gpt-5.4": {"input": 0.003, "output": 0.012},
    "gpt-5.4-mini": {"input": 0.00015, "output": 0.0006},
    "gpt-5.4-pro": {"input": 0.005, "output": 0.020},
    "gpt-4.1-mini": {"input": 0.0001, "output": 0.0004},
    "deepseek-v4-flash": {"input": 0.0001, "output": 0.0003},
}


@dataclass
class UsageRecord:
    deployment: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd: float = field(default=0.0)


def extract_usage(response: Any, deployment: str) -> UsageRecord:
    usage = getattr(response, "usage", None)
    if usage:
        prompt = usage.prompt_tokens or 0
        completion = usage.completion_tokens or 0
    else:
        prompt = 0
        completion = 0
    total = prompt + completion
    cost = _estimate_cost(deployment, prompt, completion)
    return UsageRecord(
        deployment=deployment,
        prompt_tokens=prompt,
        completion_tokens=completion,
        total_tokens=total,
        cost_usd=cost,
    )


def _estimate_cost(deployment: str, prompt: int, completion: int) -> float:
    key = deployment.lower()
    rates = COST_PER_1K.get(key, {"input": 0.001, "output": 0.002})
    return (prompt / 1000) * rates["input"] + (completion / 1000) * rates["output"]


def record_to_log_extra(record: UsageRecord) -> dict:
    return {
        "deployment": record.deployment,
        "prompt_tokens": record.prompt_tokens,
        "completion_tokens": record.completion_tokens,
        "total_tokens": record.total_tokens,
        "cost_usd": round(record.cost_usd, 6),
    }