from __future__ import annotations

from typing import Protocol, runtime_checkable, Any
from guides.fetch.base import FetchedContent, QueueItem, get_http_client, SourceKind
from guides.security.url_safety import validate_url

@runtime_checkable
class FetcherProtocol(Protocol):
    """Protocol for all content fetchers."""
    def can_fetch(self, item: QueueItem) -> bool:
        """Return True if this fetcher can handle the item."""
        ...

    def fetch(self, item: QueueItem) -> FetchedContent:
        """Fetch content and return FetchedContent. Raises on failure."""
        ...

class BaseFetcher:
    """Base class providing common utilities for fetchers."""
    
    def validate_and_get_client(self, url: str):
        """Standard validation and client access."""
        validate_url(url)
        return get_http_client()

    def is_url(self, item: QueueItem) -> bool:
        return item.source_kind == SourceKind.URL

    def is_file(self, item: QueueItem) -> bool:
        return item.source_kind == SourceKind.FILE
