#!/usr/bin/env python3
import unittest
import tempfile
import shutil
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from compile_state_schema import compile_state_schema

class TestCompileStateSchema(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.workflows_dir = self.temp_dir / "workflows"
        self.agents_dir = self.temp_dir / "agent"
        self.workflows_dir.mkdir(parents=True)
        self.agents_dir.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_compile_state_schema(self):
        (self.workflows_dir / "book.md").write_text(
            """---
name: book
nodes:
  OUTLINE:
    required_outcome: "outline_approved"
---
# Book Workflow
""",
            encoding="utf-8",
        )
        
        (self.agents_dir / "writer.md").write_text(
            """---
name: writer
capabilities:
  - id: writing.chapter.draft
    preconditions:
      structural:
        - key: outline_approved
          value: true
      semantic:
        - name: voice_consistent
          evaluator: developmental-editor
    postconditions:
      - key: chapter_draft_exists
        value: true
---
# Writer Agent
""",
            encoding="utf-8",
        )
        
        schema = compile_state_schema(self.temp_dir)
        self.assertIn("outline_approved", schema["state_keys"])
        self.assertIn("chapter_draft_exists", schema["state_keys"])
        self.assertIn("writer", schema["state_keys"]["chapter_draft_exists"]["written_by"])
        self.assertIn("writer", schema["state_keys"]["outline_approved"]["read_by"])
        self.assertIn("voice_consistent", schema["verdict_keys"])
        self.assertEqual(schema["verdict_keys"]["voice_consistent"]["evaluator"], "developmental-editor")

if __name__ == "__main__":
    unittest.main()
