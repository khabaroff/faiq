# 07 Prompts

Связанные документы: [06 Page Schema](06-page-schema.md), [03 Agent Roles](03-agent-roles.md), [04 Pipeline](04-pipeline.md), [08 Language Policy](08-language-policy.md), [00 Roadmap](00-roadmap.md), [Research: Reference Patterns](../research/reference-patterns.md).

## Назначение

Prompt templates define role behavior for agents.

Phase 0 documents prompt conventions and sketches. Actual production prompt text is written in Phase 5 with tests around output contracts.

## Prompt Location

Prompt templates live in:

```text
vault/schema/prompts/<role>.md
```

**MVP prompt files (4):**

- `curator.md`;
- `compiler.md` — объединяет classic Ingestor + Chunker + Extractor (см. [03 Agent Roles](03-agent-roles.md));
- `linker.md`;
- `note-builder.md`.

**Отложено в [PRD/future/](../future/)** (активация в M3+ или позже):

- `deduplicator.md`, `verifier.md`, `deliberator.md`, `editor.md`, `linter.md`, `publisher.md`.

Если на длинных текстах (>10K слов) Compiler начнёт деградировать — расщепить обратно на `ingestor.md` + `chunker.md` + `extractor.md` (это обратимо).

## Prompt Front Matter

Each prompt includes front matter:

```yaml
---
id: prompt-curator
role: curator
version: 0.1.0
language: ru
output_format: json
updated_at: 2026-04-28
---
```

Versioning uses semver:

- patch: wording changes that preserve output shape;
- minor: new optional fields;
- major: breaking output contract changes.

## Tone Guide

Prompts use RU primary.

Style:

- concise;
- technical;
- evidence-oriented;
- no motivational language;
- no unsupported synthesis;
- preserve uncertainty.

## Terminology Rule

When an English term is important, keep it at first use:

```text
живая вики (living wiki)
полнотекстовый поиск (full-text search)
векторный поиск (vector search)
```

After first use, Russian term can be used.

See [08 Language Policy](08-language-policy.md).

## Citation Rule

Agents must separate:

- Russian synthesis;
- original quote;
- source id;
- quote language;
- claim id.

Claims and evidence must follow [06 Page Schema](06-page-schema.md).

## Curator Prompt Sketch

Input:

- source title;
- source path;
- source text excerpt;
- source metadata.

Output:

- relevance score 0-10;
- reason;
- suggested topics;
- accept/reject.

Instruction sketch:

```text
Оцени, относится ли источник к теме AI-assisted learning и LAAI.
Не пересказывай весь источник.
Верни JSON по контракту Curator.
```

## Compiler Prompt Sketch

Compiler объединяет classic Ingestor + Chunker + Extractor одним вызовом. Один контекст у модели — меньше координации между шагами.

Input:

- raw source (markdown);
- Curator result (score, reason, suggested_topics).

Output (один JSON):

- `source_metadata` — title, source_path, language, author?, date?, notable_quotes[];
- `chunks[]` — каждый со `id`, `kind` ∈ `{claim, evidence, definition, example, citation}`, `text`, `lang`, `span` (опц.);
- `claims[]` — каждый со stable `id`, ссылками на supporting `<evidence>` chunks;
- `entities[]` — names, types (person/product/model/tool/organization), aliases.

Instruction sketch:

```text
Прочитай источник целиком. За один раз:
1. Нормализуй текст в source-page draft (RU primary, оригинальные цитаты verbatim).
2. Разбей на смысловые chunks (claim/evidence/definition/example/citation).
3. Извлеки проверяемые claims (с привязкой к evidence-chunks по id).
4. Извлеки entities (имена сущностей, продуктов, концепций).
Не создавай wiki pages — это работа Note Builder.
Не путай claim и evidence: claim — твоё RU-утверждение, evidence — оригинальная цитата.
```

> **Если на длинных текстах (>10K слов) Compiler начнёт давать слабые claims/entities** — расщепить на отдельные prompts `ingestor.md` + `chunker.md` + `extractor.md`. Это обратимо (M2+).

## Linker Prompt Sketch

Input:

- extracted claims;
- terms;
- existing candidate nodes;
- top-K совпадений во **всём** индексе — published nodes **и** candidates (drafts are searchable; см. [03 Agent Roles](03-agent-roles.md), «Linker queries everything, not just candidates», и [12 risk-based curation](../future/06-auto-approval-gates.md), «Drafts are searchable»). Кандидат-совпадения помечены `is_candidate: true`;
- список разрешённых edge types с verification-questions (см. ниже).

Output:

- typed edges с `src_id`, `src_kind`, `dst_id`, `dst_kind`, `type`, `provenance_state`, `confidence`;
- провенанс-цитаты для `extracted` рёбер (короткий фрагмент источника, подтверждающий связь).

Instruction sketch:

```text
Предложи связи между claims, chunks и wiki nodes.
Используй только разрешённые edge types.
Для каждой предложенной связи задай себе verification-question (ниже).
Если ответа уверенно «да» нет — НЕ предлагай эту связь.
Лучше пропустить, чем нагенерить «всё связано со всем».
```

### Verification Questions per Edge Type (MVP — 5 типов)

Задача verification-questions — заставить модель явно рассуждать о критерии каждой связи, а не свободно ассоциировать. Без этого фильтра Linker склонен размечать всё подряд как `mentions`. См. R6 llm-wiki-agent (двухпроходный graph build) и R3 llm-wiki-compiler в [Research: Reference Patterns](../research/reference-patterns.md).

| Edge type | Verification question | Контр-сигнал (если ответ «нет / не уверен» — не ставь) |
|---|---|---|
| `mentions` | Назван ли Б в А **по имени** (как сущность, продукт, человек, концепция)? | Тематическое сходство без явного упоминания — не mentions. |
| `cites` | Содержит ли текст А прямую отсылку к Б как к источнику (цитата, footnote, ссылка, фраза «по словам Б», «в работе Б»)? | Просто сходная тема — не цитирование. |
| `contradicts` | Если А истинно, означает ли это, что Б ложно? Делают ли А и Б взаимоисключающие утверждения о **том же** вопросе? | Разные акценты на одну тему ≠ противоречие. |
| `supersedes` (опц.) | Является ли А более новой/уточнённой версией Б, отвечающей на тот же canonical question? Содержит ли А явное указание на устаревание Б? | Просто более свежий источник на смежную тему — не supersedes. |
| `derived_from` (опц.) | Можно ли восстановить смысл А, используя только Б и логический вывод? Является ли А развитием/применением Б? | Просто следующий по времени или похожий по теме — не derived_from. |

> **Отложено в [PRD/future/](../future/):** `same_as`, `part_of`, `expands`, `depends_on`. Они тонко различимы только на больших графах; в MVP `mentions` покрывает 80% случаев alias-связей.

Каждое предложенное ребро несёт provenance — `extracted` (есть прямой текстовый маркер связи: имя, ссылка, явная конструкция) или `inferred` (LLM вывел по семантике). Linter валидирует `extracted` рёбра string-match-ем по `vault/raw/`.

## Note Builder Prompt Sketch

Input:

- claims;
- evidence;
- entities;
- edges;
- page candidates.

Output:

- draft wiki pages following page schema.

Instruction sketch:

```text
Собери draft wiki pages.
Соблюдай YAML front matter и claim/evidence tags.
Не выдумывай sources.
```

## Output Schema Requirement (MVP — pydantic only)

Каждая роль возвращает **структурированный output**, валидируемый pydantic-моделью до того, как pipeline что-либо запишет на диск. Это inviolable: если LLM вернул что-то непарсимое — pipeline останавливается, source помечается `compile_state = "rejected"`, причина пишется в `vault/wiki/log.md` (одна строка) и в `vault/.review/rejections.jsonl` (детали).

В MVP — **pydantic-классы в коде**, без отдельных `.schema.json` файлов:

```python
from pydantic import BaseModel

class CuratorOutput(BaseModel):
    score: int  # 0..10
    reason: str
    suggested_topics: list[str]
    reject_reason: str | None = None

class CompilerOutput(BaseModel):
    source_metadata: SourceMetadata
    chunks: list[Chunk]
    claims: list[Claim]
    entities: list[Entity]
```

Pydantic сама генерирует JSON-schema по запросу (`Model.model_json_schema()`), если нужно отдать схему наружу. Хранить отдельный `.schema.json` файл = дублирование, разъезжается с pydantic-моделью.

Целевой output per role:

| Role | pydantic model | Required keys |
|---|---|---|
| Curator | `CuratorOutput` | `score`, `reason`, `suggested_topics`, `reject_reason?` |
| Compiler | `CompilerOutput` | `source_metadata`, `chunks[]`, `claims[]`, `entities[]` |
| Linker | `LinkerOutput` | `edges[]` (каждое — `src_id`, `dst_id`, `type`, `provenance`) |
| Note Builder | `NoteBuilderOutput` | `pages[]` (каждая — `id`, `type`, `path`, `frontmatter`, `body_markdown`) |

**Test fixtures:** 1 valid + 1 invalid на роль (всего 8 файлов). Negative-tests подтверждают, что pydantic ловит отсутствие обязательного поля или неверный enum. Расширение до 3+2 fixtures — когда LLM начнёт давать стабильные unexpected варианты в проде.

> **Отложено в [PRD/future/](../future/):** отдельные `<role>.schema.json` Draft 2020-12 файлы (нужны при cross-language exchange или для внешних агентов через MCP, M3+).

См. R3 llm-wiki-compiler (epistemic frontmatter, structured output) и R5 Basic Memory (`schema_infer/validate/diff`) в [Research: Reference Patterns](../research/reference-patterns.md).

## Two-Tier Model Split

Опыт R4 obsidian-llm-wiki-local показывает: имеет смысл расщепить вызовы по «весу» модели. Маппинг — короткая константа в коде (`MODEL_PER_ROLE`), не отдельный YAML:

| Tier | Модель | Роли |
|---|---|---|
| Fast | Claude Haiku 4.5 | Curator, Linker |
| Heavy | Claude Sonnet 4.6 | Compiler, Note Builder |

На потоке 2000 страниц/год экономия от fast-tier на Curator+Linker ≈ $120/год. Это уже в MVP, не «когда-нибудь».

Multi-vendor router (Azure / Grok) с per-vault `routing.yaml` отложен — добавляется только когда появится конкретная причина (rate-limits, vendor lock-in, cost-разница).

## Prompt Review

Every prompt must be reviewed against:

- role contract in [03 Agent Roles](03-agent-roles.md);
- page schema in [06 Page Schema](06-page-schema.md);
- language policy in [08 Language Policy](08-language-policy.md);
- pipeline writes in [04 Pipeline](04-pipeline.md);
- output JSON schema in `vault/schema/prompts/<role>.schema.json` (см. выше).

