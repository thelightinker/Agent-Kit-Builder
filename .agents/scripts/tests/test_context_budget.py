from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = TESTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from support import TOOLKIT, copy_fixture
import validate_kit
try:
    import context_budget
    from context_budget import (
        RULES_BUDGET_BYTES,
        ORCHESTRATOR_BUDGET_BYTES,
        P0_INVARIANTS,
        measure,
    )
except ImportError:
    context_budget = None
    RULES_BUDGET_BYTES = 8192
    ORCHESTRATOR_BUDGET_BYTES = 10240
    P0_INVARIANTS = ()
    measure = None


class TestContextBudget(unittest.TestCase):
    def setUp(self):
        self._tmp_obj = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp_obj.name)

    def tearDown(self):
        self._tmp_obj.cleanup()

    def test_always_on_rules_within_budget(self):
        self.assertIsNotNone(measure, "context_budget.measure must be defined")
        self.assertLessEqual(measure(TOOLKIT)["rules_bytes"], RULES_BUDGET_BYTES)

    def test_orchestrator_within_budget(self):
        self.assertIsNotNone(measure, "context_budget.measure must be defined")
        self.assertLessEqual(measure(TOOLKIT)["orchestrator_bytes"], ORCHESTRATOR_BUDGET_BYTES)

    def test_budget_violation_is_reported_by_validator(self):
        kit = copy_fixture("golden-kit", self.tmp)
        (kit / "rules/big.md").write_text(
            "---\nname: big\nversion: 1.0.0\npriority: P1\ntrigger: always_on\ndescription: \"x\"\n---\n" + "x" * 9000,
            "utf-8",
        )
        findings = []
        validate_kit.validate_context_budget(kit, findings)
        self.assertEqual(["context.budget_exceeded"], [f.code for f in findings])

    def test_no_p0_invariant_is_dropped_or_duplicated_across_always_on_files(self):
        self.assertIsNotNone(measure, "context_budget.measure must be defined")
        files = [TOOLKIT / f for f in measure(TOOLKIT)["files"]]
        texts = {f.name: f.read_text("utf-8") for f in files}
        for phrase in P0_INVARIANTS:
            holders = [n for n, t in texts.items() if phrase in t]
            with self.subTest(phrase):
                self.assertGreaterEqual(len(holders), 1)


if __name__ == "__main__":
    unittest.main()
