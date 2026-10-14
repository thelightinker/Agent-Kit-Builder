from __future__ import annotations

import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = TESTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from support import REPO_ROOT
try:
    import verify_all
    from verify_all import StepResult
except ImportError:
    verify_all = None
    StepResult = None


class TestVerifyAll(unittest.TestCase):
    def test_missing_dev_dependency_exits_2_with_actionable_message(self):
        self.assertIsNotNone(verify_all, "verify_all module must exist")
        with mock.patch.object(verify_all, "missing_dev_dependencies", return_value=["pytest"]), \
             contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual(2, verify_all.main([]))
        self.assertIn("requirements-dev.txt", err.getvalue())

    def test_runs_from_any_working_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run(
                [sys.executable, str(SCRIPTS_DIR / "verify_all.py"), "--only", "preflight"],
                cwd=tmp,
                capture_output=True,
                text=True,
            )
        self.assertEqual(0, r.returncode, r.stderr)

    def test_any_failed_step_makes_verdict_fail(self):
        self.assertIsNotNone(verify_all, "verify_all module must exist")
        results = [verify_all.StepResult("a", 0, 0.1), verify_all.StepResult("b", 1, 0.1)]
        self.assertEqual(1, verify_all.exit_code(results))

    def test_readme_has_no_static_status_badges(self):
        text = (REPO_ROOT / "README.md").read_text("utf-8")
        for needle in ("Toolkit_Validation", "Unit_Tests-"):
            self.assertNotIn(needle, text)


if __name__ == "__main__":
    unittest.main()
