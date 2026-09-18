#!/usr/bin/env python3
import unittest
import tempfile
import shutil
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from compile_task_classifier import compile_task_classifier

class TestCompileTaskClassifier(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.workflows_dir = self.temp_dir / "workflows"
        self.agents_dir = self.temp_dir / "agent"
        self.workflows_dir.mkdir(parents=True)
        self.agents_dir.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_compile_task_classifier(self):
        (self.workflows_dir / "book.md").write_text(
            """---
name: book
nodes:
  OUTLINE:
    required_outcome: outline_approved
---
# Book Workflow
""",
            encoding="utf-8",
        )
        
        (self.agents_dir / "writer.md").write_text(
            """---
name: writer
capabilities:
  - id: writing.outline.generate
    intent_patterns: ["create outline", "plan book"]
    postconditions:
      - key: outline_approved
        value: true
  - id: writing.quick_fix.typo
    intent_patterns: ["fix typo", "fix spelling"]
    postconditions:
      - key: typo_fixed
        value: true
---
# Writer Agent
""",
            encoding="utf-8",
        )
        
        classifier = compile_task_classifier(self.temp_dir)
        self.assertIn("workflow_bound_intents", classifier)
        self.assertIn("ad_hoc_intents", classifier)
        self.assertIn("create outline", classifier["workflow_bound_intents"])
        self.assertIn("fix typo", classifier["ad_hoc_intents"])

if __name__ == "__main__":
    unittest.main()
