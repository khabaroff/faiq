from pathlib import Path
from tempfile import TemporaryDirectory

import guides.queue as queue_mod
from guides.queue import _classify_text_file, scan_inbox


def test_classify_text_file() -> None:
    assert _classify_text_file("https://example.com/post") == "single_url"
    assert _classify_text_file("\nhttps://a.com\nhttps://b.com\nhttps://c.com\n") == "url_list"
    assert _classify_text_file(
        "Note text\n\nhttps://example.com/post\n\nMore note text"
    ) == "mixed"
    assert _classify_text_file("# Title\n\nSome markdown article text.") == "article"


def test_scan_inbox_classifies_text_files() -> None:
    with TemporaryDirectory() as tmpdir:
        state_dir = Path(tmpdir) / "state"
        (state_dir / "sources").mkdir(parents=True)

        class FakeSettings:
            def __init__(self) -> None:
                self.data_dir = state_dir

        original_settings = queue_mod.Settings
        queue_mod.Settings = FakeSettings

        inbox = Path(tmpdir) / "data" / "inbox"
        inbox.mkdir(parents=True)

        (inbox / "single.txt").write_text("https://example.com/post", encoding="utf-8")
        (inbox / "links.md").write_text(
            "https://a.com\nhttps://b.com\nhttps://c.com\n", encoding="utf-8"
        )
        (inbox / "mixed.md").write_text(
            "Note text\n\nhttps://example.com/post\n\nMore note text", encoding="utf-8"
        )

        try:
            items = scan_inbox(inbox)
            sources = [(item.source, item.source_kind.value) for item in items]

            assert sources == [
                ("https://a.com", "url"),
                ("https://b.com", "url"),
                ("https://c.com", "url"),
                (str(inbox / "mixed.md"), "file"),
                ("https://example.com/post", "url"),
            ]
        finally:
            queue_mod.Settings = original_settings


if __name__ == "__main__":
    test_classify_text_file()
    test_scan_inbox_classifies_text_files()
    print("ok")
