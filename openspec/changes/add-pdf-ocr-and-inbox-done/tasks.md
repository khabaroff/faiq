## 1. Implementation
- [x] 1.1 Add spec coverage for PDF OCR fallback and successful inbox file archiving.
- [x] 1.2 Add failing tests for weak-PDF fallback to OCR and for moving successful inbox files into `data/inbox_done/`.
- [x] 1.3 Add a vision-capable LLM helper for GPT OCR requests and wire usage accounting/tracing through it.
- [x] 1.4 Update PDF fetching to use `pdftotext` first and OCR-rendered pages only on weak extraction.
- [x] 1.5 Update `process_stream.py` and queue helpers to archive successful local inbox files into `data/inbox_done/` with collision-safe naming.
- [x] 1.6 Verify text-PDF success, OCR fallback success, and failed-processing non-archive behavior.
