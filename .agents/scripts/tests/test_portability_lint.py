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

from support import TOOLKIT
import validate_kit

CASES_BAD = [
    ("a.md",   r"[x](file:///C:/Users/nhdcb/x.md)"),
    ("b.json", r'{"p": "C:\\Users\\bob\\x"}'),
    ("c.py",   'P = "/Users/alice/proj/x"'),
    ("d.md",   "see /home/carol/work/x"),
    ("e.md",   "file:///c:/Users/nhdcb/OneDrive/Desktop/x.md"),
]


class TestPortabilityLint(unittest.TestCase):
    def _scan(self, name: str, text: str):
        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / name
            p.write_text(text, "utf-8")
            findings = []
            validate_kit.validate_portability(Path(tmpdir), findings)
            return findings

    def test_flags_absolute_user_paths_in_md_json_py(self):
        for name, text in CASES_BAD:
            with self.subTest(name):
                findings = self._scan(name, text)
                self.assertIn("path.absolute_user_path", [f.code for f in findings])

    def test_does_not_flag_urls_or_relative_paths(self):
        for text in ("https://example.com/home/x/y", "[a](../skill-creator/SKILL.md)", ".agents/skills/x"):
            with self.subTest(text):
                self.assertEqual([], self._scan("ok.md", text))

    def test_real_toolkit_has_no_absolute_user_paths(self):
        findings = []
        validate_kit.validate_portability(TOOLKIT, findings)
        self.assertEqual([], findings)


if __name__ == "__main__":
    unittest.main()
