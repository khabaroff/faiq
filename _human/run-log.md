
# 2026-05-11 — Clean rebuild after validator and scoring updates

- **Rebuild mode:** deleted generated `wiki/` and `data/sources/*`, then re-ran all `data/inbox_done`
- **Result:** 9 pages total, 1 `verified`, 8 `needs_review`
- **Verified share:** 11.11% (`1/9`)
- **What changed:** `guides-idm` now fixes page structure; `guides-dux` uses a stricter `verified` threshold and weighted quality score
- **Current limit:** most remaining pages still have English section headers in the body; `_HEADING_MAP` only normalizes headings, not full text translation
- **Takeaway:** expanding `_HEADING_MAP` can raise `verified` a bit, but full Russian body rewrite is a separate pass and not required for the current baseline

## 2026-05-11 — Первый полный прогон

- **Время:** 4м 37с (277с)
- **Источников:** 15 (9 файлов + 6 URL из них)
- **LLM вызовов:** 30 (gpt-5.4: 15 × $0.030 avg, mini: 15 × $0.0003 avg)
- **Стоимость:** $0.4578 ($0.0305/источник)
- **Статус:** все `needs_review` — vault.py пропускает запись для needs_review
- **Проблема:** ни одна страница не попала в wiki/extracts — нужно починить


  Исправлено: vault.py больше не блокирует needs_review → 15 страниц записаны.
  Причина needs_review: LLM генерирует английские заголовки вместо русских
  (нарушает has_real_heading + has_body_sections). Нужно: дофиксить промпт или
  смягчить верификатор.
