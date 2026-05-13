from __future__ import annotations

import unittest
from contextlib import nullcontext
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import process_stream
from guides.fetch.base import QueueItem, SourceKind


class ProcessStreamInboxArchiveTests(unittest.TestCase):
    def test_successful_inbox_file_moves_to_inbox_done(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            inbox_file = root / "data" / "inbox" / "sample.pdf"
            inbox_file.parent.mkdir(parents=True, exist_ok=True)
            inbox_file.write_text("pdf placeholder", encoding="utf-8")
            item = QueueItem(source=str(inbox_file), source_kind=SourceKind.FILE, received_at=datetime.now())

            with patch.object(process_stream, "ROOT", root), patch("process_stream.setup_logging"), patch(
                "process_stream.init_tracing"
            ), patch("process_stream.pipeline_run_lock", return_value=nullcontext()), patch(
                "process_stream.queue.pop_pending", return_value=[]
            ), patch(
                "process_stream.queue.scan_inbox", return_value=[item]
            ), patch(
                "process_stream.queue.already_processed", return_value=False
            ), patch(
                "process_stream.run_pipeline",
                return_value={"source": str(inbox_file), "status": "verified", "vault_path": "wiki/out.md"},
            ), patch("process_stream.queue.mark_done"), patch("process_stream.queue.clear_quarantine"):
                process_stream.main()

            self.assertFalse(inbox_file.exists())
            self.assertTrue((root / "data" / "inbox_done" / "sample.pdf").exists())

    def test_failed_inbox_file_stays_in_active_inbox(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            inbox_file = root / "data" / "inbox" / "sample.pdf"
            inbox_file.parent.mkdir(parents=True, exist_ok=True)
            inbox_file.write_text("pdf placeholder", encoding="utf-8")
            item = QueueItem(source=str(inbox_file), source_kind=SourceKind.FILE, received_at=datetime.now())

            with patch.object(process_stream, "ROOT", root), patch("process_stream.setup_logging"), patch(
                "process_stream.init_tracing"
            ), patch("process_stream.pipeline_run_lock", return_value=nullcontext()), patch(
                "process_stream.queue.pop_pending", return_value=[]
            ), patch(
                "process_stream.queue.scan_inbox", return_value=[item]
            ), patch(
                "process_stream.queue.already_processed", return_value=False
            ), patch(
                "process_stream.run_pipeline",
                return_value={"source": str(inbox_file), "status": "failed", "error": "boom"},
            ), patch("process_stream.queue.quarantine"):
                process_stream.main()

            self.assertTrue(inbox_file.exists())
            self.assertFalse((root / "data" / "inbox_done" / "sample.pdf").exists())

    def test_archive_collision_adds_suffix(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            inbox_file = root / "data" / "inbox" / "sample.pdf"
            archive_file = root / "data" / "inbox_done" / "sample.pdf"
            inbox_file.parent.mkdir(parents=True, exist_ok=True)
            archive_file.parent.mkdir(parents=True, exist_ok=True)
            inbox_file.write_text("new file", encoding="utf-8")
            archive_file.write_text("existing file", encoding="utf-8")
            item = QueueItem(source=str(inbox_file), source_kind=SourceKind.FILE, received_at=datetime.now())

            with patch.object(process_stream, "ROOT", root), patch("process_stream.setup_logging"), patch(
                "process_stream.init_tracing"
            ), patch("process_stream.pipeline_run_lock", return_value=nullcontext()), patch(
                "process_stream.queue.pop_pending", return_value=[]
            ), patch(
                "process_stream.queue.scan_inbox", return_value=[item]
            ), patch(
                "process_stream.queue.already_processed", return_value=False
            ), patch(
                "process_stream.run_pipeline",
                return_value={"source": str(inbox_file), "status": "needs_review", "vault_path": "wiki/out.md"},
            ), patch("process_stream.queue.mark_done"), patch("process_stream.queue.clear_quarantine"):
                process_stream.main()

            self.assertTrue(archive_file.exists())
            self.assertTrue((root / "data" / "inbox_done" / "sample-2.pdf").exists())


if __name__ == "__main__":
    unittest.main()
