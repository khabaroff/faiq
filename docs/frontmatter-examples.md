# Frontmatter Examples

Этот файл показывает живые примеры frontmatter для основных типов материалов в `guides/`.

Это не полный spec. Полный contract в:

- [docs/wiki-schema-for-guides.md](/Users/khabaroff/GOO_LIBARCH/guides/docs/wiki-schema-for-guides.md:1)

---

## 1. Article URL -> `article.md`

```yaml
---
id: "src-2026-05-11-a1b2c3d4"
title: "Prompting Best Practices"
type: "source-page"
status: "active"
source_type: "article"
content_format: "text"
origin: "url"
url: "https://example.com/prompting-best-practices"
created_at: "2026-05-11"
updated_at: "2026-05-11"
language: "en"
tags: ["prompting", "claude", "best-practices"]
topics: ["prompt-engineering", "developer-tools"]
entities: ["Anthropic", "Claude"]
concepts: ["few-shot prompting", "xml tags", "structured prompts"]
related: []
review_required: false
verified: true
quality_score: 0.86
provenance:
  extracted: 0.82
  inferred: 0.14
  ambiguous: 0.04
source_paths:
  - "data/sources/2026-05-11_a1b2c3d4/source.md"
prompt_version: "article_rewrite@v1"
---
```

---

## 2. YouTube -> `article.md`

```yaml
---
id: "src-2026-05-11-b2c3d4e5"
title: "Building Effective AI Agents"
type: "source-page"
status: "active"
source_type: "youtube"
content_format: "transcript"
origin: "youtube"
url: "https://www.youtube.com/watch?v=example"
created_at: "2026-05-11"
updated_at: "2026-05-11"
language: "en"
tags: ["agents", "youtube", "transcripts", "prompting"]
topics: ["agent-architecture", "prompt-engineering"]
entities: ["OpenAI"]
concepts: ["tool calling", "planning", "context management"]
related: []
review_required: false
verified: true
quality_score: 0.79
provenance:
  extracted: 0.74
  inferred: 0.20
  ambiguous: 0.06
source_paths:
  - "data/sources/2026-05-11_b2c3d4e5/source.md"
prompt_version: "youtube_summary@v1"
---
```

---

## 3. GitHub repo -> `reference.md`

```yaml
---
id: "ref-2026-05-11-c3d4e5f6"
title: "LangGraph"
type: "reference-page"
status: "active"
source_type: "github_repo"
content_format: "reference"
origin: "github"
url: "https://github.com/langchain-ai/langgraph"
created_at: "2026-05-11"
updated_at: "2026-05-11"
language: "en"
tags: ["github", "agents", "langgraph"]
topics: ["agent-architecture", "developer-tools"]
entities: ["LangGraph", "LangChain"]
concepts: ["stateful workflows", "agent graphs", "checkpointing"]
related: []
review_required: false
verified: true
quality_score: 0.81
provenance:
  extracted: 0.88
  inferred: 0.09
  ambiguous: 0.03
source_paths:
  - "data/sources/2026-05-11_c3d4e5f6/source.md"
prompt_version: "github_reference@v1"
---
```

---

## 4. PDF -> `article.md`

```yaml
---
id: "src-2026-05-11-d4e5f6g7"
title: "5C Prompt Contracts"
type: "source-page"
status: "needs-review"
source_type: "pdf"
content_format: "text"
origin: "file"
created_at: "2026-05-11"
updated_at: "2026-05-11"
language: "en"
tags: ["prompting", "pdf", "contracts"]
topics: ["prompt-engineering"]
entities: []
concepts: ["prompt contracts", "instruction design"]
related: []
review_required: true
verified: false
quality_score: 0.54
provenance:
  extracted: 0.61
  inferred: 0.25
  ambiguous: 0.14
source_paths:
  - "data/sources/2026-05-11_d4e5f6g7/source.md"
prompt_version: "article_rewrite@v1"
---
```

Пример тут специально с `needs-review`, потому что PDF extraction часто грязный.

---

## 5. Local note / markdown -> `article.md`

```yaml
---
id: "src-2026-05-11-e5f6g7h8"
title: "Notes on document parsing fallbacks"
type: "source-page"
status: "active"
source_type: "note"
content_format: "text"
origin: "file"
created_at: "2026-05-11"
updated_at: "2026-05-11"
language: "en"
tags: ["notes", "markdown", "fallbacks", "parsing"]
topics: ["document-parsing", "knowledge-management"]
entities: ["Cloudflare"]
concepts: ["markdown extraction", "fallback strategy"]
related: []
review_required: false
verified: true
quality_score: 0.73
provenance:
  extracted: 0.90
  inferred: 0.08
  ambiguous: 0.02
source_paths:
  - "data/sources/2026-05-11_e5f6g7h8/source.md"
prompt_version: "article_rewrite@v1"
---
```

---

## 6. Telegram link -> `article.md`

```yaml
---
id: "src-2026-05-11-f6g7h8i9"
title: "Telegram post import"
type: "source-page"
status: "needs-review"
source_type: "telegram"
content_format: "text"
origin: "telegram"
url: "https://t.me/example_channel/123"
created_at: "2026-05-11"
updated_at: "2026-05-11"
language: "ru"
tags: ["telegram", "capture", "inbox"]
topics: ["knowledge-management"]
entities: []
concepts: ["message ingestion"]
related: []
review_required: true
verified: false
quality_score: 0.41
provenance:
  extracted: 0.45
  inferred: 0.20
  ambiguous: 0.35
source_paths:
  - "data/sources/2026-05-11_f6g7h8i9/source.md"
prompt_version: "article_rewrite@v1"
---
```

Этот кейс тоже специально показан как более рискованный: ingestion допустим, но fetch/parse может быть слабым.
