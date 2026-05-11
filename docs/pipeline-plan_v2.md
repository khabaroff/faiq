# Pipeline plan v2: guides/

## Назначение

`guides/` — личный пайплайн для сбора и переработки технических материалов в удобные markdown-статьи и справки.

Система принимает ссылки и локальные файлы, вытаскивает исходник, сохраняет его в immutable-архив и строит производный материал:

- `article.md` для статей, постов, текстов и YouTube-транскриптов
- `reference.md` для GitHub-репозиториев

`article.md` и `reference.md` в MVP считаются не просто output-файлами, а wiki-ready pages с обязательным frontmatter и структурированным body. Базовая schema описана в `docs/wiki-schema-for-guides.md`.

Главная цель MVP: получить устойчивый цикл `ingest -> fetch -> process -> tag -> verify -> store`, который можно гонять по крону на VPS без ручного участия.

---

## Границы MVP

В MVP оставляем только то, что нужно для первого рабочего контура:

- URL статей и постов
- URL YouTube-видео
- URL GitHub-репозиториев
- локальные `.md` / `.txt` файлы из inbox
- локальные `.pdf` файлы из inbox

Что не входит в MVP:

- Telegram-бот
- GitHub docs как отдельный тип
- связи между статьями
- отдельные очереди под разные источники
- несколько cron entrypoint'ов
- `data/articles/` с symlink'ами

---

## Принципы

- Без LangGraph, LangChain и агентных графов
- Прямой Python + `openai` Azure SDK
- Один основной пайплайн, без лишней модульной дробности
- Промпты живут отдельно в `.md`
- Один source -> одна canonical папка хранения
- Итоговые `article.md` / `reference.md` обязаны быть wiki-ready pages
- Ошибки логируются, обработка не усложняется оркестрацией раньше времени

---

## Входящие каналы

На старте используем два канала:

1. `data/queue/inbox.txt`
   Один элемент на строку: URL или путь к локальному файлу.

2. `data/inbox/`
   Drop zone для файлов, которые внешний процесс или человек положил вручную.

Один `process_stream.py` за запуск:

- читает элементы из `data/queue/inbox.txt`
- сканирует `data/inbox/`
- нормализует всё в единый `QueueItem`
- передаёт в основной pipeline

---

## Типы источников

Для MVP достаточно трёх основных source type:

1. `ARTICLE`
   Любой URL, который не является YouTube и не является корнем GitHub repo, а также локальные `.md` / `.txt` / `.pdf`, которые идут в rewrite-flow.

2. `YOUTUBE`
   `youtube.com` / `youtu.be`

3. `GITHUB_REPO`
   URL корня репозитория вида `github.com/{owner}/{repo}`

Локальные текстовые и PDF-файлы не требуют отдельного продуктового режима: они просто попадают в `ARTICLE`.

---

## Режимы обработки

### 1. Article rewrite

Для:

- статей
- постов
- markdown/text файлов
- PDF после извлечения текста

Результат: `article.md`

Этот output должен соответствовать wiki schema:

- `type: source-page`
- `source_type: article|youtube|pdf|note`
- обязательный frontmatter
- структурированное body

Правила:

- сохранять все блоки кода verbatim
- сохранять промпты verbatim
- не вырезать технические детали без причины
- прозу сжимать аккуратно
- при необходимости можно разбивать материал на части по смыслу, но это не обязательное поведение MVP

### 2. YouTube summary

Для:

- YouTube-видео с доступным транскриптом

Результат: `article.md`

Этот output тоже считается `source-page`, а не отдельным ad hoc форматом.

Правила:

- транскрипт вытягивается целиком
- длинные транскрипты можно чанковать
- выход должен сохранять технические детали, команды, названия инструментов и важные формулировки

### 3. GitHub repo reference

Для:

- корневых URL репозиториев

Результат: `reference.md`

Этот output должен соответствовать wiki schema:

- `type: reference-page`
- `source_type: github_repo`
- обязательный frontmatter
- структурированное body

Формат:

- что это
- стек
- для чего использовать
- ключевые концепции
- быстрый старт
- ссылки

---

## Fetch strategy

### ARTICLE

Primary:

- `defuddle-cli`

Fallback:

- запрос страницы с `Accept: text/markdown`
- если этого недостаточно, можно добавить ещё один HTTP fallback позже

### YOUTUBE

Primary:

- `yt-dlp --write-auto-sub --skip-download`

Fallback:

- `https://youtubetranscribe.khabaroff.studio/`

Если транскрипт недоступен, элемент получает статус `needs_review`.

### GITHUB_REPO

Primary:

- GitHub API для repo metadata
- README / raw content repo

Fallback:

- raw github content без сложной логики

Если будет заметная нагрузка, добавить `GITHUB_TOKEN`.

---

## Pipeline stages

### 1. Ingest

Нормализует вход до `QueueItem`:

- `source`
- `source_kind`
- `received_at`
- `origin`

### 2. Detect

Определяет `SourceType`:

- `ARTICLE`
- `YOUTUBE`
- `GITHUB_REPO`

### 3. Fetch

Возвращает `FetchedContent` с минимально нужной структурой:

- `raw_text`
- `source_type`
- `source_meta`
- `attachments`

Не надо заранее делать слишком богатую схему. Структура должна покрывать реальный MVP, не больше.

### 4. Process

Роутинг по `source_type`:

- `ARTICLE` -> article rewrite
- `YOUTUBE` -> youtube summary
- `GITHUB_REPO` -> github reference

### 5. Enrich

В MVP enrich должен собирать не только теги, а минимальный wiki metadata layer.

Минимальный набор:

- `tags`
- `topics`
- `entities`
- `concepts`
- `related` (может быть пустым в `v1`)

`tags.py` можно расширить или разбить на несколько простых extractor stages, но итоговый `article.md` / `reference.md` должен иметь frontmatter по `docs/wiki-schema-for-guides.md`.

### 6. Verify

Проверка качества обработки:

- output-файл создан
- frontmatter валиден
- output не пустой
- кодовые блоки из source не пропали
- есть `title`
- есть `tags`, `topics`, `entities`, `concepts`
- page type и source type согласованы со schema
- `review_required`, `verified`, `quality_score`, `provenance`, `source_paths` присутствуют

Поведение:

- до 3 попыток verify / regenerate flow
- можно поддержать fallback-модели через config
- если проверка всё равно не проходит, статус `needs_review`

### 7. Store

Canonical layout:

```text
data/sources/YYYY-MM-DD_{hash8}/
├── source.md
├── article.md | reference.md
├── meta.json
└── images/
```

Правила:

- `source.md` immutable после записи
- `hash8 = SHA256(canonical_source)[:8]`
- коллизии решаются суффиксами

---

## Хранение промптов

Промпты должны храниться отдельно от Python-кода:

```text
guides/prompts/
├── article_rewrite.md
├── youtube_summary.md
├── github_reference.md
├── tags_extract.md
└── verify_check.md
```

Правила:

- каждый processor читает свой `.md`
- prompt version можно писать в frontmatter output-файла
- пользователь редактирует промпты без правок Python-кода

---

## Wiki schema

MVP официально включает wiki-ready schema для итоговых материалов.

Итог:

- `source.md` — raw immutable source
- `article.md` — `source-page`
- `reference.md` — `reference-page`

Обязательный frontmatter contract задаётся в [docs/wiki-schema-for-guides.md](/Users/khabaroff/GOO_LIBARCH/guides/docs/wiki-schema-for-guides.md:1).

Минимально обязательные поля для итоговых страниц:

- `id`
- `title`
- `type`
- `status`
- `source_type`
- `content_format`
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

Это часть MVP, а не future enhancement.

---

## Структура проекта

Для MVP достаточно такой структуры:

```text
guides/
├── guides/
│   ├── settings.py
│   ├── llm.py
│   ├── queue.py
│   ├── vault.py
│   ├── verify.py
│   ├── run.py
│   ├── prompts/
│   │   ├── article_rewrite.md
│   │   ├── youtube_summary.md
│   │   ├── github_reference.md
│   │   ├── tags_extract.md
│   │   └── verify_check.md
│   ├── fetch/
│   │   ├── base.py
│   │   ├── url.py
│   │   ├── youtube.py
│   │   └── github.py
│   ├── process/
│   │   ├── article.py
│   │   ├── youtube.py
│   │   └── reference.py
│   └── enrich/
│       └── tags.py
├── process_stream.py
├── data/
│   ├── queue/
│   │   └── inbox.txt
│   ├── inbox/
│   ├── logs/
│   └── sources/
├── docs/
├── pyproject.toml
└── .env.example
```

---

## Azure models

Нужны два логических класса моделей:

- `smart` — rewrite / transcript / reference generation
- `fast` — tags / verify

Настройки:

```python
azure_deployment_smart: str
azure_deployment_fast: str | None
```

Если `azure_deployment_fast` не задан, пайплайн может использовать `smart` как fallback.

---

## Cron

Один entrypoint:

```cron
*/15 * * * * cd /path/to/guides && uv run python process_stream.py
```

Один запуск должен:

- обработать очередь
- подобрать новые файлы из inbox
- записать лог
- завершиться без висящих процессов

---

## Порядок реализации

### Фаза 1. Основа

1. `pyproject.toml`
2. `.env.example`
3. `guides/settings.py`
4. `guides/llm.py`
5. `guides/vault.py`
6. `guides/queue.py`

Результат: проект стартует, конфиг читается, storage работает.

### Фаза 2. Fetchers

1. `guides/fetch/base.py`
2. `guides/fetch/url.py`
3. `guides/fetch/youtube.py`
4. `guides/fetch/github.py`

Результат: каждый источник отдельно вытягивает raw content.

### Фаза 3. Prompts + processors

1. `guides/prompts/*.md`
2. `guides/process/article.py`
3. `guides/process/reference.py`
4. `guides/process/youtube.py`

Результат: из fetched content получается целевой markdown в wiki-ready формате, а не просто summary text.

### Фаза 4. Enrich + verify

1. `guides/enrich/tags.py`
2. `guides/verify.py`

Результат: к output добавляются теги и статус проверки.

### Фаза 5. Orchestrator

1. `guides/run.py`
2. `process_stream.py`

Результат: полный проход от входа до сохранённого результата.

### Фаза 6. Ops

1. `cron/crontab.example`
2. базовое логирование
3. проверка запуска на VPS

### Фаза 7. Bot

После того как файловый pipeline работает стабильно:

1. `bot/main.py`
2. пересылка ссылок и файлов в очередь / inbox

---

## Открытые решения перед кодом

### 1. Verify model policy

Нужно зафиксировать:

- какие Azure deployments доступны
- есть ли отдельная fallback-модель для verify retry

### 2. `defuddle-cli` на VPS

Нужно проверить:

- ставится ли Node.js без боли
- стабильно ли работает `defuddle-cli` на типовых статьях

Если нет, основной URL-fetcher надо сразу строить на более простом HTTP fallback.

### 3. GitHub reference prompt

До кода стоит зафиксировать шаблон `reference.md`, чтобы не менять потом формат статей и verify-логику.

### 4. Wiki schema adoption

Перед полноценной реализацией processors и verify нужно считать `docs/wiki-schema-for-guides.md` source of truth для структуры `article.md` и `reference.md`.

---

## Не делаем сейчас

- Telegram ingestion
- связи между статьями
- отдельный режим GitHub docs
- отдельные stream-скрипты под каждый источник
- symlink-индекс статей
- сложную асинхронную архитектуру
- сложный multi-agent orchestration

---

## Итог

Чистый MVP для `guides/` — это один Python-пайплайн с тремя типами источников, промптами в markdown, immutable source storage, тэгированием, verify с retry и одним cron entrypoint.

Всё, что не помогает быстрее получить стабильный `article.md` / `reference.md` на VPS, в первую версию не входит.
