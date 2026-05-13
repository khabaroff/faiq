import pytest
from unittest.mock import patch
import socket


def _mock_dns_private(host, port, *a, **kw):
    # Returns a result that resolves to a private IP
    return [(socket.AF_INET, socket.SOCK_STREAM, 0, '', ('192.168.1.1', port or 0))]


def _mock_dns_public(host, port, *a, **kw):
    return [(socket.AF_INET, socket.SOCK_STREAM, 0, '', ('93.184.216.34', port or 0))]


# blocked schemes
@pytest.mark.parametrize("url", [
    "ftp://example.com/file",
    "file:///etc/passwd",
    "javascript:alert(1)",
])
def test_validate_url_blocks_bad_scheme(url):
    from guides.security.url_safety import validate_url
    with pytest.raises(ValueError):
        validate_url(url)


# blocked hosts (mock DNS to return private IPs)
@pytest.mark.parametrize("url", [
    "http://localhost/secret",
    "http://127.0.0.1/secret",
    "http://169.254.169.254/latest/meta-data/",
    "http://192.168.1.100/admin",
    "http://10.0.0.1/internal",
])
def test_validate_url_blocks_private_ip(url):
    from guides.security.url_safety import validate_url
    # For IPs, DNS returns the IP itself — patch getaddrinfo to return private
    with patch("socket.getaddrinfo", _mock_dns_private):
        with pytest.raises(ValueError):
            validate_url(url)


def test_validate_url_passes_public():
    from guides.security.url_safety import validate_url
    with patch("socket.getaddrinfo", _mock_dns_public):
        result = validate_url("https://example.com/page")
    assert result == "https://example.com/page"


def test_validate_url_returns_original_url():
    from guides.security.url_safety import validate_url
    url = "https://example.com/article?q=1"
    with patch("socket.getaddrinfo", _mock_dns_public):
        assert validate_url(url) == url
