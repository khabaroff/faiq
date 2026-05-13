import shutil
import subprocess
import tempfile
from pathlib import Path

from guides.fetch.base import FetchedContent, QueueItem, SourceType
from guides.llm import call_smart_with_images

PDF_TEXT_MIN_CHARS = 100
PDF_OCR_SYSTEM = "You are an OCR engine. Extract all readable text from the PDF page. Return plain text only."
PDF_OCR_PROMPT = "Extract all readable text from this PDF page in reading order. Do not summarize."


def _validate_path(path: Path) -> Path:
    """Reject paths starting with - to prevent flag injection."""
    if str(path.name).startswith("-"):
        raise ValueError(f"Suspicious path rejected: {path}")
    return path


def fetch_pdf(item: QueueItem) -> FetchedContent:
    text = _extract_pdf_text(item.source)
    if _has_usable_pdf_text(text):
        return FetchedContent(
            raw_text=text,
            source_type=SourceType.ARTICLE,
            source_meta={"source_path": item.source, "fetcher": "pdftotext"},
        )

    ocr_text = _ocr_pdf_fallback(item.source)
    if _has_usable_pdf_text(ocr_text):
        return FetchedContent(
            raw_text=ocr_text,
            source_type=SourceType.ARTICLE,
            source_meta={"source_path": item.source, "fetcher": "gpt-ocr"},
        )

    return FetchedContent(
        raw_text="",
        source_type=SourceType.ARTICLE,
        source_meta={"source_path": item.source, "error": "extraction_failed"},
    )


def _extract_pdf_text(pdf_path: str) -> str:
    try:
        _validate_path(Path(pdf_path))
        result = subprocess.run(
            ["pdftotext", "--", pdf_path, "-"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0:
            return result.stdout
    except Exception:
        pass
    return ""


def _has_usable_pdf_text(text: str) -> bool:
    return len(text.strip()) > PDF_TEXT_MIN_CHARS


def _ocr_pdf_fallback(pdf_path: str) -> str:
    image_paths = _render_pdf_pages(pdf_path)
    if not image_paths:
        return ""

    try:
        return _ocr_rendered_pages(image_paths)
    except Exception:
        return ""
    finally:
        _cleanup_rendered_pages(image_paths)


def _render_pdf_pages(pdf_path: str) -> list[Path]:
    temp_dir = Path(tempfile.mkdtemp(prefix="guides-pdf-ocr-"))
    output_prefix = temp_dir / "page"
    try:
        _validate_path(Path(pdf_path))
        result = subprocess.run(
            ["pdftoppm", "-png", "-r", "144", "--", pdf_path, str(output_prefix)],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            shutil.rmtree(temp_dir, ignore_errors=True)
            return []
        return sorted(temp_dir.glob("page-*.png"))
    except Exception:
        shutil.rmtree(temp_dir, ignore_errors=True)
        return []


def _ocr_rendered_pages(image_paths: list[Path]) -> str:
    page_texts: list[str] = []
    for image_path in image_paths:
        text = call_smart_with_images(PDF_OCR_PROMPT, [image_path], system=PDF_OCR_SYSTEM).strip()
        if text:
            page_texts.append(text)
    return "\n\n".join(page_texts)


def _cleanup_rendered_pages(image_paths: list[Path]) -> None:
    if not image_paths:
        return
    shutil.rmtree(image_paths[0].parent, ignore_errors=True)
