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
