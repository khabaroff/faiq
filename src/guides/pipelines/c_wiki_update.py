"""Pipeline C — Wiki Tools/Patterns Update.

Вход: public/summaries/*.md где state[slug].wiki_propagated != true.
Выход: public/tools/<tool-slug>.md + public/techniques/<technique-slug>.md
      (create / append_mention / rewrite_description — решает LLM).

Шаги:
  1. Найти саммари без wiki_propagated=true
  2. Для каждого: извлечь tools + patterns из YAML frontmatter
  3. Для каждого упоминания:
     - canonicalize slug (LLM решает дедуп: "Claude Code" == "claude-code")
     - загрузить текущую страницу (если есть)
     - прогнать через prompts/wiki_tool_update.md
     - записать обновлённую страницу
  4. state[slug].wiki_propagated = true

Routing: Azure only.

Usage:
  python -m guides.pipelines.c_wiki_update
  python -m guides.pipelines.c_wiki_update --slug foo
  python -m guides.pipelines.c_wiki_update --force
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from datetime import date, datetime
from functools import cache as _cache
from pathlib import Path

import yaml

from guides.atomic_write import atomic_write_text
from guides.frontmatter import parse_frontmatter
from guides.llm import call_llm, get_smart_client, load_prompt
from guides.models import WikiUpdateResponse
from guides.protocols import Logger, get_default_logger
from guides.security.fs_safety import assert_safe_slug, safe_join
from guides.settings import get_settings, Settings
from guides.slugify import canonicalize_slug, slugify
from guides.json_extract import extract_json

log = logging.getLogger(__name__)

def _backup_page(page_path: Path) -> None:
    """Save copy of existing page before overwrite."""
    if not page_path.exists():
        return
    backup_dir = page_path.parent / ".backups"
    backup_dir.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    backup_dir.joinpath(f"{page_path.stem}.{ts}.bak").write_bytes(page_path.read_bytes())


@_cache
def _s() -> Settings:
    return get_settings()


def extract_summary_fm(summary_md: str) -> tuple[list[str], list[str], str]:
    """Returns (tools, patterns, source_url) from summary frontmatter."""
    if not summary_md.startswith("---\n"):
        return [], [], ""
    try:
        end = summary_md.index("\n---\n", 4)
    except ValueError:
        return [], [], ""
    fm_raw = summary_md[4:end]
    try:
        fm = yaml.safe_load(fm_raw) or {}
    except yaml.YAMLError:
        return [], [], ""
    tools = fm.get("tools") or []
    patterns = fm.get("patterns") or []
    source_url = fm.get("source_url", "")
    # normalize: items can be strings or dicts with "name"
    tools = [t if isinstance(t, str) else t.get("name", "") for t in tools if t]
    patterns = [p if isinstance(p, str) else p.get("name", "") for p in patterns if p]
    return tools, patterns, source_url


def call_llm_update(
    slug: str,
    current_page_md: str,
    tool_name: str,
    tool_type: str,
    new_mention: dict,
    kind: str = "",
    logger: Logger | None = None,
) -> dict:
    cost_logger = logger or get_default_logger()
    prompt_template = load_prompt("wiki_tool_update.md")

    prompt = prompt_template.replace("{{current_page_md}}", current_page_md or "(пустая страница)")
    prompt = prompt.replace("{{tool_name}}", tool_name)
    prompt = prompt.replace("{{tool_type}}", tool_type)
    prompt = prompt.replace("{{new_mention}}", json.dumps(new_mention, ensure_ascii=False))

    system = (
        "Ты — эксперт по обновлению wiki-страниц. "
        "Верни валидный JSON согласно контракту. Никакого markdown вокруг JSON."
    )

    deployment = _s().azure_deployment_fast or _s().azure_deployment_smart
    response, usage = call_llm(get_smart_client(), deployment, prompt, system)

    parsed = WikiUpdateResponse.model_validate(extract_json(response))

    if usage:
        cost_logger.log_cost(
            slug=slug,
            action=f"wiki_{kind or tool_type}",
            model=deployment,
            tokens_in=usage.prompt_tokens,
            tokens_out=usage.completion_tokens,
            cost_usd=usage.cost_usd,
        )

    return parsed.model_dump()


def write_wiki_page(page_path: Path, name: str, slug: str, item_type: str, url: str, description: str, mentions: list) -> None:
    today = date.today().isoformat()
    created_at = today
    if page_path.exists():
        fm, _ = parse_frontmatter(page_path.read_text())
        created_at = fm.get("created_at", today)

    front_matter = (
        "---\n"
        f"name: {name}\n"
        f"slug: {slug}\n"
        f"type: {item_type}\n"
        f"url: {url or ''}\n"
        f"created_at: {created_at}\n"
        f"updated_at: {today}\n"
        "---\n\n"
    )

    body = f"# {name}\n\n"
    body += "## Что это\n\n"
    body += f"{description}\n\n"
    body += "## Упоминания\n\n"

    for m in mentions:
        source_slug = m.get("source_slug", "")
        source_url = m.get("source_url", "")
        quote = m.get("quote", "")
        body += f"- [{source_slug}](../summaries/{source_slug}.md)"
        if quote:
            body += f' — "{quote}"'
        if source_url:
            body += f" ({source_url})"
        body += "\n"

    page_path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(page_path, front_matter + body)


def append_mention_to_page(page_path: Path, new_mention: dict) -> None:
    fm, body = parse_frontmatter(page_path.read_text())

    mentions_section_match = re.search(r"## Упоминания\n\n", body)
    if mentions_section_match:
        insert_pos = mentions_section_match.end()
        source_slug = new_mention.get("source_slug", "")
        source_url = new_mention.get("source_url", "")
        quote = new_mention.get("quote", "")

        mention_line = f"- [{source_slug}](../summaries/{source_slug}.md)"
        if quote:
            mention_line += f' — "{quote}"'
        if source_url:
            mention_line += f" ({source_url})"
        mention_line += "\n"

        body = body[:insert_pos] + mention_line + body[insert_pos:]
    else:
        body += "\n## Упоминания\n\n"
        source_slug = new_mention.get("source_slug", "")
        source_url = new_mention.get("source_url", "")
        quote = new_mention.get("quote", "")
        body += f"- [{source_slug}](../summaries/{source_slug}.md)"
        if quote:
            body += f' — "{quote}"'
        if source_url:
            body += f" ({source_url})"
        body += "\n"

    fm["updated_at"] = date.today().isoformat()

    front_matter = "---\n"
    for k, v in fm.items():
        front_matter += f"{k}: {v}\n"
    front_matter += "---\n\n"

    atomic_write_text(page_path, front_matter + body)


def propagate_summary(slug: str, force: bool = False, logger: Logger | None = None) -> int:
    settings = get_settings()
    summary_path = settings.summaries_dir / f"{slug}.md"
    if not summary_path.exists():
        raise FileNotFoundError(summary_path)

    summary_md = summary_path.read_text()
    tools, patterns, source_url = extract_summary_fm(summary_md)

    processed = 0
    for kind, names, target_dir in (
        ("tool", tools, settings.tools_dir),
        ("pattern", patterns, settings.techniques_dir),
    ):
        if not target_dir.exists():
            target_dir.mkdir(parents=True, exist_ok=True)

        existing = [p.stem for p in target_dir.glob("*.md")]

        for name in names:
            if not name:
                continue

            page_slug = canonicalize_slug(name, existing, kind)
            try:
                assert_safe_slug(page_slug)
            except ValueError:
                log.warning("unsafe slug skipped: %r", page_slug)
                continue
            page_path = safe_join(target_dir, f"{page_slug}.md")

            current = ""
            if page_path.exists():
                current = page_path.read_text()

            new_mention = {
                "source_slug": slug,
                "source_url": source_url,
                "role_in_article": "",
                "quote": "",
            }

            try:
                result = call_llm_update(
                    slug=slug,
                    current_page_md=current,
                    tool_name=name,
                    tool_type=kind,
                    new_mention=new_mention,
                    logger=logger,
                )
            except Exception:
                log.exception("LLM error for %s/%s", slug, name)
                continue

            action = result.get("action", "create")
            page_md = result.get("page_md", "")
            if page_md:
                page_md = re.sub(r'<[^>]+>', '', page_md)

            _backup_page(page_path)

            if action == "create" or not page_path.exists():
                if page_md:
                    page_path.parent.mkdir(parents=True, exist_ok=True)
                    atomic_write_text(page_path, page_md)
                else:
                    write_wiki_page(page_path, name, page_slug, kind, source_url, new_mention.get("role_in_article", ""), [new_mention])
            elif action == "append_mention":
                append_mention_to_page(page_path, new_mention)
            elif action == "rewrite_description":
                _fm, _ = parse_frontmatter(current) if current else ({}, "")
                description_match = re.search(r"## Что это\n\n(.*?)(?=\n## |\Z)", page_md, re.DOTALL)
                description = description_match.group(1).strip() if description_match else new_mention.get("role_in_article", "")

                mentions_match = re.search(r"## Упоминания\n\n(.*?)$", page_md, re.DOTALL)
                mentions_text = mentions_match.group(1) if mentions_match else ""
                mentions = []
                for m in mentions_text.strip().split("\n"):
                    if m.startswith("- "):
                        mentions.append({"source_slug": slug, "quote": ""})

                mentions.append(new_mention)
                write_wiki_page(page_path, name, page_slug, kind, source_url, description, mentions)
            else:
                if page_md:
                    page_path.parent.mkdir(parents=True, exist_ok=True)
                    atomic_write_text(page_path, page_md)

            print(f"  {action:>20s}: {page_path}")
            processed += 1

    return processed


def _compute_hash(path: Path) -> str:
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    from guides.state import get_state, set_state

    ap.add_argument("--slug", help="single summary slug to propagate")
    ap.add_argument("--force", action="store_true", help="re-propagate even if already propagated")
    ap.add_argument("--batch", type=int, default=0, help="limit to N items (0 = all)")
    args = ap.parse_args(argv)
    settings = get_settings()

    if args.slug:
        slugs = [args.slug]
    else:
        if not settings.summaries_dir.exists():
            print(f"Summaries dir does not exist: {settings.summaries_dir}")
            return 1
        slugs = [p.stem for p in settings.summaries_dir.glob("*.md")]

    if args.batch > 0:
        slugs = slugs[:args.batch]

    total_processed = 0
    for slug in slugs:
        summary_path = settings.summaries_dir / f"{slug}.md"
        if summary_path.exists():
            sum_hash = _compute_hash(summary_path)
        else:
            sum_hash = None
        stored = get_state(slug)
        if not args.force and stored.get("c_hash") == sum_hash and stored.get("wiki_propagated"):
            print(f"skip (propagated): {slug}")
            continue
        print(f"propagate: {slug}")
        try:
            processed = propagate_summary(slug, args.force)
            set_state(slug, "wiki_propagated", True)
            set_state(slug, "wiki_propagated_at", date.today().isoformat())
            set_state(slug, "c_hash", sum_hash)
            set_state(slug, "status", "propagated")
            total_processed += processed
        except Exception:
            log.exception("Failed to propagate %s", slug)

    print(f"Total wiki pages updated: {total_processed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
