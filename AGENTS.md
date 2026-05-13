<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

## Skills
A skill is a set of local instructions to follow that is stored in a `SKILL.md` file. Below is the list of skills that can be used. Each entry includes a name, description, and file path so you can open the source for full instructions when using a specific skill.
### Available skills
- brainstorming: You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation. (file: /Users/khabaroff/.codex/superpowers/skills/brainstorming/SKILL.md)
- dispatching-parallel-agents: Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies (file: /Users/khabaroff/.codex/superpowers/skills/dispatching-parallel-agents/SKILL.md)
- executing-plans: Use when you have a written implementation plan to execute in a separate session with review checkpoints (file: /Users/khabaroff/.codex/superpowers/skills/executing-plans/SKILL.md)
- finishing-a-development-branch: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup (file: /Users/khabaroff/.codex/superpowers/skills/finishing-a-development-branch/SKILL.md)
- linear: Manage issues, projects & team workflows in Linear. Use when the user wants to read, create or updates tickets in Linear. (file: /Users/khabaroff/.codex/skills/linear/SKILL.md)
- linear-studio: Project Manager для Software, SaaS и digital-проектов команды "KS". Управление задачами в Linear - отслеживание подвисших тикетов, актуализация заголовков, комментирование, эскалации, статус-репорты. Автоматически использует team="KS". (file: /Users/khabaroff/.codex/skills/linear-studio/SKILL.md)
- receiving-code-review: Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation (file: /Users/khabaroff/.codex/superpowers/skills/receiving-code-review/SKILL.md)
- requesting-code-review: Use when completing tasks, implementing major features, or before merging to verify work meets requirements (file: /Users/khabaroff/.codex/superpowers/skills/requesting-code-review/SKILL.md)
- subagent-driven-development: Use when executing implementation plans with independent tasks in the current session (file: /Users/khabaroff/.codex/superpowers/skills/subagent-driven-development/SKILL.md)
- systematic-debugging: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes (file: /Users/khabaroff/.codex/superpowers/skills/systematic-debugging/SKILL.md)
- test-driven-development: Use when implementing any feature or bugfix, before writing implementation code (file: /Users/khabaroff/.codex/superpowers/skills/test-driven-development/SKILL.md)
- using-git-worktrees: Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated git worktrees with smart directory selection and safety verification (file: /Users/khabaroff/.codex/superpowers/skills/using-git-worktrees/SKILL.md)
- using-superpowers: Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before ANY response including clarifying questions (file: /Users/khabaroff/.codex/superpowers/skills/using-superpowers/SKILL.md)
- verification-before-completion: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always (file: /Users/khabaroff/.codex/superpowers/skills/verification-before-completion/SKILL.md)
- writing-plans: Use when you have a spec or requirements for a multi-step task, before touching code (file: /Users/khabaroff/.codex/superpowers/skills/writing-plans/SKILL.md)
- writing-skills: Use when creating new skills, editing existing skills, or verifying skills work before deployment (file: /Users/khabaroff/.codex/superpowers/skills/writing-skills/SKILL.md)
- skill-creator: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Codex's capabilities with specialized knowledge, workflows, or tool integrations. (file: /Users/khabaroff/.codex/skills/.system/skill-creator/SKILL.md)
- skill-installer: Install Codex skills into $CODEX_HOME/skills from a curated list or a GitHub repo path. Use when a user asks to list installable skills, install a curated skill, or install a skill from another repo (including private repos). (file: /Users/khabaroff/.codex/skills/.system/skill-installer/SKILL.md)
### How to use skills
- Discovery: The list above is the skills available in this session (name + description + file path). Skill bodies live on disk at the listed paths.
- Trigger rules: If the user names a skill (with `$SkillName` or plain text) OR the task clearly matches a skill's description shown above, you must use that skill for that turn. Multiple mentions mean use them all. Do not carry skills across turns unless re-mentioned.
- Missing/blocked: If a named skill isn't in the list or the path can't be read, say so briefly and continue with the best fallback.
- How to use a skill (progressive disclosure):
  1) After deciding to use a skill, open its `SKILL.md`. Read only enough to follow the workflow.
  2) When `SKILL.md` references relative paths (e.g., `scripts/foo.py`), resolve them relative to the skill directory listed above first, and only consider other paths if needed.
  3) If `SKILL.md` points to extra folders such as `references/`, load only the specific files needed for the request; don't bulk-load everything.
  4) If `scripts/` exist, prefer running or patching them instead of retyping large code blocks.
  5) If `assets/` or templates exist, reuse them instead of recreating from scratch.
- Coordination and sequencing:
  - If multiple skills apply, choose the minimal set that covers the request and state the order you'll use them.
  - Announce which skill(s) you're using and why (one short line). If you skip an obvious skill, say why.
- Context hygiene:
  - Keep context small: summarize long sections instead of pasting them; only load extra files when needed.
  - Avoid deep reference-chasing: prefer opening only files directly linked from `SKILL.md` unless you're blocked.
  - When variants exist (frameworks, providers, domains), pick only the relevant reference file(s) and note that choice.
- Safety and fallback: If a skill can't be applied cleanly (missing files, unclear instructions), state the issue, pick the next-best approach, and continue.

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:7510c1e2 -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

**Architecture in one line:** issues live in a local Dolt DB; sync uses `refs/dolt/data` on your git remote; `.beads/issues.jsonl` is a passive export. See https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md for details and anti-patterns.

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
<!-- END BEADS INTEGRATION -->

## Project: Guides — AI Lecture Prep System

### What this project does

Статьи/видео/PDF → автоматические русские саммари → wiki-граф инструментов → Obsidian + сайт на Quartz.

Подробнее: `_human/how-it-works.md` (для людей), `_human/processes.md` (все роботы и форматы).

### Key directories

```
src/guides/           ← весь Python-код
  pipelines/          ← a_ingest, b_summarize, c_wiki_update, d_quality_check, e_seo, g_telegram
  fetch/              ← url.py, github.py, pdf.py, youtube.py
  tools/              ← build_indexes, cost_report, daily_log, link_checker, validate_wiki
prompts/              ← LLM-промпты (summary.md, wiki_tool_update.md, seo.md, telegram_post.md)
public/               ← Obsidian vault + Quartz output
  sources/            ← отформатированные исходники
  summaries/          ← русские саммари
  tools/              ← wiki-страницы инструментов
  techniques/         ← wiki-страницы паттернов (frontmatter type: pattern)
  index/              ← семантические индексы (tools, patterns, concepts...)
data/inbox/           ← кидать сюда (файлы/URL-списки)
data/inbox/done/      ← архив обработанных
state/                ← SQLite БД (articles.db) и отчеты
```

### Running pipelines

```bash
# полный цикл (A → B → C → D → E → G)
python -m guides.pipelines.run_all

# по одному
python -m guides.pipelines.a_ingest           # fetch → public/sources/
python -m guides.pipelines.b_summarize        # summarize → public/summaries/
python -m guides.pipelines.c_wiki_update      # tools/patterns wiki pages
python -m guides.pipelines.d_quality_check    # hallucination/dedup check
python -m guides.pipelines.e_seo              # SEO title/description
python -m guides.pipelines.g_telegram         # post to Telegram channel

# инструменты
python -m guides.tools.build_indexes          # собрать семантические индексы
python -m guides.tools.cost_report            # отчёт по расходам
python -m guides.tools.daily_log              # дневной лог операций
python -m guides.tools.link_checker           # поиск битых ссылок
python -m guides.tools.validate_wiki          # валидация формата страниц
```

### LLM routing

- **gpt-5.4-mini** (`AZURE_DEPLOYMENT_FAST`): OCR картинок, саммари < 15K токенов, wiki-update, quality-check
- **gpt-5.4** (`AZURE_DEPLOYMENT_SMART`): OCR PDF, саммари ≥ 15K токенов

### Format invariants (never break these)

1. `public/sources/*.md` — всегда начинается с YAML frontmatter (`title`, `slug`, `source_url`, `source_type`, `fetched_at`, `lang`)
2. `public/summaries/*.md` — YAML frontmatter с `tools: [...]` и `patterns: [...]` (списки строк), тело с `[[wikilinks]]`
3. `public/tools/*.md` и `public/techniques/*.md` — YAML frontmatter с `name`, `slug`, `type`, `created_at`, `updated_at`
4. slug = `slugify(title)[:80]` — единственный идентификатор артикула

### Testing

```bash
python -m pytest tests/
```

<claude-mem-context>
# Memory Context

# [guides] recent context, 2026-05-11 10:33pm GMT+4

Legend: 🎯session 🔴bugfix 🟣feature 🔄refactor ✅change 🔵discovery ⚖️decision 🚨security_alert 🔐security_note
Format: ID TIME TYPE TITLE
Fetch details: get_observations([IDs]) | Search: mem-search skill

Stats: 50 obs (16,353t read) | 230,940t work | 93% savings

### May 11, 2026
S437 Assess queue state and identify next work: add new URLs, fix gist URL support, or other tasks (May 11 at 8:21 PM)
S442 Fix GitHub gist URL routing and implement end-to-end processing with graceful fallback (continuation from prior session) (May 11 at 8:22 PM)
S443 Audit and fix GitHub gist URL pipeline issues; document configuration gaps and cost optimization opportunities (May 11 at 8:27 PM)
S445 Audit pipeline configuration, identify bugs in fetchers, document issues and fixes (May 11 at 8:32 PM)
S450 Understand and document how to add annotated links (URL + comment) as files in the guides system (May 11 at 8:34 PM)
S451 Observe primary Claude session: guides-nt5 src layout refactoring task completion and pipeline testing with real inbox data (May 11 at 9:11 PM)
1262 9:26p ✅ Fixed sitecustomize.py: src/ now in sys.path
1263 " 🔵 Full test suite passes with src/ layout
1268 9:29p ⚖️ PDF OCR fallback + inbox archiving implementation plan
1269 9:30p ⚖️ Implementation plan: PDF OCR fallback and inbox file archiving
1270 " 🔵 process_stream.py located at src/process_stream.py; currently deleted in working tree
1271 9:32p 🔵 src/process_stream.py implements inbox queue processing with lock-based concurrency control
1272 " ✅ Implementation plan progress: moved to failing test phase
1273 " 🔵 Scripts directory isolated from main codebase references
1274 " 🟣 Created failing tests for PDF OCR fallback and inbox archiving
1275 " 🔄 Migrated reprocess_stale.py to src/guides/tools/
1277 9:33p 🔄 Migrated cost_report.py to src/guides/tools/
1276 " 🔵 Failing tests confirm expected behavior gaps for OCR fallback and inbox archiving
1278 " 🔵 Tools migration verified: module imports work, tests pass
1279 9:35p 🟣 Implemented PDF OCR fallback and inbox file archiving
1280 " 🟣 All tests passing: PDF OCR fallback and inbox archiving complete
1281 " 🔵 Full regression test suite passing: 17/17 tests
1282 " ✅ Marked all implementation tasks complete in OpenSpec
1283 9:36p ✅ OpenSpec validation passed and project closed
1284 " ✅ All implementation plan steps marked completed
1286 9:42p 🔵 guides-nt5 task: refactor package to src layout
1287 " 🔵 process_stream.py already refactored to src layout with guides imports
1288 " ✅ Fixed process_stream module invocation path in reprocess_stale output
1289 " 🟣 Created smoke_test.py in src/guides/tools with full guides package imports
1290 9:43p 🟣 Created test_queue.py in src/guides/tools with queue classification tests
1291 " ✅ Removed src/smoke_test.py - old location consolidation
1292 " ✅ Consolidated tools from src root to src/guides/tools directory
1293 " 🔵 Test suite passes with src layout migration complete
1294 " ⚖️ guides-nt5 task completed and closed
1295 9:44p 🔵 Inbox queue system state: 9 pending items, archive directory not yet created
1300 9:47p ✅ Reset pipeline state and vault output
1302 " 🔴 Pipeline fails to handle missing data/sources directory gracefully
1303 " ✅ Created missing pipeline state directories and re-ran pipeline
1304 " 🔵 Pipeline second run appears to hang, no new log entries or output
1305 9:48p 🔵 Pipeline runs but fails on network connectivity - no internet access
S452 Process inbox files through vault.py extraction pipeline and fix blocking behavior on needs_review pages (May 11 at 9:48 PM)
1307 9:51p 🔵 Pipeline processing failures with universal connection errors
1308 9:52p 🔵 LLM module uses Azure OpenAI with usage instrumentation
S460 Implement wiki page format validator for guides-idm task — add post-processing validation gate that detects format violations and auto-fixes simple cases before storage. (May 11 at 9:59 PM)
1324 10:07p ✅ Wiki quality issues identified and captured as tracked tasks
1325 10:10p ✅ Task dependencies added to structure wiki remediation workflow
1326 " ✅ Wiki remediation workflow dependency graph established
1327 10:15p ✅ Wiki format enforcement task claimed and started
1328 10:18p 🔵 Wiki processing pipeline has cleanup but no format validation gates
1329 10:19p 🟣 Wiki validator with rejection and autofix for format violations
1330 " 🟣 CLI tool for batch wiki validation and autofix
S461 Implement wiki page format validator for guides-idm task; add validation gates that detect format violations and auto-fix simple cases before storage. (May 11 at 10:20 PM)
1333 10:22p 🟣 Comprehensive test suite for wiki validator
1335 " ✅ Task guides-idm closed: wiki validator implementation complete
S462 Run validator on existing wiki corpus to check format compliance; identify remaining issues after bulk autofix application. (May 11 at 10:23 PM)
1338 10:23p 🔵 guides-dux task: rework quality scoring and verification thresholds
1340 10:24p 🔵 Current wiki quality score distribution is coarse and clustered
1342 " 🔵 Quality score calculation pipeline identified
1343 " 🔵 Current quality_score calculation is binary check-based with uniform weights
1361 10:32p ✅ Expanded _HEADING_MAP with 22 new heading translations

Access 231k tokens of past work via get_observations([IDs]) or mem-search skill.
</claude-mem-context>