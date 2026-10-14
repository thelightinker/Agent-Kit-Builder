from __future__ import annotations

import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest import mock

TESTS_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = TESTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

import benchmark_behavior
from benchmark_behavior import _verdict_lines

DAG_OK = {
    "write_conflict_detected": False,
    "stage_reduction_ratio": "2.0x",
    "serial_steps": 4,
    "dag_stages": 2,
    "phase1_parallel_items": 3,
}

COMPAT_OK = {
    "create-kit": {"present": True, "valid_requires": True},
    "refactor-kit": {"present": True, "valid_requires": True},
}


class TestBenchmarkVerdict(unittest.TestCase):
    def test_verdict_line_fails_when_any_convergence_case_fails(self):
        lines = _verdict_lines(
            True,
            82.4,
            88.6,
            DAG_OK,
            COMPAT_OK,
            [("Healthy Kit Baseline", False), ("Chaos 1", True)],
        )
        ok, text = lines[-1]
        self.assertFalse(ok)
        self.assertIn("1/2", text)

    def test_run_benchmark_returns_1_when_convergence_fails(self):
        with mock.patch.object(
            benchmark_behavior,
            "benchmark_convergence",
            return_value=[("x", False)],
        ), contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(1, benchmark_behavior.run_benchmark())
        self.assertNotIn("✓ Convergence", out.getvalue())

    def test_jit_range_is_not_a_literal(self):
        self.assertNotIn("82.4% - 88.6%", (SCRIPTS_DIR / "benchmark_behavior.py").read_text("utf-8"))


if __name__ == "__main__":
    unittest.main()
