# Wiki Page Update — Tools & Patterns

## PURPOSE

Update or create a wiki page when a new mention arrives from a summary.

Two page types:
- **tool** — конкретный продукт/сервис/библиотека (Claude Code, Obsidian, yt-dlp)
- **pattern** — именованный подход/паттерн (Context Engineering, ReAct, Chain-of-Thought)

Audience: speaker preparing AI lectures + students who receive these pages as reference material.

## INPUT

- `{{current_page_md}}` — current page content (empty string = new page)
- `{{tool_name}}` — canonical name
- `{{tool_type}}` — `tool` | `pattern`
- `{{new_mention}}`:
  ```json
  {
    "source_slug": "...",
    "source_url": "...",
    "role_in_article": "роль на русском",
    "quote": "verbatim quote in original language"
  }
  ```

## OUTPUT (JSON)

```json
{
  "action": "create" | "append_mention" | "rewrite_description",
  "page_md": "full updated markdown of the page",
  "reason": "one sentence why this action"
}
```

## DECISION RULES

- `create` — page doesn't exist yet. Build from this first mention.
- `append_mention` — page exists, description is still accurate. Add to Mentions only.
- `rewrite_description` — new mention adds a substantially different angle. Rewrite the description section.

## PAGE TEMPLATES

### Tool page

```markdown
---
name: Tool Name
slug: tool-slug
type: tool
url: https://official-url-or-empty
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
---

# Tool Name

## Что это

Краткое описание на русском (2-4 предложения). Что делает, зачем нужен, в каком контексте используется.
Не Википедия — живое объяснение как для студента.

## Ссылки

- [Официальный сайт](url) — если есть

## Упоминания в моих материалах

- [название статьи](../../summaries/slug.md) — "verbatim quote" 
```

### Pattern page

```markdown
---
name: Pattern Name
slug: pattern-slug
type: pattern
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
---

# Pattern Name

## Суть

Краткое определение на русском (1-2 предложения). Что это за паттерн и зачем.

## Как работает

2-4 предложения. Механизм, ключевая идея. Без занудства.

## Когда применять

- ситуация 1
- ситуация 2

## Упоминания в моих материалах

- [название статьи](../../summaries/slug.md) — "verbatim quote"
```

## WRITING RULES

- Russian throughout (except quotes — always in original language)
- Tone: concise, human, not encyclopedic. Like explaining to a smart student, not writing docs.
- Description evolves: each new mention can sharpen understanding — rewrite when it adds real value.
- Quote: verbatim from original source, never translated.
- No "This tool is..." or "This pattern represents..." — start directly with the substance.
- Language: технические имена (название инструмента, API, CLI) — в оригинале; всё остальное — по-русски; не транслитерировать.
