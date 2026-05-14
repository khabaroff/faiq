from __future__ import annotations

from functools import lru_cache
from typing import Protocol


class Logger(Protocol):
    def log_cost(
        self,
        *,
        slug: str,
        action: str,
        model: str,
        tokens_in: int,
        tokens_out: int,
        cost_usd: float,
    ) -> None: ...


class NullLogger:
    def log_cost(
        self,
        *,
        slug: str,
        action: str,
        model: str,
        tokens_in: int,
        tokens_out: int,
        cost_usd: float,
    ) -> None:
        return None


class DailyLogCostLogger:
    def log_cost(
        self,
        *,
        slug: str,
        action: str,
        model: str,
        tokens_in: int,
        tokens_out: int,
        cost_usd: float,
    ) -> None:
        from guides.tools.daily_log import append_log_entry

        append_log_entry(
            slug=slug,
            action=action,
            model=model,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            cost_usd=cost_usd,
        )


@lru_cache(maxsize=1)
def get_default_logger() -> Logger:
    return DailyLogCostLogger()
