import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from checkpoints.trust_engine import (
    record_decision,
    check_trust_proposal,
    check_compounding_batch
)

class TestTrustEngine(unittest.TestCase):
    def test_trust_engine_history_and_batching(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            history_file = os.path.join(tmp_dir, "decision_history.json")

            # 1. Record 20 approve decisions
            for _ in range(20):
                record_decision(history_file, "EXTERNAL_WRITE", "approve")

            # 2. Verify trust proposal triggered (>95% approve)
            self.assertTrue(check_trust_proposal(history_file, "EXTERNAL_WRITE"))

            # 3. Verify batching rule (>= 3 files in phase -> escalate to T2)
            self.assertEqual(check_compounding_batch(t1_file_count=2, phase_name="skill-crafting"), "T1")
            self.assertEqual(check_compounding_batch(t1_file_count=3, phase_name="skill-crafting"), "T2")

if __name__ == "__main__":
    unittest.main()
