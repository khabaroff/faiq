# Pipeline Run Issues — 2026-05-14

Наблюдения из первого реального прогона A→B→C→D→E после рефакторинга.

---

## 1. КРИТИЧНО: Неверный AZURE_OPENAI_ENDPOINT в .env

**Что произошло:** Первый запуск pipeline A вернул 404 "Resource not found" на все LLM-вызовы.

**Причина:** В `.env` endpoint был прописан как:
```
AZURE_OPENAI_ENDPOINT=https://khabaroff-sage-res.cognitiveservices.azure.com/openai/v1/
```
Клиент `AzureOpenAI` из openai SDK сам добавляет `/openai/deployments/...` к endpoint. С суффиксом `/openai/v1/` URL получался:
```
https://...cognitiveservices.azure.com/openai/v1/openai/deployments/gpt-5.4/...
```
→ дублирование пути → 404.

**Исправление:** Убрать `/openai/v1/` из endpoint:
```
AZURE_OPENAI_ENDPOINT=https://khabaroff-sage-res.cognitiveservices.azure.com/
```

**Рекомендация для разработчиков:**
- Добавить startup-проверку endpoint при инициализации Settings (попытка GET / с timeout=3, если 404 → понятная ошибка "check AZURE_OPENAI_ENDPOINT format")
- Или добавить в README/onboarding явный пример формата endpoint без `/openai/v1/`

---

## 2. БАГИ: OCR — malformed JSON от LLM (escaped closing quote)

**Файл:** `src/guides/fetch/image_ocr.py:332`, `src/guides/json_extract.py:60`

**Что произошло:** `run_vision_ocr` падал с:
```
ValueError: Unclosed JSON object in response: {"image_type":"ui-screenshot",...
RuntimeError: Failed to parse OCR result: ...
```

**Причина:** Модель gpt-5.4 иногда экранирует кавычки внутри строкового значения корректно (`\"text\"`), но при этом последний `\"` перед `}` закрывает строку экранированной кавычкой — и `}` попадает внутрь открытой строки:

```json
{"description": "...labeled \"Opus 4.7 Adaptive.\"}"
                                               ↑ escaped → } inside string!
```

Вместо корректного:
```json
{"description": "...labeled \"Opus 4.7 Adaptive.\""}
                                                 ↑ unescaped closing " then }
```

**Поведение:** Ошибка НЕ крашит всю pipeline — item пропускается (нефатальная). Но OCR-блоки для тех изображений не записываются.

**Рекомендации:**
1. В `run_vision_ocr` при `RuntimeError` — попытаться fallback: `json.loads(text)` напрямую (json.loads иногда переживает такие крайние случаи или даёт более точную позицию ошибки).
2. В `extract_json` — добавить `json.loads(text.strip())` как первый шаг перед bracket-counting (быстрый happy path для чистых ответов).
3. Добавить счётчик OCR-ошибок в summary pipeline A ("Processed X items, Y OCR failures").
4. Логировать slug + image URL при OCR failure для post-mortem анализа.

---

## 3. НАБЛЮДЕНИЕ: Скорость pipeline A

- 28 файлов за 14 мин 33 сек = ~31 сек/файл
- Большую часть времени занимает OCR (vision API calls на remote images)
- Каждый файл с ~10-30 изображениями = 10-30 API calls только на OCR
- Для 19 inbox-файлов это ~500+ API calls за один прогон

**Рекомендация:** Добавить image dedup по SHA256 между прогонами (уже есть кэш?) — повторные прогоны должны пропускать уже OCR-ированные изображения.

---

## 4. НАБЛЮДЕНИЕ: pipeline A не обрабатывает --batch

Pipeline A сканирует весь inbox без опции батч-лимита. Для отладки/тестирования хочется `--batch 3`.

---

## 5. TODO (не блокирует)

- `a_ingest.main()` возвращает `None` вместо `int` при успехе → `run_all.py` делает `rc = a_ingest.main(argv) or 0` (workaround есть, но сигнатура должна быть `-> int`).

---

---

## 6. КРИТИЧНО: Pipeline B — Azure content_filter блокирует AI-контент

**Что произошло:** Pipeline B (summarize) получает `400 BadRequestError: content_filter` на большинстве статей.

**Причина:** Azure OpenAI Content Management блокирует запросы с кодом `jailbreak: detected: true`. Статьи про Claude/AI содержат примеры промптов, инструкции ("act as", "ignore", "follow these rules"), которые Azure интерпретирует как jailbreak-паттерны.

**Затронутые slugs:**
- `2026-05-13-post-by-daily-dose-of-data-science-on-linkedin`
- `why-most-second-brain-systems-fail`
- `2026-05-13-claude-skills`
- `2026-05-13-demystifying-evals-for-ai-agents`
- `2026-05-13-how-to-supercharge-claude-code-skills-20-playbook`
- `2026-05-13-the-notebooklm-playbook`
- (и другие — ~10+ из 28)

**Варианты решений:**
1. **Azure Portal**: Запросить отключение jailbreak-фильтра для ресурса `khabaroff-sage-res` (Settings → Content filters → Jailbreak)
2. **Preprocessing**: Перед отправкой в LLM убирать/нейтрализовать паттерны, похожие на промпты (TODO: не идеально)
3. **Смена провайдера**: Использовать OpenAI напрямую или другой Azure-ресурс без строгой фильтрации

**Рекомендация:** Отключить jailbreak-filter в Azure AI Foundry для этого ресурса. Контент — легитимные статьи об AI-инструментах, не jailbreak.

---

## 7. БАГ: b_summarize.py — две missing definitions

`_compute_hash` не определена в `b_summarize.py` (определена в c/e/g, но не скопирована в b).
`logger` вместо `log` в exception handler (b_summarize использует `log = getLogger(...)`, но в одном месте было `logger.exception`).

**Исправлено:** добавлена `_compute_hash`, исправлено `logger` → `log`.

---

*Записано автоматически во время pipeline run 2026-05-14 13:14–14:xx*
