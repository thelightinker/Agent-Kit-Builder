from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

AGENTS_ROOT = Path(__file__).resolve().parents[2]
READSETS = AGENTS_ROOT / "readsets.json"

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

try:
    from readset_report import readset_bytes
except ImportError:
    readset_bytes = None


class TestReadsets(unittest.TestCase):
    def test_all_listed_files_exist(self):
        self.assertTrue(READSETS.is_file(), "readsets.json must exist")
        with READSETS.open("r", encoding="utf-8") as f:
            data = json.load(f)
        for mode, files in data.items():
            for f in files:
                target = AGENTS_ROOT / f
                self.assertTrue(target.is_file(), f"File {f} in mode {mode} must exist at {target}")

    def test_ordering_micro_lt_standard_lt_full_suite(self):
        self.assertIsNotNone(readset_bytes, "readset_bytes function must be available")
        b = {m: readset_bytes(AGENTS_ROOT, m) for m in ("micro", "standard", "mini_suite", "full_suite")}
        self.assertLess(b["micro"], b["standard"])
        self.assertLess(b["standard"], b["full_suite"])

    def test_prompt_compiling_points_to_suite_reference(self):
        content = (AGENTS_ROOT / "skills/prompt-compiling/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/prompt-compiling-suite.md", content)

    def test_prompt_compiling_shrinks_vs_baseline(self):
        skill_file = AGENTS_ROOT / "skills/prompt-compiling/SKILL.md"
        self.assertLess(skill_file.stat().st_size, 11_200)


if __name__ == "__main__":
    unittest.main()
