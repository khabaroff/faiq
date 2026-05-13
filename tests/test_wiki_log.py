from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from guides.vault import _append_wiki_log


class WikiLogTests(unittest.TestCase):
    def test_append_wiki_log_groups_by_day_and_shows_spend(self) -> None:
        today = datetime.utcnow().date().isoformat()

        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            wiki_dir = root / "wiki"
            data_logs = root / "data" / "logs"
            data_logs.mkdir(parents=True, exist_ok=True)
            (wiki_dir / "log.md").parent.mkdir(parents=True, exist_ok=True)
            (wiki_dir / "log.md").write_text("# Log\n", encoding="utf-8")

            pipeline_log = data_logs / "pipeline.log"
            pipeline_log.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "ts": f"{today}T10:00:00Z",
                                "logger": "guides.llm",
                                "msg": "llm_call",
                                "cost_usd": 0.123456,
                            },
                            ensure_ascii=False,
                        ),
                        json.dumps(
                            {
                                "ts": f"{today}T10:05:00Z",
                                "logger": "guides.llm",
                                "msg": "llm_call",
                                "cost_usd": 0.100000,
                            },
                            ensure_ascii=False,
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            _append_wiki_log(wiki_dir, "First Page", "notes", "first-page")
            _append_wiki_log(wiki_dir, "Second Page", "articles", "second-page")

            text = (wiki_dir / "log.md").read_text(encoding="utf-8")

            self.assertIn(f"## {today} | spent: $0.223456", text)
            self.assertIn("- ingest | First Page -> wiki/extracts/notes/first-page.md", text)
            self.assertIn("- ingest | Second Page -> wiki/extracts/articles/second-page.md", text)


if __name__ == "__main__":
    unittest.main()
