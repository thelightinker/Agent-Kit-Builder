#!/usr/bin/env python3
import unittest
import tempfile
import shutil
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate_kit import validate_compiler_artifacts, Finding

class TestValidateKitCompiler(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.agents_dir = self.temp_dir / "agent"
        self.workflows_dir = self.temp_dir / "workflows"
        self.agents_dir.mkdir(parents=True)
        self.workflows_dir.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_namespace_validation_finding(self):
        (self.agents_dir / "writer.md").write_text(
            """---
name: writer
capabilities:
  - id: invalid_cap_id
---
# Writer
""",
            encoding="utf-8",
        )
        findings: list[Finding] = []
        validate_compiler_artifacts(self.temp_dir, findings)
        error_codes = [f.code for f in findings]
        self.assertIn("capability.invalid_namespace", error_codes)

if __name__ == "__main__":
    unittest.main()
