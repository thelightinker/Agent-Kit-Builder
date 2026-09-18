# .agents/scripts/tests/test_lifecycle_refactor.py
import json
import tempfile
import unittest
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from lifecycle_engine import LifecycleEngine

class TestLifecycleRefactor(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.kit_path = Path(self.temp_dir.name) / "test-kit"
        self.kit_path.mkdir(parents=True, exist_ok=True)
        self.engine = LifecycleEngine()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_refactor_consumes_audit_findings_and_hands_off_to_validate(self):
        self.engine.init_lifecycle(self.kit_path, "test-kit", "1.0.0", "create-kit")
        manifest = self.kit_path / "manifest.json"
        manifest.write_text("{}", encoding="utf-8")
        self.engine.transition_state(self.kit_path, "READY_FOR_VALIDATION", "create-kit", ["manifest.json"])
        
        # Validation fails
        findings = self.kit_path / "audit_findings.json"
        findings.write_text(json.dumps({"pass": False, "score": 2, "errors": ["frontmatter.missing"]}), encoding="utf-8")
        self.engine.record_validation_verdict(self.kit_path, pass_status=False, score=2, findings_file="audit_findings.json")
        
        # Refactor repairs and hands off
        gap_file = self.kit_path / "gap_analysis.md"
        gap_file.write_text("# Gap Analysis", encoding="utf-8")
        self.engine.transition_state(
            self.kit_path,
            target_state="READY_FOR_VALIDATION",
            workflow_name="refactor-kit",
            evidence_refs=["audit_findings.json", "gap_analysis.md"],
            notes="Repaired frontmatter",
        )
        
        state = self.engine.load_lifecycle(self.kit_path)
        self.assertEqual(state["lifecycle_state"], "READY_FOR_VALIDATION")
        self.assertEqual(state["handoff"]["source_workflow"], "refactor-kit")
        self.assertEqual(state["handoff"]["target_workflow"], "validate-kit")
        self.assertEqual(state["lineage"]["repair_cycle_count"], 1)
