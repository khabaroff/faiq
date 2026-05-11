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

# [guides] recent context, 2026-05-11 8:34pm GMT+4

Legend: 🎯session 🔴bugfix 🟣feature 🔄refactor ✅change 🔵discovery ⚖️decision 🚨security_alert 🔐security_note
Format: ID TIME TYPE TITLE
Fetch details: get_observations([IDs]) | Search: mem-search skill

Stats: 50 obs (14,887t read) | 219,046t work | 93% savings

### May 11, 2026
1074 2:50p ✅ Tasks claimed and URL test dispatched to JUNIOR
1076 " ✅ Mixed file handling task dispatched to SENIOR
1080 2:51p 🔵 SENIOR completed mixed file handling implementation
1081 " 🔵 JUNIOR hit Azure API rate limit while processing URL
1082 " ✅ guides-45u closed. Git shows 9-line mixed file handling implementation
1083 " 🔵 Task queue shows blocking dependencies, no ready work available
1085 " ✅ New task created: commit mixed-file code and audit wiki indexes
1086 " ✅ Task guides-4rb claimed and dispatched to SENIOR for commit + index audit
1087 2:52p 🔵 Pipeline processes Martin Fowler distributed systems article end-to-end
1090 " 🔵 Wiki vault contains 10 extracted documents; 57 LLM calls logged with cost tracking
1091 " ✅ Both remaining tasks closed: complete work cycle finished
1092 " 🔵 needs_review.txt shows Settings validation failures in queue
1093 " 🔵 Wiki extracts organized by content type: articles, githubs, notes, pdfs, youtubes
1094 2:53p 🔵 Pipeline uses two-stage LLM processing per document: gpt-5.4 → gpt-5.4-mini
1095 " ✅ Two new multi-format source tests created: GitHub and YouTube ingestion
1096 " ✅ GitHub and YouTube ingestion tests dispatched to both agents
1099 " 🔵 YouTube test incomplete: youtubes/ directory empty, no test file created
1100 2:54p 🔵 SENIOR completed GitHub test: repo extraction and wiki generation successful
S429 Recover guides-y4y task execution after Gemini API error; request SENIOR to continue work or report status (May 11 at 3:21 PM)
S431 Plan next phase of development in guides project after completing 5 feature tasks and closing all open issues (May 11 at 3:22 PM)
S432 Plan next phase of guides project development; clarify direction after completing 5 feature tasks (May 11 at 3:22 PM)
S433 Continuous monitoring and planning status during agent infrastructure outage (May 11 at 3:36 PM)
S434 Plan next development phase; awaiting user direction while agents remain non-functional (May 11 at 3:36 PM)
S435 Plan and execute next development phase after completing 5 core features; agents non-functional, awaiting direction (May 11 at 3:37 PM)
S436 Continue session after queue emptied; assess current status and plan next work (May 11 at 3:38 PM)
S437 Assess queue state and identify next work: add new URLs, fix gist URL support, or other tasks (May 11 at 8:21 PM)
1147 8:21p 🔵 Wiki extracts inventory and directory structure
1149 8:22p 🔵 GitHub gist fetch failures in needs_review queue
1150 " 🔵 Inbox queue state: one YouTube video processed
S442 Fix GitHub gist URL routing and implement end-to-end processing with graceful fallback (continuation from prior session) (May 11 at 8:22 PM)
1153 " 🔵 URL fetcher architecture: multi-strategy chain for content extraction
1155 " 🔵 GitHub URL routing excludes gist URLs; root cause of fetch failures
1156 " 🔵 Fetch module architecture: specialized handlers for source types
1158 " 🔵 Cost tracking and LLM accounting system implemented
1159 8:23p 🔵 Cost tracking integrated with Langfuse distributed tracing
1160 " 🔵 All 13 wiki extracts have quality_score in frontmatter; 100% coverage
1161 " 🔵 Pipeline logs structure and Azure OpenAI integration details
1162 " 🔵 Processing high-complexity documents: Knowledge Unit specification ingestion
1163 " 🔵 Pipeline log truncation issue: llm_call entries exist but grep output truncated
1164 " 🔵 Complete LLM cost aggregation: 84 calls, $3.09 total cost across batch processing
1165 " 🔵 Task-specific model routing: gpt-5.4-mini for classification, gpt-5.4 for synthesis
1166 8:24p 🔵 Model routing architecture: call_smart vs call_fast with conditional deployment selection
1167 " 🔵 Task-level deployment selection: tags.py uses fast, article.py uses smart
1168 " 🔵 Hierarchical chunking for long-form content: 25k character chunks with merge pass
1169 " ✅ Added GITHUB_GIST source type enum value
1170 " ✅ Added gist URL detection to routing logic; now classifies gist.github.com URLs separately
1171 8:25p 🟣 GitHub gist fetcher implemented: fetch_github_gist with multi-file formatting
1172 " 🟣 Pipeline routing updated for GitHub gist support; gist URLs now processed end-to-end
1173 " ✅ GitHub gist wiki classification updated: gists now treated as references, not articles
1174 " ✅ YouTube chunking optimized for cost: per-chunk summaries now use fast model (gpt-5.4-mini)
1175 " 🔵 Cost reporting CLI tool: scripts/cost_report.py aggregates LLM usage by model and date
1176 8:26p 🔵 Cost report execution confirms end-to-end cost tracking: $3.09 for 84 LLM calls
1177 " ✅ GitHub gist URL added to inbox queue; detection verified working
1178 " 🔵 Missing dependency blocks queue execution: pydantic_settings not installed
1179 " 🔵 Gist URL in queue but not yet processed; remains unparsed in inbox.txt
1181 " 🔵 Queue processor is library module, not executable script; missing __main__ entry point
1183 " 🟣 Gist URL processed via process_stream.py entry point; dedup check marked as already processed
1185 8:27p 🔵 Previous gist processing failed with "gist_not_supported" error; old failure entry blocking reprocess
1187 " 🔵 Gist URL failed silently on reprocess; no entry in sources directory
S443 Audit and fix GitHub gist URL pipeline issues; document configuration gaps and cost optimization opportunities (May 11 at 8:32 PM)
**Investigated**: - Settings.py configuration structure (Azure OpenAI, GitHub token, Jina, Langfuse)
    - Runtime config state: github_token MISSING, azure_deployment_smart=gpt-5.4, azure_deployment_fast=gpt-5.4-mini
    - defuddle-cli availability and command structure (v0.1.0 via npx, requires "parse" subcommand)
    - HTTP markdown behavior on gist.github.com (404) vs raw.githubusercontent.com (200 OK, 16.4KB)
    - Fetcher fallback chain: defuddle → Jina → http-markdown
    - Cost tracking: 86 calls, 657K tokens, $3.22 total

**Learned**: - defuddle-cli has required subcommand "parse"; code called without it → always failed silently → fell back to Jina
    - GitHub API anonymous rate limit: 60 req/hour, triggers 502 on limit overflow (no auth token configured)
    - Gist URLs return 404 on direct HTTP; need GitHub API (/gists/{id}) or Jina reader proxy
    - raw.githubusercontent.com serves markdown as plain text/plain content-type (not text/markdown), still parseable
    - http-markdown filter rejects text/html content-type (correct design, filters out web pages)
    - Model routing: gpt-5.4 (smart, expensive) used for article rewrite; gpt-5.4-mini (fast) for YouTube chunks
    - Cost per document: $3.22 ÷ 13 docs = $0.24/doc (high due to gpt-5.4 volume)

**Completed**: - Fixed defuddle-cli subprocess calls: added "parse" subcommand in both npx and local paths (lines 32, 39)
    - Test confirmed fix: `npx defuddle-cli parse https://example.com` returns 186 bytes (works)
    - Created docs/todo.md with 7 prioritized issues, config status table, 4 improvements, cost analysis
    - Committed: "fix(fetch): correct defuddle-cli subcommand + add todo doc" (2 files, 90 insertions)
    - Documented critical gaps: GITHUB_TOKEN (rate limit fix), Jina API key (throttle lift), needs_review cleanup

**Next Steps**: Address critical config items from TODO:
    1. Add GITHUB_TOKEN to .env (PAT with gist read scope) → eliminates 502 errors on rate limit
    2. Add jina_api_key to Settings.py and pass Bearer auth to _try_jina() → lift 5 req/min throttle
    3. Implement README fallback (main → master → HEAD) in fetch_github_repo()
    4. Test defuddle fallback path on real article URLs to verify "parse" subcommand fix works end-to-end
    5. Optional: migrate article rewrite from gpt-5.4 to gpt-5.4-mini for cost reduction (~80% savings)


Access 219k tokens of past work via get_observations([IDs]) or mem-search skill.
</claude-mem-context>