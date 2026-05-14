"""Preprocess remote images in vault/raw markdown files with OCR captions."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import re
import sqlite3
import sys
import tempfile
import threading
import time
import urllib.parse
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Literal

import httpx
from pydantic import BaseModel

from guides.llm import call_smart_with_images
from guides.security.url_safety import validate_url
from guides.settings import get_settings

settings = get_settings()
REPO_ROOT = Path(__file__).resolve().parents[3]
ASSETS_DIR = settings.sources_dir / "_assets"
CACHE_DB_PATH = settings.state_dir / "ocr_cache.sqlite"
RUNS_LOG_PATH = settings.logs_dir / "ocr_runs.jsonl"

MODEL = settings.ocr_model
PROMPT_VERSION = "v1"
OCR_MARKER = "> **Image OCR (auto):**"
DEFAULT_TIMEOUT_SECONDS = 30
MAX_RETRIES = 3
OCR_MAX_COMPLETION_TOKENS = 4096
MAX_OCR_IMAGE_SIZE = (2048, 2048)
OCR_PARALLELISM = 4

REMOTE_IMAGE_SCHEME_RE = re.compile(r"^https?://", re.IGNORECASE)
MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\((?P<url><[^>]+>|[^)\s]+)", re.IGNORECASE)
HTML_IMAGE_RE = re.compile(
    r"<img\b[^>]*?\bsrc=(?P<quote>[\"']?)(?P<url>[^\"' >]+)(?P=quote)",
    re.IGNORECASE,
)


class OCRResult(BaseModel):
    image_type: Literal["diagram", "ui-screenshot", "other"]
    visible_text: str
    description: str


class NonImageContentError(RuntimeError):
    def __init__(self, url: str, content_type: str) -> None:
        super().__init__(f"non-image remote URL skipped: {url} ({content_type})")
        self.url = url
        self.content_type = content_type


OCR_PROMPT = (
    "You are extracting OCR from a remote image embedded in a markdown article. "
    "Classify the image as diagram, ui-screenshot, or other. Return only JSON "
    "with keys image_type, visible_text, description. For visible_text, transcribe "
    "all readable on-image text verbatim and keep the line structure/newlines. "
    "For description, write 2-4 concise sentences explaining what the image shows."
)


def _ensure_dirs() -> None:
    settings.state_dir.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    RUNS_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def _normalize_url(raw_url: str) -> str:
    url = raw_url.strip()
    if url.startswith("<") and url.endswith(">"):
        url = url[1:-1].strip()
    return url


def extract_remote_image_urls(line: str) -> list[str]:
    matches: list[tuple[int, str]] = []
    for m in MARKDOWN_IMAGE_RE.finditer(line):
        url = _normalize_url(m.group("url"))
        if REMOTE_IMAGE_SCHEME_RE.match(url):
            matches.append((m.start(), url))
    for m in HTML_IMAGE_RE.finditer(line):
        url = _normalize_url(m.group("url"))
        if REMOTE_IMAGE_SCHEME_RE.match(url):
            matches.append((m.start(), url))
    matches.sort(key=lambda item: item[0])
    return [url for _, url in matches]


def discover_markdown_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(path)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
        elif path.suffix.lower() == ".md":
            files.append(path)
    deduped: list[Path] = []
    seen: set[Path] = set()
    for path in files:
        if path in seen:
            continue
        seen.add(path)
        deduped.append(path)
    return deduped


def _download_url(url: str) -> tuple[bytes, str]:
    current_url = url
    max_redirects = 5
    redirects_followed = 0

    with httpx.Client(
        headers={"User-Agent": "guides-ocr-images/1.0"},
        timeout=DEFAULT_TIMEOUT_SECONDS,
        follow_redirects=False
    ) as client:
        while True:
            validate_url(current_url)
            try:
                resp = client.get(current_url)
                if resp.is_redirect:
                    redirects_followed += 1
                    if redirects_followed > max_redirects:
                        raise ValueError(f"Too many redirects for {url}")
                    location = resp.headers.get("location")
                    if not location:
                        raise ValueError(f"Redirect without location for {current_url}")
                    # Join relative location with current_url
                    current_url = str(httpx.URL(current_url).join(location))
                    continue
                
                resp.raise_for_status()
                data = resp.content
                content_type = resp.headers.get("content-type") or "application/octet-stream"
                if not data:
                    raise ValueError(f"Empty response for {current_url}")
                return data, content_type
                
            except (httpx.HTTPError, ValueError) as exc:
                if redirects_followed < max_redirects and isinstance(exc, httpx.HTTPError):
                     # Simple retry logic if needed, but manual re-validation is key
                     pass
                raise


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _asset_extension(content_type: str, url: str) -> str:
    ext = mimetypes.guess_extension(content_type.split(";")[0].strip()) or ""
    if ext in {".jpe", ".jpeg"}:
        ext = ".jpg"
    if ext:
        return ext
    suffix = Path(urllib.parse.urlparse(url).path).suffix
    return suffix if suffix else ".bin"


def _asset_path_for_sha(sha256: str) -> Path | None:
    matches = sorted(ASSETS_DIR.glob(f"{sha256}.*"))
    return matches[0] if matches else None


def fetch_and_cache_remote_image(url: str) -> tuple[str, Path, bytes, str]:
    _ensure_dirs()
    data, content_type = _download_url(url)
    if not content_type.lower().startswith("image/"):
        raise NonImageContentError(url, content_type)
    sha256 = _sha256_bytes(data)
    existing = _asset_path_for_sha(sha256)
    if existing is not None:
        return sha256, existing, data, content_type

    ext = _asset_extension(content_type, url)
    asset_path = ASSETS_DIR / f"{sha256}{ext}"
    if not asset_path.exists():
        asset_path.write_bytes(data)
    return sha256, asset_path, data, content_type


_TEMP_OCR_DIR = Path(tempfile.gettempdir()) / "guides-ocr"
_TEMP_OCR_DIR.mkdir(parents=True, exist_ok=True)
_TEMP_OCR_LOCK = threading.Lock()


def _prepare_image_for_ocr(image_bytes: bytes, content_type: str, asset_path: Path) -> Path:
    try:
        from PIL import Image
    except Exception:
        return asset_path

    try:
        with Image.open(asset_path) as img:
            if img.width <= MAX_OCR_IMAGE_SIZE[0] and img.height <= MAX_OCR_IMAGE_SIZE[1]:
                return asset_path

            resized = img.copy()
            resized.thumbnail(MAX_OCR_IMAGE_SIZE)
            suffix = asset_path.suffix or ".png"
            prepared = _TEMP_OCR_DIR / f"{asset_path.stem}.ocr{suffix}"
            image_format = img.format or ("PNG" if suffix.lower() == ".png" else None)
            with _TEMP_OCR_LOCK:
                resized.save(prepared, format=image_format)
            return prepared
    except Exception:
        return asset_path


def _cache_db() -> sqlite3.Connection:
    _ensure_dirs()
    conn = sqlite3.connect(str(CACHE_DB_PATH))
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ocr_cache (
            sha256 TEXT NOT NULL,
            prompt_version TEXT NOT NULL,
            model TEXT NOT NULL,
            result_json TEXT NOT NULL,
            tokens_in INTEGER NOT NULL,
            tokens_out INTEGER NOT NULL,
            cost_usd REAL NOT NULL,
            ts TEXT NOT NULL,
            PRIMARY KEY (sha256, prompt_version, model)
        )
        """
    )
    return conn


def _load_cached_ocr(
    conn: sqlite3.Connection, sha256: str, prompt_version: str, model: str
) -> OCRResult | None:
    row = conn.execute(
        """
        SELECT result_json
        FROM ocr_cache
        WHERE sha256 = ? AND prompt_version = ? AND model = ?
        """,
        (sha256, prompt_version, model),
    ).fetchone()
    if row is None:
        return None
    return OCRResult.model_validate_json(row[0])


def _store_cached_ocr(
    conn: sqlite3.Connection,
    *,
    sha256: str,
    prompt_version: str,
    model: str,
    result: OCRResult,
    tokens_in: int,
    tokens_out: int,
    cost_usd: float,
) -> None:
    conn.execute(
        """
        INSERT OR REPLACE INTO ocr_cache (
            sha256, prompt_version, model,
            result_json, tokens_in, tokens_out, cost_usd, ts
        ) VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """,
        (
            sha256,
            prompt_version,
            model,
            result.model_dump_json(),
            tokens_in,
            tokens_out,
            cost_usd,
        ),
    )
    conn.commit()


def _append_run_log(record: dict) -> None:
    _ensure_dirs()
    with RUNS_LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


from guides.json_extract import extract_json

def _extract_json_from_text(text: str) -> dict:
    return extract_json(text)


def run_vision_ocr(
    image_bytes: bytes,
    *,
    content_type: str,
    model: str = MODEL,
    asset_path: Path | None = None,
) -> tuple[OCRResult, int, int, float]:
    # We use asset_path if provided, otherwise we might need to save image_bytes to a temp file
    # for call_smart_with_images which expects Path.
    if asset_path and asset_path.exists():
        path_to_use = _prepare_image_for_ocr(image_bytes, content_type, asset_path)
    else:
        # Fallback: create a temporary file if asset_path is not available
        temp_dir = Path("data/tmp")
        temp_dir.mkdir(parents=True, exist_ok=True)
        sha256 = _sha256_bytes(image_bytes)
        path_to_use = temp_dir / f"ocr_tmp_{sha256}.png"
        path_to_use.write_bytes(image_bytes)

    text, usage = call_smart_with_images(
        OCR_PROMPT,
        [path_to_use],
        system="Return only valid JSON. Do not wrap in code fences or prose.",
        return_usage=True
    )

    try:
        result = OCRResult.model_validate(_extract_json_from_text(text))
        return result, usage.prompt_tokens, usage.completion_tokens, usage.cost_usd
    except Exception as exc:
        raise RuntimeError(f"Failed to parse OCR result: {text}") from exc


def _render_ocr_block(result: OCRResult) -> list[str]:
    lines = [OCR_MARKER, f"> **Type:** {result.image_type}"]

    text_lines = result.visible_text.splitlines() or [""]
    lines.append(f"> **Text:** {text_lines[0]}" if text_lines else "> **Text:**")
    for extra in text_lines[1:]:
        lines.append(f"> {extra}")

    desc_lines = result.description.splitlines() or [""]
    lines.append("> **Description:** " + desc_lines[0])
    for extra in desc_lines[1:]:
        lines.append(f"> {extra}")

    lines.append("")
    return lines


def _skip_existing_ocr_block(lines: list[str], start_index: int) -> int | None:
    if start_index + 1 >= len(lines):
        return None
    if lines[start_index + 1].strip() != OCR_MARKER:
        return None

    idx = start_index + 2
    while idx < len(lines) and lines[idx].startswith("> "):
        idx += 1
    if idx < len(lines) and lines[idx].strip() == "":
        idx += 1
    return idx


def _to_repo_relative(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def process_markdown_file(
    path: Path,
    *,
    fetcher: Callable[[str], tuple[str, Path, bytes, str]] = fetch_and_cache_remote_image,
    vlm_runner: Callable[..., tuple[OCRResult, int, int, float]] = run_vision_ocr,
    model: str = MODEL,
    prompt_version: str = PROMPT_VERSION,
) -> dict:
    text = path.read_text(encoding="utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    lines = text.splitlines()

    remote_urls_seen = 0
    inserted_blocks = 0
    cache_hits = 0
    changed = False

    conn = _cache_db()
    try:
        line_records: list[dict] = []
        pending_jobs: list[dict] = []
        idx = 0
        while idx < len(lines):
            line = lines[idx]
            refs = extract_remote_image_urls(line)
            if not refs:
                line_records.append({"line": line, "ocr_blocks": [], "passthrough": False})
                idx += 1
                continue

            existing_end = _skip_existing_ocr_block(lines, idx)
            if existing_end is not None:
                line_records.append(
                    {
                        "line": line,
                        "ocr_blocks": lines[idx + 1 : existing_end],
                        "passthrough": True,
                    }
                )
                idx = existing_end
                remote_urls_seen += len(refs)
                continue

            rewritten_line = line
            record: dict = {"line": rewritten_line, "ocr_blocks": [], "passthrough": False}
            for url in refs:
                remote_urls_seen += 1
                try:
                    sha256, asset_path, image_bytes, content_type = fetcher(url)
                except NonImageContentError:
                    continue
                try:
                    rel = asset_path.relative_to(path.parent)
                    rewritten_line = rewritten_line.replace(url, str(rel))
                except ValueError:
                    pass
                record["line"] = rewritten_line
                cached = _load_cached_ocr(conn, sha256, prompt_version, model)
                if cached is None:
                    pending_jobs.append(
                        {
                            "record": record,
                            "url": url,
                            "sha256": sha256,
                            "asset_path": asset_path,
                            "image_bytes": image_bytes,
                            "content_type": content_type,
                        }
                    )
                else:
                    cache_hits += 1
                    record["ocr_blocks"].extend(_render_ocr_block(cached))
                    inserted_blocks += 1

            if rewritten_line != line:
                changed = True
            if record["ocr_blocks"]:
                changed = True
            line_records.append(record)

            idx += 1

        if pending_jobs:
            max_workers = min(OCR_PARALLELISM, len(pending_jobs))
            with ThreadPoolExecutor(max_workers=max_workers) as pool:
                futures = [
                    pool.submit(
                        vlm_runner,
                        job["image_bytes"],
                        content_type=job["content_type"],
                        model=model,
                        asset_path=job["asset_path"],
                    )
                    for job in pending_jobs
                ]

                for job, future in zip(pending_jobs, futures):
                    result, tokens_in, tokens_out, cost_usd = future.result()
                    _store_cached_ocr(
                        conn,
                        sha256=job["sha256"],
                        prompt_version=prompt_version,
                        model=model,
                        result=result,
                        tokens_in=tokens_in,
                        tokens_out=tokens_out,
                        cost_usd=cost_usd,
                    )
                    _append_run_log(
                        {
                            "file": _to_repo_relative(path),
                            "image_url": job["url"],
                            "asset_path": _to_repo_relative(job["asset_path"]),
                            "sha256": job["sha256"],
                            "model": model,
                            "prompt_version": prompt_version,
                            "tokens_in": tokens_in,
                            "tokens_out": tokens_out,
                            "cost_usd": cost_usd,
                            "ts": int(time.time()),
                            "status": "ok",
                        }
                    )
                    job["record"]["ocr_blocks"].extend(_render_ocr_block(result))
                    inserted_blocks += 1
                    changed = True
    finally:
        conn.close()

    output: list[str] = []
    for record in line_records:
        output.append(record["line"])
        output.extend(record["ocr_blocks"])

    new_text = newline.join(output)
    if text.endswith(("\n", "\r")) and not new_text.endswith(newline):
        new_text += newline
    if changed and new_text != text:
        path.write_text(new_text, encoding="utf-8")

    return {
        "file": str(path),
        "remote_urls": remote_urls_seen,
        "inserted_blocks": inserted_blocks,
        "cache_hits": cache_hits,
        "changed": changed,
    }


def process_inputs(
    inputs: list[Path],
    *,
    fetcher: Callable[[str], tuple[str, Path, bytes, str]] = fetch_and_cache_remote_image,
    vlm_runner: Callable[..., tuple[OCRResult, int, int, float]] = run_vision_ocr,
    model: str = MODEL,
    prompt_version: str = PROMPT_VERSION,
) -> list[dict]:
    files = discover_markdown_files(inputs)
    results = []
    for path in files:
        results.append(
            process_markdown_file(
                path,
                fetcher=fetcher,
                vlm_runner=vlm_runner,
                model=model,
                prompt_version=prompt_version,
            )
        )
    return results


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Markdown files and/or directories")
    return parser


def main(
    argv: list[str] | None = None,
    *,
    fetcher: Callable[[str], tuple[str, Path, bytes, str]] = fetch_and_cache_remote_image,
    vlm_runner: Callable[..., tuple[OCRResult, int, int, float]] = run_vision_ocr,
) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    inputs = [Path(arg) for arg in args.paths]
    try:
        results = process_inputs(inputs, fetcher=fetcher, vlm_runner=vlm_runner)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    remote_urls = sum(item["remote_urls"] for item in results)
    inserted_blocks = sum(item["inserted_blocks"] for item in results)
    cache_hits = sum(item["cache_hits"] for item in results)
    changed = sum(1 for item in results if item["changed"])
    print(
        f"ocr_images: files={len(results)} remote_urls={remote_urls} "
        f"blocks={inserted_blocks} cache_hits={cache_hits} changed={changed}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
