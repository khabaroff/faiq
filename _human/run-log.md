
# 2026-05-14 — Первый полный прогон A→B→C→D→E после рефакторинга

| Pipeline | Время | Результат |
|----------|-------|-----------|
| A (ingest) | 14m 33s | 28 файлов из inbox |
| B (summarize) | ~31с/файл | 31/31 ✓ |
| C (wiki update) | 4m 33s | 250 страниц |
| D (quality check) | 6m 25s | 5 ok / 12 minor_fix / 17 needs_resummarize / 129 needs_cleanup |
| E (seo) | 45s | 31/31 ✓ |

**Проблемы при запуске:**
- Azure endpoint имел лишний `/openai/v1/` → 404 на все LLM вызовы. Убран из `.env`.
- Azure jailbreak-filter блокировал все AI-статьи в Pipeline B. Отключён вручную в Azure AI Foundry.
- `b_summarize.py`: отсутствовала `_compute_hash` + `logger` вместо `log`. Пофикшено.
- `d_quality_check.py`: `Settings()` вместо `get_settings()`. Пофикшено.

**Что нужно сделать по результатам:**
- 129 `needs_cleanup` = битые `../summaries/slug.md` ссылки в wiki. Фикс в промпте C + `--force`.
- 17 `needs_resummarize` = галлюцинации. Перезапустить B с `--force` для этих slugs.
- Детали: `_human/TODO-2026-05-14.md`, `_human/pipeline-issues-2026-05-14.md`

---

# 2026-05-11 — Clean rebuild after validator and scoring updates

- **Rebuild mode:** deleted generated `wiki/` and `data/sources/*`, then re-ran all `data/inbox_done`
- **Result:** 9 pages total, 1 `verified`, 8 `needs_review`
- **Verified share:** 11.11% (`1/9`)
- **What changed:** `guides-idm` now fixes page structure; `guides-dux` uses a stricter `verified` threshold and weighted quality score

## 2026-05-11 — Первый полный прогон (старая архитектура)

- **Время:** 4м 37с (277с)
- **Источников:** 15 (9 файлов + 6 URL)
- **LLM вызовов:** 30
- **Стоимость:** $0.4578 ($0.0305/источник)
