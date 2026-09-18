#!/usr/bin/env python3
import unittest
import tempfile
import shutil
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from compile_invariants import compile_invariants

class TestCompileInvariants(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.workflows_dir = self.temp_dir / "workflows"
        self.agents_dir = self.temp_dir / "agent"
        self.workflows_dir.mkdir(parents=True)
        self.agents_dir.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_compile_invariants(self):
        (self.workflows_dir / "book.md").write_text(
            """---
name: book
global_invariants:
  - id: research_before_writing
    description: "Must finish research before writing"
    check: "all(research_completed)"
---
# Book Workflow
""",
            encoding="utf-8",
        )
        
        (self.agents_dir / "writer.md").write_text(
            """---
name: writer
negative_scope:
  cannot_modify:
    - outline.md
  cannot_trigger_state_transition:
    - PUBLISHED
---
# Writer Agent
""",
            encoding="utf-8",
        )
        
        invariants = compile_invariants(self.temp_dir)
        self.assertEqual(len(invariants["global_invariants"]), 1)
        self.assertEqual(invariants["global_invariants"][0]["id"], "research_before_writing")
        self.assertIn("writer", invariants["negative_boundaries"])
        self.assertIn("outline.md", invariants["negative_boundaries"]["writer"]["cannot_modify"])

if __name__ == "__main__":
    unittest.main()
