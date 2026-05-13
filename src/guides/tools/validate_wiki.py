"""CLI: validate and optionally autofix wiki extract pages."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from guides.process.validate import ValidationResult, autofix_file, check_file


def _fmt_result(r: ValidationResult) -> str:
    if r.is_valid and not r.warnings:
        return f"  OK  {r.path}"
    lines = [f"{'FAIL' if r.errors else 'WARN'}  {r.path}"]
    for v in r.violations:
        tag = "E" if v.severity == "error" else "W"
        lines.append(f"        [{tag}] {v.rule}: {v.detail}")
    return "\n".join(lines)


def _iter_wiki_pages(wiki_dir: Path) -> list[Path]:
    extracts_dir = wiki_dir / "extracts"
    if extracts_dir.exists():
        return sorted(p for p in extracts_dir.rglob("*.md") if p.is_file())
    return sorted(
        p
        for p in wiki_dir.rglob("*.md")
        if p.is_file() and "_indexes" not in p.parts and p.name != "log.md"
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Validate wiki extract pages")
    p.add_argument("wiki_dir", nargs="?", default="wiki", help="Path to wiki directory")
    p.add_argument("--fix", action="store_true", help="Autofix violations in-place")
    p.add_argument("--errors-only", action="store_true", help="Print only pages with errors")
    args = p.parse_args(argv)

    wiki_dir = Path(args.wiki_dir)
    if not wiki_dir.exists():
        print(f"error: {wiki_dir} does not exist", file=sys.stderr)
        return 1

    pages = _iter_wiki_pages(wiki_dir)
    if not pages:
        print("No .md files found.")
        return 0

    total = ok = errors = warnings_only = fixed = 0
    for path in pages:
        total += 1
        if args.fix:
            changed, applied = autofix_file(path)
            if changed:
                fixed += 1
                print(f"  FIX  {path}  ({', '.join(applied)})")
        result = check_file(path)
        if result.errors:
            errors += 1
            print(_fmt_result(result))
        elif result.warnings:
            warnings_only += 1
            if not args.errors_only:
                print(_fmt_result(result))
        else:
            ok += 1
            if not args.errors_only:
                print(_fmt_result(result))

    print()
    print(f"Checked {total} pages: {ok} OK, {warnings_only} warn, {errors} errors", end="")
    if args.fix:
        print(f", {fixed} fixed", end="")
    print()
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
