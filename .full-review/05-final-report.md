# Comprehensive Code Review Report — faiq/Guides

## Review Target

Полный Python-кодбаз `src/guides/` (27 модулей, ~3569 LOC) + `tests/` (14 файлов) + `prompts/` (6 LLM-промптов). Pipeline A→B→C→D→E→G, Azure OpenAI dual routing, SQLite state, Obsidian + Quartz + Telegram surfaces.

Commit `bfbfa7c`. Started 2026-05-13T14:44:28Z. Framework: Python 3.13, uv, pytest 9. Flags: security_focus=no, performance_critical=no, strict_mode=no.

## Executive Summary

Намерение пайплайна продумано: security helpers есть, prompts включают injection-warning, slug-валидация работает, idempotency-флаги в SQLite спроектированы. **Но**: helpers подключены лишь в малую долю attack surface; реализация рассыпается на 3-4 несогласованных способа делать одно и то же (slugify×3, YAML emit×3, JSON regex×4, frontmatter parser×2). Самые опасные пути — SSRF в `fetch/url.py` и stored-XSS через LLM-output → disk — открыты по умолчанию. Cost-leak в Pipeline D без идемпотентности при росте до 10K статей стоит ~$100/ночь.

Архитектурно: одна Settings не владеет `public/`; `state.py` течёт SQL и стартует миграцию при импорте; нет CI; нет бэкапа `state/articles.db`. **235 findings суммарно, 37 Critical.**

## Findings by Priority

### Critical (P0 — fix immediately)

**Security / data integrity:**
- SSRF в `fetch/url.py` / `github.py` / `jina.py` — `validate_url` не подключён к основному ingest path. AWS metadata → Telegram. (Phase 2A C1) → **guides-7al**
- `npx -y defuddle-cli` per ingest — unpinned supply chain. (Phase 2A C4) → **guides-vld**
- LLM `page_md` → `write_text` без санитизации → stored XSS / Quartz injection. (Phase 2A C3, H1) → **guides-u40**
- Path-traversal defense-in-depth: `canonicalize_slug` fallback обходит `assert_safe_slug` если убрать второй guard. (Phase 2A C2) → **guides-cxj** (slugify unify)
- Pipeline D затирает wiki-страницы без бэкапа. (Phase 1A) → **guides-9xm**
- `parse_frontmatter` ломается на теле с `\n---\n`. (Phase 1A) → **guides-rlj**
- `state.py` модульные side-effects (init_db + JSON-миграция при import); connect-per-call → race при `--workers 4`. (Phase 1A, 1B C3) → **guides-ldh**
- `llm._extract_response_text` пустой ответ молча проходит, помечает summary как готовый. (Phase 1A) → **guides-8pp**
- `get_state` падает если ALTER не сделан. (Phase 1A) → **guides-yri**

**Architecture:**
- Hard-coded paths (`ROOT`/`CONTENT_DIR`/`SUMMARIES_DIR`) дублируются в 6+ модулях. Settings не владеет `public/`. (Phase 1B C1) → **guides-tg0**
- State schema drift: SQLite колонки vs frontmatter-writers (3 разных) vs prompt-emitted YAML — не унифицированы. (Phase 1B C2) → **guides-qfz**

**Performance / cost:**
- SQLite connect-per-call + no `busy_timeout` + WAL race под `--workers 4` → silent slug loss. (Phase 2B P-C1) → **guides-ldh**
- N×UPSERT per slug (3-5 транзакций × fsync). (Phase 2B P-C2) → **guides-ldh**
- Token router: `len(text)//4` занижает кириллицу в ~2× → retry-шторма. (Phase 2B P-C3) → **guides-lmk**
- Pipeline D без идемпотентности — $10/ночь при 1000, $100/ночь при 10K статей. (Phase 2B P-C4) → **guides-9hk**
- No retry/backoff на 429/500. (Phase 2B P-C5) → **guides-f9y**

**Frameworks / CI:**
- Vanilla `OpenAI` против Azure endpoint; `azure_openai_api_version` dead config. (Phase 4A F-C1) → **guides-6zu**
- `d_quality_check.py` импортирует `guides.log_setup` — модуля нет. (Phase 4A F-C2; Phase 3B D-C3) → **guides-13n**
- `requires-python>=3.11` + `ruff target=py311` при runtime 3.13/3.14. (Phase 4A F-C4) → **guides-kie**
- Нет CI/CD вообще — 235 findings без enforcement. (Phase 4B CD-C1) → **guides-95a**
- Нет бэкапа `state/articles.db`. (Phase 4B CD-C2) → **guides-ipz**
- Secrets в plaintext `.env`, нет ротации. (Phase 4B CD-C3) → **guides-01k**
- Нет cron lock + `*/15 * * * *` → гарантированная race. (Phase 4B CD-C4) → **guides-9id**
- Нет алёртов на cron fail / cost spike. (Phase 4B CD-C5) → **guides-pnj**

**Documentation:**
- `_human/vps-deploy.md` → несуществующий `src/process_stream.py`. (Phase 3B D-C1) → **guides-13n**
- Inbox path drift: code `inbox/`, ВСЯ документация `data/inbox/`. (Phase 3B D-C2) → **guides-13n**
- `state.py` schema/миграции не задокументированы. (Phase 3B D-C4) → **guides-210**
- `_human/usecase-annotated-link.md` ссылается на удалённые paths. (Phase 3B D-C5) → **guides-13n**

**Testing:**
- 5 Critical missing tests (= Phase 2 Critical/High без guard'ов). → **guides-cvp**

### High (P1 — fix this sprint)

71 findings. Группы покрыты задачами:
- YAML injection в hand-rolled frontmatter writers (H2, H3) + `parse_front_matter_simple` duplicated (1B H4) → **guides-ll6**
- Telegram token leak в httpx exception (H4) → **guides-1w7**
- image_ocr/yt-dlp redirect re-validation отсутствует (H5, H7) → **guides-wss**
- Stored prompt-injection в C/D/E/G (H6) → **guides-u40**
- `daily_log` O(n²) rewrite + race (P-H1) → **guides-3y7**
- Pipeline D 5K-char slice ignores tokens (P-H2) → **guides-5er**
- `b_summarize` retry пересылает весь body (P-H3) → **guides-i6q**
- `npx -y` cold start 5-15s per URL (P-H4) → **guides-vld**
- YouTube fetcher serializes 60s (P-H5) → **guides-rem**
- Greedy `{[\s\S]*}` regex в 4+ файлах (P-H6, 1B H3) → **guides-5hb**
- Vision images uncompressed base64 + serial OCR (P-H7) → **guides-ss8**
- No indexes на `content_hash`, `wiki_propagated`, `seo_optimized`, `published_telegram` (P-H8) → **guides-ldh**
- Fetch fallback chains bespoke без `Fetcher` protocol (1B H2) → **guides-d2k**
- Idempotency-стратегия разная (content-hash / file-exists / state flag / none) (1B H1) → **guides-i3d**
- Pipelines → `guides.tools.daily_log` — wrong dependency direction (1B H5) → **guides-sud**
- `run_all` без единого pipeline contract + глотает `ImportError` (1B H6; 1A High) → **guides-87e**
- Нет mypy/pyright gate (F-C3 + Frameworks High) → **guides-bwi**
- 13 missing behavioural tests one-to-one с Phase 2 Critical/High → **guides-cvp**
- 7 required NEW docs (SECURITY.md, ADR-001/002, prompts/README.md, runbook, MIGRATIONS, quartz-setup) → **guides-zrh** + **guides-210**

### Medium (P2 — plan next sprint)

74 findings. Среди важных:
- Self-written YAML emit без эскейпинга (унификация через `yaml.safe_dump`) — covered by **guides-ll6**
- 18+ `except: pass` без логирования — addressed in **guides-13n** (log_setup)
- Файлы пишутся неатомарно — **guides-9tq**
- Три реализации `slugify()` с разной семантикой — **guides-cxj**
- Summary помечается `wiki_propagated` даже когда update wiki упал — **guides-i3d**
- MD5 для slug fallback (CWE-327) — **guides-cxj**
- pdf TOCTOU + symlink
- `Settings()` instantiated 13 раз — **guides-tg0**
- `link_checker` O(files × wikilinks × dirs)
- `cost_report` парсит весь log каждый раз — **guides-3y7**
- Hand-written frontmatter в `c_wiki_update.py:228-231` round-trips LLM-supplied keys — **guides-ll6**
- Pydantic v2 idioms / structured outputs не используются — **guides-6zu**
- `subprocess.run` без env scrubbing / PATH pinning

### Low (P3 — backlog)

53 findings. Style guide, легкие code smells, dead options (`OCR_MAX_COMPLETION_TOKENS` defined но не используется), `Settings.azure_openai_endpoint` без https schema check, etc.

## Findings by Category

- **Code Quality (1A)**: 56 (6 / 15 / 20 / 15)
- **Architecture (1B)**: 22 (3 / 6 / 7 / 6)
- **Security (2A)**: 24 (4 / 7 / 6 / 7)
- **Performance (2B)**: 26 (5 / 8 / 8 / 5)
- **Testing (3A)**: 27 (5 / 9 / 8 / 5)
- **Documentation (3B)**: 26 (5 / 9 / 8 / 4)
- **Frameworks (4A)**: 31 (4 / 9 / 11 / 7)
- **CI/CD & DevOps (4B)**: 23 (5 / 8 / 6 / 4)

**Total: 235** (37 / 71 / 74 / 53)

## Recommended Action Plan

Все задачи на починку созданы в beads issue tracker. Спринты независимы внутри (parallel work возможен), epics зависят последовательно (Sprint 1 → 2 → 3 → 4).

### Sprint 1 (Week 1) — Stop the bleeding [EPIC guides-40a, ~13ч]

Цель: убрать financial leak, закрыть SSRF, добавить CI gate.

1. **guides-9hk** — Pipeline D idempotency (P-C4) — содержит самую крупную $$ утечку. Колонка `qc_hash`, skip-if-unchanged. ~4ч.
2. **guides-lmk** — Token router via tiktoken (P-C3) — убирает retry-шторма на RU. ~1ч.
3. **guides-7al** — SSRF в fetch/url.py + github.py + jina.py (C1) — `validate_url` на каждый hop + manual redirect re-validation. ~4ч.
4. **guides-6zu** — OpenAI client config (F-H3 + F-C1) — переход на `AzureOpenAI`, `timeout=120`, `max_retries=4`. ~2ч.
5. **guides-95a** — Minimal CI (CD-C1) — `ci.yml` (ruff + pytest + gitleaks). Без gate ничего не держится. ~1ч.
6. **guides-ipz** — `state/articles.db` бэкап (CD-C2) — daily `.backup` + rclone. ~30мин.
7. **guides-9id** — Cron `flock` wrapper (CD-C4) — против overlap workers. ~15мин.
8. **guides-rlj** — parse_frontmatter `\n---\n` bug (30мин).
9. **guides-8pp** — llm._extract_response_text silent empty (30мин).
10. **guides-yri** — get_state ALTER ordering (60мин).
11. **guides-9xm** — Pipeline D wiki backup (60мин).
12. **guides-pnj** — Alerts on cron fail + cost spike (60мин).

### Sprint 2 (Week 2) — Security & State hardening [EPIC guides-buj, ~20ч]

13. **guides-vld** — Replace npx -y defuddle-cli → trafilatura (C4 + P-H4) — ~2ч.
14. **guides-ll6** — YAML safe_dump everywhere (H2 + H3 + F-M5) — централизованный `frontmatter.dump`. ~3ч.
15. **guides-u40** — LLM page_md Pydantic validation + size cap (C3 + H1) — ~4ч.
16. **guides-ldh** — State.py refactor — threading-local connection + `busy_timeout=30000` + batched `update_state(**fields)` + indexes. (P-C1 + P-C2 + P-H8 + 1B C3) — ~6ч.
17. **guides-9tq** — Atomic write helper (P-M8) — `tmp.replace(path)` для всех frontmatter writes. ~1ч.
18. **guides-5hb** — Central JSON extractor (P-H6 + 1B H3) — bracket-balanced parser в `guides/llm.py`. ~1ч.
19. **guides-1w7** — httpx token redaction (H4) — wrap Telegram errors. ~30мин.
20. **guides-wss** — image_ocr/yt-dlp redirect re-validation (H5 + H7) — ~2ч.
21. **guides-01k** — .env secrets management + rotation (CD-C3) — ~90мин.
22. **guides-i6q** — b_summarize retry оптимизация (P-H3) — ~1ч.
23. **guides-f9y** — LLM retry/backoff на 429/500 (P-C5) — ~1ч.
24. **guides-5er** — Pipeline D 5K char → token-aware (P-H2) — ~1ч.

### Sprint 3 (Week 3) — Documentation & Testing [EPIC guides-bxr, ~29ч]

25. **guides-cvp** — 13 behavioural tests (Phase 3A Critical Issues table) — ~16ч.
26. **guides-zrh** — SECURITY.md + ADR-001 + ADR-002 — ~4ч.
27. **guides-210** — prompts/README.md + state/MIGRATIONS.md + runbook + quartz-setup — ~5ч.
28. **guides-13n** — Doc fixes (vps-deploy + inbox path + log_setup + schema + usecase) — ~3ч.
29. **guides-bwi** — mypy/pyright gate + pytest/coverage config (F-C3) — ~3ч.
30. **guides-kie** — Python version mismatch >=3.13 (F-C4) — ~15мин.
31. **guides-qfz** — State schema drift unification — ~3ч.
32. **guides-4v0** — Deploy story (rollback + env sep + log rotation + runbook) — ~3ч.

### Sprint 4 (Week 4) — Architecture cleanup [EPIC guides-3jg, ~19ч]

33. **guides-tg0** — Hard-coded paths → Settings.public_dir/sources/summaries (1B C1) — ~3ч.
34. **guides-cxj** — Three slugify → one canonical (F-M4 + 1A High) — ~2ч.
35. **guides-3y7** — Daily log JSONL append-only (P-H1) — ~3ч.
36. **guides-d2k** — Fetcher protocol для fetch fallback chains (1B H2) — ~4ч.
37. **guides-i3d** — Unified idempotency strategy (1B H1) — ~3ч.
38. **guides-sud** — Pipelines → daily_log dependency inversion (1B H5) — ~2ч.
39. **guides-87e** — `run_all` contract + remove ImportError swallow (1B H6) — ~2ч.
40. **guides-ss8** — Vision/PDF performance (P-H7) — ~3ч.
41. **guides-rem** — YouTube fail-fast (P-H5) — ~1ч.

**Total estimate ~81-90 hours** для всех Critical + High. Medium/Low уходят в backlog.

## Review Metadata

- Review date: 2026-05-13
- Phases completed: 00-scope, 1A, 1B, 2A, 2B, 3A, 3B, 4A, 4B, 5
- Flags applied: framework=python
- Total findings: 235 (37 Critical / 71 High / 74 Medium / 53 Low)
- Estimated remediation: ~81-90 hours for Critical+High
- Beads issues: 4 epics + 37 tasks (guides-40a, guides-buj, guides-bxr, guides-3jg + individual issues)

## How programmers use this

```bash
bd ready                       # See what's unblocked right now
bd show guides-9hk             # Read full task spec
bd update guides-9hk --claim   # Claim work
# ... implement ...
bd close guides-9hk            # Mark done; unblocks dependent tasks
```

Sprint epics (`guides-40a/buj/bxr/3jg`) для tracking. Issues внутри спринта параллелятся.
