# Design: QualityCheck Idempotency

## Data Schema
- Add `qc_hash` column to `articles` table (SQLite).
- Add `quality_checked` (bool) flag.

## Implementation Details
- **Hash calculation:** `qc_hash = sha256(source_text + summary_text)`.
- **Logic:**
  1. Load `ArticleState` from DB.
  2. If `quality_checked` is true AND `stored.qc_hash == current_qc_hash`, skip.
  3. Otherwise, run LLM check and update `qc_hash` and `quality_checked`.
