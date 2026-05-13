"""Pipeline G — Telegram Publisher.

Input: public/summaries/*.md where state[slug].published_telegram is empty.
Output: Post to Telegram channel.

Prompt: prompts/telegram_post.md
Config: TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID from .env.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import httpx
import yaml

from guides.llm import call_llm, get_smart_client, load_prompt
from guides.settings import Settings
from guides.state import get_state, set_state

logger = logging.getLogger(__name__)

ROOT = Path.cwd()
CONTENT_DIR = ROOT / "public"
SUMMARIES_DIR = CONTENT_DIR / "summaries"

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

def _render_telegram_prompt(fm: dict) -> str:
    prompt_template = load_prompt("telegram_post.md")
    
    prompt = prompt_template
    prompt = prompt.replace("{{title}}", fm.get("title") or fm.get("slug") or "Untitled")
    prompt = prompt.replace("{{tldr}}", fm.get("seo_description") or "")
    prompt = prompt.replace("{{key_claims}}", json.dumps(fm.get("key_claims", []), ensure_ascii=False))
    prompt = prompt.replace("{{tools}}", json.dumps(fm.get("tools", []), ensure_ascii=False))
    prompt = prompt.replace("{{patterns}}", json.dumps(fm.get("patterns", []), ensure_ascii=False))
    prompt = prompt.replace("{{source_url}}", fm.get("source_url", ""))
    
    # summary_url is optional, could be constructed if site domain is known
    # For now, let's leave it empty or use a placeholder if needed
    prompt = prompt.replace("{{summary_url}}", "")
    
    return prompt

def call_llm_telegram(fm: dict) -> str:
    prompt = _render_telegram_prompt(fm)
    
    deployment = s.azure_deployment_fast or s.azure_deployment_smart
    system = "You are a social media manager for a technical AI channel. Write a concise and engaging Telegram post. Follow the format exactly."
    
    response = call_llm(get_smart_client(), deployment, prompt, system)
    return response.strip()

def send_telegram_message(text: str) -> bool:
    if not s.telegram_bot_token or not s.telegram_channel_id:
        logger.error("TELEGRAM_BOT_TOKEN or TELEGRAM_CHANNEL_ID not set")
        return False
    
    url = f"https://api.telegram.org/bot{s.telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": s.telegram_channel_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
        return True
    except Exception as e:
        logger.error("Failed to send Telegram message: %s", e)
        # If markdown parsing fails, try sending as plain text
        if "can't parse entities" in str(e).lower():
            logger.warning("Markdown parsing failed, retrying as plain text")
            payload.pop("parse_mode")
            try:
                with httpx.Client(timeout=10.0) as client:
                    resp = client.post(url, json=payload)
                    resp.raise_for_status()
                return True
            except Exception as e2:
                logger.error("Retry failed: %s", e2)
        return False

def publish_one(slug: str, dry_run: bool = False) -> bool:
    summary_path = SUMMARIES_DIR / f"{slug}.md"
    if not summary_path.exists():
        logger.error(f"Summary file not found: {summary_path}")
        return False
    
    text = summary_path.read_text(encoding="utf-8")
    fm, _ = parse_front_matter_yaml(text)
    
    print(f"Generating Telegram post for: {slug}...")
    try:
        post_content = call_llm_telegram(fm)
        
        if dry_run:
            print("--- DRY RUN PREVIEW ---")
            print(post_content)
            print("-----------------------")
            return True
        
        if send_telegram_message(post_content):
            set_state(slug, "published_telegram", datetime.now().isoformat())
            return True
        return False
    except Exception as e:
        logger.error("Failed to publish to Telegram for %s: %s", slug, e)
        return False

def main() -> int:
    parser = argparse.ArgumentParser(description="Pipeline G: Telegram Publisher")
    parser.add_argument("--slug", help="Process only this slug")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, do not post")
    parser.add_argument("--force", action="store_true", help="Reprocess even if already published")
    args = parser.parse_args()

    if args.slug:
        slugs = [args.slug]
    else:
        # Find all summaries
        if not SUMMARIES_DIR.exists():
            print(f"Summaries dir does not exist: {SUMMARIES_DIR}")
            return 1
        slugs = [p.stem for p in SUMMARIES_DIR.glob("*.md")]

    processed_count = 0
    for slug in slugs:
        state = get_state(slug)
        if not args.force and state.get("published_telegram"):
            continue
            
        if publish_one(slug, dry_run=args.dry_run):
            processed_count += 1
            if not args.dry_run:
                print(f"  → Published: {slug}")
            else:
                print(f"  → Previewed: {slug}")

    print(f"Done. Processed {processed_count} summaries.")
    return 0

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    sys.exit(main())
