from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import process_stream


class ProcessStreamLockTests(unittest.TestCase):
    def test_second_lock_attempt_fails_while_first_is_held(self) -> None:
        with TemporaryDirectory() as tmpdir:
            lock_path = Path(tmpdir) / "process_stream.lock"

            with process_stream.pipeline_run_lock(lock_path):
                with self.assertRaises(RuntimeError):
                    with process_stream.pipeline_run_lock(lock_path):
                        pass


if __name__ == "__main__":
    unittest.main()
