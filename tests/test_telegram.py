import pytest
from unittest.mock import MagicMock, patch


def test_escape_markdown_v2_plain_text():
    from guides.pipelines.g_telegram import _escape_markdown_v2
    assert _escape_markdown_v2("Hello World") == "Hello World"


def test_escape_markdown_v2_escapes_specials():
    from guides.pipelines.g_telegram import _escape_markdown_v2
    # MarkdownV2 special chars: _ * [ ] ( ) ~ ` > # + - = | { } . !
    result = _escape_markdown_v2("Hello_World")
    assert r"\_" in result or "\\_" in result  # underscore must be escaped


def test_escape_markdown_v2_escapes_dot():
    from guides.pipelines.g_telegram import _escape_markdown_v2
    result = _escape_markdown_v2("v1.0")
    assert "\\." in result


def test_escape_markdown_v2_empty_string():
    from guides.pipelines.g_telegram import _escape_markdown_v2
    assert _escape_markdown_v2("") == ""


def test_send_redacts_token_on_error():
    from guides.pipelines.g_telegram import send_telegram_message

    settings = MagicMock(
        telegram_bot_token="12345:SECRET_TOKEN",
        telegram_channel_id="@chan",
    )

    with patch("guides.pipelines.g_telegram._s", return_value=settings), patch(
        "guides.pipelines.g_telegram.logger"
    ) as logger_mock, patch("guides.pipelines.g_telegram.httpx.Client") as client_cls:
        client = client_cls.return_value.__enter__.return_value
        client.post.side_effect = RuntimeError("boom 12345:SECRET_TOKEN exploded")

        with pytest.raises(RuntimeError):
            send_telegram_message("hi")

        logged = logger_mock.error.call_args[0][1]
        assert "SECRET_TOKEN" not in logged
        assert "<TOKEN>" in logged
