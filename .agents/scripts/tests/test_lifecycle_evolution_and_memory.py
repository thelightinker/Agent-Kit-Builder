# .agents/scripts/tests/test_lifecycle_evolution_and_memory.py
import json
import tempfile
import unittest
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from lifecycle_engine import LifecycleEngine, UnauthorizedTransitionError

class TestEvolutionAndMemory(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.kit_path = Path(self.temp_dir.name) / "test-kit"
        self.kit_path.mkdir(parents=True, exist_ok=True)
        self.engine = LifecycleEngine()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_remember_kit_rejects_unvalidated_or_low_score_kit(self):
        self.engine.init_lifecycle(self.kit_path, "test-kit", "1.0.0", "create-kit")
        # Attempt promotion while in DRAFT -> MUST FAIL
        with self.assertRaises(UnauthorizedTransitionError):
            self.engine.promote_to_memory(self.kit_path, "memory/test.md")
            
        # Score is only 3 -> MUST FAIL
        findings = self.kit_path / "audit.json"
        findings.write_text("{}", encoding="utf-8")
        self.engine.record_validation_verdict(self.kit_path, pass_status=True, score=3, findings_file="audit.json")
        with self.assertRaises(UnauthorizedTransitionError):
            self.engine.promote_to_memory(self.kit_path, "memory/test.md")

    def test_remember_kit_succeeds_on_exemplar(self):
        self.engine.init_lifecycle(self.kit_path, "test-kit", "1.0.0", "create-kit")
        manifest = self.kit_path / "manifest.json"
        manifest.write_text("{}", encoding="utf-8")
        findings = self.kit_path / "audit.json"
        findings.write_text("{}", encoding="utf-8")
        
        self.engine.transition_state(self.kit_path, "READY_FOR_VALIDATION", "create-kit", ["manifest.json"])
        self.engine.record_validation_verdict(self.kit_path, pass_status=True, score=5, findings_file="audit.json")
        self.assertEqual(self.engine.load_lifecycle(self.kit_path)["lifecycle_state"], "VALIDATED")
        
        self.engine.promote_to_memory(self.kit_path, "memory/golden_pattern.md")
        state = self.engine.load_lifecycle(self.kit_path)
        self.assertEqual(state["lifecycle_state"], "EXEMPLAR_ARCHIVED")
        self.assertTrue(state["verdicts"]["memory_promotion"]["promoted"])

    def test_architecture_evolution_change_gate_lifecycle(self):
        self.engine.init_lifecycle(self.kit_path, "test-kit", "1.0.0", "create-kit")
        self.assertIsNone(self.engine.load_lifecycle(self.kit_path)["active_change_gate"])
        
        # Open Gate
        self.engine.open_change_gate(self.kit_path, "architecture_evolution")
        self.assertEqual(self.engine.load_lifecycle(self.kit_path)["active_change_gate"], "architecture_evolution")
        
        # Close Gate
        self.engine.close_change_gate(self.kit_path)
        self.assertIsNone(self.engine.load_lifecycle(self.kit_path)["active_change_gate"])
