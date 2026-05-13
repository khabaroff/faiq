# Решения, которые надо принять

Документ для собственных раздумий. Отсортировано по приоритету (P0 → P3). Решённые перенесены в конец.

**Дата создания**: 2026-05-13
**Последнее обновление**: 2026-05-13
**Контекст**: после Sprint 1 + частичного Sprint 2 (18/41 закрыто). 29 issues open.

---

## P0 — блокирующее, решить сейчас

### P0.1 — faiq это personal tool или product? (мета)

Это решает всё остальное. **Решить первым**.

**Варианты**:
- **A**: personal tool (только для меня → Telegram канал) — Sprint 3/4 не нужен, security threshold ниже
- **B**: product / open-source (другие будут разворачивать) — Sprint 3/4 нужны, security жёстче
- **C**: hybrid (личное использование сейчас, open-source через 6 мес) — Sprint 3 docs нужны, тесты желательны

**Влияет на**: P0.3, P1.1, P2.1, P2.2

---

### P0.2 — ~~atomic write helper (guides-9tq)~~ ✅ РЕШЕНО (2026-05-13, commit 6036c1e)

`atomic_write_text` реализован, все 18 мест подменены.

---

### P0.3 — healthchecks.io alerts (guides-pnj)

**Что нужно**: cron failure alert + cost spike alert.

**Варианты**:
- **A**: healthchecks.io free tier (20 checks, Telegram integration) — 1ч setup
- **B**: Cronitor ($5/мес) — better cost tracking
- **C**: self-host healthchecks (Docker на том же VPS) — бесплатно, но VPS лёг → alert мёртв
- **D**: `MAILTO=` в crontab — primitive, нет spike detection

**Мой склон**: A. Зависит от VPS = single point of failure, hosted сервис обходит это.

**Что подумать**:
- Cost spike threshold — где брать цифру? Парсить state.db daily usage? OpenAI budget alert (встроенный в портале)?
- Если parse state.db — отдельный cron шлёт `$HC_URL/fail` если daily > $X. Какой X — $10? $20?

**Зависит от P0.1**: если personal — A. Если product — B (better visibility).

---

## P1 — важно, на ближайший спринт

### P1.1 — .env secrets management (guides-01k)

**Что предлагается** в issue: encryption at rest (age/SOPS), rotation policy (90 дней), audit log.

**Реальность для faiq**:
- Solo dev, VPS, один пользователь
- Секреты: AZURE_OPENAI_API_KEY, TELEGRAM_BOT_TOKEN
- Доступ к VPS — SSH key, .env права 600
- Threat model: root на VPS → encryption-at-rest не спасает (decrypt key тоже на VPS)

**Варианты**:
- **A**: ничего не делать — VPS isolation хватит
- **B**: только rotation (раз в 3 мес вручную крутить ключи)
- **C**: SOPS + age (1-2ч setup, защита от `git add .env`)
- **D**: 1Password / Bitwarden Secrets Manager ($20/мес)

**Мой склон**: B + `.env` в `.gitignore` + gitleaks в CI (уже есть).

**Что подумать**: реальный threat — "compromise VPS" или "случайно запушил .env"? Второй важнее, и его закрывает gitleaks. Тогда A достаточно.

**Зависит от P0.1**: если product — C. Если personal — A или B.

---

### P1.2 — trafilatura замена npx defuddle (guides-vld)

**Что**: убрать runtime зависимость от `npx -y defuddle-cli`. Supply chain hardening (npm package compromise).

**Решение нужно**: только подтверждение что делаем. Замена технически чистая (trafilatura — pure python, pip install).

**Зависит от P0.1**: если product — обязательно. Если personal — желательно но не критично.

**3ч работы**. Просто решить — да/нет.

---

### P1.3 — Sprint 2 nice-to-have (7 задач, ~10ч)

**Содержимое** (все P1):
- `guides-5hb` — central JSON extractor (bracket-balanced parser)
- `guides-1w7` — Telegram redaction (token leaks в трейсах)
- `guides-wss` — redirect revalidation (chain-of-trust для image_ocr/yt-dlp)
- `guides-i6q` — b_summarize retry без переотправки body
- `guides-f9y` — granular LLM retry/backoff (cross-ref guides-6zu)
- `guides-5er` — Pipeline D 5K char slice → token-aware
- `guides-87e` — run_all contract + remove ImportError swallow

**Варианты**:
- **A**: делать все 7
- **B**: только security (1w7, wss) — 2-3ч
- **C**: только cost optimization (5er, i6q) — 2ч
- **D**: пропустить целиком

**Мой склон**: B. 1w7/wss закрывают реальные security holes. Остальные nice-to-have.

**Что подумать**: что реально болит — leak в логах, redirect attacks, или преждевременная оптимизация?

---

## P2 — на следующий спринт или backlog

### P2.1 — Sprint 3 docs/tests (29ч)

**Содержимое**:
- 13 behavioural тестов (`guides-cvp`)
- SECURITY.md + 2 ADR (`guides-zrh`)
- 4 runbook (`guides-210`: prompts/README, MIGRATIONS, _human/runbook, _human/quartz-setup)
- mypy/pyright gate (`guides-bwi`)
- Doc drift fixes (`guides-13n`)
- Schema drift (`guides-qfz`)
- Deploy story (`guides-4v0`)

**Варианты**:
- **A**: всё — для onboarding / open-source
- **B**: только тесты (cvp) — личная страховка от регрессий
- **C**: только docs (ADR + runbook) — память на 6 мес вперёд
- **D**: пропустить целиком

**Мой склон**: B + минимум C (только ADR-001 npx + runbook).

**Что подумать**: faiq long-term или эксперимент? Если эксперимент — D. Long-term — B.

**Зависит от P0.1**: product → A. Personal long-term → B+C. Эксперимент → D.

---

### P2.2 — Sprint 4 architecture cleanup (19ч)

**Содержимое** (все P1/P2):
- Settings.public_dir centralization (`guides-tg0`)
- Slugify unification (`guides-cxj`)
- JSONL daily log (`guides-3y7`)
- Fetcher protocol (`guides-d2k`)
- Idempotency contract (`guides-i3d`)
- Dependency inversion (`guides-sud`)
- run_all contract (`guides-87e`) [дубль с P1.3]
- Vision/PDF perf (`guides-ss8`)
- YouTube fail-fast (`guides-rem`)

**Мой склон**: пропустить целиком. Refactor без бизнес-value.

**Исключение**: `guides-rem` (YouTube serial 60с hang) — если реально мешает, взять только его.

**Что подумать**: какие из 9 реально болят на практике? Если ни одно — не трогать.

---

## P3 — низкий приоритет, мониторить

(пусто)

---

## Шаблон для добавления решений

```
### PX.N — [Название] (issue-id если есть)

**Что**:
**Варианты**: A / B / C
**Мой склон**:
**Что подумать**:
**Зависит от**: PY.M
```

---

## ✅ Решённые

### 2026-05-13

- **Python version bump (guides-kie)** — bump до `>=3.13` (pyproject + ruff target). Match runtime 3.13.13.
- **YAML safe_dump (guides-ll6)** — закрыто.
- **page_md Pydantic + size cap (guides-u40)** — закрыто.
- **state.py SQLite race (guides-ldh)** — закрыто.
- **atomic_write_text (guides-9tq)** — commit 6036c1e, все 18 `.write_text()` подменены на `tmp+os.replace`.

---

## Порядок действий (TL;DR)

1. **P0.1** — решить personal vs product. Без этого остальное в воздухе.
2. **P0.3** — выбрать вариант healthchecks (зависит от P0.1).
3. **P1.1/P1.2** — решить .env policy + trafilatura (зависит от P0.1).
4. **P1.3** — выбрать subset Sprint 2 nice-to-have.
5. **P2.1/P2.2** — defer до завершения P0/P1.
