from __future__ import annotations

import logging
import uuid

from guides.enrich.tags import extract_tags
from guides.fetch.base import QueueItem, SourceKind, detect_source_type
from guides.fetch.github import fetch_github_repo
from guides.fetch.pdf import fetch_pdf
from guides.fetch.telegram import fetch_telegram
from guides.fetch.url import fetch_url
from guides.fetch.youtube import fetch_youtube
from guides.process.article import rewrite_article
from guides.process.reference import build_reference
from guides.process.wiki import strip_frontmatter, wrap_with_frontmatter
from guides.process.youtube import summarize_youtube
from guides.settings import Settings
from guides.verify import run_verify
from guides.vault import store
from guides.tracing import trace_run


logger = logging.getLogger(__name__)


def run_pipeline(item: QueueItem) -> dict:
    run_id = str(uuid.uuid4())
    with trace_run(run_id, item.source):
        try:
            source_type = detect_source_type(item)

            if (
                item.source_kind == SourceKind.FILE
                and item.source.lower().endswith(".pdf")
            ):
                fetched = fetch_pdf(item)
                if not fetched.raw_text.strip():
                    store(item.source, "", "", "article.md", [], "ARTICLE", "needs_review", data_dir=Settings().data_dir)
                    return {"source": item.source, "source_type": "ARTICLE", "status": "needs_review", "error": "pdf_extraction_failed"}
            elif "t.me" in item.source:
                fetched = fetch_telegram(item)
            elif source_type.value == "ARTICLE":
                fetched = fetch_url(item)
            elif source_type.value == "YOUTUBE":
                fetched = fetch_youtube(item)
            else:
                fetched = fetch_github_repo(item)

            if "t.me" in item.source:
                output_text = rewrite_article(fetched)
                output_filename = "article.md"
            elif source_type.value == "ARTICLE":
                output_text = rewrite_article(fetched)
                output_filename = "article.md"
            elif source_type.value == "YOUTUBE":
                output_text = summarize_youtube(fetched)
                output_filename = "article.md"
            else:
                output_text = build_reference(fetched)
                output_filename = "reference.md"

            taxonomy = extract_tags(strip_frontmatter(output_text))
            if source_type.value == "GITHUB_REPO":
                wiki_source_type = "reference"
            elif source_type.value == "YOUTUBE":
                wiki_source_type = "youtube"
            else:
                wiki_source_type = "article"

            is_file = item.source_kind == SourceKind.FILE
            source_url = "" if is_file else item.source
            source_path = item.source if is_file else ""

            body = strip_frontmatter(output_text)
            wrap_kwargs = dict(
                source_type=wiki_source_type,
                source_url=source_url,
                tags=taxonomy["tags"],
                topics=taxonomy["topics"],
                entities=taxonomy["entities"],
                concepts=taxonomy["concepts"],
                source_path=source_path,
            )
            output_text = wrap_with_frontmatter(body, **wrap_kwargs)

            status, checks = run_verify(fetched.raw_text, output_text, taxonomy["tags"], source_type=wiki_source_type)
            if status == "verified":
                output_text = wrap_with_frontmatter(body, **wrap_kwargs, status="verified")

            vault_path = store(
                item.source,
                fetched.raw_text,
                output_text,
                output_filename,
                taxonomy["tags"],
                source_type.value,
                status,
                data_dir=Settings().data_dir,
            )

            return {
                "source": item.source,
                "source_type": source_type.value,
                "status": status,
                "tags": taxonomy["tags"],
                "vault_path": str(vault_path),
            }
        except Exception as e:
            logger.exception("Pipeline failed for %s", item.source)
            return {"source": item.source, "status": "failed", "error": str(e)}
