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
from pathlib import Path

import yaml

from guides.llm import call_llm, get_smart_client, load_prompt
from guides.settings import Settings
from guides.state import get_state, set_state

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent.parent.parent
CONTENT_DIR = ROOT / "public"
SUMMARIES_DIR = CONTENT_DIR / "summaries"
SOURCES_DIR = CONTENT_DIR / "sources"

s = Settings()


def parse_front_matter_yaml(text: str) -> tuple[dict, str]:
    """YAML-aware parser. Returns (fm, body)."""
    if not text.startswith("---\n"):
        return {}, text
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        return {}, text
    fm_raw = text[4:end]
    body = text[end + 5:]
    try:
        fm = yaml.safe_load(fm_raw) or {}
        if not isinstance(fm, dict):
            fm = {}
        return fm, body
    except yaml.YAMLError:
        return {}, text


def _extract_json(text: str) -> dict:
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError(f"No JSON found in response: {text[:200]}")
    return json.loads(match.group())


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
    
    deployment = s.azure_deployment_fast or s.azure_deployment_smart
    system = "You are a technical SEO expert. Return only valid JSON as requested. No prose."
    
    response, _ = call_llm(get_smart_client(), deployment, prompt, system)
    return _extract_json(response)


def optimize_one(slug: str) -> bool:
    summary_path = SUMMARIES_DIR / f"{slug}.md"
    if not summary_path.exists():
        return False
    
    text = summary_path.read_text(encoding="utf-8")
    fm, body = parse_front_matter_yaml(text)
    
    # Try to get title from source if not in summary fm
    if not fm.get("title"):
        source_path = SOURCES_DIR / f"{slug}.md"
        if source_path.exists():
            src_fm, _ = parse_front_matter_yaml(source_path.read_text(encoding="utf-8"))
            fm["title"] = src_fm.get("title")

    print(f"Optimizing SEO for: {slug}...")
    try:
        seo_meta = call_llm_seo(fm, body)
        
        # Update frontmatter
        fm.update(seo_meta)
        
        # Write back
        fm_str = "---\n" + yaml.dump(fm, allow_unicode=True, default_flow_style=False) + "---\n\n"
        summary_path.write_text(fm_str + body, encoding="utf-8")
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
        if not SUMMARIES_DIR.exists():
            print(f"Summaries dir does not exist: {SUMMARIES_DIR}")
            return 1
        slugs = [p.stem for p in SUMMARIES_DIR.glob("*.md")]

    processed_count = 0
    for slug in slugs:
        state = get_state(slug)
        if not args.force and state.get("seo_optimized"):
            continue
            
        if optimize_one(slug):
            set_state(slug, "seo_optimized", True)
            # We don't have a specific seo_optimized_at in set_state helpers yet, 
            # but we can add it or just rely on the boolean for now.
            processed_count += 1
            print(f"  → Optimized: {slug}")

    print(f"Done. Processed {processed_count} summaries.")
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    sys.exit(main())
