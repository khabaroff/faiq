"""Pipeline B — Summarize.

Вход: public/sources/*.md без соответствующего public/summaries/<slug>.md
Выход: public/summaries/<slug>.md (YAML frontmatter + markdown body)

Шаги:
  1. Найти source-файлы без саммари
  2. Для каждого: загрузить, прогнать через prompts/summary.md
  3. Валидировать frontmatter (tools + patterns), retry до 3 раз
  4. Записать public/summaries/<slug>.md
  5. state/index.json: <slug>.summary = true

Routing: Azure mini для <15K токенов, gpt-5.4 для длинных.

Usage:
  python -m guides.pipelines.b_summarize            # batch все unsummarized
  python -m guides.pipelines.b_summarize --slug foo # один источник
  python -m guides.pipelines.b_summarize --force    # пересуммировать всё
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from functools import cache as _cache
from pathlib import Path

import yaml

from guides.frontmatter import parse_frontmatter
from guides.llm import call_llm, get_smart_client, load_prompt
from guides.settings import Settings
from guides.tools.daily_log import append_log_entry


@_cache
def _s() -> "Settings":
    return Settings()

ROOT = Path(__file__).resolve().parent.parent.parent.parent
CONTENT_DIR = ROOT / "public"
SOURCES_DIR = CONTENT_DIR / "sources"
SUMMARIES_DIR = CONTENT_DIR / "summaries"

MAX_RETRIES = 3
_CORRECTION = (
    "Твой ответ не содержит корректный YAML frontmatter. "
    "Начни ответ СТРОГО с:\n"
    "---\n"
    "tools: []\n"
    "patterns: []\n"
    "key_claims:\n"
    "  - тезис\n"
    "lecture_hooks:\n"
    "  - вопрос\n"
    "---\n"
    "Ключи tools и patterns ОБЯЗАТЕЛЬНЫ (пустые списки если нет). Повтори весь ответ."
)

def count_tokens(text: str) -> int:
    return len(text) // 4


def parse_front_matter_simple(text: str) -> tuple[dict, str]:
    """Simple key: value parser (no lists). For source files."""
    if not text.startswith("---\n"):
        return {}, text
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        return {}, text
    fm_raw = text[4:end]
    body = text[end + 5:]
    fm = {}
    for line in fm_raw.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm, body


def _validate_summary_md(text: str) -> bool:
    if not text.startswith("---\n"):
        return False
    fm, _ = parse_frontmatter(text)
    if not fm:
        return False
    return isinstance(fm.get("tools"), list) and isinstance(fm.get("patterns"), list)


def _render_summary_prompt(source_text: str, source_url: str, source_type: str, lang_orig: str) -> str:
    prompt = load_prompt("summary.md")
    prompt = prompt.replace("{{source_text}}", source_text)
    prompt = prompt.replace("{{source_url}}", source_url)
    prompt = prompt.replace("{{source_type}}", source_type)
    prompt = prompt.replace("{{lang_orig}}", lang_orig)
    return prompt


def call_llm_summary(slug: str, source_text: str, source_url: str, source_type: str, lang_orig: str) -> str:
    """Returns full markdown string (validated). Raises on repeated failure."""
    base_prompt = _render_summary_prompt(source_text, source_url, source_type, lang_orig)

    token_count = count_tokens(source_text)
    deployment = _s().azure_deployment_fast or _s().azure_deployment_smart
    if token_count >= 15000:
        deployment = _s().azure_deployment_smart

    system = (
        "Ты — экспертный ассистент для анализа технических статей. "
        "Начни ответ строго с YAML frontmatter (---), затем markdown-тело."
    )

    client = get_smart_client()
    last_response = ""
    last_usage = None
    for attempt in range(MAX_RETRIES):
        if attempt == 0:
            prompt = base_prompt
        else:
            prompt = base_prompt + f"\n\n---\n\n**ВАЖНО (попытка {attempt + 1}):** {_CORRECTION}"

        last_response, last_usage = call_llm(client, deployment, prompt, system)

        if _validate_summary_md(last_response):
            if last_usage:
                append_log_entry(
                    slug=slug,
                    action="summary",
                    model=deployment,
                    tokens_in=last_usage.prompt_tokens,
                    tokens_out=last_usage.completion_tokens,
                    cost_usd=last_usage.cost_usd,
                )
            return last_response

        print(f"  attempt {attempt + 1}/{MAX_RETRIES}: bad frontmatter format", file=sys.stderr)

    print(f"  all {MAX_RETRIES} attempts failed, marking needs_review", file=sys.stderr)
    return f"---\ntools: []\npatterns: []\nquality: needs_review\n---\n\n{last_response}"


def summarize_one(slug: str) -> Path:
    src = SOURCES_DIR / f"{slug}.md"
    if not src.exists():
        raise FileNotFoundError(src)

    src_text = src.read_text()
    src_fm, src_body = parse_front_matter_simple(src_text)

    summary_md = call_llm_summary(
        slug=slug,
        source_text=src_body,
        source_url=src_fm.get("source_url", ""),
        source_type=src_fm.get("source_type", "article"),
        lang_orig=src_fm.get("lang", "ru"),
    )

    llm_fm, llm_body = parse_frontmatter(summary_md)

    today = date.today().isoformat()

    canonical_fm: dict = {
        "slug": slug,
        "source_url": src_fm.get("source_url", ""),
        "source_type": src_fm.get("source_type", "article"),
        "summarized_at": today,
        "status": "reviewed",
        "tools": llm_fm.get("tools") or [],
        "patterns": llm_fm.get("patterns") or [],
        "key_claims": llm_fm.get("key_claims") or [],
        "lecture_hooks": llm_fm.get("lecture_hooks") or [],
    }
    if llm_fm.get("quality") == "needs_review":
        canonical_fm["quality"] = "needs_review"

    fm_str = "---\n" + yaml.dump(canonical_fm, allow_unicode=True, default_flow_style=False) + "---\n\n"

    out = SUMMARIES_DIR / f"{slug}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(fm_str + llm_body)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", help="single slug to summarize")
    ap.add_argument("--force", action="store_true", help="re-summarize even if exists")
    ap.add_argument("--batch", type=int, default=0, help="limit to N items (0 = all)")
    from guides.state import get_state, set_state, list_pending

    args = ap.parse_args(argv)

    if args.slug:
        slugs = [args.slug]
    else:
        if not SOURCES_DIR.exists():
            print(f"Sources dir does not exist: {SOURCES_DIR}")
            return 1
        slugs = [p.stem for p in SOURCES_DIR.glob("*.md")]

    if args.batch > 0:
        slugs = slugs[:args.batch]

    processed = 0
    for slug in slugs:
        if not args.force and (SUMMARIES_DIR / f"{slug}.md").exists():
            print(f"skip (exists): {slug}")
            continue
        print(f"summarize: {slug}")
        try:
            out = summarize_one(slug)
            set_state(slug, "summarized_at", date.today().isoformat())
            set_state(slug, "status", "reviewed")
            print(f"  → {out}")
            processed += 1
        except Exception as e:
            print(f"ERROR {slug}: {e}", file=sys.stderr)

    print(f"Processed {processed} summaries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
