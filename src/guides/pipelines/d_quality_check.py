"""Pipeline D — Quality Check.

Two modes:
  - summary_check: source + summary → verdict (ok | needs_resummarize | minor_fix)
  - wiki_clean:    wiki page → cleaned page (if needed)

Prompt: prompts/quality_check.md
LLM: Azure mini (cheap).
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from datetime import date
from pathlib import Path

from guides.llm import call_llm, get_smart_client, load_prompt
from guides.settings import Settings

logger = logging.getLogger(__name__)

ROOT = Path.cwd()
STATE_FILE = ROOT / "state" / "index.json"
QC_REPORT = ROOT / "state" / "quality-report.json"

# Content paths
PUBLIC_DIR = ROOT / "public"
SOURCES_DIR = PUBLIC_DIR / "sources"
SUMMARIES_DIR = PUBLIC_DIR / "summaries"
TOOLS_DIR = PUBLIC_DIR / "tools"
TECH_DIR = PUBLIC_DIR / "techniques"


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _extract_json(text: str) -> dict:
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError(f"No JSON found in response: {text[:200]}")
    return json.loads(match.group())


def call_llm_summary_check(source_text: str, summary_text: str, slug: str) -> dict:
    prompt_template = load_prompt("quality_check.md")
    
    # Simple replacement for placeholder template
    prompt = prompt_template + f"\n\n## Вход\n\n### Source ({slug})\n{source_text[:5000]}\n\n### Summary\n{summary_text}"
    
    s = Settings()
    deployment = s.azure_deployment_fast or s.azure_deployment_smart
    
    system = "Ты — эксперт по качеству технической документации. Твоя задача — проверить соответствие саммари исходному тексту. Верни только JSON."
    
    response, _ = call_llm(get_smart_client(), deployment, prompt, system)
    return _extract_json(response)


def call_llm_wiki_clean(page_text: str, slug: str) -> dict:
    prompt_template = load_prompt("quality_check.md")
    
    prompt = prompt_template + f"\n\n## Вход\n\n### Wiki Page ({slug})\n{page_text}"
    
    s = Settings()
    deployment = s.azure_deployment_fast or s.azure_deployment_smart
    
    system = "Ты — редактор технической вики. Твоя задача — очистить страницу от дублей и битых ссылок. Верни только JSON."
    
    response, _ = call_llm(get_smart_client(), deployment, prompt, system)
    return _extract_json(response)


def check_summaries(slug_filter: str | None = None) -> list[dict]:
    results = []
    if slug_filter:
        sum_files = [SUMMARIES_DIR / f"{slug_filter}.md"]
    else:
        sum_files = list(SUMMARIES_DIR.glob("*.md"))

    for sum_path in sum_files:
        if not sum_path.exists():
            continue
        slug = sum_path.stem
        src_path = SOURCES_DIR / f"{slug}.md"
        if not src_path.exists():
            logger.warning("Source for summary %s not found", slug)
            continue
        
        print(f"Checking summary: {slug}...")
        try:
            res = call_llm_summary_check(src_path.read_text(encoding="utf-8"), sum_path.read_text(encoding="utf-8"), slug)
            res["slug"] = slug
            res["mode"] = "summary_check"
            results.append(res)
        except Exception as e:
            logger.error("Failed QC for summary %s: %s", slug, e)
            results.append({"slug": slug, "mode": "summary_check", "verdict": "error", "error": str(e)})
            
    return results


def clean_wiki_pages(slug_filter: str | None = None) -> list[dict]:
    results = []
    
    targets = []
    if slug_filter:
        for d in (TOOLS_DIR, TECH_DIR):
            p = d / f"{slug_filter}.md"
            if p.exists():
                targets.append(p)
    else:
        targets.extend(list(TOOLS_DIR.glob("*.md")))
        targets.extend(list(TECH_DIR.glob("*.md")))

    for page in targets:
        slug = page.stem
        print(f"Cleaning wiki page: {slug}...")
        try:
            res = call_llm_wiki_clean(page.read_text(encoding="utf-8"), slug)
            res["slug"] = slug
            res["mode"] = "wiki_clean"
            res["path"] = str(page.relative_to(ROOT))
            
            if res.get("verdict") == "needs_cleanup" and "cleaned_page_md" in res:
                page.write_text(res["cleaned_page_md"], encoding="utf-8")
                print(f"  -> Cleaned: {slug}")
            
            results.append(res)
        except Exception as e:
            logger.error("Failed QC for wiki page %s: %s", slug, e)
            results.append({"slug": slug, "mode": "wiki_clean", "verdict": "error", "error": str(e)})
            
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Pipeline D: Quality Check")
    parser.add_argument("--mode", choices=["summary", "wiki", "both"], default="both")
    parser.add_argument("--slug", help="Process only this slug")
    args = parser.parse_args()

    state = load_state()
    all_results = []

    if args.mode in ("summary", "both"):
        all_results.extend(check_summaries(args.slug))
    
    if args.mode in ("wiki", "both"):
        all_results.extend(clean_wiki_pages(args.slug))

    if not all_results:
        print("No items to check.")
        return 0

    # Update state
    for res in all_results:
        if res.get("verdict") != "error":
            slug = res["slug"]
            state.setdefault(slug, {})["quality_checked"] = True

    save_state(state)

    QC_REPORT.parent.mkdir(parents=True, exist_ok=True)
    QC_REPORT.write_text(json.dumps({
        "ts": date.today().isoformat(),
        "results": all_results,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"\nDone. Report saved to {QC_REPORT}")
    return 0


if __name__ == "__main__":
    from guides.log_setup import setup_logging
    setup_logging()
    sys.exit(main())
