import time
from unittest.mock import MagicMock, patch

import pytest
from openai import APIStatusError, RateLimitError

# Ensure src is on path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from guides.llm import _should_retry, _WaitWithRetryAfter, call_llm
from guides.json_extract import extract_json


class FakeRetryState:
    def __init__(self, exc, attempt_number=1):
        self.outcome = MagicMock()
        self.outcome.exception.return_value = exc
        self.attempt_number = attempt_number


def test_should_retry_429():
    exc = RateLimitError("rate limit", response=MagicMock(), body=None)
    assert _should_retry(exc) is True


def test_should_retry_500():
    resp = MagicMock()
    resp.status_code = 500
    exc = APIStatusError("server error", response=resp, body=None)
    assert _should_retry(exc) is True


def test_should_not_retry_400():
    resp = MagicMock()
    resp.status_code = 400
    exc = APIStatusError("bad request", response=resp, body=None)
    assert _should_retry(exc) is False


def test_should_not_retry_401():
    resp = MagicMock()
    resp.status_code = 401
    exc = APIStatusError("unauthorized", response=resp, body=None)
    assert _should_retry(exc) is False


def test_wait_with_retry_after_uses_header():
    resp = MagicMock()
    resp.headers = {"Retry-After": "0.1"}
    exc = RateLimitError("rate limit", response=resp, body=None)
    wait = _WaitWithRetryAfter()
    delay = wait(FakeRetryState(exc))
    assert abs(delay - 0.1) < 0.01


def test_wait_with_retry_after_fallback_exponential():
    resp = MagicMock()
    resp.headers = {}
    exc = RateLimitError("rate limit", response=resp, body=None)
    wait = _WaitWithRetryAfter()
    delay = wait(FakeRetryState(exc))
    assert delay >= 2.0
    assert delay <= 30.0


def test_400_fails_fast_no_retry():
    client = MagicMock()
    resp = MagicMock()
    resp.status_code = 400
    exc = APIStatusError("bad request", response=resp, body=None)
    client.chat.completions.create.side_effect = exc

    with pytest.raises(APIStatusError):
        call_llm(client, "gpt-4o", "say hi")

    assert client.chat.completions.create.call_count == 1


def test_429_retries_and_respects_retry_after():
    client = MagicMock()
    resp = MagicMock()
    resp.headers = {"Retry-After": "0.1"}
    exc = RateLimitError("rate limit", response=resp, body=None)

    ok_response = MagicMock()
    ok_response.usage.prompt_tokens = 1
    ok_response.usage.completion_tokens = 1
    ok_response.usage.total_tokens = 2
    ok_response.choices = [MagicMock()]
    ok_response.choices[0].message.content = "hi"

    client.chat.completions.create.side_effect = [exc, ok_response]

    start = time.monotonic()
    text, usage = call_llm(client, "gpt-4o", "say hi")
    elapsed = time.monotonic() - start

    assert text == "hi"
    assert client.chat.completions.create.call_count == 2
    assert elapsed >= 0.08  # at least ~0.1s wait


def test_extract_json_balanced_brace():
    payload = 'prefix {"a":"x { y }", "nested":{"b":1}} suffix {"ignored":true}'
    assert extract_json(payload) == {"a": "x { y }", "nested": {"b": 1}}
