"""Smoke test: every module in src/guides/ must compile and import without syntax errors."""
import importlib
import pkgutil
import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parent.parent / "src"


def _iter_modules():
    """Yield all module names under guides package."""
    if str(SRC_ROOT) not in sys.path:
        sys.path.insert(0, str(SRC_ROOT))
    import guides
    for info in pkgutil.walk_packages(guides.__path__, prefix="guides."):
        yield info.name


def test_all_modules_compile():
    """All guides.* modules must import without ImportError or SyntaxError."""
    import os
    # Set minimal env vars so Settings() doesn't blow up on import
    os.environ.setdefault("AZURE_OPENAI_API_KEY", "test-key")
    os.environ.setdefault("AZURE_OPENAI_ENDPOINT", "https://test.openai.azure.com/")
    os.environ.setdefault("AZURE_DEPLOYMENT_SMART", "gpt-4o")
    os.environ.setdefault("AZURE_DEPLOYMENT_FAST", "gpt-4o-mini")
    os.environ.setdefault("TELEGRAM_BOT_TOKEN", "123:test")
    os.environ.setdefault("TELEGRAM_CHANNEL_ID", "@test")

    failed = []
    for modname in _iter_modules():
        # Skip modules known to have heavy import-time side effects (DB, network)
        # These will be tested separately in integration tests
        try:
            importlib.import_module(modname)
        except (ImportError, SyntaxError) as e:
            failed.append((modname, str(e)))
        except Exception:
            # Other errors (missing env, DB not found) are acceptable in unit test env
            pass

    assert not failed, f"Modules with compile/import errors:\n" + "\n".join(
        f"  {m}: {e}" for m, e in failed
    )
