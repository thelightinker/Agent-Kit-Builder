# .agents/scripts/tests/test_lifecycle_validation.py
import json
import tempfile
import unittest
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from lifecycle_engine import LifecycleEngine
from validate_kit import run_validation_and_update_lifecycle

class TestLifecycleValidation(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.kit_path = Path(self.temp_dir.name) / "test-kit"
        self.kit_path.mkdir(parents=True, exist_ok=True)
        self.engine = LifecycleEngine()
        self.engine.init_lifecycle(self.kit_path, "test-kit", "1.0.0", "create-kit")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_validation_creates_audit_findings_and_updates_lifecycle(self):
        # Create minimal kit files
        (self.kit_path / "VERSION").write_text("2026.8.24", encoding="utf-8")
        manifest = self.kit_path / "manifest.json"
        manifest.write_text("{}", encoding="utf-8")
        self.engine.transition_state(self.kit_path, "READY_FOR_VALIDATION", "create-kit", ["manifest.json"])
        
        findings_path = self.kit_path / "audit_findings.json"
        result = run_validation_and_update_lifecycle(self.kit_path, findings_output=findings_path)
        
        self.assertTrue(findings_path.is_file())
        findings = json.loads(findings_path.read_text(encoding="utf-8"))
        self.assertIn("pass", findings)
        self.assertIn("score", findings)
        self.assertIn("errors", findings)
        
        # Verify lifecycle.json updated
        state = self.engine.load_lifecycle(self.kit_path)
        self.assertIn(state["lifecycle_state"], ["VALIDATED", "NEEDS_REFACTOR"])
        self.assertIsNotNone(state["verdicts"]["validation"]["findings_file"])
