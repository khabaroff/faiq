# Change: Refactor guides to a `src/` layout

## Why
The repository currently has a duplicated shape (`guides/guides/...`) because the repo root and the Python package share the same name. This is confusing, harder to navigate, and makes the project look larger and flatter than it is. Moving the package under `src/` keeps the package name stable while making the repository structure clearer.

## What Changes
- Move the Python package from `guides/guides/` to `src/guides/`.
- Keep the package import name `guides` unchanged.
- Update test and runtime imports so the project still runs from the repository root.
- Update developer docs and examples to reflect the new layout.
- Keep pipeline behavior and wiki outputs unchanged.

## Impact
- Affected code: package imports, entrypoints, tests, packaging/tooling.
- Affected docs: repository layout docs and any setup instructions.
- Affected behavior: none intended beyond path/layout changes.

