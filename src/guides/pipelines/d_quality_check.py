"""Pipeline D — Quality Check.

Two modes:
  - summary_check: source + summary → verdict (ok | needs_resummarize | minor_fix)
  - wiki_clean:    wiki page → cleaned page (if needed)

Prompt: prompts/quality_check.md
LLM: Azure mini (cheap).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
import sys
from datetime import date
from pathlib import Path

from guides.atomic_write import atomic_write_text
from guides.llm import call_llm, get_smart_client, load_prompt
from guides.models import SummaryCheckResponse, WikiCleanResponse
from guides.settings import Settings
from guides.state import get_state, set_state, update_frontmatter
from guides.utils.json_extract import extract_first_json

logger = logging.getLogger(__name__)

settings = Settings()
ROOT = Path(__file__).resolve().parent.parent.parent.parent
QC_REPORT = settings.state_dir / "quality-report.json"

# Content paths
SOURCES_DIR = settings.sources_dir
SUMMARIES_DIR = settings.summaries_dir
TOOLS_DIR = settings.tools_dir
TECH_DIR = settings.techniques_dir


_extract_json = extract_first_json


def _qc_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def call_llm_summary_check(source_text: str, summary_text: str, slug: str) -> dict:
    prompt_template = load_prompt("quality_check.md")

    prompt = prompt_template + f"\n\n## Вход\n\n### Source ({slug})\n{source_text[:5000]}\n\n### Summary\n{summary_text}"

    s = Settings()
    deployment = s.azure_deployment_fast or s.azure_deployment_smart

    system = "Ты — эксперт по качеству технической документации. Твоя задача — проверить соответствие саммари исходному тексту. Верни только JSON."

    response, _ = call_llm(get_smart_client(), deployment, prompt, system)
    raw = _extract_json(response)
    return SummaryCheckResponse.model_validate(raw).model_dump()


def call_llm_wiki_clean(page_text: str, slug: str) -> dict:
    prompt_template = load_prompt("quality_check.md")

    prompt = prompt_template + f"\n\n## Вход\n\n### Wiki Page ({slug})\n{page_text}"

    s = Settings()
    deployment = s.azure_deployment_fast or s.azure_deployment_smart

    system = "Ты — редактор технической вики. Твоя задача — очистить страницу от дублей и битых ссылок. Верни только JSON."

    response, _ = call_llm(get_smart_client(), deployment, prompt, system)
    raw = _extract_json(response)
    return WikiCleanResponse.model_validate(raw).model_dump()


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
            source_text = src_path.read_text(encoding="utf-8")
            summary_text = sum_path.read_text(encoding="utf-8")
            new_hash = _qc_hash(source_text + summary_text)
            stored = get_state(slug)
            if stored.get("qc_hash") == new_hash and stored.get("quality_checked"):
                print(f"  [skip] {slug} unchanged")
                continue
            res = call_llm_summary_check(source_text, summary_text, slug)
            res["slug"] = slug
            res["mode"] = "summary_check"
            res["qc_hash"] = new_hash
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
            page_text = page.read_text(encoding="utf-8")
            new_hash = _qc_hash(page_text)
            stored = get_state(slug)
            if stored.get("qc_hash") == new_hash and stored.get("quality_checked"):
                print(f"  [skip] {slug} unchanged")
                continue
            res = call_llm_wiki_clean(page_text, slug)
            res["slug"] = slug
            res["mode"] = "wiki_clean"
            res["path"] = str(page.relative_to(ROOT))
            res["qc_hash"] = new_hash

            if res.get("verdict") == "needs_cleanup" and "cleaned_page_md" in res:
                content = res["cleaned_page_md"]
                content = re.sub(r'<[^>]+>', '', content)
                atomic_write_text(page, content)
                print(f"  -> Cleaned: {slug}")

            results.append(res)
        except Exception as e:
            logger.error("Failed QC for wiki page %s: %s", slug, e)
            results.append({"slug": slug, "mode": "wiki_clean", "verdict": "error", "error": str(e)})

    return results


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Pipeline D: Quality Check")
    parser.add_argument("--mode", choices=["summary", "wiki", "both"], default="both")
    parser.add_argument("--slug", help="Process only this slug")
    args = parser.parse_args(argv)

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
            set_state(slug, "quality_checked", True)
            if res.get("qc_hash"):
                set_state(slug, "qc_hash", res["qc_hash"])
            if res.get("verdict"):
                set_state(slug, "quality", res["verdict"])
                if res["verdict"] == "ok":
                    set_state(slug, "status", "quality_ok")

    # Update frontmatter for all non-error results
    for res in all_results:
        if res.get("verdict") != "error":
            slug = res["slug"]
            summary_path = SUMMARIES_DIR / f"{slug}.md"
            if summary_path.exists():
                update_frontmatter(summary_path, {"status": "quality_ok" if res.get("verdict") == "ok" else "quality_needs_review"})

    QC_REPORT.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(QC_REPORT, json.dumps({
        "ts": date.today().isoformat(),
        "results": all_results,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nDone. Report saved to {QC_REPORT}")
    return 0


if __name__ == "__main__":
    from guides.log_setup import setup_logging
    setup_logging()
    sys.exit(main())
