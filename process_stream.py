from __future__ import annotations

import logging
import sys
from pathlib import Path

from guides import queue
from guides.run import run_pipeline


ROOT = Path(__file__).resolve().parent


def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(message)s")
    log = logging.getLogger("process_stream")

    queue_file = ROOT / "data" / "queue" / "inbox.txt"
    inbox_dir = ROOT / "data" / "inbox"

    items = queue.pop_pending(queue_file)
    items.extend(queue.scan_inbox(inbox_dir))

    quarantine_file = ROOT / "data" / "queue" / "needs_review.txt"

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
