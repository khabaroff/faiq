import subprocess

from guides.fetch.base import FetchedContent, QueueItem, SourceType


def fetch_pdf(item: QueueItem) -> FetchedContent:
    try:
        result = subprocess.run(
            ["pdftotext", item.source, "-"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0 and len(result.stdout.strip()) > 100:
            return FetchedContent(
                raw_text=result.stdout,
                source_type=SourceType.ARTICLE,
                source_meta={"path": item.source, "fetcher": "pdftotext"},
            )
    except Exception:
        pass

    return FetchedContent(
        raw_text="",
        source_type=SourceType.ARTICLE,
        source_meta={"path": item.source, "error": "extraction_failed"},
    )