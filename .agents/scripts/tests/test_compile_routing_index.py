#!/usr/bin/env python3
import unittest
import tempfile
import shutil
import json
from pathlib import Path
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from compile_routing_index import compile_routing_index, validate_capability_namespace

class TestCompileRoutingIndex(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.agents_dir = self.temp_dir / "agent"
        self.skills_dir = self.temp_dir / "skills"
        self.agents_dir.mkdir(parents=True)
        self.skills_dir.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_namespace_validation(self):
        self.assertTrue(validate_capability_namespace("writing.chapter.draft"))
        self.assertTrue(validate_capability_namespace("video.timeline.cut"))
        self.assertFalse(validate_capability_namespace("draft_chapter"))
        self.assertFalse(validate_capability_namespace("writing.draft"))
        self.assertFalse(validate_capability_namespace("writing.chapter.draft.extra"))

    def test_compile_single_agent_capability(self):
        agent_file = self.agents_dir / "writer.md"
        agent_file.write_text(
            """---
name: writer
version: 1.0.0
tools: [Read, Write]
skills: [deep-writing]
capabilities:
  - id: writing.chapter.draft
    intent_patterns:
      - "write chapter"
      - "draft chapter"
    preconditions:
      structural:
        - key: outline_approved
          value: true
    postconditions:
      - key: chapter_draft_exists
        value: true
    evidence_schema:
      structural:
        - check: file_exists
          path: "draft.md"
    failure_policy:
      on_structural_failure: "retry(max=2) → escalate_human"
---
# Writer Agent
""",
            encoding="utf-8",
        )
        
        index = compile_routing_index(self.temp_dir)
        self.assertIn("writing.chapter.draft", index["capabilities"])
        cap = index["capabilities"]["writing.chapter.draft"]
        self.assertEqual(cap["owner_agent"], "writer")
        self.assertIn("write chapter", index["intent_map"])
        self.assertIn("writing.chapter.draft", index["intent_map"]["write chapter"])

if __name__ == "__main__":
    unittest.main()
