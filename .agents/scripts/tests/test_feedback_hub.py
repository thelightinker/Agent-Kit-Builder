import unittest
import tempfile
import json
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import feedback_hub

class TestFeedbackHub(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.hub_dir = Path(self.temp_dir.name)
        self.kit_file = self.hub_dir / "kit_feedback.jsonl"
        self.bld_file = self.hub_dir / "builder_feedback.jsonl"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_append_and_fold_events(self):
        # 1. New event
        e1 = feedback_hub.append_event(self.kit_file, {
            "id": "fb-001",
            "source": "user",
            "target": "agent_kit",
            "agent_kit": "test-kit",
            "content": "Initial bug",
            "status": "new"
        })
        self.assertEqual(e1["status"], "new")

        # 2. Transition to fixed
        e2 = feedback_hub.append_event(self.kit_file, {
            "id": "fb-001",
            "status": "fixed",
            "resolution": {"commit": "c1", "version": "v1.0"}
        })

        # 3. Fold state
        folded = feedback_hub.load_and_fold_events(self.kit_file)
        self.assertIn("fb-001", folded)
        self.assertEqual(folded["fb-001"]["status"], "fixed")
        self.assertEqual(folded["fb-001"]["resolution"]["commit"], "c1")
        self.assertEqual(len(folded["fb-001"]["history"]), 2)

    def test_lifecycle_failed_retry_verified(self):
        feedback_hub.append_event(self.kit_file, {"id": "fb-002", "agent_kit": "test-kit", "status": "new", "content": "Bug 2"})
        feedback_hub.append_event(self.kit_file, {"id": "fb-002", "status": "fixed", "resolution": {"commit": "c2"}})
        feedback_hub.append_event(self.kit_file, {"id": "fb-002", "status": "failed", "note": "Still reproduced"})
        feedback_hub.append_event(self.kit_file, {"id": "fb-002", "status": "retry"})
        
        # Must be in unresolved
        unresolved = feedback_hub.query_unresolved(self.kit_file, agent_kit="test-kit")
        self.assertEqual(len(unresolved), 1)
        self.assertEqual(unresolved[0]["status"], "retry")

        # Now verify it
        feedback_hub.append_event(self.kit_file, {"id": "fb-002", "status": "verified", "verification": {"evidence": "Pass", "regression_rule": "Rule A"}})
        unresolved_after = feedback_hub.query_unresolved(self.kit_file, agent_kit="test-kit")
        self.assertEqual(len(unresolved_after), 0)

        # Must be in regression knowledge
        knowledge = feedback_hub.query_regression_knowledge(self.kit_file, agent_kit="test-kit")
        self.assertEqual(len(knowledge), 1)
        self.assertEqual(knowledge[0]["verification"]["regression_rule"], "Rule A")

    def test_render_board(self):
        feedback_hub.append_event(self.kit_file, {"id": "fb-001", "agent_kit": "kit-a", "status": "new", "content": "Unresolved bug"})
        board_content = feedback_hub.render_feedback_board(self.hub_dir)
        self.assertIn("Feedback & Learning Dashboard", board_content)
        self.assertIn("fb-001", board_content)
        board_file = self.hub_dir / "FEEDBACK_BOARD.md"
        self.assertTrue(board_file.is_file())

    def test_audit_kit_summary(self):
        feedback_hub.append_event(self.kit_file, {"id": "fb-101", "agent_kit": "target-kit", "status": "new", "content": "Bug X"})
        feedback_hub.append_event(self.kit_file, {"id": "fb-102", "agent_kit": "target-kit", "status": "fixed", "resolution": {"commit": "c10"}})
        feedback_hub.append_event(self.kit_file, {"id": "fb-103", "agent_kit": "target-kit", "status": "verified", "verification": {"regression_rule": "Rule Z"}})

        audit = feedback_hub.audit_kit_feedback(self.kit_file, "target-kit")
        self.assertEqual(len(audit["unresolved"]), 2)
        self.assertEqual(len(audit["regression_knowledge"]), 1)

if __name__ == "__main__":
    unittest.main()
