# LAAI Corpus Candidates

## 1. _archives/articles/Knowledge Unit Specification

- **Path:** /Users/khabaroff/DEV/LAAI/_archives/articles/2026-04-12 — Knowledge Unit Specification.md
- **Source type:** article
- **Why useful:** Core LAAI design doc about knowledge unit schema — tests ingest of structured technical prose with specification language, lists, and embedded references.
- **Risk notes:** Long filename with em-dash spaces; may need careful shell quoting.

## 2. llm/token_counter.py

- **Path:** /Users/khabaroff/DEV/LAAI/llm/token_counter.py
- **Source type:** reference
- **Why useful:** Self-contained 200-line Python module with docstrings, provider-agnostic token counting, and LLM cost estimation. Good test for how the pipeline handles code-as-reference (docstring extraction for body).
- **Risk notes:** Python source, not markdown — pipeline needs to handle code files gracefully.

## 3. _archives/articles/The Wiki That Thinks

- **Path:** /Users/khabaroff/DEV/LAAI/_archives/articles/2026-04-12 — The Wiki That Thinks_ Ingest, Lint, and the Question of What Knowledge Is For.md
- **Source type:** article
- **Why useful:** Philosophical/technical essay about self-maintaining knowledge bases. Tests LLM analysis of nuanced, mixed-genre content with both technical and reflective prose.
- **Risk notes:** Long title, may need truncation or special character handling in output filename.