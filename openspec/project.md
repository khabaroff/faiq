# Project Context

## Purpose

Guides — система подготовки лекционного материала по AI-инструментам. Берёт статьи, видео, PDF, репозитории → делает структурированные русскоязычные саммари → строит wiki-граф инструментов и паттернов → публикует как статический сайт (Quartz) и в Telegram.

Целевой пользователь: преподаватель / исследователь AI (Сергей Хабаров), который собирает корпус знаний об AI-агентах, context engineering, LLM-паттернах для лекций в ИИЧАВО.

## Tech Stack

- Python 3.12, `uv` для пакетов
- `src/` layout: `src/guides/`
- Azure OpenAI: gpt-5.4-mini (fast), gpt-5.4 (smart)
- pyyaml 6.0 для frontmatter
- httpx, defuddle-cli, yt-dlp для фетчинга
- Obsidian + Quartz для публикации

## Pipeline Architecture

```
data/inbox/ → Pipeline A → public/sources/*.md
                          → Pipeline B → public/summaries/*.md
                                       → Pipeline C → public/tools/*.md
                                                     public/techniques/*.md
                                                   → Pipeline D (QualityBot)
                                                   → Pipeline E (SEO Optimizer)
                                                   → Pipeline G (Telegram Publisher)
```

Состояние: `state/articles.db` — SQLite, таблица `articles`.

### Таблица `articles` (SQLite Schema)

| Колонка | Тип | Описание |
|---|---|---|
| `slug` | TEXT | PRIMARY KEY. Human-readable ID (slug). |
| `raw` | INTEGER | 0/1. Обработан ли фетчером (Pipeline A). |
| `content_hash` | TEXT | SHA256 исходного контента. |
| `summarized_at` | TEXT | Дата саммаризации (Pipeline B). |
| `wiki_propagated` | INTEGER | 0/1. Обновлена ли wiki (Pipeline C). |
| `wiki_propagated_at` | TEXT | Дата обновления wiki. |
| `seo_optimized` | INTEGER | 0/1. Проведен ли SEO-анализ (Pipeline E). |
| `published_telegram` | TEXT | Дата публикации в TG канал (Pipeline G). |
| `quality` | TEXT | Вердикт QualityBot (Pipeline D). |
| `quality_checked` | INTEGER | 0/1. Пройден ли контроль качества. |
| `qc_hash` | TEXT | Хэш контента при последнем QC. |
| `status` | TEXT | Статус ворклоу (\`draft\`, \`verified\`, \`quality_ok\`, и т.д.). |
| `revision_count` | INTEGER | Количество итераций обработки. |
| `last_edited_at` | TEXT | ISO timestamp последнего изменения. |
| `last_edited_by` | TEXT | Кто изменил (user/bot). |
| `compacted` | INTEGER | 0/1. Признак агрегации в лонгрид. |

### Формат public/sources/*.md

```yaml
---
title: ...
slug: ...
source_url: https://...
source_type: article | youtube | pdf | repo | gist
fetched_at: YYYY-MM-DD
lang: en | ru
---
```

### Формат public/summaries/*.md

```yaml
---
slug: ...
source_url: https://...
source_type: article
summarized_at: YYYY-MM-DD
tools: [Claude Code, LangChain]
patterns: [Context Engineering, ReAct]
key_claims:
  - тезис 1
lecture_hooks:
  - вопрос для аудитории
quality: ok | needs_review   # needs_review = LLM не справился 3x
# После Pipeline E:
seo_title: "..."          # ≤60 символов
seo_description: "..."    # ≤160 символов
og_description: "..."
# После Pipeline G:
published_telegram: "2026-05-13T14:00:00"
---
```

Тело — 9 секций, технические названия в оригинале (без транслитерации), `[[Tool Name]]` wikilinks.

### Формат public/tools/*.md и public/techniques/*.md (frontmatter `type: pattern`)

```yaml
---
name: Claude Code
slug: claude-code
type: tool | pattern
url: https://...
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
---
```

## Project Conventions

### Code Style

- Python, type hints, `from __future__ import annotations`
- Все CLI-точки входа через `if __name__ == "__main__": sys.exit(main())`
- Логи через `logging`, не `print` (в pipeline-коде)
- `print()` допустим в CLI-инструментах (tools/)
- Нет `TODO`/`FIXME` в коде — для этого есть beads-задачи

### Architecture Patterns

- Идемпотентность: каждый пайплайн проверяет state перед обработкой
- Retry: до 3 попыток на LLM-вызов с correction prompt при сбое формата
- Fallback-цепочки: defuddle → cloudflare-markdown → jina (для URL)
- Slug-based identity: `slug = slugify(title)[:80]` — уникальный ID артикула

### Testing Strategy

- pytest в `tests/`
- Юнит-тесты для парсеров, slugify, extract_summary_fm
- Интеграционные тесты по возможности используют реальный LLM (не mock)
- Запуск: `python -m pytest tests/`

### Git Workflow

- Ветка `main`, коммиты напрямую
- Conventional commits: `fix:`, `feat:`, `refactor:`, `docs:`, `chore:`
- После каждой рабочей сессии: `git push`

## Domain Context

Контент: статьи/доклады/видео про AI-агентов, LLM-паттерны, context engineering, prompt engineering, инструменты (Claude Code, Cursor, LangGraph и т.д.).

Саммари пишутся **по-русски** для русскоязычных лекций. Технические названия инструментов и паттернов — в оригинале (не "Клод Код", а "Claude Code"). Транслитерация запрещена.

Obsidian vault = `public/`. Относительные ссылки работают в Obsidian-граф и в Quartz-сайте.

## Important Constraints

- `public/` = одновременно Obsidian vault + Quartz publish folder
- `state/articles.db` — не трогать руками, только пайплайны
- `data/inbox/done/` — архив, не удалять
- Azure OpenAI — не менять routing-логику без обсуждения (стоимость)
- Вся пользовательская документация — в `_human/`, не в `docs/`

## External Dependencies

- Azure OpenAI API (`AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_DEPLOYMENT_FAST`, `AZURE_DEPLOYMENT_SMART`)
- Jina Reader API (`JINA_API_KEY` — опционально, без него медленнее)
- GitHub API (`GITHUB_TOKEN` — опционально, для приватных репо)
- Telegram Bot API (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHANNEL_ID` — для Pipeline G)
- `defuddle-cli` (npm) — для чистки статей
- `yt-dlp` (pip) — для YouTube субтитров
- `pdftotext` (poppler) — для PDF