import os
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from checkpoints.impact_engine import (
    classify_blast_radius,
    prioritize_and_truncate_diff,
    generate_impact_summary
)

class TestImpactEngine(unittest.TestCase):
    def test_2d_blast_radius_matrix(self):
        # 1. Modify HIGH path -> T3
        radius, reason, tier = classify_blast_radius(".agents/rules/universal-rules.md", "modify")
        self.assertEqual((radius, reason, tier), ("HIGH", "POLICY_BOUNDARY", "T3"))

        # 2. Delete on MEDIUM path -> T3 (Auto +1 Tier)
        radius, reason, tier = classify_blast_radius("output/my-kit/manifest.json", "delete")
        self.assertEqual((radius, reason, tier), ("HIGH", "IRREVERSIBLE_ACTION", "T3"))

        # 3. Create on MEDIUM path -> T2
        radius, reason, tier = classify_blast_radius("output/my-kit/SKILL.md", "create")
        self.assertEqual((radius, reason, tier), ("MEDIUM", "EXTERNAL_WRITE", "T2"))

        # 4. Create on LOW path -> T1
        radius, reason, tier = classify_blast_radius("output/draft/tmp.txt", "create")
        self.assertEqual((radius, reason, tier), ("LOW", "INTERNAL_DRAFT", "T1"))

    def test_risk_prioritized_diff_truncation(self):
        raw_diff = (
            "+ normal line 1\n"
            "+ normal line 2\n"
            "- deletion line in core .agents/rules/\n"
            "+ normal line 3\n"
        )
        truncated = prioritize_and_truncate_diff(raw_diff, max_lines=2)
        # Deletion line MUST be prioritized first
        self.assertIn("- deletion line in core", truncated)

if __name__ == "__main__":
    unittest.main()
