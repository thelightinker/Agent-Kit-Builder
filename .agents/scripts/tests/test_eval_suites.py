from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = TESTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from support import TOOLKIT
import eval_runner


class TestEvalSuites(unittest.TestCase):
    def test_every_active_suite_is_runnable_by_eval_runner(self):
        for path in (TOOLKIT / "evals").glob("*.json"):
            if path.name == "quality_baseline.json":
                continue
            report = eval_runner.run_eval_suite(path, TOOLKIT)
            self.assertGreater(report["total"], 0, f"Suite {path.name} has no test cases")
            self.assertEqual(report["failed"], 0, f"Suite {path.name} failed on real toolkit")


    def test_golden_kit_suite_covers_required_structural_failure_modes(self):
        suite_path = TOOLKIT / "evals/golden_kit_suite.json"
        self.assertTrue(suite_path.is_file(), "golden_kit_suite.json must exist")
        suite = json.loads(suite_path.read_text("utf-8"))
        modes = {tc.get("failure_mode") for tc in suite.get("test_cases", [])}
        for expected in ("missing_negative_boundaries", "missing_capabilities", "missing_when_to_use", "broken_state_machine"):
            self.assertIn(expected, modes)

    def test_eval_runner_result_includes_failure_mode(self):
        suite = TOOLKIT / "evals/golden_kit_suite.json"
        self.assertTrue(suite.is_file(), "golden_kit_suite.json must exist")
        report = eval_runner.run_eval_suite(suite, TOOLKIT)
        for res in report["results"]:
            self.assertIn("failure_mode", res)

    def test_evals_json_moved_to_legacy(self):
        self.assertFalse((TOOLKIT / "evals/evals.json").exists())
        self.assertTrue((TOOLKIT / "evals/legacy/evals-v3-prompts.json").exists())


if __name__ == "__main__":
    unittest.main()
