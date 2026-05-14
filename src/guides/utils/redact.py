from functools import lru_cache


@lru_cache(maxsize=1)
def _get_secret_tokens() -> tuple[str, ...]:
    try:
        from guides.settings import get_settings
        s = get_settings()
        return tuple(
            t for t in (
                s.telegram_bot_token,
                s.azure_openai_api_key,
                s.github_token,
                s.jina_api_key,
            )
            if t and len(t) > 5
        )
    except Exception:
        return ()


def redact_tokens(text: str) -> str:
    redacted = text
    for t in _get_secret_tokens():
        redacted = redacted.replace(t, "<TOKEN>")
    return redacted
