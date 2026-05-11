import re


def _parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    result: dict[str, object] = {}
    current_key = None
    for line in block.splitlines():
        list_item = re.match(r"^\s+-\s+(.*)", line)
        if list_item and current_key:
            val = list_item.group(1).strip().strip('"').strip("'")
            if isinstance(result.get(current_key), list):
                result[current_key].append(val)
            else:
                result[current_key] = [val]
            continue
        m = re.match(r"^(\w+):\s*(.*)", line)
        if m:
            current_key = m.group(1)
            val = m.group(2).strip().strip('"').strip("'")
            result[current_key] = val if val else None
    return result


def _extract_tags_from_fm(fm: dict) -> list[str]:
    raw = fm.get("tags", "")
    if isinstance(raw, list):
        return raw
    if not raw:
        return []
    parts = re.findall(r"[\w\-\.]+", str(raw))
    return parts


def verify_output(source_text: str, output_text: str, tags: list[str], source_type: str = "article") -> dict:
    checks: dict[str, bool] = {}

    checks["not_empty"] = len(output_text) > 100
    checks["has_heading"] = any(line.startswith("#") for line in output_text.splitlines())
    checks["has_tags"] = bool(tags)
    checks["code_blocks_preserved"] = "```" not in source_text or "```" in output_text

    fm = _parse_frontmatter(output_text)
    required_keys = {"id", "title", "source_type", "status"}
    checks["has_frontmatter"] = bool(fm) and required_keys.issubset(fm.keys())
    checks["valid_source_type"] = fm.get("source_type", "") in ("article", "reference", "note", "file")

    if source_type == "article":
        checks["has_body_sections"] = (
            "## Краткое изложение" in output_text
            or "## Ключевые идеи" in output_text
            or "## Детали" in output_text
        )
    elif source_type == "reference":
        checks["has_body_sections"] = (
            "## Назначение" in output_text
            or "## Стек и зависимости" in output_text
            or "## Как использовать" in output_text
        )
    else:
        checks["has_body_sections"] = False

    fm_tags = _extract_tags_from_fm(fm)
    checks["fm_tags"] = bool(fm_tags)

    return {
        "passed": all(checks.values()),
        "checks": checks,
    }


def run_verify(source_text: str, output_text: str, tags: list[str], max_attempts: int = 3, source_type: str = "article") -> tuple:
    result = verify_output(source_text, output_text, tags, source_type=source_type)
    if not result["checks"].get("has_frontmatter", True):
        return ("needs_review", result)
    return ("verified", result) if result["passed"] else ("needs_review", result)
