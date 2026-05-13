## ADDED Requirements

### Requirement: PDF ingestion falls back to OCR when text extraction is weak
The system SHALL attempt PDF ingestion with local text extraction first and SHALL invoke GPT-based OCR only when the extracted text is empty or too weak to process reliably.

#### Scenario: Text PDF succeeds without OCR
- **WHEN** a PDF in `data/inbox/` yields sufficient text through the primary extractor
- **THEN** the pipeline uses that extracted text
- **AND** GPT OCR is not invoked.

#### Scenario: Scanned PDF falls back to OCR
- **WHEN** a PDF in `data/inbox/` yields empty or weak text through the primary extractor
- **THEN** the pipeline renders page images and runs GPT-based OCR
- **AND** the OCR text is used as the fetched content if OCR succeeds.

#### Scenario: OCR fallback also fails
- **WHEN** both the primary extractor and OCR fallback fail to produce usable text
- **THEN** the pipeline returns `needs_review`
- **AND** the result includes a PDF extraction failure signal instead of crashing the run.

### Requirement: Successful local inbox files are archived out of the active inbox
The system SHALL move successfully processed local files from `data/inbox/` into `data/inbox_done/`.

#### Scenario: Local inbox file finishes successfully
- **WHEN** a file-based item from `data/inbox/` completes with a non-`failed` pipeline status
- **THEN** the source file is moved into `data/inbox_done/`
- **AND** the active `data/inbox/` no longer contains that file.

#### Scenario: Local inbox file processing fails
- **WHEN** a file-based item from `data/inbox/` completes with `failed`
- **THEN** the source file remains in `data/inbox/`
- **AND** the failure is still recorded in the review/quarantine flow.

#### Scenario: Archived filename already exists
- **WHEN** a successful local inbox file is moved to `data/inbox_done/` and a file with the same name already exists there
- **THEN** the system preserves both files by writing the new archive entry with a collision-safe suffix.
