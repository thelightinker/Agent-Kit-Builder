from __future__ import annotations

import re
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

from support import TOOLKIT, copy_fixture
import validate_kit
import export_kit
from compile_routing_index import compile_routing_index
from compile_invariants import compile_invariants
from compile_state_schema import compile_state_schema
from compile_task_classifier import compile_task_classifier
from compile_evidence_schemas import compile_evidence_schemas


class TestGoldenKitE2E(unittest.TestCase):
    def setUp(self):
        self._tmp_obj = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp_obj.name)
        try:
            self.kit = copy_fixture("golden-kit", self.tmp)
        except Exception:
            self.kit = self.tmp / "golden-kit"

    def tearDown(self):
        self._tmp_obj.cleanup()

    def test_fixture_validates_clean(self):
        errs = [f for f in validate_kit.validate(self.kit, auto_heal=False) if f.severity == "error"]
        self.assertEqual([], errs)

    def test_compilers_emit_non_empty_artifacts(self):
        self.assertIn("golden.outline.draft", compile_routing_index(self.kit)["capabilities"])
        self.assertTrue(compile_routing_index(self.kit)["intent_map"])
        self.assertTrue(compile_state_schema(self.kit)["state_keys"])
        self.assertTrue(compile_evidence_schemas(self.kit)["schemas"])
        self.assertTrue(compile_task_classifier(self.kit)["workflow_bound_intents"])
        self.assertEqual(
            ["approved_outline"],
            compile_invariants(self.kit)["negative_boundaries"]["golden-writer"]["cannot_modify"],
        )

    def test_removing_capabilities_triggers_routing_empty_capabilities(self):
        agent = self.kit / "agent/golden-writer.md"
        agent.write_text(re.sub(r"(?s)capabilities:.*?\n(?=\w[\w-]*:|---)", "", agent.read_text("utf-8")), "utf-8")
        codes = [f.code for f in validate_kit.validate(self.kit, auto_heal=False)]
        self.assertIn("routing.empty_capabilities", codes)

    def test_export_writes_cursor_rules(self):
        out = self.tmp / "dist"
        export_kit.export_kit(self.kit, out, target="all")
        self.assertTrue(any(out.rglob(".cursorrules")))






if __name__ == "__main__":
    unittest.main()
