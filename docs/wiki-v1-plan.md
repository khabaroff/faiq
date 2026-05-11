# Wiki V1 Plan

Этот документ фиксирует, какой должна быть первая рабочая версия вики для `guides/`.

Это не абстрактная knowledge system. Это практичная личная рабочая вики для изучения технических штук, которую ты смотришь глазами. Иногда из неё можно что-то показывать студентам, но это не основной режим.

---

## Короткий итог

Будет две зоны:

- `data/` — сырьё, логи, usage, техническое хранилище
- `wiki/` — только то, что реально читается человеком

В `wiki/` не будет raw source. Только extract-pages и индексы.

Главный принцип:

**один источник -> одна extract-page**

Без автоматического слияния. Слияние, концепты, entities и syntheses — это отдельный будущий пайплайн.

---

## Для кого это

Первая версия вики делается:

1. сначала для тебя;
2. как рабочая база плотных конспектов;
3. не как учебник;
4. не как polished knowledge graph.

Значит:

- страницы могут быть плотными;
- важнее полезность, чем “красивость”;
- важнее точность и удобство поиска, чем финальная редакторская гладкость.

---

## Что будет в `data/`

`data/` — технический слой. Его читает пайплайн, а не человек.

```text
data/
  sources/
    YYYY-MM-DD_hash/
      source.md
      meta.json
      images/
  logs/
    events-YYYY-MM-DD.jsonl
    fetch-YYYY-MM-DD.jsonl
    process-YYYY-MM-DD.jsonl
    errors-YYYY-MM-DD.jsonl
  state/
    usage.db
```

### Правила

- `source.md` — immutable raw source
- `meta.json` — служебные данные по source
- `images/` — вложения при наличии
- в `wiki/` raw source не дублируется

---

## Что будет в `wiki/`

`wiki/` — слой, который ты открываешь и читаешь.

```text
wiki/
  extracts/
    articles/
    youtubes/
    pdfs/
    githubs/
    notes/
  _indexes/
    recent.md
    by-topic.md
    by-kind.md
    needs-review.md
    githubs.md
    prompts.md
  log.md
```

### Смысл папок

- `extracts/` — основной рабочий корпус
- `_indexes/` — автоматически собранная навигация
- `log.md` — короткий человеческий журнал операций

### Чего в `wiki/` пока не будет

- `concepts/`
- `entities/`
- `connections/`
- `syntheses/` как постоянного слоя

Это не потому, что они не нужны вообще. Это потому, что для `v1` они преждевременны.

---

## Структура `extracts/`

Папки внутри `wiki/extracts/` задаются **только по типу источника**:

- `articles/`
- `youtubes/`
- `pdfs/`
- `githubs/`
- `notes/`

Это важно.

Мы **не** делаем папки вроде:

- `tools/`
- `skills/`
- `prompts/`
- `methods/`

Потому что это уже не про source type, а про смысл материала. Смысл будет храниться в frontmatter.

---

## Как раскладываются разные материалы

### Статья

Идёт в:

- `wiki/extracts/articles/`

### YouTube

Идёт в:

- `wiki/extracts/youtubes/`

### PDF

Идёт в:

- `wiki/extracts/pdfs/`

### GitHub repo / tool repo / skills repo

Идёт в:

- `wiki/extracts/githubs/`

Даже если по смыслу это tool или skill, папка всё равно определяется source type.

### Локальная заметка / markdown / txt

Идёт в:

- `wiki/extracts/notes/`

---

## Как будут называться файлы

Файлы называются:

- `slug.md`

Пример:

- `prompting-best-practices.md`
- `building-effective-ai-agents.md`
- `langgraph.md`

Если возникает коллизия slug:

- добавляется короткий суффикс с hash

Пример:

- `prompting-best-practices-a1b2c3d4.md`

То есть имя файла остаётся человеческим, а стабильность держится через `source_id` во frontmatter.

---

## Базовое правило по страницам

Главное правило:

**один источник = одна extract-page**

Это default.

### Исключение

Очень длинные YouTube и PDF могут порождать несколько extract-pages.

Но это special case, не базовая модель.

Если такое случается:

- у частей должен быть общий `source_id`
- нужен `part_index`
- нужен `part_total`

Но в `v1` это не надо делать обязательным поведением.

---

## Язык вики

Основной язык вики:

- **русский**

Правила:

- тело extract-page пишется по-русски;
- английские термины сохраняются там, где они важны;
- английские названия можно хранить в metadata;
- `entities` и `concepts` могут содержать canonical EN формы.

То есть:

- вики русскоязычная;
- техническая терминология не уничтожается переводом.

---

## Что будет в frontmatter

Минимальный набор:

```yaml
id: "src-2026-05-11-a1b2c3d4"
title: "Prompting Best Practices"
type: "source-page"
status: "active"
source_type: "article"
knowledge_kinds: ["prompt", "guide"]
topics: ["prompt-engineering"]
entities: ["Anthropic", "Claude"]
concepts: ["few-shot prompting", "xml tags"]
review_required: false
verified: true
quality_score: 0.82
source_paths:
  - "data/sources/2026-05-11_a1b2c3d4/source.md"
prompt_version: "article_rewrite@v1"
```

Плюс:

- `origin`
- `created_at`
- `updated_at`
- `language`
- `related`
- `provenance`

---

## Какой metadata design принят

Мы не используем один общий мусорный `tags: []`.

Вместо этого:

### `source_type`

Закрытый список:

- `article`
- `youtube`
- `pdf`
- `github`
- `note`

### `knowledge_kinds`

Закрытый список:

- `tool`
- `prompt`
- `workflow`
- `method`
- `guide`
- `repo`
- `skill`
- `theory`
- `case-study`
- `tutorial`

Это отвечает на вопрос: “что это за штука по смыслу?”

### `topics`

Тоже контролируемый список.

Начальный набор:

- `prompt-engineering`
- `context-engineering`
- `agent-architecture`
- `developer-tools`
- `document-parsing`
- `knowledge-management`
- `automation`
- `llm-evals`
- `research-workflow`

### `entities`

Proper names:

- компании
- продукты
- модели
- авторы
- библиотеки

### `concepts`

Идеи и техники:

- `few-shot prompting`
- `tool calling`
- `structured outputs`
- `prompt caching`

### Почему так

Так тебе будет удобнее:

- глазами читать
- фильтровать
- строить индексы
- потом выделять concepts/entities отдельным пайплайном

---

## Какими должны быть страницы

`extract-page` — это плотный рабочий конспект для тебя.

Не “красивый студенческий учебник”.

Значит:

- можно писать плотнее;
- можно держать много технических деталей;
- код, команды и промпты не выбрасываются;
- summary не должен быть слишком маркетинговым или прилизанным.

Базовая форма тела:

- `Summary`
- `Key Ideas`
- `Details`
- `Code and Commands`
- `Entities`
- `Concepts`
- `Related`
- `Notes for Review`

---

## Индексы

Индексы нужны с первого дня.

Они должны быть:

- markdown-страницами;
- автоматически генерируемыми;
- обновляться после каждого прогона пайплайна.

### Какие индексы нужны в `v1`

#### `recent.md`

Показывает недавно добавленные extract-pages.

#### `by-topic.md`

Группирует страницы по `topics`.

#### `by-kind.md`

Группирует страницы по `knowledge_kinds`.

#### `needs-review.md`

Показывает всё, что требует ручной проверки.

#### `githubs.md`

Быстрый вход во всё, что связано с repo/tool/framework ссылками.

#### `prompts.md`

Быстрый список всего, где `knowledge_kinds` содержит `prompt`.

### Зачем это нужно

Потому что ты будешь пользоваться вики глазами, а не только query/search.

---

## `wiki/log.md`

Это короткий человеческий журнал.

Он не заменяет машинные логи.

Он нужен, чтобы было видно:

- что добавилось;
- что переписалось;
- что упало в `needs-review`;
- где сработал fallback.

Пример записи:

```md
## [2026-05-11] ingest | Prompting Best Practices -> wiki/extracts/articles/prompting-best-practices.md
## [2026-05-11] verify-fail | 5c-prompt-contracts -> needs-review
## [2026-05-11] fallback | youtube transcript HTTP fallback used for building-effective-ai-agents
```

Правило:

- коротко;
- без stack traces;
- без токеномусора;
- только human-readable события.

---

## Логи и usage

Для машинной аналитики нужен отдельный слой.

### JSONL logs

В `data/logs/` писать:

- события пайплайна
- ошибки
- срабатывание fallback
- verify failures
- успешные записи страниц

Минимальные поля:

- `run_id`
- `item_id`
- `stage`
- `source_type`
- `status`
- `fallback_used`
- `duration_ms`
- `error_type`
- `error_message`
- `model`
- `prompt_version`
- `tokens_in`
- `tokens_out`
- `cost_usd`

### Usage DB

В `data/state/usage.db` хранить usage/cost таблицу.

Минимум:

- `run_id`
- `item_id`
- `stage`
- `provider`
- `model`
- `tokens_in`
- `tokens_out`
- `cost_usd`
- `status`
- `created_at`

### Внешний monitoring

Можно потом подключить Langfuse.

Но source of truth всё равно остаётся локальным:

- `data/logs/*.jsonl`
- `data/state/usage.db`

---

## Что будет потом, но не сейчас

Вот это сознательно не часть `v1`:

- `wiki/concepts/`
- `wiki/entities/`
- `wiki/syntheses/`
- автоматическое слияние нескольких источников
- graph-first knowledge model
- сложный curator/reviewer loop

Но текущая metadata schema делается так, чтобы всё это потом можно было нарастить поверх `extracts/`.

---

## Почему это хорошая версия `v1`

Потому что она:

- простая;
- глазами обозримая;
- не требует большой онтологии;
- подходит под один рабочий поток;
- сохраняет raw отдельно;
- не мешает потом строить concepts/entities/syntheses отдельным пайплайном.

И главное:

она соответствует твоему реальному сценарию использования, а не красивой архитектуре ради архитектуры.
