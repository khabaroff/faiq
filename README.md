# Guides — AI Lecture Prep System

Automatic ingestion of articles/videos/PDFs into Russian summaries, wiki-graph of tools, and Obsidian + Quartz site.

## Quick Start

```bash
# Install dependencies
uv sync

# Run full pipeline
python -m guides.pipelines.run_all

# Or step by step
python -m guides.pipelines.a_ingest
python -m guides.pipelines.b_summarize
python -m guides.pipelines.c_wiki_update
```

## Configuration

```bash
cp .env.example .env
# Edit .env with your keys
```

Secrets live in `.env` (never committed). See [Runbook: Secrets & Operations](_human/runbook.md) for rotation procedures.

## Secrets Rotation Procedure

| Secret | Rotate at | How |
|---|---|---|
| Azure OpenAI key | Azure Portal → Keys & Endpoints | every 90 days |
| Telegram bot token | @BotFather → /revoke | every 180 days |
| GitHub PAT | Settings → Developer settings → Tokens | every 90 days |
| Jina API key | https://jina.ai/keys | every 180 days |

Detailed steps (including rollback and test commands) are in `_human/runbook.md`.

## Project Structure

- `src/guides/` — Python code (pipelines, fetchers, tools)
- `prompts/` — LLM prompts
- `public/` — Obsidian vault output
- `data/inbox/` — drop articles here
- `state/` — SQLite database & reports

## Testing

```bash
python -m pytest tests/
```

## CI

GitHub Actions runs `gitleaks` secrets scan, `ruff` lint, and `pytest` on every PR.
