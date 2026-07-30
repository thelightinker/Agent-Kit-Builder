import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from checkpoint_gate import render_envelope, evaluate_checkpoint

class TestCheckpointGate(unittest.TestCase):
    def test_checkpoint_gate_t3_confirm_code(self):
        envelope_t3 = render_envelope(
            risk_tier="T3",
            reason_code="IRREVERSIBLE_ACTION",
            summary="Delete core rule",
            core_delta="- legacy rule",
            confirm_code="CONFIRM 8492"
        )
        self.assertIn("CONFIRM 8492", envelope_t3)
        self.assertIn("CRITICAL CHECKPOINT REVIEW", envelope_t3)

    def test_evaluate_checkpoint_t2_approve(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = os.path.join(tmp_dir, "output", "my-kit")
            os.makedirs(output_dir, exist_ok=True)
            test_file = os.path.join(output_dir, "SKILL.md")
            with open(test_file, "w", encoding="utf-8") as f:
                f.write('{"key": "val"}')

            history_file = os.path.join(tmp_dir, "history.json")

            res = evaluate_checkpoint(
                node_id="test-node",
                target_files=[test_file],
                operation="modify",
                history_file=history_file,
                interactive=False,
                mock_input="1"
            )
            self.assertEqual(res["status"], "APPROVED")
            self.assertEqual(res["risk_tier"], "T2")

if __name__ == "__main__":
    unittest.main()
