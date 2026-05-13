# SEO Meta Prompt

## PURPOSE

Generate SEO-optimized metadata for a summary page.
Output goes into the page's YAML frontmatter.

## INPUT

- `{{title}}` — article title (from source)
- `{{tldr}}` — 1-2 sentence summary
- `{{key_claims}}` — list of key claims
- `{{tools}}` — tools mentioned (list)
- `{{patterns}}` — patterns mentioned (list)
- `{{source_url}}` — original URL

## OUTPUT (JSON only, no markdown)

```json
{
  "seo_title": "Title under 60 chars",
  "seo_description": "Description under 160 chars. Specific, useful, no clickbait.",
  "og_description": "Open Graph description, 1-2 sentences. Same tone as seo_description."
}
```

## RULES

- `seo_title`: 50-60 chars. Factual, keyword-rich. No ":" if possible. No "How to", no "The Ultimate Guide".
- `seo_description`: 130-160 chars. Включает ключевые термины из статьи. Пишем по-русски если статья на русском, по-английски если на английском.
- If tools or patterns are prominent — mention them by name in description.
- No exclamation marks. No "This article...". No "Learn how to...".
- Tone: direct, specific, like a good librarian's annotation.

## LANGUAGE

Match source language: Russian article → Russian seo_description. English → English.
Technical names (Claude Code, LangChain) stay in original regardless.
