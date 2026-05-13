# Как работает система

## TL;DR

Ты кидаешь материал в `data/inbox/` → крон запускает пайплайны → результат лежит в `public/` → читаешь в Obsidian, публикуешь через Quartz.

---

## Папки

```
data/inbox/          ← СЮДА КЛАСТЬ всё входящее
  _assets/           ← (авто) скачанные картинки для OCR
  done/              ← (авто) обработанные файлы переезжают сюда

public/             ← ПАБЛИК-ПАПКА (Quartz публикует как сайт)
  sources/           ← чистые отформатированные исходники
  summaries/         ← RU саммари по каждому исходнику
  tools/             ← страницы инструментов (Claude Code, Obsidian...)
  techniques/        ← страницы паттернов и подходов (frontmatter type: pattern)

prompts/             ← промпты (можешь редактировать)
state/articles.db    ← SQLite — что обработано (не трогать руками)
logs/YYYY-MM-DD.md   ← дневной лог: что появилось и сколько стоило
```

---

## Что класть в inbox

### Статья по URL (один)

Создай файл `.txt` или `.md` с одним URL:
```
https://habr.com/ru/articles/12345/
```

### Несколько URL сразу

`.txt` или `.md` файл где каждая строка — один URL (никакого другого текста):
```
https://habr.com/ru/articles/12345/
https://openai.com/blog/gpt-5
https://www.youtube.com/watch?v=xxxxx
```
Система создаст отдельный `public/sources/` файл для каждого URL. Исходный файл-список переедет в `done/` после обработки.

Или добавь URL прямо в `data/queue/inbox.txt` (по одной строке).

### Статья уже скачана (markdown-файл)

Просто брось `.md`-файл в `data/inbox/`. Система определит что это уже текст и не будет качать повторно.

### YouTube видео

```
https://www.youtube.com/watch?v=xxxxx
```
Система скачает субтитры через `yt-dlp` (ru/en автоматически).

### PDF файл

Брось `.pdf` в `data/inbox/`. Система извлечёт текст через `pdftotext`, при необходимости — OCR через gpt-5.4 vision.

### Репозиторий GitHub

```
https://github.com/owner/repo
```
Система скачает README + metadata (звёзды, язык, описание).

---

## Что НЕ нужно делать

- Не чистить `data/inbox/done/` — это архив, пусть лежит
- Не трогать `state/articles.db` — пайплайны сами отслеживают что обработано
- Не редактировать `public/sources/` вручную — перезапишется при reingest

---

## Как запускать

Крон на сервере запускает автоматически. Вручную:

```bash
# Всё сразу (A → B → C → D → E → G)
python -m guides.pipelines.run_all

# Только скачать + отформатировать
python -m guides.pipelines.a_ingest

# Только саммари (для ещё не суммированных)
python -m guides.pipelines.b_summarize

# Только обновить страницы инструментов/техник
python -m guides.pipelines.c_wiki_update

# Проверка качества (дешёвая модель)
python -m guides.pipelines.d_quality_check

# SEO-оптимизация (добавляет seo_title, seo_description, og_description)
python -m guides.pipelines.e_seo

# Публикация в Telegram-канал
python -m guides.pipelines.g_telegram
```

Для запуска нужны переменные окружения из `.env` (Azure OpenAI, Telegram и т.д.).

---

## Что получается

### `public/sources/<slug>.md`

Чистый markdown с YAML-шапкой:
```yaml
---
title: Building Effective AI Agents
slug: building-effective-ai-agents-8b3f
source_url: https://...
source_type: article
fetched_at: 2026-05-13
lang: en
---
```
Картинки внутри статьи — описаны через OCR (`<!-- OCR: описание изображения -->`).

### `public/summaries/<slug>.md`

YAML-шапка + тело на русском:
```yaml
---
slug: building-effective-ai-agents
source_url: https://...
source_type: article
summarized_at: 2026-05-13
tools: [Claude Code, LangChain]
patterns: [Context Engineering, ReAct]
key_claims:
  - главный тезис 1
lecture_hooks:
  - провокационный вопрос для аудитории
---
```

Тело — 9 секций (Идеи / Тезисы / Цитаты / Факты / Рекомендации / Метафоры / Q&A / Упоминания / Для лекции). Инструменты и паттерны упоминаются как `[[Claude Code]]` — Obsidian строит граф автоматически.

Если LLM трижды не смог дать правильный формат — в шапке появится `quality: needs_review`. Пайплайн C всё равно обработает, просто tools/patterns будут пустыми.

После прогона через Pipeline E добавляются SEO-поля:
```yaml
seo_title: "Строим агентов на Claude Code — паттерны и инструменты"
seo_description: "Разбор Context Engineering, ReAct и практик построения AI-агентов. 22 конкретных тезиса."
og_description: "Саммари статьи Anthropic про паттерны агентов."
```

После публикации в Telegram:
```yaml
published_telegram: "2026-05-13T14:00:00"
```

### `public/tools/claude-code.md`

Страница инструмента. Каждый раз когда инструмент упоминается в новом саммари — LLM решает: добавить упоминание или переписать описание.

```
## Что это
Краткое описание из всех источников.

## Упоминания
- [статья 1](../../summaries/...) — "цитата"
- [статья 2](../../summaries/...) — "цитата"
```

---

## Obsidian

Открой `public/` как Vault в Obsidian. Ссылки между страницами работают (относительные пути). Поиск по всему корпусу.

---

## Публикация через Quartz

`public/` = папка которую Quartz публикует как статический сайт.
Конфиг Quartz смотри в `_human/quartz-setup.md` (TODO: создать).

---

## Стоимость

```bash
# Посмотреть расход за день
cat logs/$(date +%Y-%m-%d).md

# Детальный отчёт по моделям
python -m guides.tools.cost_report
```

Ориентиры (Azure mini / gpt-5.4):
- Саммари статьи ~10-20K знаков: $0.01-0.03
- OCR одной картинки: $0.005
- Обновление tool-страницы: $0.005