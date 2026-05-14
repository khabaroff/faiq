# ADR-002: Pipeline D (QualityBot) Idempotency

## Background
Pipeline D (QualityBot) was re-running on every execution because it didn't track the state of the content it had already checked. This led to redundant LLM calls and increased cost.

## Proposal
Implement idempotency for Pipeline D using a `qc_hash` field in the SQLite state.

## Rationale
- **Cost Efficiency:** Only re-run QualityBot if the source text or the summary has changed.
- **Performance:** Skip already-verified slugs during batch runs.
