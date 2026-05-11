# TODO / Что нужно решить

## Баги — исправить

### 1. defuddle-cli: неправильная команда
**Файл:** `guides/fetch/url.py` → `_try_defuddle()`

Текущий вызов: `npx defuddle-cli <url>`
Правильный вызов: `npx defuddle-cli parse <url>`

defuddle-cli требует подкоманду `parse`. Из-за этого он всегда падает и код
падает на Jina. Нужно добавить "parse" в subprocess.run.

### 2. GitHub API 502 без токена
**Файл:** `guides/fetch/github.py`

GitHub API без токена: 60 req/час анонимно, часто возвращает 502 при лимите.
Сейчас gist и repo fetchers падают на fallback или теряют данные.
Нужен `GITHUB_TOKEN` в `.env`.

---

## Ключи и сервисы — настроить

### Обязательно

| Ключ | Статус | Где взять |
|------|--------|-----------|
| `AZURE_OPENAI_API_KEY` | ✅ есть | Azure Portal |
| `AZURE_OPENAI_ENDPOINT` | ✅ есть | Azure Portal |
| `AZURE_DEPLOYMENT_SMART` | ✅ `gpt-5.4` | Azure Portal |
| `AZURE_DEPLOYMENT_FAST` | ✅ `gpt-5.4-mini` | Azure Portal |
| `GITHUB_TOKEN` | ❌ нет | github.com → Settings → Tokens (PAT, scope: `gist` read) |

### Опционально

| Сервис | Статус | Зачем |
|--------|--------|-------|
| Langfuse | ❌ `LANGFUSE_ENABLED=false` | Трассировка вызовов LLM, dashboard расходов. Бесплатен self-hosted, cloud.langfuse.com бесплатный tier. |
| Jina API key | ❌ нет | Без ключа Jina rate-limit ~5 req/мин. Ключ даёт 1M token/мес бесплатно. Переменная не в Settings пока. |

---

## Улучшения — сделать

### 3. Jina API key support
**Файл:** `guides/fetch/url.py`, `guides/settings.py`

Добавить `jina_api_key: str | None = None` в Settings.
Передавать `Authorization: Bearer <key>` в `_try_jina()`.
Без ключа Jina throttles на публичных IP.

### 4. http-markdown fetcher слишком узкий
**Файл:** `guides/fetch/url.py` → `_try_http_markdown()`

Текущий фильтр: пропускает только ответы без "html" в Content-Type.
Большинство сайтов возвращают `text/html` даже когда Accept=text/markdown → fetcher всегда молчит.
Решение: либо убрать (Jina справляется), либо использовать только для
raw.githubusercontent.com и подобных.

### 5. process_stream.py: нет stdout при успехе
Сейчас при успешной обработке ничего не печатается в stdout — только в лог.
Неудобно при ручном запуске. Нужно добавить `print()` или `logging.INFO` который виден в stderr.

### 6. needs_review.txt содержит только failed записи
`data/queue/needs_review.txt` — нет очистки старых failed.
При повторной обработке (после исправления бага) старая `#failed#` запись остаётся.
Нужна логика: при успешной обработке URL — убирать из needs_review.

### 7. GitHub API: fallback на мастер README
**Файл:** `guides/fetch/github.py` → `_try_fetch_readme()`

Пробует только `main`. Многие репо используют `master`.
Нужен fallback: main → master → HEAD.

---

## Расходы (текущие)

| Модель | Вызовов | Токенов | Стоимость |
|--------|---------|---------|-----------|
| gpt-5.4 | 44 | 442 215 | $3.18 |
| gpt-5.4-mini | 42 | 214 811 | $0.04 |
| **Итого** | 86 | 657 026 | **$3.22** |

Среднее: ~$0.24/документ (13 документов на $3.22)
Дорого из-за gpt-5.4 в article rewrite. Альтернатива: переключить rewrite на mini
и оставить smart только для verify — сэкономит ~80%.
