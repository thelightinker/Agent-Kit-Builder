# .agents/scripts/tests/test_lifecycle_engine.py
import json
import tempfile
import unittest
from pathlib import Path
import sys

# Ensure scripts dir is on sys.path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from lifecycle_engine import (
    LifecycleEngine,
    LifecycleError,
    UnauthorizedTransitionError,
    MissingEvidenceError,
    MaxRepairCyclesExceededError,
)

class TestLifecycleEngine(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.kit_path = Path(self.temp_dir.name) / "test-kit"
        self.kit_path.mkdir(parents=True, exist_ok=True)
        self.engine = LifecycleEngine()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_init_lifecycle_creates_valid_draft(self):
        data = self.engine.init_lifecycle(self.kit_path, "test-kit", "1.0.0", "create-kit")
        self.assertEqual(data["lifecycle_state"], "DRAFT")
        self.assertEqual(data["schema_version"], "1.0.0")
        self.assertEqual(data["kit_version"], "1.0.0")
        self.assertEqual(data["lineage"]["repair_cycle_count"], 0)
        self.assertTrue((self.kit_path / "lifecycle.json").is_file())

    def test_transition_without_evidence_fails(self):
        self.engine.init_lifecycle(self.kit_path, "test-kit", "1.0.0", "create-kit")
        with self.assertRaises(MissingEvidenceError):
            self.engine.transition_state(
                self.kit_path,
                target_state="READY_FOR_VALIDATION",
                workflow_name="create-kit",
                evidence_refs=[],
            )

    def test_unauthorized_state_mutation_rejected(self):
        self.engine.init_lifecycle(self.kit_path, "test-kit", "1.0.0", "create-kit")
        # create manifest evidence
        manifest_file = self.kit_path / "manifest.json"
        manifest_file.write_text("{}", encoding="utf-8")
        self.engine.transition_state(
            self.kit_path,
            target_state="READY_FOR_VALIDATION",
            workflow_name="create-kit",
            evidence_refs=["manifest.json"],
        )
        
        # refactor-kit attempts to self-certify VALIDATED -> MUST FAIL
        findings_file = self.kit_path / "audit_findings.json"
        findings_file.write_text("{}", encoding="utf-8")
        with self.assertRaises(UnauthorizedTransitionError):
            self.engine.transition_state(
                self.kit_path,
                target_state="VALIDATED",
                workflow_name="refactor-kit",
                evidence_refs=["audit_findings.json"],
            )

    def test_repair_cycle_quota_and_escalation(self):
        self.engine.init_lifecycle(self.kit_path, "test-kit", "1.0.0", "create-kit")
        manifest_file = self.kit_path / "manifest.json"
        manifest_file.write_text("{}", encoding="utf-8")
        findings_file = self.kit_path / "audit_findings.json"
        findings_file.write_text("{}", encoding="utf-8")
        
        self.engine.transition_state(self.kit_path, "READY_FOR_VALIDATION", "create-kit", ["manifest.json"])
        
        # Cycle 1
        self.engine.record_validation_verdict(self.kit_path, pass_status=False, score=2, findings_file="audit_findings.json")
        self.assertEqual(self.engine.load_lifecycle(self.kit_path)["lifecycle_state"], "NEEDS_REFACTOR")
        self.engine.transition_state(self.kit_path, "READY_FOR_VALIDATION", "refactor-kit", ["audit_findings.json"])
        self.assertEqual(self.engine.load_lifecycle(self.kit_path)["lineage"]["repair_cycle_count"], 1)

        # Cycle 2
        self.engine.record_validation_verdict(self.kit_path, pass_status=False, score=2, findings_file="audit_findings.json")
        self.engine.transition_state(self.kit_path, "READY_FOR_VALIDATION", "refactor-kit", ["audit_findings.json"])
        self.assertEqual(self.engine.load_lifecycle(self.kit_path)["lineage"]["repair_cycle_count"], 2)

        # Cycle 3
        self.engine.record_validation_verdict(self.kit_path, pass_status=False, score=2, findings_file="audit_findings.json")
        self.engine.transition_state(self.kit_path, "READY_FOR_VALIDATION", "refactor-kit", ["audit_findings.json"])
        self.assertEqual(self.engine.load_lifecycle(self.kit_path)["lineage"]["repair_cycle_count"], 3)

        # Cycle 4 -> Exceeds max 3 repair cycles -> MUST escalate to NEEDS_HUMAN_INTERVENTION
        self.engine.record_validation_verdict(self.kit_path, pass_status=False, score=2, findings_file="audit_findings.json")
        data = self.engine.load_lifecycle(self.kit_path)
        self.assertEqual(data["lifecycle_state"], "NEEDS_HUMAN_INTERVENTION")


class TestLifecycleBackCompat(unittest.TestCase):
    def setUp(self):
        self.schema_path = Path(__file__).resolve().parents[2] / "schemas" / "lifecycle.schema.json"
        self.schema = json.loads(self.schema_path.read_text(encoding="utf-8"))
        self.temp_dir = tempfile.TemporaryDirectory()
        self.kit_path = Path(self.temp_dir.name) / "test-kit"
        self.kit_path.mkdir(parents=True, exist_ok=True)
        self.engine = LifecycleEngine()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_old_lifecycle_with_visual_qa_still_validates(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        data = self.engine.init_lifecycle(self.kit_path, "test-kit", "1.0.0", "create-kit")
        data["verdicts"]["visual_qa"] = {
            "evidence_file": "visual_qa_report.json",
            "last_checked_at": "2026-10-14T10:00:00Z",
        }
        jsonschema.validate(instance=data, schema=self.schema)

    def test_new_lifecycle_without_visual_qa_validates(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        data = self.engine.init_lifecycle(self.kit_path, "test-kit", "1.0.0", "create-kit")
        self.assertNotIn("visual_qa", data["verdicts"])
        jsonschema.validate(instance=data, schema=self.schema)

