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
from guides.llm import call_llm, count_tokens, get_smart_client, load_prompt, truncate_to_tokens
from guides.models import SummaryCheckResponse, WikiCleanResponse
from guides.settings import get_settings
from guides.state import get_state, set_state, update_frontmatter
from guides.json_extract import extract_json

logger = logging.getLogger(__name__)

MAX_QC_TOKENS = 8000
CHUNK_OVERLAP = 500

_extract_json = extract_json


def _qc_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def _chunk_text_by_tokens(text: str, max_tokens: int, overlap: int = 500) -> list[str]:
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
    except Exception:
        # fallback to rough char slicing if tiktoken fails
        chars_per_token = 2 # RU conservative
        chunk_chars = max_tokens * chars_per_token
        overlap_chars = overlap * chars_per_token
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_chars
            chunks.append(text[start:end])
            if end >= len(text):
                break
            start = end - overlap_chars
        return chunks

    tokens = enc.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + max_tokens
        chunk_tokens = tokens[start:end]
        chunks.append(enc.decode(chunk_tokens))
        if end >= len(tokens):
            break
        start = end - overlap
    return chunks


def call_llm_summary_check(source_text: str, summary_text: str, slug: str) -> dict:
    prompt_template = load_prompt("quality_check.md")
    
    source_tokens = count_tokens(source_text)
    
    if source_tokens <= MAX_QC_TOKENS:
        return _call_qc_single(prompt_template, source_text, summary_text, slug)
    
    # Sliding window
    logger.info("Source too long (%d tokens), using sliding window for %s", source_tokens, slug)
    chunks = _chunk_text_by_tokens(source_text, MAX_QC_TOKENS, CHUNK_OVERLAP)
    results = []
    
    for i, chunk in enumerate(chunks):
        part_info = f"ВНИМАНИЕ: Это часть {i+1} из {len(chunks)} исходного текста. Проверь саммари на соответствие ЭТОЙ части. Саммари может содержать факты из других частей — не считай их галлюцинациями, если они не противоречат текущей части."
        res = _call_qc_single(prompt_template, chunk, summary_text, slug, prefix=part_info)
        results.append(res)
    
    return _aggregate_qc_results(results)


def _call_qc_single(prompt_template: str, source_text: str, summary_text: str, slug: str, prefix: str = "") -> dict:
    input_block = f"\n\n## Вход\n\n### Source ({slug})\n<UNTRUSTED_CONTENT>\n{source_text}\n</UNTRUSTED_CONTENT>\n\n### Summary\n<INPUT_DATA>\n{summary_text}\n</INPUT_DATA>"
    if prefix:
        prompt = prefix + "\n\n" + prompt_template + input_block
    else:
        prompt = prompt_template + input_block

    s = get_settings()
    deployment = s.azure_deployment_fast or s.azure_deployment_smart

    system = "Ты — эксперт по качеству технической документации. Твоя задача — проверить соответствие саммари исходному тексту. Верни только JSON."

    response, _ = call_llm(get_smart_client(), deployment, prompt, system)
    raw = _extract_json(response)
    return SummaryCheckResponse.model_validate(raw).model_dump()


def _aggregate_qc_results(results: list[dict]) -> dict:
    verdict_priority = {"needs_resummarize": 3, "minor_fix": 2, "ok": 1, "error": 0}
    
    final_verdict = "ok"
    final_issues = []
    seen_issues = set()
    
    for res in results:
        v = res.get("verdict", "ok")
        if verdict_priority.get(v, 0) > verdict_priority.get(final_verdict, 0):
            final_verdict = v
        
        for issue in res.get("issues", []):
            if issue not in seen_issues:
                final_issues.append(issue)
                seen_issues.add(issue)
                
    return {
        "mode": "summary_check",
        "verdict": final_verdict,
        "issues": final_issues
    }


def call_llm_wiki_clean(page_text: str, slug: str) -> dict:
    prompt_template = load_prompt("quality_check.md")

    prompt = prompt_template + f"\n\n## Вход\n\n### Wiki Page ({slug})\n{page_text}"

    s = get_settings()
    deployment = s.azure_deployment_fast or s.azure_deployment_smart

    system = "Ты — редактор технической вики. Твоя задача — очистить страницу от дублей и битых ссылок. Верни только JSON."

    response, _ = call_llm(get_smart_client(), deployment, prompt, system)
    raw = _extract_json(response)
    return WikiCleanResponse.model_validate(raw).model_dump()


def check_summaries(slug_filter: str | None = None) -> list[dict]:
    settings = get_settings()
    results = []
    if slug_filter:
        sum_files = [settings.summaries_dir / f"{slug_filter}.md"]
    else:
        sum_files = list(settings.summaries_dir.glob("*.md"))

    for sum_path in sum_files:
        if not sum_path.exists():
            continue
        slug = sum_path.stem
        src_path = settings.sources_dir / f"{slug}.md"
        if not src_path.exists():
            logger.warning("Source for summary %s not found", slug)
            continue

        print(f"Checking summary: {slug}...")
        try:
            source_text = src_path.read_text(encoding="utf-8")
            summary_text = sum_path.read_text(encoding="utf-8")
            new_hash = _qc_hash(source_text + summary_text)
            stored = get_state(slug)
            if (stored.get("d_hash") == new_hash or stored.get("qc_hash") == new_hash) and stored.get("quality_checked"):
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
    settings = get_settings()
    results = []

    targets = []
    if slug_filter:
        for d in (settings.tools_dir, settings.techniques_dir):
            p = d / f"{slug_filter}.md"
            if p.exists():
                targets.append(p)
    else:
        targets.extend(list(settings.tools_dir.glob("*.md")))
        targets.extend(list(settings.techniques_dir.glob("*.md")))

    for page in targets:
        slug = page.stem
        print(f"Cleaning wiki page: {slug}...")
        try:
            page_text = page.read_text(encoding="utf-8")
            new_hash = _qc_hash(page_text)
            stored = get_state(slug)
            if (stored.get("d_hash") == new_hash or stored.get("qc_hash") == new_hash) and stored.get("quality_checked"):
                print(f"  [skip] {slug} unchanged")
                continue
            res = call_llm_wiki_clean(page_text, slug)
            res["slug"] = slug
            res["mode"] = "wiki_clean"
            res["path"] = str(page.relative_to(settings.public_dir))
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
                set_state(slug, "d_hash", res["qc_hash"])
            if res.get("verdict"):
                set_state(slug, "quality", res["verdict"])
                if res["verdict"] == "ok":
                    set_state(slug, "status", "quality_ok")

    # Update frontmatter for all non-error results
    settings = get_settings()
    for res in all_results:
        if res.get("verdict") != "error":
            slug = res["slug"]
            summary_path = settings.summaries_dir / f"{slug}.md"
            if summary_path.exists():
                update_frontmatter(summary_path, {"status": "quality_ok" if res.get("verdict") == "ok" else "quality_needs_review"})

    qc_report = settings.state_dir / "quality-report.json"
    qc_report.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(qc_report, json.dumps({
        "ts": date.today().isoformat(),
        "results": all_results,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nDone. Report saved to {qc_report}")
    return 0


if __name__ == "__main__":
    from guides.log_setup import setup_logging
    setup_logging()
    sys.exit(main())
