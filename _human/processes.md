# Процессы и роботы

## Общая картина

```mermaid
flowchart TD
    HUM([👤 Человек]) -->|кидает URL / файл / pdf / youtube| INBOX[data/inbox/]

    INBOX --> ROBOT_A

    subgraph ROBOT_A["🤖 Robot A — Fetcher+Formatter"]
        A1[определить тип]
        A2[скачать текст]
        A3[OCR картинок]
        A4[добавить YAML]
        A1 --> A2 --> A3 --> A4
    end

    ROBOT_A -->|public/sources/<slug>.md| SOURCES[(public/sources/)]
    INBOX -->|done/| DONE[data/inbox/done/]

    SOURCES --> ROBOT_B

    subgraph ROBOT_B["🤖 Robot B — Summarizer"]
        B1[прочитать source]
        B2[LLM → саммари RU]
        B3[извлечь tools + patterns]
        B1 --> B2 --> B3
    end

    ROBOT_B -->|public/summaries/<slug>.md| SUMMARIES[(public/summaries/)]

    SUMMARIES --> ROBOT_C

    subgraph ROBOT_C["🤖 Robot C — WikiBot"]
        C1[достать tools_mentioned из JSON]
        C2[LLM: канонизировать slug]
        C3{страница есть?}
        C4[create]
        C5[append_mention]
        C6[rewrite_description]
        C1 --> C2 --> C3
        C3 -->|нет| C4
        C3 -->|да, описание ок| C5
        C3 -->|да, новый взгляд| C6
    end

    ROBOT_C -->|public/tools/<tool>.md| TOOLS[(public/tools/)]
    ROBOT_C -->|public/patterns/<tech>.md| TECH[(public/patterns/)]

    TOOLS --> ROBOT_D
    TECH --> ROBOT_D
    SUMMARIES --> ROBOT_D

    subgraph ROBOT_D["🤖 Robot D — QualityBot"]
        D1[проверить цитаты vs исходник]
        D2[найти дубли упоминаний]
        D3[починить или пометить]
    end

    ROBOT_D -->|✅ ok / 🔧 cleaned| TOOLS
    ROBOT_D -->|✅ ok / ♻️ needs_resummarize| SUMMARIES

    SUMMARIES --> ROBOT_E

    subgraph ROBOT_E["🤖 Robot E — SEO Optimizer"]
        E1[прочитать summary]
        E2[LLM → seo_title + seo_description]
        E3[обновить frontmatter]
        E1 --> E2 --> E3
    end

    ROBOT_E -->|public/summaries/<slug>.md| SUMMARIES

    SUMMARIES --> ROBOT_G
    TOOLS --> ROBOT_G
    TECH --> ROBOT_G

    subgraph ROBOT_G["🤖 Robot G — Telegram Publisher"]
        G1[следить за новыми summaries]
        G2[LLM → пост для канала]
        G3[отправить в Telegram]
        G1 --> G2 --> G3
    end

    ROBOT_G -->|published_telegram| SUMMARIES

    TOOLS --> PUB
    TECH --> PUB
    SUMMARIES --> PUB
    SOURCES --> PUB

    subgraph PUB["📖 Публикация"]
        OBS[Obsidian Vault]
        QUARTZ[Quartz → HTML сайт]
    end
```

---

## Роботы

### Robot A — Fetcher+Formatter

**Запуск:** `python -m guides.pipelines.a_ingest`
**Триггер:** новые файлы в `data/inbox/`
**Идемпотентен:** да (пропускает если `state[slug].raw == true`)

| Тип входа | Как скачивает | Модель |
|---|---|---|
| URL статья | defuddle-cli → cloudflare-markdown → jina | не нужна |
| `.md` файл | читает напрямую | не нужна |
| `.pdf` файл | pdftotext → LLM OCR fallback | **gpt-5.4** (только OCR) |
| YouTube URL | yt-dlp субтитры → khabaroff.studio API | не нужна |
| GitHub repo | GitHub API → README | не нужна |
| GitHub gist | GitHub API → jina fallback | не нужна |

OCR картинок внутри статьи: **gpt-5.4-mini** (дёшево, per-image, с SQLite-кешем).

---

### Robot B — Summarizer

**Запуск:** `python -m guides.pipelines.b_summarize`
**Триггер:** новые файлы в `public/sources/`
**Идемпотентен:** да (пропускает если `public/summaries/<slug>.md` существует)

Промпт: `prompts/summary.md`

**Модель по размеру:**
- статья < 15K токенов → **gpt-5.4-mini** ($0.01-0.03)
- статья ≥ 15K токенов → **gpt-5.4** (длинный контекст, точнее)

**Retry:** до 3 попыток если LLM не вернул корректный frontmatter. При финальном сбое — `quality: needs_review`.

Выход — markdown с YAML frontmatter:
```yaml
---
slug: article-slug
source_url: https://...
source_type: article
summarized_at: 2026-05-13
tools: [Claude Code, LangChain]
patterns: [Context Engineering, ReAct]
key_claims:
  - тезис 1
lecture_hooks:
  - вопрос для аудитории
---
```

Тело использует `[[Claude Code]]` и `[[Context Engineering]]` как wikilinks.

---

### Robot C — WikiBot

**Запуск:** `python -m guides.pipelines.c_wiki_update`
**Триггер:** новые файлы в `public/summaries/`
**Идемпотентен:** да (`state[slug].wiki_propagated`)

Промпт: `prompts/wiki_tool_update.md`
**Модель:** всегда **gpt-5.4-mini** (короткие запросы, дедуп по семантике)

Вход: `tools` и `patterns` списки из frontmatter саммари (plain names, не JSON-блок).

Три режима:
- `create` — новая страница инструмента/паттерна
- `append_mention` — добавить упоминание
- `rewrite_description` — переписать «Что это» если новый взгляд

Саммари с `quality: needs_review` обрабатываются как обычно, просто tools/patterns будут пустыми.

---

### Robot D — QualityBot

**Запуск:** `python -m guides.pipelines.d_quality_check`
**Триггер:** периодически (не блокирует A/B/C)
**Модель:** всегда **gpt-5.4-mini** (дёшево)

Два режима:
- `summary_check` — проверяет цитаты в исходнике, ловит галлюцинации
- `wiki_clean` — дедуп упоминаний, противоречия в описаниях

---

### Robot E — SEO Optimizer

**Запуск:** `python -m guides.pipelines.e_seo`
**Триггер:** новые файлы в `public/summaries/`
**Идемпотентен:** да (`state[slug].seo_optimized`)

**Модель:** gpt-5.4-mini
**Промпт:** `prompts/seo.md`

Генерирует SEO-поля для frontmatter саммари: `seo_title` (≤60 символов), `seo_description` (≤160 символов), `og_description`. Используется Quartz/Astro для `<head>` мета-тегов.

---

### Robot G — Telegram Publisher

**Запуск:** `python -m guides.pipelines.g_telegram`
**Триггер:** новые файлы в `public/summaries/` без `published_telegram`
**Идемпотентен:** да (`state[slug].published_telegram`)

**Промпт:** `prompts/telegram_post.md`
**Config:** `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHANNEL_ID` в `.env`

Постит одну статью за раз в канал: bold заголовок + tldr + 2-3 тезиса + ссылки. Ставит `state[slug].published_telegram = ISO date`. `--dry-run` для превью без публикации.

---

## State Machine (guides-y7n)

Сейчас: `state/index.json` — плоский JSON.
Будущее: SQLite `state/articles.db`, таблица `articles`:

| Поле | Тип | Смысл |
|---|---|---|
| slug | TEXT PK | идентификатор |
| raw | INTEGER | Pipeline A выполнен |
| summarized_at | TEXT | дата Pipeline B |
| wiki_propagated | INTEGER | Pipeline C выполнен |
| seo_optimized | INTEGER | Pipeline E выполнен |
| published_telegram | TEXT | дата публикации |
| quality | TEXT | ok / needs_review |

Позволяет запросы типа: `SELECT slug WHERE seo_optimized=0 AND quality='ok'`.

---

## Модели и стоимость

| Задача | Модель | Цена за единицу |
|---|---|---|
| OCR картинки (vision) | gpt-5.4-mini | ~$0.005 |
| OCR PDF страницы | gpt-5.4 | ~$0.02 |
| Саммари < 15K токенов | gpt-5.4-mini | ~$0.01-0.03 |
| Саммари ≥ 15K токенов | gpt-5.4 | ~$0.05-0.15 |
| WikiBot update | gpt-5.4-mini | ~$0.003 |
| QualityBot check | gpt-5.4-mini | ~$0.005 |

---

## Крон-расписание (TODO: настроить)

```
# каждые 15 минут — полный цикл
*/15 * * * * cd /path/to/guides && python -m guides.pipelines.run_all >> logs/cron.log 2>&1
```

Или через Codex CLI:
```bash
codex run "python -m guides.pipelines.run_all"
```

---

## Перекрёстные ссылки

Страница инструмента ссылается на все саммари где упоминается:
```markdown
## Упоминания
- [Karpathy Second Brain](../../summaries/karpathy-second-brain.md) — "цитата"
- [Building Effective AI Agents](../../summaries/building-effective-ai-agents.md) — "цитата"
```

Саммари ссылается обратно на source:
```markdown
source: [оригинал](../../sources/karpathy-second-brain.md)
```

Всё внутри `public/` — относительные ссылки. Obsidian их видит как граф.

---

## YouTube — два способа

1. **yt-dlp** — скачивает `.vtt` субтитры локально (en → ru → all)
2. **khabaroff.studio API** — fallback если yt-dlp не справился:
   `GET https://youtubetranscribe.khabaroff.studio/?url=<youtube_url>`
   (TODO: уточнить endpoint из /docs)