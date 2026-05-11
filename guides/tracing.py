from __future__ import annotations

import logging
import uuid
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Generator

logger = logging.getLogger(__name__)

_langfuse = None
_current_trace: ContextVar[object | None] = ContextVar("current_langfuse_trace", default=None)


def init_tracing() -> None:
    global _langfuse
    from guides.settings import Settings

    s = Settings()
    if not s.langfuse_enabled:
        return

    try:
        from langfuse import Langfuse

        _langfuse = Langfuse(
            public_key=s.langfuse_public_key,
            secret_key=s.langfuse_secret_key,
            host=s.langfuse_host,
        )
    except Exception as e:
        logger.warning("Langfuse init failed, tracing disabled: %s", e)


def get_current_trace() -> object | None:
    return _current_trace.get()


@contextmanager
def trace_run(run_id: str, source: str) -> Generator:
    if _langfuse is None:
        yield None
        return

    trace = None
    token = None
    try:
        run_id = run_id or str(uuid.uuid4())
        trace = _langfuse.trace(id=run_id, name="pipeline_run", metadata={"source": source})
        token = _current_trace.set(trace)
        yield trace
    except Exception as e:
        logger.warning("Langfuse trace failed: %s", e)
        yield None
    finally:
        if token is not None:
            _current_trace.reset(token)
        if _langfuse:
            try:
                _langfuse.flush()
            except Exception:
                pass


def trace_llm_call(trace, deployment: str, prompt_tokens: int, completion_tokens: int, cost_usd: float) -> None:
    if trace is None:
        return
    try:
        trace.generation(
            name="llm_call",
            model=deployment,
            usage={"input": prompt_tokens, "output": completion_tokens},
            metadata={"cost_usd": cost_usd},
        )
    except Exception as e:
        logger.warning("Langfuse generation trace failed: %s", e)
