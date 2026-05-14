"""Pydantic response models for LLM JSON outputs."""
from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, field_validator


def _strip_html(text: str) -> str:
    if not text:
        return ""
    # Remove all HTML tags
    return re.sub(r'<[^>]+>', '', text)


class WikiUpdateResponse(BaseModel):
    action: Literal["create", "append_mention", "rewrite_description"] = "create"
    page_md: str = ""

    @field_validator("action", mode="before")
    @classmethod
    def _normalize_action(cls, v: object) -> str:
        if v not in {"create", "append_mention", "rewrite_description"}:
            return "create"
        return v  # type: ignore[return-value]

    @field_validator("page_md", mode="before")
    @classmethod
    def _sanitize_page_md(cls, v: object) -> str:
        s = _strip_html(str(v))
        return s[:50000]


class SummaryCheckResponse(BaseModel):
    verdict: Literal["ok", "needs_resummarize", "minor_fix", "error"] = "error"
    issues: list[str] = []
    notes: str = ""


class WikiCleanResponse(BaseModel):
    verdict: Literal["ok", "needs_cleanup", "error"] = "error"
    cleaned_page_md: str = ""
    issues: list[str] = []

    @field_validator("cleaned_page_md", mode="before")
    @classmethod
    def _sanitize_cleaned_page_md(cls, v: object) -> str:
        s = _strip_html(str(v))
        return s[:50000]


class SeoResponse(BaseModel):
    seo_title: str = ""
    seo_description: str = ""
    og_description: str = ""
    seo_optimized_at: str = ""

    @field_validator("seo_title", "seo_description", "og_description", mode="before")
    @classmethod
    def _truncate_str(cls, v: object) -> str:
        s = str(v) if v is not None else ""
        return s[:300]


class ArticleState(BaseModel):
    """Single source of truth for pipeline state fields.
    
    Must stay in sync with:
      - SQLite schema (articles table columns except slug PK)
      - _VALID_FIELDS in state.py
      - State keys written to markdown frontmatter
    """
    raw: bool = False
    content_hash: str | None = None
    summarized_at: str | None = None
    wiki_propagated: bool = False
    wiki_propagated_at: str | None = None
    seo_optimized: bool = False
    published_telegram: str | None = None
    quality: str | None = None
    quality_checked: bool = False
    qc_hash: str | None = None
    status: str = "draft"
    revision_count: int = 0
    last_edited_at: str | None = None
    last_edited_by: str | None = None
    compacted: bool = False
