import asyncio
import unittest
from datetime import datetime
from unittest.mock import patch, Mock, AsyncMock

from guides.fetch.base import QueueItem, SourceKind, SourceType
from guides.fetch.youtube import _cache_key_for_url, fetch_youtube
from guides.utils.fetch_cache import cache_failure, get_cached_failure

class YouTubeRemTests(unittest.IsolatedAsyncioTestCase):
    async def test_youtube_file_scheme_blocked(self):
        item = QueueItem(source="file:///etc/passwd", source_kind=SourceKind.URL, received_at=datetime.now())
        with self.assertRaises(ValueError):
            await fetch_youtube(item)

    @patch("guides.fetch.youtube.validate_url", side_effect=lambda url: url)
    @patch("guides.fetch.youtube.get_cached_failure", return_value=403)
    async def test_youtube_cache_hit(self, mock_cache, mock_validate):
        item = QueueItem(source="https://youtube.com/watch?v=bad", source_kind=SourceKind.URL, received_at=datetime.now())
        res = await fetch_youtube(item)
        self.assertEqual(res.source_meta["error"], "cached_403")

    def test_cache_key_uses_video_id(self):
        a = "https://www.youtube.com/watch?v=abc123XYZ"
        b = "https://youtube.com/watch?v=abc123XYZ&t=42"
        self.assertEqual(_cache_key_for_url(a), _cache_key_for_url(b))
        self.assertEqual(_cache_key_for_url(a), "youtube:abc123XYZ")

    @patch("guides.fetch.youtube.validate_url", side_effect=lambda url: url)
    @patch("asyncio.create_subprocess_exec")
    async def test_youtube_fail_fast_403(self, mock_exec, mock_validate):
        mock_proc = AsyncMock()
        mock_proc.communicate.return_value = (b"", b"ERROR: [youtube] bad: YouTube said: Account has been terminated (403)")
        mock_proc.returncode = 1
        mock_exec.return_value = mock_proc

        item = QueueItem(source="https://youtube.com/watch?v=403", source_kind=SourceKind.URL, received_at=datetime.now())

        with patch("guides.fetch.youtube.cache_failure") as mock_cache_fail:
            res = await fetch_youtube(item)
            mock_cache_fail.assert_called_once_with("youtube:403", 403)
            self.assertEqual(res.raw_text, "")
            self.assertEqual(res.source_meta["error"], "no_transcript")
            mock_exec.assert_called_once()

    @patch("guides.fetch.youtube.validate_url", side_effect=lambda url: url)
    @patch("asyncio.create_subprocess_exec")
    @patch("guides.fetch.youtube._try_transcribe_service", return_value=None)
    async def test_youtube_timeout_logic(self, mock_transcribe, mock_exec, mock_validate):
        mock_proc = AsyncMock()
        mock_proc.communicate = Mock(return_value=object())
        mock_proc.kill = Mock()
        mock_proc.returncode = None
        mock_exec.return_value = mock_proc

        item = QueueItem(source="https://youtube.com/watch?v=timeout", source_kind=SourceKind.URL, received_at=datetime.now())
        
        with patch("asyncio.wait_for", side_effect=asyncio.TimeoutError):
            res = await fetch_youtube(item)
            self.assertEqual(res.source_meta["error"], "no_transcript")

    @patch("guides.fetch.youtube.validate_url", side_effect=lambda url: url)
    @patch("asyncio.create_subprocess_exec")
    async def test_ytdlp_uses_socket_timeout_10(self, mock_exec, mock_validate):
        mock_proc = AsyncMock()
        mock_proc.communicate.return_value = (b"", b"")
        mock_proc.returncode = 0
        mock_proc.kill = Mock()
        mock_exec.return_value = mock_proc

        item = QueueItem(source="https://youtube.com/watch?v=socket", source_kind=SourceKind.URL, received_at=datetime.now())
        await fetch_youtube(item)

        first_cmd = mock_exec.call_args_list[0].args
        self.assertIn("--socket-timeout", first_cmd)
        idx = first_cmd.index("--socket-timeout")
        self.assertEqual(first_cmd[idx + 1], "10")

if __name__ == "__main__":
    unittest.main()

if __name__ == "__main__":
    unittest.main()
