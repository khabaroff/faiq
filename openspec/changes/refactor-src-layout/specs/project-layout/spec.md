## MODIFIED Requirements

### Requirement: Repository layout uses a `src/` package root
The repository SHALL store the Python package under `src/guides/` instead of `guides/guides/`.

#### Scenario: Developer opens the repo
- **WHEN** a developer inspects the repository tree
- **THEN** the Python package is under `src/guides/`
- **AND** the package import name remains `guides`
- **AND** the duplicated `guides/guides` path no longer exists.

### Requirement: Existing pipeline behavior is preserved
The layout change SHALL not alter pipeline outputs, wiki generation, or runtime behavior.

#### Scenario: Running the pipeline after migration
- **WHEN** the developer runs the existing entrypoint from the repository root
- **THEN** the pipeline still processes inputs successfully
- **AND** the generated wiki and data artifacts follow the same contracts as before the layout change.

