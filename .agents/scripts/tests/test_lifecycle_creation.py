# .agents/scripts/tests/test_lifecycle_creation.py
import json
import tempfile
import unittest
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from lifecycle_engine import LifecycleEngine

class TestLifecycleCreation(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.kit_path = Path(self.temp_dir.name) / "test-kit"
        self.kit_path.mkdir(parents=True, exist_ok=True)
        self.engine = LifecycleEngine()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_kit_handoff_contract(self):
        self.engine.init_lifecycle(self.kit_path, "test-kit", "1.0.0", "create-kit")
        manifest = self.kit_path / "manifest.json"
        manifest.write_text("{}", encoding="utf-8")
        
        self.engine.transition_state(
            self.kit_path,
            target_state="READY_FOR_VALIDATION",
            workflow_name="create-kit",
            evidence_refs=["manifest.json"],
        )
        
        state = self.engine.load_lifecycle(self.kit_path)
        self.assertEqual(state["lifecycle_state"], "READY_FOR_VALIDATION")
        self.assertEqual(state["handoff"]["source_workflow"], "create-kit")
        self.assertEqual(state["handoff"]["target_workflow"], "validate-kit")
        self.assertEqual(state["handoff"]["contract_version"], "1.0.0")

