from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

# We import check_hook from check_hook script
import sys

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from check_hook import check_hook

HOOK_TEMPLATE = Path(__file__).resolve().parents[2] / "templates" / "validate-tool-call.mjs"


@unittest.skipUnless(shutil.which("node"), "node required")
class TestCheckHook(unittest.TestCase):
    def test_template_hook_passes(self):
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / "hooks").mkdir()
            shutil.copy(HOOK_TEMPLATE, Path(t) / "hooks" / "validate-tool-call.mjs")
            self.assertEqual(check_hook(Path(t)), [])

    def test_empty_file_hook_fails(self):
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / "hooks").mkdir()
            (Path(t) / "hooks" / "validate-tool-call.mjs").write_text("", "utf-8")
            self.assertTrue(check_hook(Path(t)))

    def test_always_allow_hook_reports_not_blocking(self):
        with tempfile.TemporaryDirectory() as t:
            (Path(t) / "hooks").mkdir()
            (Path(t) / "hooks" / "validate-tool-call.mjs").write_text(
                'process.stdout.write(JSON.stringify({decision: "allow"})); process.exit(0);',
                "utf-8",
            )
            errors = check_hook(Path(t))
            self.assertTrue(any(e.startswith("hook.not_blocking:") for e in errors))

    def test_missing_hook_reports_missing(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(check_hook(Path(t)), ["hook.missing"])


if __name__ == "__main__":
    unittest.main()
