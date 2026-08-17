import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from checkpoints.guard_engine import (
    compute_scoped_hash,
    create_snapshot,
    verify_staleness,
    rollback_snapshot
)

class TestGuardEngine(unittest.TestCase):
    def test_guard_engine_hash_and_rollback(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            file1 = os.path.join(tmp_dir, "test1.txt")
            with open(file1, "w", encoding="utf-8") as f:
                f.write("initial content")

            # 1. Compute scoped hash
            hash_val = compute_scoped_hash([file1])
            self.assertTrue(isinstance(hash_val, str) and len(hash_val) == 64)

            # 2. Create snapshot
            snap_dir = os.path.join(tmp_dir, "snapshot")
            create_snapshot([file1], snap_dir)
            self.assertTrue(os.path.exists(os.path.join(snap_dir, "test1.txt")))

            # 3. Verify no staleness initially
            self.assertTrue(verify_staleness([file1], hash_val))

            # 4. Mutate file (simulate drift)
            with open(file1, "w", encoding="utf-8") as f:
                f.write("tampered content")

            # 5. Verify staleness detected
            self.assertFalse(verify_staleness([file1], hash_val))

            # 6. Rollback snapshot
            rollback_snapshot(snap_dir, [file1])
            with open(file1, "r", encoding="utf-8") as f:
                self.assertEqual(f.read(), "initial content")

if __name__ == "__main__":
    unittest.main()
