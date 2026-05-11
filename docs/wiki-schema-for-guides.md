# Wiki Schema for guides

Этот документ задаёт минимальную, но полезную схему для итоговых материалов `guides/`.

Цель:

- чтобы `article.md` и `reference.md` были не просто markdown-файлами;
- чтобы они были частью общей wiki;
- чтобы поверх них потом могли работать агенты: линтить, чистить, связывать, переписывать, строить синтез.

---

## Общая идея

У `guides/` должно быть два слоя:

### 1. Raw layer

Это сырой источник.

Файл:

- `source.md`

Свойства:

- immutable;
- хранит исходный материал как можно ближе к оригиналу;
- не переписывается после записи.

### 2. Wiki-ready layer

Это уже обработанный материал.

Файлы:

- `article.md`
- `reference.md`

Свойства:

- имеют frontmatter;
- имеют структурированное тело;
- пригодны для последующей автоматической чистки и связывания.

---

## Что не делать

Не надо в первой версии строить слишком тяжёлую ontology-систему с десятками page types.

Для `guides` сейчас достаточно:

- source page на один источник;
- reference page на один GitHub repo;
- метаданные, по которым потом можно выделить entities, concepts, topics и связи.

То есть сначала делаем сильные source pages, а не полноценный graph engine.

---

## Page types

Для первой версии достаточно двух итоговых типов страниц:

### `source-page`

Используется для:

- статьи
- поста
- YouTube-транскрипта
- PDF
- markdown/text note
- Telegram-derived content позже

Файл:

- `article.md`

### `reference-page`

Используется для:

- GitHub repo summary/reference

Файл:

- `reference.md`

---

## Frontmatter: обязательные поля

Вот минимальный frontmatter, который стоит считать обязательным для итоговых wiki-ready страниц.

```yaml
---
id: "src-2026-05-11-abcdefgh"
title: "Prompting best practices"
type: "source-page"
status: "active"
source_type: "article"
content_format: "text"
origin: "url"
created_at: "2026-05-11"
updated_at: "2026-05-11"
language: "en"
tags: ["prompting", "claude", "best-practices"]
topics: ["prompt-engineering"]
entities: ["Anthropic", "Claude"]
concepts: ["few-shot prompting", "xml tags"]
related: []
review_required: false
verified: true
quality_score: 0.82
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
source_paths:
  - "data/sources/2026-05-11_abcdefgh/source.md"
prompt_version: "article_rewrite@v1"
---
```

---

## Поля frontmatter — смысл

### `id`

Стабильный идентификатор страницы.

Формат для `guides`:

- `src-YYYY-MM-DD-hash8` для source page
- `ref-YYYY-MM-DD-hash8` для reference page

Нужен для:

- будущих `related` links
- индексации
- lint/check workflows

---

### `title`

Человеческий заголовок страницы.

Это не slug и не id.

---

### `type`

Тип wiki-ready страницы.

Допустимые значения:

- `source-page`
- `reference-page`

В будущем можно добавить:

- `entity-page`
- `concept-page`
- `synthesis-page`

Но не в первой версии.

---

### `status`

Состояние страницы.

Рекомендуемые значения:

- `active`
- `needs-review`
- `stale`
- `archived`

Смысл:

- `active` — материал нормальный и актуальный;
- `needs-review` — автоматике не стоит полностью доверять;
- `stale` — источник или обработка устарели;
- `archived` — материал больше не в активной работе.

---

### `source_type`

Что это был за исходник.

Рекомендуемые значения:

- `article`
- `youtube`
- `github_repo`
- `pdf`
- `note`
- `telegram`

Это отдельное поле от `type`.

Пример:

- `type: source-page`
- `source_type: youtube`

---

### `content_format`

Какого рода итоговый контент перед нами.

Рекомендуемые значения:

- `text`
- `transcript`
- `reference`

Пример:

- YouTube page: `content_format: transcript`
- GitHub repo page: `content_format: reference`

---

### `origin`

Откуда материал пришёл в систему.

Рекомендуемые значения:

- `url`
- `file`
- `youtube`
- `github`
- `telegram`
- `manual`

Нужно, чтобы потом было видно не только “что это”, но и “как это попало в пайплайн”.

---

### `created_at`, `updated_at`

Дата создания и последнего обновления итоговой страницы.

Формат:

- `YYYY-MM-DD`

---

### `language`

Язык итогового документа.

Примеры:

- `en`
- `ru`
- `mixed`

---

## Поля для будущих агентов

Вот эти поля особенно важны, если потом поверх будут бегать чистящие агенты.

### `tags`

Короткие retrieval tags.

Правила:

- 3-8 штук;
- lowercase;
- лучше kebab-case;
- без мусорных “ai”, “tech”, “interesting”, если они ничего не дают.

Примеры:

- `prompting`
- `agents`
- `rag`
- `evals`
- `markdown`
- `transcripts`

---

### `topics`

Более крупные тематические корзины.

Правила:

- 1-3 штуки;
- контролируемый набор;
- нужны для навигации по вики, а не для keyword noise.

Примеры:

- `prompt-engineering`
- `context-engineering`
- `agent-architecture`
- `knowledge-management`
- `document-parsing`
- `developer-tools`

---

### `entities`

Именованные сущности: люди, компании, продукты, библиотеки, проекты.

Правила:

- proper names;
- canonical capitalization;
- без slugification в самом значении.

Примеры:

- `Anthropic`
- `Claude`
- `OpenAI`
- `Gemini`
- `LangGraph`
- `Obsidian`
- `Andrej Karpathy`

---

### `concepts`

Ключевые идеи, техники, методы, frameworks.

Правила:

- human-readable phrases;
- не только бренды;
- это именно идеи, а не просто имена сущностей.

Примеры:

- `few-shot prompting`
- `chain-of-thought`
- `tool calling`
- `prompt caching`
- `structured outputs`
- `wikilinks`
- `provenance tracking`

---

### `related`

Ссылки на другие wiki pages.

На `v1` можно хранить пустой список или список page ids / slugs.

Правило:

- не свободный текст;
- не длинные объяснения;
- только ссылки на другие page identifiers.

Пример:

```yaml
related:
  - "src-2026-05-10-abc12345"
  - "ref-2026-05-11-def67890"
```

---

### `review_required`

Булево поле.

Если `true`, значит материал требует ручной или агентной проверки.

Причины могут быть такие:

- плохой source extraction;
- неуверенный summary;
- потеря структуры;
- конфликтный content;
- verify не прошёл уверенно.

---

### `verified`

Булево поле.

Показывает, прошёл ли материал автоматическую проверку.

Важно:

- `verified: true` не означает “идеально”;
- это означает “автоматика не нашла критических проблем”.

---

### `quality_score`

Число от `0.0` до `1.0`.

Нужно для сортировки и последующей чистки.

Пример интерпретации:

- `0.8+` — сильный материал
- `0.5-0.79` — нормальный, но не reference-grade
- `<0.5` — слабый или грязный, нужен review

---

### `provenance`

Очень полезное поле из референсных схем.

Показывает, какая доля content:

- взята напрямую из источника;
- выведена моделью;
- осталась сомнительной.

Формат:

```yaml
provenance:
  extracted: 0.80
  inferred: 0.15
  ambiguous: 0.05
```

Это сильно помогает при будущей чистке и trust ranking.

---

### `source_paths`

Список путей к raw source files.

Обычно будет один путь:

```yaml
source_paths:
  - "data/sources/2026-05-11_abcdefgh/source.md"
```

Но список лучше, чем одно поле, если потом появятся merged materials.

---

### `prompt_version`

Версия prompt-файла, которым был сделан output.

Пример:

- `article_rewrite@v1`
- `youtube_summary@v2`

Это нужно для воспроизводимости.

---

## Дополнительные полезные поля

Не обязательны в `v1`, но полезны, если захочется аккуратнее:

```yaml
aliases: []
authors: []
url: ""
canonical_url: ""
summary_kind: "rewrite"
ingest_batch: ""
```

Где:

- `aliases` — альтернативные названия
- `authors` — авторы или спикеры
- `url` — исходная ссылка
- `canonical_url` — нормализованная ссылка
- `summary_kind` — например `rewrite`, `summary`, `reference`
- `ingest_batch` — если материал пришёл пачкой

---

## Рекомендуемая структура тела `article.md`

Для `source-page` я рекомендую такой layout:

```markdown
# {Title}

## Summary
Коротко о чём материал.

## Key Ideas
- idea 1
- idea 2

## Details
Основное содержание с нормальной структурой.

## Code and Commands
Оригинальные блоки кода, команды, промпты.

## Entities
- Anthropic
- Claude

## Concepts
- few-shot prompting
- xml tags

## Related
- [[ref-...]]
- [[src-...]]

## Notes for Review
- что может быть сомнительным
```

---

## Рекомендуемая структура тела `reference.md`

Для `reference-page`:

```markdown
# {Repository Name}

## What It Is
Короткое описание.

## Stack
- Python
- FastAPI

## When To Use It
- use case 1
- use case 2

## Key Concepts
- concept 1
- concept 2

## Quick Start
Команды и базовые шаги.

## Caveats
Ограничения, риски, чего не хватает.

## Related
- [[src-...]]
- [[ref-...]]
```

---

## Рекомендуемая taxonomy для `guides`

Чтобы теги не расползлись в кашу, лучше заранее различать 4 слоя.

### Layer 1: tags

Короткие retrieval tags:

- `prompting`
- `agents`
- `rag`
- `evals`
- `markdown`
- `youtube`
- `transcripts`
- `github`
- `knowledge-base`

### Layer 2: topics

Тематические области:

- `prompt-engineering`
- `context-engineering`
- `agent-architecture`
- `knowledge-management`
- `document-parsing`
- `developer-tools`
- `llm-evals`
- `retrieval`

### Layer 3: entities

Именованные объекты:

- `OpenAI`
- `Anthropic`
- `Claude`
- `Gemini`
- `Obsidian`
- `LangGraph`
- `Karpathy`

### Layer 4: concepts

Идеи и методы:

- `few-shot prompting`
- `chain-of-thought`
- `structured outputs`
- `tool calling`
- `prompt caching`
- `wikilinks`
- `provenance tracking`

---

## Почему это лучше, чем просто `tags: []`

Потому что просто список тегов быстро превращается в мусор:

- смешиваются бренды, идеи, форматы и темы;
- агентам сложнее чистить и связывать;
- поиск хуже;
- сложнее строить later-stage wiki pages.

Разделение на:

- `tags`
- `topics`
- `entities`
- `concepts`

даёт уже достаточно структуры, но не перегружает систему.

---

## Минимальный schema contract для MVP

Если совсем уж резать до живого минимума, то для `article.md` и `reference.md` обязательно должны быть:

- `id`
- `title`
- `type`
- `status`
- `source_type`
- `origin`
- `created_at`
- `updated_at`
- `language`
- `tags`
- `topics`
- `entities`
- `concepts`
- `related`
- `review_required`
- `verified`
- `quality_score`
- `provenance`
- `source_paths`

Это уже достаточно, чтобы:

- индексировать;
- искать;
- линтить;
- чистить агентами;
- строить следующий слой wiki позже.

---

## Итог

Для `guides` сейчас лучшее решение такое:

- `source.md` остаётся immutable raw source;
- `article.md` и `reference.md` становятся wiki-ready pages;
- у них есть не только `tags`, но и `topics`, `entities`, `concepts`, `related`, provenance и review-поля;
- полноценные `entity/concept/synthesis` pages можно добавить потом, когда накопится достаточно материала.

Иными словами:

сейчас мы строим не просто summaries, а хорошие source pages для будущей wiki.
