## Context
The pipeline currently accepts `.pdf` files from `data/inbox/`, but extraction is limited to `pdftotext`. When that path fails, the PDF is stored as `needs_review` with no content recovery. The inbox scanner also treats `data/inbox/` as a passive source directory and never archives successful local files, so operators must manually infer what has already been ingested.

## Goals / Non-Goals
- Goals:
  - Recover readable text from scanned or weakly extracted PDFs using GPT-based OCR only when needed.
  - Preserve the cheap `pdftotext` path for normal text PDFs.
  - Move successfully processed local inbox files into `data/inbox_done/` automatically.
  - Keep failed local files visible in `data/inbox/` and `needs_review.txt`.
- Non-Goals:
  - Full OCR for every document type.
  - OCR for remote URLs.
  - Human review UI or retry queue redesign.

## Decisions
- Decision: Keep `pdftotext` as the primary extractor and use OCR as a fallback only when extracted text is empty or below a quality threshold.
  - Alternatives considered: always OCR all PDFs; rejected due to cost and latency.
- Decision: Render PDF pages to images locally, then pass page images to the existing Azure OpenAI deployment through a new vision-capable LLM helper.
  - Alternatives considered: external OCR services or local Tesseract; rejected to avoid a second OCR vendor and to stay aligned with the existing GPT stack.
- Decision: Archive only successful local inbox files to `data/inbox_done/`.
  - Alternatives considered: move all attempted files or introduce `data/inbox_failed/`; rejected to keep failures visible in the original inbox.
- Decision: Preserve filenames when moving to `data/inbox_done/`, but add a collision suffix if a name already exists there.

## Risks / Trade-offs
- OCR fallback increases token usage and runtime for scanned PDFs.
  - Mitigation: invoke only on weak/empty extraction and limit OCR to page text extraction, not summarization.
- PDF rendering introduces a local dependency on a page-to-image toolchain.
  - Mitigation: fail cleanly back to current `needs_review` behavior if rendering is unavailable.
- Large PDFs may produce very large OCR prompts.
  - Mitigation: process per page and concatenate page text rather than sending the whole PDF as one request.

## Migration Plan
1. Introduce a spec and tests for OCR fallback and inbox archiving.
2. Add the OCR helper and PDF page rendering pipeline behind fallback conditions.
3. Update `process_stream.py` to move successful local inbox files into `data/inbox_done/`.
4. Validate text-PDF, scanned/weak-PDF, and failed-processing paths.

## Open Questions
- The weak-text threshold will start as a simple character-count heuristic unless implementation shows a stronger signal is needed.
