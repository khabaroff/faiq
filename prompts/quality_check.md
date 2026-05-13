# Quality Check (RU, cheap model)

> Pipeline D — дешёвая модель проверяет качество саммари и чистит wiki-страницы.

## Назначение

Два режима:

### Режим 1: проверка саммари

Прочитать `vault/sources/<slug>.md` + `vault/summaries/<slug>.md`. Оценить:

- TL;DR покрывает основные идеи?
- Tools/techniques не пропущены?
- Цитаты реально присутствуют в исходнике?
- Нет ли явных галлюцинаций?

Выход:
```json
{
  "mode": "summary_check",
  "slug": "...",
  "verdict": "ok" | "needs_resummarize" | "minor_fix",
  "issues": ["список проблем"]
}
```

### Режим 2: чистка wiki-страницы

Прочитать `vault/wiki/tools/<slug>.md` или `vault/wiki/techniques/<slug>.md`. Оценить:

- Дубликаты упоминаний?
- Битые ссылки?
- Секция "Что это" противоречит упоминаниям?
- Слишком короткое описание (< 2 предложений) при наличии >2 упоминаний?

Выход:
```json
{
  "mode": "wiki_clean",
  "slug": "...",
  "verdict": "ok" | "needs_cleanup",
  "cleaned_page_md": "..." // только если verdict == needs_cleanup
}
```

## Правила

- Cheap model (Azure mini family). Без reasoning. Быстро.
- Не выдумывать факты. Только сверка с исходником/страницей.
- Verdict `needs_resummarize` ставится только при серьёзных пропусках или галлюцинациях.

## Инструкция модели

(TODO: финальный промпт)
