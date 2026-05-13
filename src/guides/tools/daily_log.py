"""Daily log for pipeline actions."""

from datetime import datetime
from pathlib import Path


def _get_log_path() -> Path:
    now = datetime.now()
    filename = now.strftime("%Y-%m-%d") + ".md"
    return Path(__file__).resolve().parent.parent.parent.parent / "logs" / filename


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

    now = datetime.now().strftime("%H:%M:%S")
    total_tokens = tokens_in + tokens_out
    cost_str = f"{cost_usd:.4f}"

    table_row = f"| {slug} | {action} | {model} | {total_tokens} | ${cost_str} | {now} |"

    if not log_path.exists():
        header = """# Daily Pipeline Log

| slug | action | model | tokens | cost | time |
| ---- | ------ | ----- | ------ | ---- | ---- |
"""
        log_path.write_text(header, encoding="utf-8")

    existing = log_path.read_text(encoding="utf-8")

    lines = existing.splitlines()

    total_idx = None
    for i, line in enumerate(lines):
        if line.startswith("Total cost:"):
            total_idx = i
            break

    current_total = 0.0
    if total_idx is not None:
        try:
            current_total = float(lines[total_idx].split("$")[1].strip())
        except (IndexError, ValueError):
            pass

    new_total = current_total + cost_usd
    total_line = f"Total cost: ${new_total:.4f}"

    if total_idx is not None:
        lines[total_idx] = total_line
        lines.insert(total_idx, table_row)
    else:
        lines.append("")
        lines.append(total_line)
        lines.append(table_row)

    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")