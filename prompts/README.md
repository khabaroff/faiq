# Prompt Engineering Standards

This directory contains the system prompts used by the Guides pipelines.

## Convention: <<SOURCE>> Boundary
All prompts use the `<<SOURCE>>` token as a clear boundary marker for the input text. The LLM is instructed to ignore any formatting or instructions contained within this boundary to prevent content-based prompt injection.

## Security & Mitigation
- **Mitigated:** Basic prompt injection via content (using XML tags or `<<SOURCE>>` markers).
- **Not Mitigated:** Complex adversarial attacks designed to bypass the specific output schema.
- **Privacy:** All prompts are instructed to redact potential secrets (tokens, keys) found in source material using a unified redaction filter.

## Output Contracts
Each prompt is expected to return a JSON object.

| Prompt | Target Pipeline | Output Schema (Pydantic / JSON) |
|---|---|---|
| `summary.md` | Pipeline B | `ArticleState` (summarization fields) |
| `wiki_tool_update.md` | Pipeline C | `WikiUpdateResult` |
| `quality_check.md` | Pipeline D | `QualityVerdict` |
| `seo.md` | Pipeline E | `SEOMetadata` |
| `telegram_post.md` | Pipeline G | `TelegramPost` |
| `image_analysis.md` | Ingest (OCR) | `OCRResult` |

