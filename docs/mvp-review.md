# MVP Review: что строим, что режем

Анализ плана с точки зрения минимального рабочего результата.

---

## Что уже решено (из аннотаций в плане)

- **GITHUB_DOCS убираем** — остаётся 3 типа: ARTICLE, YOUTUBE, GITHUB_REPO
- **Промпты в отдельных .md файлах** — пользователь контролирует, не зашиваем в код
- **Markdown из URL:** defuddle-cli (primary) / Cloudflare `Accept: text/markdown` header (fallback)
- **Split:** по смыслу (LLM решает), не по длине
- **Verify fail:** retry 3 раза, можно на разных моделях

---

## Что режем из плана (оверинжиниринг для MVP)

### 1. `data/articles/` symlinks — убрать
Плоская папка со symlinks добавляет сложность без пользы. Один человек пишет контент, знает где `data/sources/`. Убрать насовсем.

### 2. `enrich/connections.py` — отложить в v2
Нет смысла искать связи между статьями пока их 5 штук. Включить когда контента станет заметно.

### 3. Отдельные очереди `urls.txt` / `youtube.txt` — один `inbox.txt`
Зачем два файла? Тип URL определяется автоматически по адресу. Одна очередь, один stream на старте.

### 4. `youtube_stream.py` и `inbox_stream.py` — объединить
Три отдельных крон-скрипта для одного пользователя — лишнее. Один `process_stream.py` читает `data/queue/inbox.txt` + сканирует `data/inbox/` за один запуск.

### 5. `src/guides/guides/` вложенность — упростить
Для личного инструмента `src/` обёртка избыточна. Пакет прямо в корне: `guides/`.

---

## Реальный MVP: что нужно чтобы это работало

**Минимум для первого прогона:**
1. `guides/settings.py` — Azure env + пути
2. `guides/llm.py` — два клиента (smart / fast)
3. `guides/vault.py` — запись source.md + article.md
4. `guides/queue.py` — pop/mark_done для inbox.txt
5. `guides/fetch/url.py` — defuddle-cli + Cloudflare fallback
6. `guides/fetch/youtube.py` — yt-dlp + HTTP fallback
7. `guides/fetch/github.py` — только REPO тип (не DOCS)
8. `guides/prompts/` — .md файлы промптов
9. `guides/process/article.py` — rewrite (главный)
10. `guides/process/reference.py` — GitHub repo справка
11. `guides/process/youtube.py` — транскрипт → summary
12. `guides/enrich/tags.py` — теги
13. `guides/verify.py` — проверка + retry 3x
14. `guides/run.py` — оркестратор
15. `process_stream.py` — крон-точка входа

Бот — после того как пайплайн работает на файлах.

---

## Порядок работы (переработанный)

```
Фаза 1 — Ядро пайплайна
  pyproject.toml + settings + llm + vault + queue
  → можно запустить и проверить что файлы создаются

Фаза 2 — Fetchers
  fetch/url.py (defuddle + fallback)
  fetch/youtube.py
  fetch/github.py (только repo)
  → тест: каждый fetcher отдельно

Фаза 3 — Processors + prompts
  prompts/*.md
  process/article.py → process/reference.py → process/youtube.py
  → тест: подать конкретный URL, проверить article.md

Фаза 4 — Enrich + Verify
  enrich/tags.py
  verify.py (с retry)
  → полный прогон от URL до article.md с тегами

Фаза 5 — Stream + Cron
  process_stream.py
  crontab.example
  → работает без участия человека

Фаза 6 — Бот
  bot/main.py (aiogram)
  → пересылка ссылок в очередь
```

---

## Вопросы которые нужно решить до кода

**1. Промпты — структура файлов**
Как именно храним? Предлагаю:
```
guides/prompts/
  article_rewrite.md      # системный промпт для ArticleRewriter
  youtube_summary.md      # для YoutubeProcessor
  github_reference.md     # для ReferencePageBuilder
  tags_extract.md         # для тегов
  verify_check.md         # для верификации
```
Каждый .md читается в начале процессора. Промпт = просто текст файла (или frontmatter + body если нужны параметры).

**2. Verify retry — какие модели**
Plan говорит "retry на других моделях". Нужно решить: у тебя есть несколько Azure deployments? Или fallback на другого провайдера? Нужно знать чтобы прописать в settings.

**3. defuddle-cli — как ставить на VPS**
Это npm-пакет. На VPS нужен Node.js. Либо: установить node + defuddle как системную зависимость, либо использовать только Cloudflare header (проще, но работает только для Cloudflare-сайтов). Или jina.ai как единственный fallback.

**4. GitHub repo — что именно в `reference.md`**
Нужно согласовать шаблон до написания промпта. Предложение:
```markdown
# {repo name}

**Что это:** одна строка
**Стек:** языки, ключевые зависимости
**Для чего использовать:** 2-3 ситуации
**Ключевые концепции:** список с кратким описанием
**Быстрый старт:** установка + первый запуск (из README)
**Ссылки:** repo URL, docs если есть
```

---

## Риски

- **defuddle-cli на VPS** — может быть головная боль с Node.js зависимостью. Тест нужен до построения системы.
- **yt-dlp транскрипты** — не для всех видео есть авто-субтитры. Нужно явно обрабатывать "транскрипт недоступен".
- **GitHub rate limit** — API без токена = 60 req/hr. Нужен `GITHUB_TOKEN` в env если будет много репозиториев.
