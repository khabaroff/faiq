from __future__ import annotations

import logging

from guides.enrich.tags import extract_tags
from guides.fetch.base import QueueItem, detect_source_type
from guides.fetch.github import fetch_github_repo
from guides.fetch.url import fetch_url
from guides.fetch.youtube import fetch_youtube
from guides.process.article import rewrite_article
from guides.process.reference import build_reference
from guides.process.youtube import summarize_youtube
from guides.settings import Settings
from guides.verify import run_verify
from guides.vault import store


logger = logging.getLogger(__name__)


def run_pipeline(item: QueueItem) -> dict:
    try:
        source_type = detect_source_type(item)

        if source_type.value == "ARTICLE":
            fetched = fetch_url(item)
            output_text = rewrite_article(fetched)
            output_filename = "article.md"
        elif source_type.value == "YOUTUBE":
            fetched = fetch_youtube(item)
            output_text = summarize_youtube(fetched)
            output_filename = "article.md"
        else:
            fetched = fetch_github_repo(item)
            output_text = build_reference(fetched)
            output_filename = "reference.md"

        tags = extract_tags(output_text)
        status, checks = run_verify(fetched.raw_text, output_text, tags)
        vault_path = store(
            item.source,
            fetched.raw_text,
            output_text,
            output_filename,
            tags,
            source_type.value,
            status,
            data_dir=Settings().data_dir,
        )

        return {
            "source": item.source,
            "source_type": source_type.value,
            "status": status,
            "tags": tags,
            "vault_path": str(vault_path),
        }
    except Exception as e:
        logger.exception("Pipeline failed for %s", item.source)
        return {"source": item.source, "status": "failed", "error": str(e)}
