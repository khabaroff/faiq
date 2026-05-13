from __future__ import annotations

import subprocess
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from guides.fetch.base import QueueItem, SourceKind
from guides.fetch.pdf import fetch_pdf


class FetchPdfTests(unittest.TestCase):
    def test_strong_pdftotext_output_skips_ocr(self) -> None:
        item = QueueItem(source="/tmp/sample.pdf", source_kind=SourceKind.FILE, received_at=datetime.now())

        with patch("guides.fetch.pdf.subprocess.run") as run_mock, patch(
            "guides.fetch.pdf._render_pdf_pages", create=True
        ) as render_mock, patch("guides.fetch.pdf._ocr_rendered_pages", create=True) as ocr_mock:
            run_mock.return_value = subprocess.CompletedProcess(
                args=["pdftotext"], returncode=0, stdout="x" * 150, stderr=""
            )

            content = fetch_pdf(item)

        self.assertEqual(content.raw_text, "x" * 150)
        self.assertEqual(content.source_meta["fetcher"], "pdftotext")
        render_mock.assert_not_called()
        ocr_mock.assert_not_called()

    def test_weak_pdftotext_output_falls_back_to_ocr(self) -> None:
        item = QueueItem(source="/tmp/scanned.pdf", source_kind=SourceKind.FILE, received_at=datetime.now())

        with patch("guides.fetch.pdf.subprocess.run") as run_mock, patch(
            "guides.fetch.pdf._render_pdf_pages", return_value=[Path("/tmp/page-1.png")], create=True
        ) as render_mock, patch(
            "guides.fetch.pdf._ocr_rendered_pages", return_value="OCR " + ("y" * 180), create=True
        ) as ocr_mock:
            run_mock.return_value = subprocess.CompletedProcess(
                args=["pdftotext"], returncode=0, stdout="too short", stderr=""
            )

            content = fetch_pdf(item)

        self.assertTrue(render_mock.called)
        self.assertTrue(ocr_mock.called)
        self.assertIn("OCR", content.raw_text)
        self.assertEqual(content.source_meta["fetcher"], "gpt-ocr")

    def test_failed_ocr_fallback_keeps_extraction_failed_signal(self) -> None:
        item = QueueItem(source="/tmp/bad.pdf", source_kind=SourceKind.FILE, received_at=datetime.now())

        with patch("guides.fetch.pdf.subprocess.run") as run_mock, patch(
            "guides.fetch.pdf._render_pdf_pages", return_value=[Path("/tmp/page-1.png")], create=True
        ), patch("guides.fetch.pdf._ocr_rendered_pages", return_value="", create=True) as ocr_mock:
            run_mock.return_value = subprocess.CompletedProcess(
                args=["pdftotext"], returncode=0, stdout="tiny", stderr=""
            )

            content = fetch_pdf(item)

        self.assertTrue(ocr_mock.called)
        self.assertEqual(content.raw_text, "")
        self.assertEqual(content.source_meta["error"], "extraction_failed")


if __name__ == "__main__":
    unittest.main()
