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

# [guides] recent context, 2026-05-11 2:08pm GMT+4

Legend: 🎯session 🔴bugfix 🟣feature 🔄refactor ✅change 🔵discovery ⚖️decision 🚨security_alert 🔐security_note
Format: ID TIME TYPE TITLE
Fetch details: get_observations([IDs]) | Search: mem-search skill

Stats: 50 obs (15,758t read) | 210,549t work | 93% savings

### May 11, 2026
844 12:17p 🔵 LAAI Project Architecture: Three-Layer Wiki with Log-Driven Event Tracking
846 12:18p 🟣 Ingestion fixture matrix and smoke test completed
847 " 🔵 Task progression: fixture matrix closed; P0 pipeline MVP next ready
848 12:19p ✅ Smoke test validation requested for fixture matrix implementation
853 12:24p ✅ JUNIOR assigned integration validation task while SENIOR finishes
854 12:26p 🟣 Processor schema implementation completed and committed
856 " ✅ Schema enforcement implementation complete; P0 pipeline MVP unblocked
860 12:27p ✅ Reference document body section validation expanded
863 12:28p 🔵 Pipeline bug: verify() not receiving source_type parameter
864 " ✅ Prepare run.py fix for source_type parameter handling
865 12:29p ✅ Pipeline bug fixed: source_type parameter and frontmatter tags population
867 " 🔵 Frontmatter tags extraction failing: YAML list parsing issue
868 " ✅ Frontmatter parser enhanced to handle YAML list format
870 12:30p ✅ Project milestone: P0 content pipeline MVP completed; all tasks closed
871 12:33p ⚖️ Wiki V1 Architecture: Two-Zone Model with Source-Type Organization
872 12:34p 🟣 Wiki Schema Enforcement Across Processors and Verification
873 12:36p ⚖️ Wiki V1 Roadmap Created: Seven P1 Issues for Implementation
874 12:40p 🔵 ALF repository structure and composition
875 " 🔵 ALF (Adaptive Learning Feed) architecture and implementation status
876 " 🔵 Cost tracking and LLM routing infrastructure
888 12:52p 🟣 Wiki V1 filesystem layout fully implemented with dual-layer storage
889 " 🟣 Prompts adapted to dense Russian extract-page format for Wiki V1
890 " 🔵 Index rebuild system designed to populate from extract pages on first real pipeline run
891 12:58p 🔵 Wiki index generation task guides-qey completed and closed
892 " 🔵 Wiki V1 schema implementation checkpoint: 4 major tasks completed, 1 in progress
893 " ⚖️ Task dispatch: Cost accounting helper (guides-p53) assigned to JUNIOR
894 12:59p ⚖️ Task decomposition: guides-oio split into sequential curation phases
895 1:00p 🟣 Cost accounting module guides-p53 completed and committed
896 " 🟣 Wiki V1 prompt adaptation guides-ley completed
897 " 🔵 Wiki V1 infrastructure complete: 6 tasks shipped in single session
898 " ✅ Task queue evolved: Wiki V1 + accounting complete, next phase is corpus curation and validation
899 1:01p 🔵 Next phase tasks planned: cost reporting + corpus curation for smoke testing
900 " ⚖️ Three testing/reporting tasks claimed and dispatched
901 " ⚖️ Corpus curation tasks dispatched: ALF and LAAI candidate selection
902 " 🔵 Progress on cost report and corpus curation; JUNIOR hit permission check
908 1:02p 🔵 JUNIOR scanning ALF and LAAI corpus; SENIOR building cost report script
914 1:06p 🟣 Cost report script guides-0sq created and staged in git
917 " 🟣 Cost accounting integration verified in guides/llm.py call_llm()
918 1:07p 🔵 Deployment names configured in settings.py for cost tracking
S386 Complete Wiki V1 pipeline infrastructure setup and preparation. Prepare clean environment for end-to-end pipeline test (guides-5ei). Monitor parallel agent execution (SENIOR Langfuse, JUNIOR pipeline test). (May 11 at 1:14 PM)
S400 Monitor agents (SENIOR surface:23, JUNIOR surface:12) in workspace:5 every 2 minutes: detect "TASK N DONE" markers, close completed tasks via bd, dispatch next work from bd ready queue (May 11 at 1:15 PM)
S401 Monitor two parallel agents (SENIOR/JUNIOR) every 2 minutes to manage Wiki V1 infrastructure completion: detect task completion markers, close finished tasks, and dispatch next work from task queue (May 11 at 1:16 PM)
S402 Continuous /loop monitoring of two Claude agents (SENIOR/surface:23, JUNIOR/surface:12) in workspace:5 via cmux, dispatching tasks from bd queue every 2 minutes, detecting completion markers and managing task lifecycle (May 11 at 1:34 PM)
S403 Monitor two Claude agents (SENIOR/surface:23, JUNIOR/surface:12) in workspace:5, dispatch Wiki V1 infrastructure tasks from bd queue every 2 minutes, detect completion markers, manage task lifecycle until pipeline finalization (May 11 at 1:34 PM)
S404 Continue /loop monitoring of two agents (SENIOR/surface:23 patching wiki.py, JUNIOR/surface:12 validating source/output pairs). Maintain 2-minute polling interval, await task completion markers, dispatch next work items. (May 11 at 1:40 PM)
S406 Set up multi-agent task supervision system with autonomous task distribution and monitoring loop between SENIOR and JUNIOR agents (May 11 at 1:41 PM)
S407 Multi-agent task supervision: recovering SENIOR agent from Gemini API error, JUNIOR continues processing (May 11 at 2:05 PM)
S408 Multi-agent task supervision: recover SENIOR from error, dispatch concurrent tasks, autonomous monitoring (May 11 at 2:05 PM)
956 2:06p 🔵 SENIOR agent recovered from Gemini API error
957 " 🟣 guides-9yn task dispatched to SENIOR: concurrent pipeline duplicate protection verification
958 " 🔵 SENIOR: pytest dependency missing in project venv
959 " 🔵 JUNIOR appears hung or unresponsive to input
960 2:07p 🔵 Supervisor prompts JUNIOR for status/completion after hung state
961 " 🔵 JUNIOR responsive: shows progress on ongoing task (~50% complete)
962 " 🟣 SENIOR successfully ran pipeline lock test — test passed
963 " 🟣 SENIOR analyzing and fixing redundant processing logic
964 " 🟣 JUNIOR completed guides-e1s task — completion signal detected
965 2:08p 🔵 guides-e1s closed successfully, task queue stalled on blocking dependencies
966 " ✅ Supervisor notified JUNIOR: task queue blocked, agent to idle
S409 Multi-agent task supervision: manage concurrent work on guides backlog, handle dependency blocking, autonomous agent monitoring (May 11 at 2:08 PM)
**Investigated**: SENIOR: pipeline lock mechanism verification (test passed 1/1), redundant processing fix implementation. JUNIOR: URL extraction task from file contents (completed). Task queue state: blocked on dependencies. Agent error recovery: /clear context reset effectiveness.

**Learned**: Agent recovery pattern: context reset via /clear successful for protocol errors. Test validation via direct Python when pytest unavailable. Task completion signaling: agents write "TASK N DONE" marker. Queue blocking: dependent tasks cannot progress until prerequisites complete. Multi-agent concurrency: both agents work independently, supervisor coordinates via cmux surfaces and bd task system.

**Completed**: JUNIOR completed guides-e1s task (URL extraction utility). Task closed in bd. SENIOR verified test_process_stream_lock.py passes (1 test, 0.001s). SENIOR reading code files (process_stream.py, validation logic). Supervisor recovered from Gemini API errors via context reset. Autonomous 2-minute monitoring loop active.

**Next Steps**: SENIOR finalizing guides-9yn: complete redundant processing fix analysis and document findings. JUNIOR idle waiting for task queue unblock (blocked on dependency resolution). Supervisor checks both agents every 2 minutes (next at 14:11 UTC). Monitor for SENIOR completion signal "TASK guides-9yn DONE" and close task when ready.


Access 211k tokens of past work via get_observations([IDs]) or mem-search skill.
</claude-mem-context>