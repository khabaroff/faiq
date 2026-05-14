import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WRAPPER = REPO_ROOT / "scripts" / "cron_wrapper.sh"


def test_cron_wrapper_syntax():
    result = subprocess.run(["bash", "-n", str(WRAPPER)], capture_output=True)
    assert result.returncode == 0, result.stderr.decode()


def test_cron_wrapper_exits_nonzero_on_pipeline_failure(monkeypatch):
    # Simulate a failing pipeline by pointing PYTHONPATH to a mock
    mock_dir = REPO_ROOT / "tests" / "_mock_pipeline"
    mock_dir.mkdir(exist_ok=True)
    init = mock_dir / "__init__.py"
    init.write_text("")
    (mock_dir / "guides").mkdir(exist_ok=True)
    (mock_dir / "guides" / "__init__.py").write_text("")
    (mock_dir / "guides" / "pipelines").mkdir(exist_ok=True)
    (mock_dir / "guides" / "pipelines" / "__init__.py").write_text("")
    (mock_dir / "guides" / "pipelines" / "run_all.py").write_text("import sys; sys.exit(1)\n")

    env = {
        **subprocess.os.environ,
        "PYTHONPATH": str(mock_dir),
        "HEALTHCHECKS_URL": "https://hc-ping.com/fake-test-url",
    }
    result = subprocess.run(
        ["bash", str(WRAPPER)],
        capture_output=True,
        text=True,
        env=env,
        cwd=REPO_ROOT,
    )
    assert result.returncode == 1
    # On failure wrapper should not ping healthchecks; exit code alone proves fail path.
