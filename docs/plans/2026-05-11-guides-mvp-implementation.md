# Guides MVP Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Собрать минимальный рабочий pipeline для `guides/`, который принимает URL и локальные файлы, строит `article.md` или `reference.md` и сохраняет результат в canonical storage.

**Architecture:** Один Python pipeline с тремя source type: `ARTICLE`, `YOUTUBE`, `GITHUB_REPO`. Один cron entrypoint `process_stream.py` читает `data/queue/inbox.txt` и `data/inbox/`, дальше запускает `detect -> fetch -> process -> tags -> verify -> store`. Промпты лежат отдельно в `guides/prompts/*.md`.

**Tech Stack:** Python, `openai` Azure SDK, `yt-dlp`, `defuddle-cli`, GitHub API, markdown files, cron.

---

### Task 1: Project skeleton

**Files:**
- Create: `pyproject.toml`
- Create: `.env.example`
- Create: `guides/__init__.py`
- Create: `guides/settings.py`

**Step 1: Create package and config files**

Add the base project files and package directory.

**Step 2: Define settings**

Add config for:
- Azure endpoint / key / deployments
- `GITHUB_TOKEN`
- data paths
- prompt directory path

**Step 3: Verify config import**

Run: `uv run python -c "from guides.settings import Settings; print('ok')"`
Expected: `ok`

**Step 4: Commit**

```bash
git add pyproject.toml .env.example guides/__init__.py guides/settings.py
git commit -m "feat: add guides project skeleton"
```

### Task 2: LLM and prompt loading

**Files:**
- Create: `guides/llm.py`
- Create: `guides/prompts/article_rewrite.md`
- Create: `guides/prompts/youtube_summary.md`
- Create: `guides/prompts/github_reference.md`
- Create: `guides/prompts/tags_extract.md`
- Create: `guides/prompts/verify_check.md`

**Step 1: Add prompt files**

Create one markdown prompt file per processor.

**Step 2: Add LLM client factory**

Implement cached Azure clients for `smart` and `fast`.

**Step 3: Add prompt loader**

Expose helper to load prompt text by filename.

**Step 4: Verify prompt loading**

Run: `uv run python -c "from guides.llm import load_prompt; print(bool(load_prompt('article_rewrite.md')))"`  
Expected: `True`

**Step 5: Commit**

```bash
git add guides/llm.py guides/prompts
git commit -m "feat: add llm clients and prompt files"
```

### Task 3: Queue and storage

**Files:**
- Create: `guides/queue.py`
- Create: `guides/vault.py`
- Create: `data/queue/inbox.txt`
- Create: `data/inbox/.gitkeep`
- Create: `data/logs/.gitkeep`
- Create: `data/sources/.gitkeep`

**Step 1: Implement queue reader**

Support:
- reading pending lines from `data/queue/inbox.txt`
- marking consumed items
- skipping empty and duplicate lines

**Step 2: Implement canonical storage**

Write helper that creates:

```text
data/sources/YYYY-MM-DD_{hash8}/
├── source.md
├── article.md | reference.md
├── meta.json
└── images/
```

**Step 3: Verify storage write**

Run a small script that writes a fake source and output.
Expected: a new directory under `data/sources/`

**Step 4: Commit**

```bash
git add guides/queue.py guides/vault.py data
git commit -m "feat: add queue and canonical storage"
```

### Task 4: Source detection and shared models

**Files:**
- Create: `guides/fetch/base.py`

**Step 1: Define shared types**

Add:
- `SourceType`
- `QueueItem`
- `FetchedContent`

**Step 2: Implement source detection**

Support detection for:
- article URL
- YouTube URL
- GitHub repo URL
- local `.md` / `.txt` / `.pdf`

**Step 3: Verify detection**

Run a few direct calls in `python -c`.
Expected: each sample maps to the right `SourceType`

**Step 4: Commit**

```bash
git add guides/fetch/base.py
git commit -m "feat: add source detection models"
```

### Task 5: URL fetcher

**Files:**
- Create: `guides/fetch/url.py`

**Step 1: Implement article fetch**

Primary:
- `defuddle-cli`

Fallback:
- HTTP request with `Accept: text/markdown`

**Step 2: Return normalized `FetchedContent`**

Populate:
- `raw_text`
- `source_meta`
- `attachments`

**Step 3: Verify on one real URL**

Run the fetcher on a known article.
Expected: non-empty markdown-like text

**Step 4: Commit**

```bash
git add guides/fetch/url.py
git commit -m "feat: add url fetcher"
```

### Task 6: YouTube and GitHub fetchers

**Files:**
- Create: `guides/fetch/youtube.py`
- Create: `guides/fetch/github.py`

**Step 1: Implement YouTube transcript fetch**

Primary:
- `yt-dlp --write-auto-sub --skip-download`

Fallback:
- `youtubetranscribe.khabaroff.studio`

**Step 2: Implement GitHub repo fetch**

Fetch:
- repo metadata
- README or raw repo intro content

**Step 3: Verify both fetchers**

Run one real YouTube URL and one real GitHub repo URL.
Expected: non-empty transcript / repo content

**Step 4: Commit**

```bash
git add guides/fetch/youtube.py guides/fetch/github.py
git commit -m "feat: add youtube and github fetchers"
```

### Task 7: Processors

**Files:**
- Create: `guides/process/article.py`
- Create: `guides/process/youtube.py`
- Create: `guides/process/reference.py`

**Step 1: Implement article rewrite processor**

Rules:
- keep code verbatim
- keep prompts verbatim
- compress prose carefully

**Step 2: Implement YouTube processor**

Support transcript chunking when needed.

**Step 3: Implement GitHub reference processor**

Output sections:
- what it is
- stack
- use cases
- key concepts
- quick start
- links

**Step 4: Verify each processor with fixture input**

Expected: markdown output with title and body

**Step 5: Commit**

```bash
git add guides/process
git commit -m "feat: add content processors"
```

### Task 8: Tags and verify

**Files:**
- Create: `guides/enrich/tags.py`
- Create: `guides/verify.py`

**Step 1: Implement tag extraction**

Return normalized JSON tag list.

**Step 2: Implement deterministic verify**

Checks:
- output exists
- title exists
- tags exist
- output not empty
- code blocks not dropped

**Step 3: Add retry policy**

Allow up to 3 verification/regeneration attempts.

**Step 4: Verify failure path**

Run one passing and one intentionally broken sample.
Expected: `verified` or `needs_review`

**Step 5: Commit**

```bash
git add guides/enrich/tags.py guides/verify.py
git commit -m "feat: add tags and verify pipeline"
```

### Task 9: Orchestrator

**Files:**
- Create: `guides/run.py`

**Step 1: Wire the full pipeline**

Pipeline flow:
- detect
- fetch
- process
- tag
- verify
- store

**Step 2: Add status handling**

Support:
- success
- failed
- needs_review

**Step 3: Verify end-to-end on three samples**

Samples:
- one article URL
- one YouTube URL
- one GitHub repo URL

Expected: output folders created under `data/sources/`

**Step 4: Commit**

```bash
git add guides/run.py
git commit -m "feat: add pipeline orchestrator"
```

### Task 10: Stream and cron entrypoint

**Files:**
- Create: `process_stream.py`
- Create: `cron/crontab.example`

**Step 1: Implement queue + inbox runner**

One launch should:
- read `data/queue/inbox.txt`
- scan `data/inbox/`
- pass items into `guides.run`
- write logs

**Step 2: Add cron example**

Use one cron entry.

**Step 3: Verify full stream run**

Run: `uv run python process_stream.py`
Expected: queue items processed and logs written

**Step 4: Commit**

```bash
git add process_stream.py cron/crontab.example
git commit -m "feat: add cron stream entrypoint"
```

### Task 11: VPS smoke test

**Files:**
- Modify: `.env.example`
- Modify: `docs/pipeline-plan_v2.md`

**Step 1: Install runtime dependencies on VPS**

Verify:
- Python / uv
- Node.js for `defuddle-cli`
- `yt-dlp`

**Step 2: Run one sample per source type**

Expected:
- folders created in `data/sources/`
- output markdown readable
- failures marked as `needs_review`

**Step 3: Document operational caveats**

Add short notes for:
- missing transcript
- GitHub rate limit
- fetch fallback behavior

**Step 4: Commit**

```bash
git add .env.example docs/pipeline-plan_v2.md
git commit -m "docs: add vps runtime notes"
```

## Output layout

Итоговые материалы будут лежать здесь:

```text
data/sources/YYYY-MM-DD_{hash8}/
├── source.md
├── article.md | reference.md
├── meta.json
└── images/
```

Где что:

- `source.md` — исходный материал в raw/normalized виде
- `article.md` — итоговая статья по статье, тексту, PDF или YouTube
- `reference.md` — итоговая справка по GitHub-репозиторию
- `meta.json` — метаданные, source URL/path, type, verify status, tags, timestamps
- `images/` — скачанные картинки, если нужны

Если нужен "человеческий" индекс позже, его можно добавить отдельным `v2`-слоем, но в MVP canonical truth живёт только в `data/sources/`.
