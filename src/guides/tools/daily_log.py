"""Daily log for pipeline actions — append-only JSONL."""

import json
import os
from datetime import datetime
from pathlib import Path

try:
    import fcntl
except ImportError:
    fcntl = None


def _get_log_path() -> Path:
    now = datetime.now()
    filename = now.strftime("%Y-%m-%d") + ".jsonl"
    return Path(__file__).resolve().parent.parent.parent.parent / "logs" / filename


def _write_jsonl(path: Path, record: dict) -> None:
    line = json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
    with open(path, "a", encoding="utf-8") as f:
        if fcntl is not None:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            f.write(line)
            f.flush()
            os.fsync(f.fileno())
        finally:
            if fcntl is not None:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def append_log_entry(
    slug: str,
    action: str,
    model: str = "",
    tokens_in: int = 0,
    tokens_out: int = 0,
    cost_usd: float = 0.0,
) -> None:
    log_path = _get_log_path()
    log_path.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "msg": "llm_call",
        "slug": slug,
        "action": action,
        "deployment": model,
        "prompt_tokens": tokens_in,
        "completion_tokens": tokens_out,
        "total_tokens": tokens_in + tokens_out,
        "cost_usd": cost_usd,
    }
    _write_jsonl(log_path, record)
