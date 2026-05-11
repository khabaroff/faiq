# Pipeline plan: guides/

## Назначение

Хранилище технических материалов для обучения. Принимает ссылки на посты, репозитории, YouTube-видео, тексты. Обрабатывает по типу контента, сохраняет структурированные статьи/справки.

> Комментарий: для `v1` лучше сузить формулировку до "ссылки + текстовые файлы + YouTube". Репозитории, Telegram и PDF можно держать в плане, но не тащить в первый рабочий контур.

---

## Входящие каналы

- **Telegram-бот** — пересылка сообщений, ссылок, файлов (в этом проекте)
- **Папка `data/inbox/`** — drop zone; внешние автоматизации кладут сюда, крон подбирает
- **Текстовые файлы очереди** — `data/queue/urls.txt`, `data/queue/youtube.txt`

> Комментарий: здесь явный кандидат на упрощение. Для первого запуска достаточно `data/inbox/` + одного текстового queue-файла. Бот лучше подключать только после того, как базовый цикл fetch -> process -> store стабильно работает локально и на VPS.

---

## Нужен ли LangGraph?

**Нет.** LangGraph нужен для stateful графов с прерываниями, циклических retry-loops, нескольких агентов с checkpointing. Здесь этого нет — простые последовательные вызовы.

Стек: прямой `openai` Python SDK + `asyncio`. Роутинг по типу — обычный `match/case`.

> Комментарий: согласен. Я бы ещё сильнее упростил: пока не нужен даже обязательный `asyncio` как архитектурная ставка. Синхронный код или точечный `async` там, где он реально нужен, даст меньше сложности на старте.

---

## Типы источников → режимы обработки

| Тип | Как определяем | Режим обработки | Файл выхода |
|-----|---------------|-----------------|-------------|
| Статья/пост | URL → не GitHub, не YouTube | Rewrite: сохраняем код, промпты, детали | `article.md` |
| YouTube | `youtube.com` или `youtu.be` в URL | Транскрипт → summarize | `article.md` |
| GitHub repo | `github.com/user/repo` (корень) | Справочная страница: README + стек + когда использовать | `reference.md` |
| GitHub docs/мануал | `github.com/*/docs/*` или `*/blob/*/README*` | Паттерны + команды + примеры кода | `manual.md` |
| Текстовый файл | `.txt` / `.md` в inbox | Если ссылки — роутим; если текст — rewrite | `article.md` |
| PDF | `.pdf` в inbox | `pdftotext` → rewrite | `article.md` |

Определение типа — функция `detect_source_type(url_or_path) -> SourceType`. Расширяется исключениями.

> Комментарий: для `v1` я бы оставил только 4 типа: `article_url`, `youtube_url`, `local_text`, `local_pdf`. Отдельные режимы `GITHUB_REPO` и `GITHUB_DOCS` пока выглядят как premature split. GitHub-ссылки можно сначала обрабатывать как обычные URL или markdown-source и посмотреть, где реально не хватает отдельного роутинга.

---

## Независимые этапы

### Этап 1: Ingestion (приём)

Принимает ввод из любого канала, нормализует до `QueueItem`, добавляет в очередь.

- Бот получает forwarded message → парсит URL → кладёт в `queue/urls.txt` или `queue/youtube.txt`
- Бот получает файл/текст → сохраняет в `data/inbox/`
- `inbox_stream` сканирует `data/inbox/` по расписанию → определяет тип → роутит в нужную очередь

**Независим от остальных.** Новый канал → новый обработчик в ingestion, пайплайн не трогаем.

> Комментарий: хорошее разделение. Но для `v1` ingestion не должен "знать" много каналов. Один нормализатор входа и один формат `QueueItem` уже достаточно.

---

### Этап 2: Fetch (скачивание)

По URL или пути скачивает raw-контент: текст, изображения, метаданные.

| Источник | Primary | Fallback |
|---------|---------|---------|
| Статья/URL | `requests` + md-lib (пользователь предоставит) | jina.ai `r.jina.ai/{url}` |
| YouTube | `yt-dlp --write-auto-sub --skip-download` → парсим `.vtt` | HTTP к `youtubetranscribe.khabaroff.studio` |
| GitHub repo | GitHub API `/repos/{owner}/{repo}` + tree | raw githubusercontent |
| GitHub docs | Скачиваем конкретный `.md` / директорию `/docs` | — |
| Файл из inbox | Читаем напрямую | — |

Результат: `FetchedContent(raw_text, images: list[Path], meta: dict, source_type)`.

Изображения скачиваются в `images/`, упоминаются в article как `![](images/0.png)`. VLM-анализ — v2.

**Независим:** любой fetcher заменяется без изменений в пайплайне.

> Комментарий: здесь важно не перетащить в `v1` слишком богатый `FetchedContent`. Достаточно `raw_text`, `source_meta`, `attachments[]`. Если структура будет слишком детальной заранее, потом её всё равно придётся ломать под реальные кейсы.

---

### Этап 3: Route (маршрутизация)

По `source_type` из `FetchedContent` выбирает процессор:

```python
match content.source_type:
    case SourceType.ARTICLE:      processor = ArticleRewriter()
    case SourceType.YOUTUBE:      processor = YoutubeProcessor()
    case SourceType.GITHUB_REPO:  processor = ReferencePageBuilder()
    case SourceType.GITHUB_DOCS:  processor = ManualExtractor()
```

**Независим:** новый тип = новый процессор, существующие не трогаем.

> Комментарий: после упрощения типов этот роутер станет почти тривиальным, и это хорошо. Чем меньше специальных веток на старте, тем проще понять, где пайплайн реально расходится.

---

### Этап 4: Process (LLM-обработка)

Специфичная для типа трансформация через Azure LLM.

**ArticleRewriter** (smart LLM):
- Сохранять ВСЕ блоки кода, промпты, технические примеры verbatim
- Прозу — сжимать без потери смысла
- При `SPLIT_ARTICLES=true` + большой текст — можно разбить на несколько `article-1.md`, `article-2.md`

**YoutubeProcessor** (smart LLM):
- Транскрипт длинный → разбиваем на chunks → summarize каждый → объединяем
- Структура: тема, ключевые моменты, технические детали

**ReferencePageBuilder** (fast LLM):
- GitHub repo: название, назначение, стек, ключевые концепции, когда использовать
- Формат: структурированная справка (не длинная статья)

**ManualExtractor** (smart LLM):
- GitHub docs/мануал: паттерны, команды, примеры кода — всё verbatim
- Формат: практический мануал

**Независим:** каждый процессор — отдельный файл, не знает о других.

> Комментарий: на старте я бы сделал не 4 процессора, а 2:
> 1. `rewrite_processor` для статьи / markdown / PDF / GitHub docs
> 2. `transcript_processor` для YouTube
>
> `reference.md` для репозиториев выглядит как отдельный продуктовый режим. Его лучше добавить позже, когда накопятся реальные примеры и станет понятно, чем он стабильно отличается от обычного rewrite/manual.

> Комментарий: требование про "промпты отдельно в md" стоит поднять из open question в обязательную часть архитектуры. Иначе потом придётся выносить промпты из кода обратной миграцией.

---

### Этап 5: Enrich (теги + связи)

Добавляет метаданные к обработанному контенту.

**Tags** (fast LLM): JSON-список тегов из содержимого статьи. Пример: `[Agents, Claude, LangGraph, Prompting]`.

**Connections** (без LLM): читаем frontmatter всех существующих статей → ищем пересечения по тегам → список slug'ов. Детерминированно, быстро.

**Независим:** каждую часть можно выключить или заменить.

> Комментарий: теги в `v1` разумны. Связи по тегам я бы отложил. Это уже вторая производная ценность, а не ядро пайплайна. Сначала нужно научиться стабильно получать хороший `article.md`.

---

### Этап 6: Verify (верификация)

Fast LLM проверяет качество обработки:
- Все блоки кода из source присутствуют в article?
- Есть title, теги?
- Длина разумная (не обрезано, не раздуто)?

Пишет `verified: true/false` в frontmatter. При `false` — логируем, продолжаем (не падаем).

**Независим:** пропускается флагом `--skip-verify`.

> Комментарий: тут бы я не начинал с LLM-verify как основного механизма. Для `v1` полезнее дешёвые детерминированные проверки:
> - файл создан;
> - frontmatter валиден;
> - кодовые блоки не исчезли;
> - выход не пустой.
>
> LLM-verify можно оставить как optional second pass, если детерминированная проверка не прошла или если материал важный.

---

### Этап 7: Store (хранение)

Сохраняет в vault по паттерну из `usiki`:

```
data/sources/YYYY-MM-DD_{hash8}/
├── source.md     # raw content + метаданные — IMMUTABLE, не трогать после записи
├── article.md    # (или reference.md / manual.md) — обработанный output
└── images/       # скачанные изображения
```

`data/articles/` — плоский список symlinks на output-файлы для быстрого доступа.

Naming: `hash8 = SHA256(canonical_url)[:8]`. Коллизия → суффикс `-2`, `-3`.

> Комментарий: структура с `data/sources/YYYY-MM-DD_{hash8}/` выглядит здраво. А вот `data/articles/` с symlink'ами я бы пока не добавлял: это лишний слой поддержки. Сначала достаточно одного canonical storage layout.

---

## Структура проекта

```
guides/
├── src/
│   └── guides/
│       ├── settings.py          # Pydantic-settings: Azure env, флаги
│       ├── llm.py               # AzureOpenAI клиенты (smart / fast), @lru_cache
│       ├── queue.py             # pop_pending / mark_done для txt-очередей
│       ├── vault.py             # хранение: naming, write source.md, write output
│       ├── fetch/
│       │   ├── base.py          # FetchedContent, SourceType enum, detect_source_type()
│       │   ├── url.py           # HTTP + md-lib + jina.ai fallback
│       │   ├── youtube.py       # yt-dlp + HTTP fallback
│       │   └── github.py        # GitHub API: repo + docs
│       ├── process/
│       │   ├── article.py       # ArticleRewriter
│       │   ├── youtube.py       # YoutubeProcessor
│       │   ├── reference.py     # ReferencePageBuilder
│       │   └── manual.py        # ManualExtractor
│       ├── enrich/
│       │   ├── tags.py          # fast LLM → JSON теги
│       │   └── connections.py   # tag-match по существующим статьям
│       ├── verify.py            # fast LLM quality check
│       └── run.py               # оркестратор: fetch → route → process → enrich → verify → store
├── bot/
│   └── main.py                  # aiogram polling: forwarded msg/file → queue или inbox
├── streams/
│   ├── url_stream.py            # cron: читает data/queue/urls.txt
│   ├── youtube_stream.py        # cron: читает data/queue/youtube.txt
│   └── inbox_stream.py          # cron: сканирует data/inbox/
├── data/
│   ├── queue/
│   │   ├── urls.txt             # одна URL на строку
│   │   └── youtube.txt
│   ├── inbox/                   # drop zone
│   ├── sources/                 # YYYY-MM-DD_{hash8}/
│   └── articles/                # symlinks на output
├── docs/                        # этот файл и другая документация
├── cron/
│   └── crontab.example
├── pyproject.toml
├── .env.example
└── CLAUDE.md
```

> Комментарий: я бы не раскладывал проект по стольким модулям до первого рабочего прохода. Для `v1` хватит компактной сборки:
> - `settings.py`
> - `models.py` или `types.py`
> - `prompts/`
> - `fetchers.py`
> - `processors.py`
> - `storage.py`
> - `pipeline.py`
> - `streams/run_queue.py`
>
> Когда появятся 2-3 устойчиво разные процессора, тогда и есть смысл дробить по подпакетам.

---

## Azure Models

```python
# settings.py
azure_deployment_smart: str   # ArticleRewriter, YoutubeProcessor, ManualExtractor
azure_deployment_fast: str    # ReferencePageBuilder, tags, verify
```

Прямой `openai.AzureOpenAI`, не langchain. `@lru_cache` на клиентах.

> Комментарий: тут всё нормально. Я бы только сразу зафиксировал policy: `fast` и `smart` задаются конфигом, но пайплайн может работать и с одним deployment, если второй не задан. Это упростит первый деплой на VPS.

---

## Cron streams

```
*/15 * * * *  cd /path/to/guides && uv run python -m streams.url_stream
*/30 * * * *  cd /path/to/guides && uv run python -m streams.youtube_stream
*/10 * * * *  cd /path/to/guides && uv run python -m streams.inbox_stream
```

Каждый stream независим. Ошибка в одном не влияет на остальные. Логи в `data/logs/YYYY-MM-DD.log`.

> Комментарий: для `v1` не нужны три отдельных stream entrypoint'а. Один `run_queue` по крону проще в эксплуатации, логировании и ретраях. Разделять на несколько cron jobs имеет смысл только если реально разные SLA или тяжёлые источники начинают мешать друг другу.

---

## Порядок реализации

1. `pyproject.toml` + `.env.example` + `CLAUDE.md`
2. `settings.py` + `llm.py`
3. `vault.py` + `queue.py`
4. `fetch/base.py` → `fetch/url.py` → `fetch/youtube.py` → `fetch/github.py`
5. `process/article.py` → остальные процессоры
6. `enrich/tags.py` → `enrich/connections.py` → `verify.py`
7. `run.py` — сборка пайплайна
8. `streams/url_stream.py` — первый рабочий поток
9. Остальные streams + `bot/main.py`
10. `cron/crontab.example`

> Комментарий: я бы переформулировал первый milestone так:
> 1. Конфиг + Azure client + prompts в `.md`
> 2. Canonical storage layout
> 3. Один ingest path: `data/inbox/` или `queue.txt`
> 4. Два fetch mode: URL и YouTube
> 5. Два process mode: rewrite и transcript summary
> 6. Store + простая детерминированная verify
> 7. Один cron runner
>
> Всё остальное после этого уже можно добавлять по фактической боли.

---

## Открытые вопросы

1. **Markdown библиотека** — какую использовать для URL→MD конвертации?
https://github.com/kepano/defuddle-cli

https://blog.cloudflare.com/markdown-for-agents/
curl https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/ \
  -H "Accept: text/markdown"

Комментарий: решение без оверинжиниринга такое:
- основной fetcher должен уметь принимать уже готовый markdown/text;
- URL->MD конвертацию завернуть в простой adapter interface;
- начать с одного primary способа и одного fallback, не больше.

Если нужен практичный старт, я бы взял:
- primary: обычный article fetch + readability/markdown converter;
- fallback: `r.jina.ai/http://...` или другой HTTP-based markdown source.

`defuddle-cli` имеет смысл только если реально даст заметно чище markdown на ваших типах источников.

2. **GitHub routing** — ещё исключения в `detect_source_type` помимо repo/docs?
потом

Комментарий: пока не решать. Лучшее решение здесь — не плодить исключения до появления плохих реальных кейсов.

3. **Split articles** — когда разбивать? По разделам (H2)? По порогу длины?
по смыслу я бы сказал. выделить может быть идеи и тогда разбивать. токены не жалко

Комментарий: для `v1` не разбивать вообще. Один source -> один output. Разбиение добавлять только когда появятся реальные тексты, которые невозможно читать в одном файле.

4. **Verify fail** — только логировать, или ещё уведомление в бот?
можно сделать retry 3 раза и можно на других можелях я могу дать

Комментарий: `v1`:
- 1 автоматический retry;
- потом статус `needs_review`;
- без бота.

Многомодельные retry и уведомления лучше отложить, иначе операционная сложность вырастет быстрее пользы.

5. **reference.md формат** — что именно должно быть в справочной странице репо?
придумаем

Комментарий: это явный `v2+`. Пока нет примеров, лучше не проектировать формат заранее.

+++
GITHUB_DOCS - этого не будет
важно - промпты я хочу контролировать и хранить их отдельно в md

Комментарий: это, по сути, уже решение. Я бы закрепил его в явных требованиях:
- `prompts/*.md` лежат отдельно от Python-кода;
- каждый processor ссылается на конкретный prompt file;
- prompt version можно писать в frontmatter output-файла для воспроизводимости.
