import pytest


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
