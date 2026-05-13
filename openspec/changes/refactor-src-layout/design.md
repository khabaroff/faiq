## Context
The repository root is named `guides`, and the Python package is also named `guides`. That produces a redundant `guides/guides` path, which is confusing and makes future structural changes harder.

## Goals / Non-Goals
- Goals: remove the duplicated path shape; keep the `guides` package name; preserve runtime behavior.
- Non-Goals: rename the product/package; change pipeline logic; redesign wiki/storage behavior.

## Decisions
- Decision: use a standard `src/` layout with `src/guides/...`.
- Decision: keep the import namespace as `guides`.
- Decision: migrate docs and tests in the same change to avoid half-switched paths.

## Risks / Trade-offs
- Risk: import path regressions in tests or scripts.
  - Mitigation: add/adjust packaging config and run the full test suite.
- Risk: temporary confusion while both old and new paths are referenced in docs.
  - Mitigation: update docs in the same change and keep migration scoped.

## Migration Plan
1. Move package files under `src/guides/`.
2. Update test/import configuration.
3. Fix entrypoints and docs.
4. Run tests and verify the pipeline still works.

