Верни только JSON-объект по тексту статьи.

Формат:
```json
{
  "tags": ["LangGraph"],
  "topics": ["agent-architecture"],
  "entities": ["Anthropic"],
  "concepts": ["checkpointing"]
}
```

Правила:
- Возвращай только валидный JSON, без markdown и без пояснений.
- `tags`: 3-8 технических тегов, Title Case.
- `topics`: 2-5 high-level topic slugs, lowercase-hyphenated.
- `entities`: ≤5 самых значимых named entities — инструменты, компании, люди, проекты.
- `concepts`: ≤4 абстрактных concepts в lowercase.
- Убирай мусорные, слишком общие и дублирующиеся значения.
- Если чего-то нет, верни пустой массив.
