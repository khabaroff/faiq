import pytest
import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parent.parent / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

# Minimal env stubs so Settings() doesn't blow up on import
import os
os.environ.setdefault("AZURE_OPENAI_API_KEY", "test-key")
os.environ.setdefault("AZURE_OPENAI_ENDPOINT", "https://test.openai.azure.com")
os.environ.setdefault("AZURE_DEPLOYMENT_SMART", "gpt-4o")
os.environ.setdefault("AZURE_DEPLOYMENT_FAST", "gpt-4o-mini")
os.environ.setdefault("TELEGRAM_BOT_TOKEN", "test-token")
os.environ.setdefault("TELEGRAM_CHANNEL_ID", "test-channel")


@pytest.fixture()
def isolated_state_db(tmp_path, monkeypatch):
    import guides.state as state_mod
    monkeypatch.setattr(state_mod, "DB_PATH", tmp_path / "articles.db")
    monkeypatch.setattr(state_mod, "STATE_DIR", tmp_path)
    state_mod.init_db()
    return tmp_path
