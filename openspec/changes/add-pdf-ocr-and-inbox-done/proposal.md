# Change: Add PDF OCR fallback and inbox_done archiving

## Why
PDF ingestion currently depends on `pdftotext` only. Text PDFs usually work, but scanned PDFs or weak extractions fall through to `needs_review` with no OCR recovery path. Separately, files processed from `data/inbox/` remain in place forever, so the inbox does not reflect what still needs work.

## What Changes
- Add a PDF OCR fallback that runs only when `pdftotext` extraction is empty or too weak to use.
- Use GPT-based OCR on rendered PDF pages to recover text from scanned or image-heavy PDFs.
- Keep the existing fast path for text PDFs so OCR is not invoked unnecessarily.
- Move successfully processed local inbox files from `data/inbox/` to `data/inbox_done/`.
- Leave failed inbox files in place so they remain visible for retry and debugging.

## Impact
- Affected code: PDF fetch/extraction, LLM client utilities, pipeline orchestration, inbox lifecycle handling, tests.
- Affected runtime behavior: scanned PDFs can succeed instead of falling straight to `needs_review`; successful inbox file items no longer remain in `data/inbox/`.
- Affected operations: OCR increases LLM usage cost for fallback cases only; `data/inbox_done/` becomes the archive location for processed local files.
