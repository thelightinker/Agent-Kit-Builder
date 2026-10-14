from __future__ import annotations

import shutil
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

from support import TOOLKIT, copy_toolkit
import validate_kit

try:
    import preflight
except ImportError:
    preflight = None


class TestDependencyContract(unittest.TestCase):
    def _temp_kit_without(self, rel_path: str) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        kit = copy_toolkit(Path(tmp.name))
        target = kit / rel_path
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()
        return kit

    def _temp_kit_with_text(self, rel_path: str, text: str) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        kit = copy_toolkit(Path(tmp.name))
        target = kit / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return kit

    def test_preflight_reports_missing_skill_creator(self):
        if preflight is None:
            self.fail("preflight module not found")
        kit = self._temp_kit_without("skills/skill-creator/SKILL.md")
        self.assertEqual(["skills/skill-creator/SKILL.md"], preflight.check_preflight(kit))

    def test_undeclared_external_dependency_is_an_error(self):
        kit = self._temp_kit_with_text("workflows/x.md", "use superpowers:made-up-skill")
        findings = []
        validate_kit.validate_dependencies(kit, findings)
        self.assertEqual(["dependency.undeclared"], [f.code for f in findings])

    def test_every_external_token_in_real_toolkit_is_declared(self):
        findings = []
        validate_kit.validate_dependencies(TOOLKIT, findings)
        self.assertEqual([], findings)

    def test_create_kit_runs_preflight_before_step_zero(self):
        text = (TOOLKIT / "workflows/create-kit.md").read_text("utf-8")
        self.assertLess(text.index("preflight.py"), text.index("BƯỚC 0"))
        self.assertIn("dự phòng", text.lower())


if __name__ == "__main__":
    unittest.main()
