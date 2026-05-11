# Concurrency and Deduplication in Guides Pipeline

This document describes how the `guides` pipeline protects against duplicate processing and race conditions during concurrent runs.

## 1. Concurrency Protection (Locking)

The main entry point `process_stream.py` uses a PID-based locking mechanism to ensure that only one instance of the pipeline is running at a time.

- **Lock File:** `data/state/process_stream.lock`
- **Mechanism:** 
    1. When starting, the script checks if the lock file exists.
    2. If it exists, it reads the PID and checks if a process with that PID is still running.
    3. If the process is running, it raises `RuntimeError` and exits.
    4. If the process is not running (stale lock), it removes the file.
    5. It then creates a new lock file with its own PID.
    6. The lock is automatically removed when the script finishes or crashes (via context manager).

## 2. Item Deduplication

Items to be processed are collected from two sources:
- `data/queue/inbox.txt` (via `pop_pending`)
- `data/inbox/` directory (via `scan_inbox`)

### deduplication within a single run
Before processing, `process_stream.py` deduplicates the combined list of items by their `source` string. This ensures that if the same URL or file is present in both the queue file and the inbox folder, it is only processed once.

### deduplication against already processed items
In the processing loop, every item is checked using `queue.already_processed(source)`. 
- **Check:** It hashes the source string and looks for a corresponding directory in `data/sources/`.
- **Action:** If a directory already exists, the item is skipped.
- **Queue Cleanup:** If the item came from `inbox.txt`, it is still marked as `#done#` even if skipped, to prevent it from appearing in the next run.

## 3. Optimization in Inbox Scanning

The `scan_inbox` function performs early deduplication to keep the processing list lean:
- **Files:** Skips files that have already been processed (checked via `already_processed`).
- **Extracted URLs:** If a file contains URLs (e.g., a `.txt` file with a single URL), it extracts the URL and checks `already_processed` for the URL itself before adding it to the queue.
- **Done Files:** Skips files starting with `#done#`.

## 4. Queue Persistence

The `mark_done` function ensures that successfully processed (or skipped) items from `inbox.txt` are not picked up again:
- It prepends `#done# ` to the line in `inbox.txt`.
- `pop_pending` ignores any lines starting with `#`.

## Summary Table

| Protection Layer | Component | Target | Purpose |
|------------------|-----------|--------|---------|
| **Locking** | `process_stream.py` | Entire Process | Prevent concurrent runs |
| **Source Dedup** | `process_stream.py` | Memory List | Prevent processing same source twice in one run |
| **Processed Guard** | `process_stream.py` | Loop Item | Skip items already in `data/sources/` |
| **Inbox Filter** | `guides/queue.py` | `scan_inbox` | Skip files/URLs already in `data/sources/` |
| **Queue Marking** | `guides/queue.py` | `inbox.txt` | Persistently mark queue items as done |
