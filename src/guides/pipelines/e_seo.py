"""Pipeline E — SEO Optimizer.

Input: public/summaries/*.md where state[slug].seo_optimized != True.
Output: Update summaries frontmatter with seo_title, seo_description, and og_description.

Prompt: prompts/seo.md
Model: Azure mini (fast).
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from datetime import date
from functools import cache as _cache
from pathlib import Path

from guides.frontmatter import parse_frontmatter
from guides.llm import call_llm, get_smart_client, load_prompt
from guides.models import SeoResponse
from guides.settings import get_settings, Settings
from guides.state import get_state, set_state, update_frontmatter
from guides.json_extract import extract_json

logger = logging.getLogger(__name__)


@_cache
def _s() -> Settings:
    return get_settings()


_extract_json = extract_json


def _render_seo_prompt(fm: dict, body: str) -> str:
    prompt_template = load_prompt("seo.md")

    # Simple extraction of TL;DR from body if present
    tldr = ""
    tldr_match = re.search(r"## TL;DR\n\n(.*?)(?=\n## |\Z)", body, re.DOTALL)
    if tldr_match:
        tldr = tldr_match.group(1).strip()

    prompt = prompt_template
    prompt = prompt.replace("{{title}}", fm.get("title") or fm.get("slug") or "Untitled")
    prompt = prompt.replace("{{tldr}}", tldr)
    prompt = prompt.replace("{{key_claims}}", json.dumps(fm.get("key_claims", []), ensure_ascii=False))
    prompt = prompt.replace("{{tools}}", json.dumps(fm.get("tools", []), ensure_ascii=False))
    prompt = prompt.replace("{{patterns}}", json.dumps(fm.get("patterns", []), ensure_ascii=False))
    prompt = prompt.replace("{{source_url}}", fm.get("source_url", ""))

    return prompt


def call_llm_seo(fm: dict, body: str) -> dict:
    prompt = _render_seo_prompt(fm, body)

    deployment = _s().azure_deployment_fast or _s().azure_deployment_smart
    system = "You are a technical SEO expert. Return only valid JSON as requested. No prose."

    response, _ = call_llm(get_smart_client(), deployment, prompt, system)
    raw = _extract_json(response)
    return SeoResponse.model_validate(raw).model_dump(exclude_defaults=False)


def optimize_one(slug: str) -> bool:
    settings = get_settings()
    summary_path = settings.summaries_dir / f"{slug}.md"
    if not summary_path.exists():
        return False

    text = summary_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)

    # Try to get title from source if not in summary fm
    if not fm.get("title"):
        source_path = settings.sources_dir / f"{slug}.md"
        if source_path.exists():
            src_fm, _ = parse_frontmatter(source_path.read_text(encoding="utf-8"))
            fm["title"] = src_fm.get("title")

    print(f"Optimizing SEO for: {slug}...")
    try:
        seo_meta = call_llm_seo(fm, body)

        # Update frontmatter
        seo_meta.setdefault("seo_optimized_at", date.today().isoformat())
        update_frontmatter(summary_path, seo_meta)
        return True
    except Exception as e:
        logger.error("Failed SEO optimization for %s: %s", slug, e)
        return False


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Pipeline E: SEO Optimizer")
    parser.add_argument("--slug", help="Process only this slug")
    parser.add_argument("--force", action="store_true", help="Reprocess even if optimized")
    args = parser.parse_args(argv)

    if args.slug:
        slugs = [args.slug]
    else:
        settings = get_settings()
        if not settings.summaries_dir.exists():
            print(f"Summaries dir does not exist: {settings.summaries_dir}")
            return 1
        slugs = [p.stem for p in settings.summaries_dir.glob("*.md")]

    processed_count = 0
    for slug in slugs:
        state = get_state(slug)
        if not args.force and state.get("seo_optimized"):
            continue

        if optimize_one(slug):
            set_state(slug, "seo_optimized", True)
            set_state(slug, "status", "seo_optimized")
            processed_count += 1
            print(f"  → Optimized: {slug}")

    print(f"Done. Processed {processed_count} summaries.")
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    sys.exit(main())
