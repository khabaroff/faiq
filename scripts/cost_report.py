#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path


@dataclass
class Totals:
    calls: int = 0
    tokens: int = 0
    cost_usd: float = 0.0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Show guides LLM usage cost report")
    parser.add_argument("--days", type=int, default=None, help="Only include the last N days")
    return parser.parse_args()


def _log_dir() -> Path:
    return Path("data/logs")


def _iter_log_files(log_dir: Path) -> list[Path]:
    files = sorted(p for p in log_dir.glob("pipeline.log*") if p.is_file())
    return files


def _parse_ts(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None


def _within_days(ts: datetime, days: int | None) -> bool:
    if days is None:
        return True
    cutoff = datetime.now(ts.tzinfo) - timedelta(days=days - 1) if days > 0 else datetime.min
    return ts >= cutoff


def _format_usd(amount: float) -> str:
    return f"${amount:.4f}"


def _collect_entries(log_files: list[Path], days: int | None) -> list[dict]:
    entries: list[dict] = []
    for path in log_files:
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            if payload.get("msg") != "llm_call":
                continue
            ts = _parse_ts(str(payload.get("ts", "")))
            if ts is None or not _within_days(ts, days):
                continue
            entries.append(payload)
    return entries


def _aggregate(entries: list[dict]) -> tuple[dict[str, Totals], dict[str, Totals], Totals]:
    by_model: dict[str, Totals] = defaultdict(Totals)
    by_date: dict[str, Totals] = defaultdict(Totals)
    grand = Totals()

    for row in entries:
        deployment = str(row.get("deployment", "unknown"))
        ts = str(row.get("ts", ""))
        day = ts[:10] if len(ts) >= 10 else "unknown"
        tokens = int(row.get("total_tokens", 0) or 0)
        cost = float(row.get("cost_usd", 0) or 0)

        for bucket in (by_model[deployment], by_date[day], grand):
            bucket.calls += 1
            bucket.tokens += tokens
            bucket.cost_usd += cost

    return by_model, by_date, grand


def _print_section(title: str, rows: list[tuple[str, Totals]]) -> None:
    print(title)
    for key, totals in rows:
        print(
            f"{key:<22} calls={totals.calls:<4} tokens={totals.tokens:<8} cost={_format_usd(totals.cost_usd)}"
        )


def main() -> int:
    args = _parse_args()
    log_dir = _log_dir()
    if not log_dir.exists():
        print("No logs found in data/logs")
        return 0

    entries = _collect_entries(_iter_log_files(log_dir), args.days)
    by_model, by_date, grand = _aggregate(entries)

    label = "all time" if args.days is None else f"last {args.days} days"
    print(f"=== Cost Report ({label}) ===")
    print()
    _print_section("By Model:", sorted(by_model.items()))
    print()
    _print_section("By Date:", sorted(by_date.items()))
    print()
    print(f"TOTAL: {grand.calls} calls, {grand.tokens} tokens, {_format_usd(grand.cost_usd)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
