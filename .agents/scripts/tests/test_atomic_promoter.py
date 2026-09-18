import unittest
import tempfile
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import atomic_promoter

class TestAtomicPromoter(unittest.TestCase):
    def test_two_phase_promotion_and_archive(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            staging = root / "staging" / "my-kit"
            canonical = root / "Output" / "my-kit"
            target = root / "AI Agent" / "my-kit"
            eng_archive = root / "Output" / ".archive"
            tgt_archive = root / "AI Agent" / ".archive"
            
            # Setup v1 active in canonical and target
            canonical.mkdir(parents=True)
            (canonical / "v.txt").write_text("v1.0.0", encoding="utf-8")
            target.mkdir(parents=True)
            (target / "v.txt").write_text("v1.0.0", encoding="utf-8")
            
            # Setup v2 candidate in staging
            staging.mkdir(parents=True)
            (staging / "v.txt").write_text("v2.0.0", encoding="utf-8")
            (staging / "new_feature.txt").write_text("feature content", encoding="utf-8")
            
            result = atomic_promoter.execute_two_phase_promotion(
                staging, canonical, target, eng_archive, tgt_archive
            )
            
            self.assertTrue(result["success"])
            self.assertEqual((canonical / "v.txt").read_text("utf-8"), "v2.0.0")
            self.assertEqual((target / "v.txt").read_text("utf-8"), "v2.0.0")
            self.assertTrue(result["checksum_verified"])
            
            # Verify v1 was archived
            self.assertTrue(eng_archive.exists())
            self.assertTrue(tgt_archive.exists())

if __name__ == "__main__":
    unittest.main()
