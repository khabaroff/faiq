# SQLite State Migrations

## Initial Schema
Table `articles` created with basic fields: `slug`, `raw`, `summarized_at`, `wiki_propagated`, `wiki_propagated_at`, `seo_optimized`, `published_telegram`, `quality`.

## Migration: Auto-ALTER from ArticleState
The system now automatically adds missing columns from `ArticleState` Pydantic model in `src/guides/models.py`.

### Added columns:
- `content_hash` (TEXT): SHA256 of source content.
- `quality_checked` (INTEGER): 0/1 flag from Pipeline D.
- `qc_hash` (TEXT): Content hash used for last quality check.
- `status` (TEXT): current workflow status (`draft`, `verified`, `quality_ok`, etc).
- `revision_count` (INTEGER): number of LLM iterations.
- `last_edited_at` (TEXT): ISO timestamp of last change.
- `last_edited_by` (TEXT): Actor who made the change.
- `compacted` (INTEGER): 0/1 flag for long-form aggregation.
