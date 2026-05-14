import unittest
from pathlib import Path
from unittest.mock import patch, Mock
import socket

from guides.security.fs_safety import safe_join, assert_safe_slug
from guides.security.url_safety import validate_url


class FSSafetyTests(unittest.TestCase):
    def test_safe_join_valid(self):
        base = Path("/tmp/base")
        # Note: we don't need real FS for these tests as long as we mock or use relative paths carefully
        # Actually resolve() needs real paths if they exist, or it just resolves symbols.
        # Use TemporaryDirectory to be safe.
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir).resolve()
            subdir = base / "subdir"
            subdir.mkdir()
            
            self.assertEqual(safe_join(base, "subdir/file.txt"), base / "subdir/file.txt")
            self.assertEqual(safe_join(base, "file.txt"), base / "file.txt")

    def test_safe_join_escapes(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir).resolve()
            
            with self.assertRaisesRegex(ValueError, "escapes"):
                safe_join(base, "../escaped.txt")
            
            with self.assertRaisesRegex(ValueError, "escapes"):
                safe_join(base, "/etc/passwd")

    def test_assert_safe_slug_valid(self):
        self.assertEqual(assert_safe_slug("valid-slug-123"), "valid-slug-123")
        self.assertEqual(assert_safe_slug("a"), "a")

    def test_assert_safe_slug_invalid(self):
        with self.assertRaises(ValueError):
            assert_safe_slug("-invalid")
        with self.assertRaises(ValueError):
            assert_safe_slug("Invalid_Slug")
        with self.assertRaises(ValueError):
            assert_safe_slug("too" + "o" * 80)
        with self.assertRaises(ValueError):
            assert_safe_slug("")


class URLSafetyTests(unittest.TestCase):
    @patch("socket.getaddrinfo")
    def test_validate_url_valid(self, mock_getaddrinfo):
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 80))
        ]
        self.assertEqual(validate_url("https://example.com/path"), "https://example.com/path")

    def test_validate_url_blocked_scheme(self):
        with self.assertRaisesRegex(ValueError, "scheme blocked"):
            validate_url("file:///etc/passwd")
        with self.assertRaisesRegex(ValueError, "scheme blocked"):
            validate_url("ftp://example.com")

    def test_validate_url_no_host(self):
        with self.assertRaisesRegex(ValueError, "no host"):
            validate_url("https://")

    def test_validate_url_blocked_host(self):
        for host in ["169.254.169.254", "metadata.google.internal", "localhost"]:
            with self.assertRaisesRegex(ValueError, "Host blocked"):
                validate_url(f"http://{host}/")

    @patch("socket.getaddrinfo")
    def test_validate_url_private_ip(self, mock_getaddrinfo):
        private_ips = ["127.0.0.1", "10.0.0.1", "192.168.1.1", "172.16.0.1", "::1"]
        for ip in private_ips:
            mock_getaddrinfo.return_value = [
                (socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, 80))
            ]
            with self.assertRaisesRegex(ValueError, "restricted range"):
                validate_url("http://private-host.com/")

    @patch("socket.getaddrinfo")
    def test_fetch_url_blocks_metadata_ip(self, mock_getaddrinfo):
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("169.254.169.254", 80))
        ]
        with self.assertRaisesRegex(ValueError, "restricted range|Host blocked"):
            validate_url("http://metadata.example.com/latest/meta-data/")

    @patch("socket.getaddrinfo")
    def test_validate_url_invalid_ip_format(self, mock_getaddrinfo):
        # Case where getaddrinfo returns something that ipaddress.ip_address doesn't like
        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("not-an-ip", 80)),
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 80))
        ]
        # Should skip "not-an-ip" and succeed with the second one
        self.assertEqual(validate_url("http://example.com/"), "http://example.com/")

    @patch("socket.getaddrinfo")
    def test_validate_url_dns_failure(self, mock_getaddrinfo):
        mock_getaddrinfo.side_effect = OSError("DNS Error")
        with self.assertRaisesRegex(ValueError, "DNS resolution failed"):
            validate_url("http://nonexistent.example.com/")


if __name__ == "__main__":
    unittest.main()
