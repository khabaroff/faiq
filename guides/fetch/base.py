import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path

from pydantic import BaseModel


class SourceKind(str, Enum):
    URL = "url"
    FILE = "file"


class SourceType(str, Enum):
    ARTICLE = "ARTICLE"
    YOUTUBE = "YOUTUBE"
    GITHUB_REPO = "GITHUB_REPO"


class QueueItem(BaseModel):
    source: str
    source_kind: SourceKind
    received_at: datetime
    origin: str = "inbox"


@dataclass
class FetchedContent:
    raw_text: str
    source_type: SourceType
    source_meta: dict = field(default_factory=dict)
    attachments: list[Path] = field(default_factory=list)


def detect_source_type(item: QueueItem) -> SourceType:
    source = item.source.lower()

    if "youtube.com" in source or "youtu.be" in source:
        return SourceType.YOUTUBE

    if re.search(r"github\.com/[^/]+/[^/]+/?$", source):
        return SourceType.GITHUB_REPO

    return SourceType.ARTICLE
