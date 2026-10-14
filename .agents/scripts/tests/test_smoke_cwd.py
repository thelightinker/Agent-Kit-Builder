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

import validate_kit


def _make_kit(root: Path) -> None:
    for d in ("agent", "skills", "workflows", "rules", "memory", "templates", "references", "schemas", "scripts"):
        (root / d).mkdir(parents=True, exist_ok=True)


def _write_skill(root: Path, name: str) -> Path:
    skill_dir = root / "skills" / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f'---\nname: {name}\ndescription: "Test skill for {name}"\n'
        f'when_to_use: "When testing {name}"\nallowed-tools: Read\nversion: 1.0.0\n---\n\n'
        f"# {name}\n\n## Example\nInput: test\nOutput: result\n",
        encoding="utf-8",
    )
    return skill_dir


class TestSmokeCwd(unittest.TestCase):
    def test_script_importing_sibling_package_passes_smoke_when_run_from_skill_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            kit = Path(tmp) / ".agents"
            _make_kit(kit)
            skill = _write_skill(kit, "demo")
            (skill / "scripts").mkdir(parents=True, exist_ok=True)
            (skill / "scripts/__init__.py").write_text("", encoding="utf-8")
            (skill / "scripts/utils.py").write_text("def f():\n    return 1\n", encoding="utf-8")
            (skill / "scripts/run.py").write_text(
                "import argparse\nfrom scripts.utils import f\n"
                'if __name__ == "__main__":\n'
                "    p = argparse.ArgumentParser()\n"
                "    p.parse_args()\n",
                encoding="utf-8",
            )
            findings = []
            validate_kit.validate_python(kit, findings)
            self.assertNotIn("script.smoke_failed", [f.code for f in findings])


if __name__ == "__main__":
    unittest.main()
