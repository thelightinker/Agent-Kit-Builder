from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = TESTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

try:
    from support import REPO_ROOT, TOOLKIT, copy_toolkit
except ImportError:
    TOOLKIT = Path(__file__).resolve().parents[2]
    REPO_ROOT = TOOLKIT.parent
    copy_toolkit = None

import validate_kit


class TestToolkitTestsDoNotMutateRepo(unittest.TestCase):
    TRACKED = ("manifest.lock.json", "ARCHITECTURE.md", "execution_policy.json")

    def test_validate_and_sync_on_copy_leave_real_toolkit_untouched(self):
        if copy_toolkit is None:
            self.fail("support.copy_toolkit is not implemented")
        before = {n: (TOOLKIT / n).read_bytes() for n in self.TRACKED if (TOOLKIT / n).exists()}
        with tempfile.TemporaryDirectory() as tmp:
            kit = copy_toolkit(Path(tmp))
            validate_kit.validate(kit)          # auto_heal=True writes into the copy only
            validate_kit.sync_registry(kit)
        after = {n: (TOOLKIT / n).read_bytes() for n in self.TRACKED if (TOOLKIT / n).exists()}
        self.assertEqual(before, after)

    def test_test_toolkit_never_passes_real_toolkit_to_mutating_calls(self):
        src = (TESTS_DIR / "test_toolkit.py").read_text("utf-8")
        for call in ("validate_kit.validate(TOOLKIT)", "validate_kit.sync_registry(TOOLKIT)"):
            self.assertNotIn(call, src)


if __name__ == "__main__":
    unittest.main()
