# .agents/scripts/tests/test_lifecycle_e2e.py
import json
import tempfile
import unittest
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from lifecycle_engine import (
    LifecycleEngine,
    UnauthorizedTransitionError,
    MissingEvidenceError,
)
from validate_kit import run_validation_and_update_lifecycle


class TestLifecycleE2E(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.kit_path = Path(self.temp_dir.name) / "e2e-kit"
        self.kit_path.mkdir(parents=True, exist_ok=True)
        self.engine = LifecycleEngine()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_full_closed_loop_lifecycle(self):
        # 1. CREATE-KIT: Initialize DRAFT -> READY_FOR_VALIDATION
        self.engine.init_lifecycle(self.kit_path, "e2e-kit", "1.0.0", "create-kit")
        manifest = self.kit_path / "manifest.json"
        manifest.write_text("{}", encoding="utf-8")
        version_file = self.kit_path / "VERSION"
        version_file.write_text("2026.8.24", encoding="utf-8")
        
        self.engine.transition_state(self.kit_path, "READY_FOR_VALIDATION", "create-kit", ["manifest.json"])
        self.assertEqual(self.engine.load_lifecycle(self.kit_path)["lifecycle_state"], "READY_FOR_VALIDATION")
        
        # 2. VALIDATE-KIT: Initial run fails due to missing skills/agent
        findings_file = self.kit_path / "audit_findings.json"
        findings_file.write_text(json.dumps({"pass": False, "score": 2, "errors": ["agent.missing"]}), encoding="utf-8")
        self.engine.record_validation_verdict(self.kit_path, pass_status=False, score=2, findings_file="audit_findings.json")
        self.assertEqual(self.engine.load_lifecycle(self.kit_path)["lifecycle_state"], "NEEDS_REFACTOR")
        
        # 3. REFACTOR-KIT: Applies delta patch, repairs agent.md, hands off back to validate
        gap_file = self.kit_path / "gap_analysis.md"
        gap_file.write_text("# Repaired agent.md", encoding="utf-8")
        self.engine.transition_state(
            self.kit_path,
            target_state="READY_FOR_VALIDATION",
            workflow_name="refactor-kit",
            evidence_refs=["audit_findings.json", "gap_analysis.md"],
        )
        self.assertEqual(self.engine.load_lifecycle(self.kit_path)["lineage"]["repair_cycle_count"], 1)
        
        # 4. VALIDATE-KIT (RE-VALIDATE): Now passes with 5/5 score
        findings_file.write_text(json.dumps({"pass": True, "score": 5, "errors": []}), encoding="utf-8")
        self.engine.record_validation_verdict(self.kit_path, pass_status=True, score=5, findings_file="audit_findings.json")
        self.assertEqual(self.engine.load_lifecycle(self.kit_path)["lifecycle_state"], "VALIDATED")
        
        # 5. REMEMBER-KIT: Promotes 5/5 verified kit to Exemplar
        self.engine.promote_to_memory(self.kit_path, "memory/e2e_pattern.md")
        state = self.engine.load_lifecycle(self.kit_path)
        self.assertEqual(state["lifecycle_state"], "EXEMPLAR_ARCHIVED")
        self.assertTrue(state["verdicts"]["memory_promotion"]["promoted"])

    def test_oscillation_and_max_repair_cycle_tripwire(self):
        self.engine.init_lifecycle(self.kit_path, "e2e-kit", "1.0.0", "create-kit")
        manifest = self.kit_path / "manifest.json"
        manifest.write_text("{}", encoding="utf-8")
        findings_file = self.kit_path / "audit_findings.json"
        findings_file.write_text("{}", encoding="utf-8")
        gap_file = self.kit_path / "gap_analysis.md"
        gap_file.write_text("{}", encoding="utf-8")

        self.engine.transition_state(self.kit_path, "READY_FOR_VALIDATION", "create-kit", ["manifest.json"])

        # 3 Repair cycles
        for cycle in range(1, 4):
            self.engine.record_validation_verdict(self.kit_path, pass_status=False, score=2, findings_file="audit_findings.json")
            self.engine.transition_state(self.kit_path, "READY_FOR_VALIDATION", "refactor-kit", ["audit_findings.json", "gap_analysis.md"])
            self.assertEqual(self.engine.load_lifecycle(self.kit_path)["lineage"]["repair_cycle_count"], cycle)

        # 4th validation failure triggers escalation
        self.engine.record_validation_verdict(self.kit_path, pass_status=False, score=2, findings_file="audit_findings.json")
        state = self.engine.load_lifecycle(self.kit_path)
        self.assertEqual(state["lifecycle_state"], "NEEDS_HUMAN_INTERVENTION")
        self.assertEqual(state["handoff"]["target_workflow"], "manual_escalation")
