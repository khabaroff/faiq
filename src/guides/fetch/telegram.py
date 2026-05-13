from __future__ import annotations

import html
import re

import httpx

from guides.fetch.base import FetchedContent, QueueItem, SourceType


_TG_URL_RE = re.compile(r"(?:https?://)?t\.me/([^/]+)/([0-9]+)")


def fetch_telegram(item: QueueItem) -> FetchedContent:
    match = _TG_URL_RE.search(item.source)
    if not match:
        return FetchedContent(raw_text="", source_type=SourceType.ARTICLE, source_meta={"url": item.source, "error": "post_not_found"})

    channel, post_id = match.group(1), match.group(2)
    original_url = item.source

    try:
        response = httpx.get(
            f"https://t.me/s/{channel}/{post_id}",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=30,
            follow_redirects=True,
        )
        response.raise_for_status()
    except Exception:
        return FetchedContent(raw_text="", source_type=SourceType.ARTICLE, source_meta={"url": original_url, "error": "post_not_found"})

    target = f'data-post="{channel}/{post_id}"'
    for block in response.text.split('<div class="tgme_widget_message_wrap'):
        if target not in block:
            continue
        text_match = re.search(r'class="tgme_widget_message_text[^\"]*"[^>]*>(.*?)</div>', block, re.S)
        if not text_match:
            continue
        text = re.sub(r"<[^>]+>", " ", text_match.group(1))
        text = html.unescape(re.sub(r"\s+", " ", text)).strip()
        if text:
            return FetchedContent(
                raw_text=text,
                source_type=SourceType.ARTICLE,
                source_meta={"url": original_url, "channel": channel, "post_id": post_id, "fetcher": "telegram-web"},
            )

    return FetchedContent(raw_text="", source_type=SourceType.ARTICLE, source_meta={"url": original_url, "error": "post_not_found"})
