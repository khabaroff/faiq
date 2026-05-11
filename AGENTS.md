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


<claude-mem-context>
# Memory Context

# [guides] recent context, 2026-05-11 10:58am GMT+4

Legend: 🎯session 🔴bugfix 🟣feature 🔄refactor ✅change 🔵discovery ⚖️decision 🚨security_alert 🔐security_note
Format: ID TIME TYPE TITLE
Fetch details: get_observations([IDs]) | Search: mem-search skill

Stats: 24 obs (12,751t read) | 215,185t work | 94% savings

### May 11, 2026
S328 Init: Explore GOO_LIBARCH/guides project structure, understand OpenSpec workflow, update CLAUDE.md with production guidance (May 11 at 10:06 AM)
S327 Initialize guides project by exploring directory structure and creating project configuration (May 11 at 10:06 AM)
732 10:07a 🔵 Project uses Beads (bd) for issue tracking with mandatory git push workflow
733 10:08a ✅ Updated CLAUDE.md with filled-in OpenSpec workflow and project structure
S329 User examined 5 reference repositories as context: usiki (Mnemon Knowledge Vault), usiki-docs (Russian knowledge vault), khabaroff-writer (Telegram bot), LAAI (knowledge system research), LAAI-refrepos (30+ reference projects). Goal: establish reference architecture and scope boundaries before active work. (May 11 at 10:08 AM)
734 10:13a 🔵 User's Multi-Repository Knowledge System Architecture
736 " ✅ Added Model Delegation and Context Management sections to guides CLAUDE.md
735 10:14a 🔵 LAAI PRD Documentation Structure and Operational Model
S330 Init: Establish OpenSpec workflow, project structure, and AI delegation patterns in guides project CLAUDE.md (May 11 at 10:14 AM)
S333 Review comprehensive architecture plan for guides/ — technical content pipeline project. User requested full plan examination and commentary. (May 11 at 10:15 AM)
737 10:17a 🔵 guides/task.md: Content Pipeline for Technical Learning Materials
738 " 🔵 usiki Mnemon Vault: Live Extract Example (YouTube Interview Transcription)
739 " 🔵 khabaroff-writer Deployment Architecture: Multi-Tier LLM Routing with Fallbacks
740 " 🔵 LAAI-refrepos Reference Inventory: 33 Knowledge System Implementations
741 10:18a ⚖️ Simple Cron-Based Content Pipeline Scope for task.md
742 10:24a ⚖️ guides/ Pipeline Architecture: Sequential Processing with Queue-Based Streams
743 10:28a ⚖️ guides/ content pipeline architecture — multi-stage async design
S334 Document and export guides/ pipeline architecture plan to project docs. User requested full plan be written to file and open for feedback. (May 11 at 10:29 AM)
S335 MVP Product Director analysis: Review guides pipeline plan and identify what to build vs. cut without over-engineering (May 11 at 10:30 AM)
745 10:41a ⚖️ Pipeline v1 Scope Reduction: Defer Complex Features
744 " ⚖️ MVP Scope: Cut 5 features, collapse streams, simplify structure
S336 Locate SENIOR and JUNIOR surfaces in cmux workspaces (May 11 at 10:43 AM)
746 10:50a ⚖️ MVP scope refined: explicit cuts from original pipeline plan
747 " ⚖️ Three unresolved architecture questions documented for MVP implementation
748 10:52a ✅ Pipeline plan refined and saved as v2: clean MVP architecture with 7 stages and 3 source types
750 10:54a ✅ Implementation plan created: 11 tasks from skeleton to VPS smoke test
749 10:55a 🔵 Located SENIOR and JUNIOR surfaces in cmux workspace
S337 Evaluate task management approaches for SENIOR and JUNIOR agent dispatch (May 11 at 10:56 AM)
751 10:57a 🔵 Beads (bd) task management tool is installed and available
752 " 🔵 SENIOR and JUNIOR are Claude agents with Azure Foundry MCP backends
753 " 🔵 Beads (bd) workflow conventions established for guides project
754 " 🔵 guides project MVP specification: content ingestion pipeline
755 " 🔵 Guides MVP implementation plan: 11 sequential tasks with verification

Access 215k tokens of past work via get_observations([IDs]) or mem-search skill.
</claude-mem-context>