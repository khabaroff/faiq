import asyncio
import unittest
from datetime import datetime
from unittest.mock import patch, Mock, AsyncMock

from guides.fetch.base import QueueItem, SourceKind, SourceType
from guides.fetch.youtube import fetch_youtube
from guides.utils.fetch_cache import cache_failure, get_cached_failure

class YouTubeRemTests(unittest.IsolatedAsyncioTestCase):
    async def test_youtube_file_scheme_blocked(self):
        item = QueueItem(source="file:///etc/passwd", source_kind=SourceKind.URL, received_at=datetime.now())
        with self.assertRaises(ValueError):
            await fetch_youtube(item)

    @patch("guides.fetch.youtube.get_cached_failure", return_value=403)
    async def test_youtube_cache_hit(self, mock_cache):
        item = QueueItem(source="https://youtube.com/watch?v=bad", source_kind=SourceKind.URL, received_at=datetime.now())
        res = await fetch_youtube(item)
        self.assertEqual(res.source_meta["error"], "cached_403")

    @patch("asyncio.create_subprocess_exec")
    async def test_youtube_fail_fast_403(self, mock_exec):
        mock_proc = AsyncMock()
        mock_proc.communicate.return_value = (b"", b"ERROR: [youtube] bad: YouTube said: Account has been terminated (403)")
        mock_proc.returncode = 1
        mock_exec.return_value = mock_proc

        item = QueueItem(source="https://youtube.com/watch?v=403", source_kind=SourceKind.URL, received_at=datetime.now())
        
        with patch("guides.fetch.youtube.cache_failure") as mock_cache_fail:
            res = await fetch_youtube(item)
            mock_cache_fail.assert_called_once_with(item.source, 403)
            self.assertEqual(res.raw_text, "")
            self.assertEqual(res.source_meta["error"], "no_transcript")

    @patch("asyncio.create_subprocess_exec")
    @patch("guides.fetch.youtube._try_transcribe_service", return_value=None)
    async def test_youtube_timeout_logic(self, mock_transcribe, mock_exec):
        mock_proc = AsyncMock()
        mock_proc.communicate.side_effect = asyncio.TimeoutError
        mock_proc.returncode = None
        mock_exec.return_value = mock_proc

        item = QueueItem(source="https://youtube.com/watch?v=timeout", source_kind=SourceKind.URL, received_at=datetime.now())
        
        with patch("asyncio.wait_for", side_effect=asyncio.TimeoutError):
            res = await fetch_youtube(item)
            self.assertEqual(res.source_meta["error"], "no_transcript")

if __name__ == "__main__":
    unittest.main()

if __name__ == "__main__":
    unittest.main()
