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

[To be filled: Brief description of what this project does]

## OpenSpec Workflow

This project uses OpenSpec for spec-driven development. Always check `@/openspec/AGENTS.md` when working with proposals, specs, or planning changes.

### Key Commands

```bash
# View active changes and specs
openspec list                  # List active change proposals
openspec list --specs          # List all specifications
openspec show [item]           # View change or spec details

# Create and validate proposals
openspec validate [change] --strict --no-interactive  # Validate changes
openspec archive <change-id> --yes  # Archive completed change

# Project context
# Edit openspec/project.md to add project-specific context
```

### When to Create Proposals

Create OpenSpec change proposal for:

- New features or capabilities
- Breaking changes (API, schema, architecture)
- Performance/security work that changes behavior

Skip proposals for:

- Bug fixes (restoring intended behavior)
- Typos, formatting, comments
- Dependency updates (non-breaking)

See `openspec/AGENTS.md` for complete workflow details.

## Development Commands

### Setup

```bash
npm install -g @fission-ai/openspec@latest
# [Add additional installation/setup commands here]
```

### Build & Run

```bash
# [Add build commands]
# [Add run/start commands]
```

### Testing

```bash
# [Add test commands]
# [Add single test run command if applicable]
```

### Linting & Formatting

```bash
# [Add linting commands]
# [Add formatting commands]
```

## Architecture

[To be filled: High-level architecture overview that requires understanding multiple files]

### Key Patterns

[To be filled: Important architectural patterns, design decisions, or conventions used in this codebase]

### Directory Structure

[To be filled: Only non-obvious structural decisions that affect how code should be organized]

## Important Notes

[To be filled: Project-specific context that would be difficult to discover by reading individual files]


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
