"""URL validation to prevent SSRF attacks."""
from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse

ALLOWED_SCHEMES = frozenset({"http", "https"})
BLOCKED_HOSTS = frozenset({
    "169.254.169.254",  # AWS/GCP metadata
    "metadata.google.internal",
    "metadata",
    "localhost",
})


def validate_url(url: str) -> str:
    """Validate URL is safe to fetch. Raises ValueError if unsafe."""
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"URL scheme blocked: {parsed.scheme!r} in {url!r}")
    host = (parsed.hostname or "").lower()
    if not host:
        raise ValueError(f"URL has no host: {url!r}")
    if host in BLOCKED_HOSTS:
        raise ValueError(f"Host blocked: {host!r}")
    try:
        infos = socket.getaddrinfo(host, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except OSError as exc:
        raise ValueError(f"DNS resolution failed for {host!r}: {exc}") from exc
    for info in infos:
        try:
            ip = ipaddress.ip_address(info[4][0])
        except ValueError:
            continue
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
        ):
            raise ValueError(f"IP address in restricted range: {ip} (host={host!r})")
    return url
