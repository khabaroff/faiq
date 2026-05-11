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

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pure spec repository — no application code. Uses OpenSpec for spec-driven development. Fill in `openspec/project.md` with project-specific context.

## Setup

```bash
npm install -g @fission-ai/openspec@latest
```

## Key Commands

```bash
openspec list                                         # Active change proposals
openspec list --specs                                 # All specifications
openspec show [item]                                  # Change or spec details
openspec show [change] --json --deltas-only           # Debug delta parsing
openspec validate [change] --strict --no-interactive  # Validate before sharing
openspec archive <change-id> --yes                    # Archive after deployment
rg -n "Requirement:|Scenario:" openspec/specs         # Full-text search
```

## Three-Stage Workflow

**Stage 1 — Propose:** Scaffold `openspec/changes/<id>/` with `proposal.md`, `tasks.md`, and delta specs under `specs/<capability>/spec.md`. Run validate. Wait for approval before Stage 2.

**Stage 2 — Implement:** Follow `tasks.md` sequentially. Mark all items `[x]` only after everything is done.

**Stage 3 — Archive:** `openspec archive <change-id> --yes`, then validate to confirm.

## Directory Structure

```
openspec/
├── project.md          # Project conventions — read this first
├── specs/              # Truth: what IS built (capability/spec.md)
├── changes/            # Proposals: what SHOULD change
│   ├── <change-id>/
│   │   ├── proposal.md
│   │   ├── tasks.md
│   │   ├── design.md   # Optional; only for cross-cutting/complex changes
│   │   └── specs/<capability>/spec.md  # Deltas: ADDED/MODIFIED/REMOVED
│   └── archive/        # Completed changes
```

## Spec Format Rules

- Scenarios: `#### Scenario: Name` (4 hashtags — not bullets, bold, or 3 hashtags)
- Every requirement needs at least one scenario
- Requirements use SHALL/MUST (not should/may)
- MODIFIED deltas must include full requirement text (archiver replaces entire block)
- Change IDs: kebab-case, verb-led (`add-`, `update-`, `remove-`, `refactor-`)

## Skip Proposals For

Bug fixes restoring intended behavior, typos/formatting, non-breaking dependency updates, config changes, tests for existing behavior.

## Model Delegation

Принцип: Opus = мозг, делегируй всё что не требует стратегического мышления. Не спрашивай — делегируй сразу.

**→ Haiku** (`Agent(subagent_type="Explore", model="haiku")`):
- Поиск по репо больше 1 файла, grep по содержимому, обход структуры
- Проверка "существует ли X", "найди все упоминания Y"

**→ Sonnet** (`Agent(subagent_type="general-purpose", model="sonnet")`):
- Правка/написание текста > 50 строк
- Параллельные независимые подзадачи (несколько Sonnet-агентов сразу)

**Opus сам:**
- Архитектура, стратегия, оценка качества, выбор между вариантами
- Короткие задачи < 30 сек — делегация дороже выполнения

**Subagent fallback:** если субагент не может писать файлы из-за прав — главный агент завершает запись сам.

**Пометки в ответах:** `[Haiku] ищу X...` / `[Sonnet] правлю Y...`

## Context Management

Sonnet 4.6 — 200K (autocompact на ~80%). При деградации (путаница имён, повторение обсуждённого) — сообщай сразу. Для многошаговых задач: после каждой фазы — короткий summary.


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
