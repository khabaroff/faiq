"""Tests for image_ocr.process_markdown_file via injectable fetcher/vlm_runner."""
from __future__ import annotations

import time
from pathlib import Path
from urllib.parse import urlparse

import httpx
import pytest

from guides.fetch.image_ocr import (
    OCRResult,
    NonImageContentError,
    process_markdown_file,
    _download_url,
    _prepare_image_for_ocr,
)

_FAKE_SHA = "a" * 64
_FAKE_CONTENT_TYPE = "image/png"
_FAKE_BYTES = b"\x89PNG"


def _make_fetcher(asset_path: Path):
    def fetcher(url: str):
        return _FAKE_SHA, asset_path, _FAKE_BYTES, _FAKE_CONTENT_TYPE
    return fetcher


def _make_vlm(result: OCRResult):
    def vlm_runner(image_bytes, *, content_type, model, asset_path):
        return result, 10, 5, 0.0001
    return vlm_runner


_GOOD_RESULT = OCRResult(
    image_type="diagram",
    visible_text="Hello World",
    description="A test diagram.",
)


def test_no_images_unchanged(tmp_path):
    md = tmp_path / "article.md"
    md.write_text("# Title\n\nJust text, no images.\n")
    stats = process_markdown_file(
        md,
        fetcher=_make_fetcher(tmp_path / "img.png"),
        vlm_runner=_make_vlm(_GOOD_RESULT),
    )
    assert stats["remote_urls"] == 0
    assert stats["inserted_blocks"] == 0
    assert not stats["changed"]
    assert md.read_text() == "# Title\n\nJust text, no images.\n"


def test_remote_image_gets_ocr_block(tmp_path):
    asset = tmp_path / (_FAKE_SHA + ".png")
    asset.write_bytes(_FAKE_BYTES)
    md = tmp_path / "article.md"
    md.write_text("![fig](https://example.com/img.png)\n")
    stats = process_markdown_file(
        md,
        fetcher=_make_fetcher(asset),
        vlm_runner=_make_vlm(_GOOD_RESULT),
    )
    assert stats["inserted_blocks"] == 1
    assert stats["changed"]
    content = md.read_text()
    assert "> **Image OCR (auto):**" in content
    assert "Hello World" in content
    assert "A test diagram." in content


def test_non_image_url_skipped(tmp_path):
    def fetcher_raises(url: str):
        raise NonImageContentError(url, "text/html")

    md = tmp_path / "article.md"
    md.write_text("![fig](https://example.com/page.html)\n")
    original = md.read_text()
    stats = process_markdown_file(
        md,
        fetcher=fetcher_raises,
        vlm_runner=_make_vlm(_GOOD_RESULT),
    )
    assert stats["inserted_blocks"] == 0
    assert not stats["changed"]


def test_existing_ocr_block_not_duplicated(tmp_path):
    asset = tmp_path / (_FAKE_SHA + ".png")
    asset.write_bytes(_FAKE_BYTES)
    md = tmp_path / "article.md"
    content = (
        "![fig](https://example.com/img.png)\n"
        "> **Image OCR (auto):**\n"
        "> **Type:** diagram\n"
        "> **Text:** Existing\n"
        "> **Description:** Already there.\n"
        "\n"
    )
    md.write_text(content)
    stats = process_markdown_file(
        md,
        fetcher=_make_fetcher(asset),
        vlm_runner=_make_vlm(_GOOD_RESULT),
    )
    assert stats["inserted_blocks"] == 0


def test_multiple_images_in_one_file(tmp_path):
    asset = tmp_path / (_FAKE_SHA + ".png")
    asset.write_bytes(_FAKE_BYTES)
    md = tmp_path / "article.md"
    md.write_text(
        "![a](https://example.com/a.png)\n"
        "\nSome text\n\n"
        "![b](https://example.com/b.png)\n"
    )
    stats = process_markdown_file(
        md,
        fetcher=_make_fetcher(asset),
        vlm_runner=_make_vlm(_GOOD_RESULT),
    )
    assert stats["remote_urls"] == 2
    assert stats["inserted_blocks"] == 2
    assert stats["changed"]


def test_parallel_ocr_keeps_output_order_and_reduces_wall_time(tmp_path):
    sha_a = "c" * 64
    sha_b = "d" * 64
    asset_a = tmp_path / (sha_a + ".png")
    asset_b = tmp_path / (sha_b + ".png")
    asset_a.write_bytes(_FAKE_BYTES)
    asset_b.write_bytes(_FAKE_BYTES)
    md = tmp_path / "article.md"
    md.write_text(
        "![a](https://example.com/a.png)\n"
        "![b](https://example.com/b.png)\n"
    )

    def fetcher(url: str):
        if url.endswith("/a.png"):
            return sha_a, asset_a, _FAKE_BYTES, _FAKE_CONTENT_TYPE
        return sha_b, asset_b, _FAKE_BYTES, _FAKE_CONTENT_TYPE

    def vlm_runner(image_bytes, *, content_type, model, asset_path):
        time.sleep(0.2)
        name = asset_path.stem[0].upper()
        return OCRResult(
            image_type="diagram",
            visible_text=f"Text {name}",
            description=f"Desc {name}",
        ), 10, 5, 0.0001

    start = time.perf_counter()
    stats = process_markdown_file(md, fetcher=fetcher, vlm_runner=vlm_runner)
    elapsed = time.perf_counter() - start

    content = md.read_text()
    assert stats["inserted_blocks"] == 2
    assert "Text C" in content
    assert "Text D" in content
    assert content.index("Text C") < content.index("Text D")
    assert elapsed < 0.35


def test_prepare_image_for_ocr_without_pillow_returns_original_asset(tmp_path):
    asset = tmp_path / "img.png"
    asset.write_bytes(_FAKE_BYTES)
    prepared = _prepare_image_for_ocr(_FAKE_BYTES, "image/png", asset)
    assert prepared == asset


from unittest.mock import patch, MagicMock

def test_redirect_to_metadata_blocked():
    # Initial URL is safe, but redirects to metadata IP
    target_url = "https://safe.com/img.png"
    metadata_url = "http://169.254.169.254/secret.png"
    
    mock_resp = MagicMock(spec=httpx.Response)
    mock_resp.is_redirect = True
    mock_resp.status_code = 301
    mock_resp.headers = {"location": metadata_url}
    
    def fake_validate_url(url: str) -> str:
        host = (urlparse(url).hostname or "").lower()
        if host == "169.254.169.254":
            raise ValueError(f"Host blocked: {host!r}")
        return url

    with patch("guides.fetch.image_ocr.validate_url", side_effect=fake_validate_url), patch("httpx.Client.get", return_value=mock_resp):
        with pytest.raises(ValueError, match="Host blocked"):
            _download_url(target_url)


def test_file_scheme_rejected():
    with pytest.raises(ValueError, match="URL scheme blocked"):
        _download_url("file:///etc/passwd")
