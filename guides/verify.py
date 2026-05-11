def verify_output(source_text: str, output_text: str, tags: list[str]) -> dict:
    checks: dict[str, bool] = {}

    checks["not_empty"] = len(output_text) > 100
    checks["has_heading"] = any(line.startswith("#") for line in output_text.splitlines())
    checks["has_tags"] = bool(tags)
    checks["code_blocks_preserved"] = (
        "```" not in source_text or "```" in output_text
    )

    return {
        "passed": all(checks.values()),
        "checks": checks,
    }


def run_verify(source_text: str, output_text: str, tags: list[str], max_attempts: int = 3) -> tuple:
    result = verify_output(source_text, output_text, tags)
    return ("verified", result) if result["passed"] else ("needs_review", result)