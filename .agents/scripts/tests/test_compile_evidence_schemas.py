#!/usr/bin/env python3
import unittest
import tempfile
import shutil
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from compile_evidence_schemas import compile_evidence_schemas

class TestCompileEvidenceSchemas(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.agents_dir = self.temp_dir / "agent"
        self.agents_dir.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_compile_evidence_schemas(self):
        (self.agents_dir / "writer.md").write_text(
            """---
name: writer
capabilities:
  - id: writing.chapter.draft
    evidence_schema:
      structural:
        - check: file_exists
          path: "draft.md"
        - check: word_count_min
          min_value: 2000
      semantic:
        - name: voice_consistent
          evaluator: editor
---
# Writer Agent
""",
            encoding="utf-8",
        )
        
        compiled = compile_evidence_schemas(self.temp_dir)
        self.assertIn("writing.chapter.draft", compiled["schemas"])
        cap_schema = compiled["schemas"]["writing.chapter.draft"]
        self.assertEqual(len(cap_schema["structural"]), 2)
        self.assertEqual(cap_schema["structural"][0]["check"], "file_exists")
        self.assertEqual(cap_schema["semantic"][0]["name"], "voice_consistent")

if __name__ == "__main__":
    unittest.main()
