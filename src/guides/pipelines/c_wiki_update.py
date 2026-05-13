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
import re
import sys
from datetime import date
from pathlib import Path

import yaml

from guides.llm import call_llm, get_smart_client, load_prompt
from guides.settings import Settings
from guides.tools.daily_log import append_log_entry

ROOT = Path(__file__).resolve().parent.parent.parent.parent
CONTENT_DIR = ROOT / "public"
SUMMARIES_DIR = CONTENT_DIR / "summaries"
WIKI_TOOLS_DIR = CONTENT_DIR / "tools"
WIKI_TECH_DIR = CONTENT_DIR / "techniques"
STATE_FILE = ROOT / "state" / "index.json"

s = Settings()


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def slugify(name: str) -> str:
    s = re.sub(r"[^\w\s-]", "", name.lower())
    return re.sub(r"[-\s]+", "-", s).strip("-")[:80]


def canonicalize_slug(name: str, existing_slugs: list[str], item_type: str) -> str:
    prompt = f"""Канонизируй slug для {item_type} с именем "{name}".

Существующие slugs в системе: {existing_slugs[:10] if existing_slugs else 'нет'}

Верни JSON:
{{"slug": "каноничный-slug", "reason": "краткое пояснение"}}

Правила:
- Если имя точно совпадает с существующим slug — используй его
- Если "{name}" может означать то же, что существующий slug — используй существующий
- Иначе — создай новый slug на основе имени (только a-z, дефисы)
- Не более 80 символов"""

    system = "Ты — эксперт по нормализации данных. Верни валидный JSON."

    try:
        response, _ = call_llm(get_smart_client(), s.azure_deployment_fast or s.azure_deployment_smart, prompt, system)
        json_match = re.search(r"\{[\s\S]*\}", response)
        if json_match:
            result = json.loads(json_match.group())
            return result.get("slug", slugify(name))
    except Exception:
        pass
    return slugify(name)


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


def call_llm_update(slug: str, current_page_md: str, tool_name: str, tool_type: str, new_mention: dict) -> dict:
    prompt_template = load_prompt("wiki_tool_update.md")

    prompt = prompt_template.replace("{{current_page_md}}", current_page_md or "(пустая страница)")
    prompt = prompt.replace("{{tool_name}}", tool_name)
    prompt = prompt.replace("{{tool_type}}", tool_type)
    prompt = prompt.replace("{{new_mention}}", json.dumps(new_mention, ensure_ascii=False))

    system = (
        "Ты — эксперт по обновлению wiki-страниц. "
        "Верни валидный JSON согласно контракту. Никакого markdown вокруг JSON."
    )

    deployment = s.azure_deployment_fast or s.azure_deployment_smart
    response, usage = call_llm(get_smart_client(), deployment, prompt, system)

    json_match = re.search(r"\{[\s\S]*\}", response)
    if not json_match:
        raise ValueError(f"No JSON in LLM response: {response[:200]}")

    result = json.loads(json_match.group())

    if usage:
        append_log_entry(
            slug=slug,
            action=f"wiki_{kind}",
            model=deployment,
            tokens_in=usage.prompt_tokens,
            tokens_out=usage.completion_tokens,
            cost_usd=usage.cost_usd,
        )

    return result


def write_wiki_page(page_path: Path, name: str, slug: str, item_type: str, url: str, description: str, mentions: list) -> None:
    today = date.today().isoformat()
    created_at = today
    if page_path.exists():
        fm, _ = parse_front_matter(page_path.read_text())
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
        role = m.get("role_in_article", "")
        quote = m.get("quote", "")
        body += f"- [{source_slug}](../summaries/{source_slug}.md)"
        if quote:
            body += f' — "{quote}"'
        if source_url:
            body += f" ({source_url})"
        body += "\n"

    page_path.parent.mkdir(parents=True, exist_ok=True)
    page_path.write_text(front_matter + body)


def parse_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.index("\n---\n", 4)
    fm_raw = text[4:end]
    body = text[end + 5:]
    fm = {}
    for line in fm_raw.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm, body


def append_mention_to_page(page_path: Path, new_mention: dict) -> None:
    fm, body = parse_front_matter(page_path.read_text())

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

    page_path.write_text(front_matter + body)


def propagate_summary(slug: str, force: bool = False) -> int:
    summary_path = SUMMARIES_DIR / f"{slug}.md"
    if not summary_path.exists():
        raise FileNotFoundError(summary_path)

    summary_md = summary_path.read_text()
    tools, patterns, source_url = extract_summary_fm(summary_md)

    processed = 0
    for kind, names, target_dir in (
        ("tool", tools, WIKI_TOOLS_DIR),
        ("pattern", patterns, WIKI_TECH_DIR),
    ):
        if not target_dir.exists():
            target_dir.mkdir(parents=True, exist_ok=True)

        existing = [p.stem for p in target_dir.glob("*.md")]

        for name in names:
            if not name:
                continue

            page_slug = canonicalize_slug(name, existing, kind)
            page_path = target_dir / f"{page_slug}.md"

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
                )
            except Exception as e:
                print(f"  LLM error for {name}: {e}", file=sys.stderr)
                continue

            action = result.get("action", "create")
            page_md = result.get("page_md", "")

            if action == "create" or not page_path.exists():
                if page_md:
                    page_path.parent.mkdir(parents=True, exist_ok=True)
                    page_path.write_text(page_md)
                else:
                    write_wiki_page(page_path, name, page_slug, kind, source_url, new_mention.get("role_in_article", ""), [new_mention])
            elif action == "append_mention":
                append_mention_to_page(page_path, new_mention)
            elif action == "rewrite_description":
                fm, _ = parse_front_matter(current) if current else ({}, "")
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
                    page_path.write_text(page_md)

            print(f"  {action:>20s}: {page_path}")
            processed += 1

    return processed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", help="single summary slug to propagate")
    ap.add_argument("--force", action="store_true", help="re-propagate even if already propagated")
    ap.add_argument("--batch", type=int, default=0, help="limit to N items (0 = all)")
    args = ap.parse_args()

    state = load_state()

    if args.slug:
        slugs = [args.slug]
    else:
        if not SUMMARIES_DIR.exists():
            print(f"Summaries dir does not exist: {SUMMARIES_DIR}")
            return 1
        slugs = [p.stem for p in SUMMARIES_DIR.glob("*.md")]

    if args.batch > 0:
        slugs = slugs[:args.batch]

    total_processed = 0
    for slug in slugs:
        if not args.force and state.get(slug, {}).get("wiki_propagated"):
            print(f"skip (propagated): {slug}")
            continue
        print(f"propagate: {slug}")
        try:
            processed = propagate_summary(slug, args.force)
            state.setdefault(slug, {})["wiki_propagated"] = True
            state[slug]["wiki_propagated_at"] = date.today().isoformat()
            total_processed += processed
        except Exception as e:
            print(f"ERROR {slug}: {e}", file=sys.stderr)

    save_state(state)
    print(f"Total wiki pages updated: {total_processed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())