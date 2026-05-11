from __future__ import annotations

import logging
import os
from contextlib import contextmanager
from pathlib import Path

from guides import queue
from guides.log_setup import setup_logging
from guides.run import run_pipeline
from guides.tracing import init_tracing


ROOT = Path(__file__).resolve().parent


def _pid_is_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


@contextmanager
def pipeline_run_lock(lock_path: Path):
    if lock_path.exists():
        try:
            existing_pid = int(lock_path.read_text(encoding="utf-8").strip())
        except ValueError:
            existing_pid = 0
        if existing_pid and _pid_is_running(existing_pid):
            raise RuntimeError(f"process_stream is already running with pid={existing_pid}")
        lock_path.unlink(missing_ok=True)

    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(str(os.getpid()), encoding="utf-8")
    try:
        yield
    finally:
        lock_path.unlink(missing_ok=True)


def main() -> None:
    setup_logging(ROOT / "data" / "logs")
    init_tracing()
    log = logging.getLogger("process_stream")

    queue_file = ROOT / "data" / "queue" / "inbox.txt"
    inbox_dir = ROOT / "data" / "inbox"

    items = queue.pop_pending(queue_file)
    items.extend(queue.scan_inbox(inbox_dir))
    seen_sources: set[str] = set()
    deduped = []
    for it in items:
        if it.source not in seen_sources:
            seen_sources.add(it.source)
            deduped.append(it)
    items = deduped

    quarantine_file = ROOT / "data" / "queue" / "needs_review.txt"
    lock_path = ROOT / "data" / "state" / "process_stream.lock"

    with pipeline_run_lock(lock_path):
        for item in items:
            result = run_pipeline(item)
            if result.get("status") == "failed":
                log.info("source=%s status=failed error=%s", result["source"], result.get("error", ""))
                queue.quarantine(item, result.get("error", "unknown"), quarantine_file)
                continue

            log.info(
                "source=%s status=%s vault_path=%s",
                result["source"],
                result.get("status", ""),
                result.get("vault_path", ""),
            )
            queue.mark_done(queue_file, item)


if __name__ == "__main__":
    main()
