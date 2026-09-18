#!/usr/bin/env python3
"""Test Suite for Deterministic Upgrade Gate & Anti-Bloat Guardrails.

Verifies that the Upgrade Gate reliably filters out bad upgrades, approval fatigue traps,
Goodhart attacks, and accepts profitable trade-offs with verifiable evidence.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

# Add scripts directory to sys.path
SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from upgrade_gate_evaluator import evaluate_proposal, UpgradeEvaluationResult


class TestUpgradeGate(unittest.TestCase):
    def test_case_1_good_upgrade_ast_parser(self):
        """Case 1: Genuine optimization - AST Parser replaces 15 regexes."""
        proposal = {
            "proposal_id": "UPG-2026-001",
            "title": "Single-Pass AST Parser with JIT Cache in validate_kit",
            "target_scope": "builder_core",
            "extraction_provenance": {
                "what_works": "Single-pass AST parsing accurately catches nested violations without regex drift.",
                "why_it_works": "AST represents syntax tree deterministically without regex backtracking vulnerabilities.",
                "generalizable_principle": "Replace brittle pattern matching with semantic AST visitors across all schema checks.",
                "domain_specific_discarded": "None, pure python AST.",
                "adapted_architecture_plan": "Integrate AST visitor into validate_kit.py preserving existing Finding contract."
            },
            "evidence": {
                "benchmarks": [
                    {"metric_name": "validation_latency_ms", "baseline": 850, "after": 110, "source": "benchmarks/linter_speed.json"}
                ],
                "automated_tests": ["tests/test_validate_kit.py", "tests/test_toolkit.py"],
                "measurable_metrics": [
                    {"name": "code_reduction", "delta_summary": "Replaced 15 regex helpers with 1 AST visitor (-120 LOC)"}
                ]
            },
            "value_deltas": {
                "power": 1.2,
                "flexibility": 0.5,
                "automation": 1.0,
                "optimization": 1.5,
                "collaboration": 0.3
            },
            "cost_deltas": {
                "token_delta_percent": 0.0,
                "latency_delta_percent": -87.0,
                "structural_complexity_delta": -0.4,
                "human_attention_friction": 0.0,
                "regression_risk": 0.05
            }
        }

        res: UpgradeEvaluationResult = evaluate_proposal(proposal)
        self.assertTrue(res.hard_gate_passed, f"Hard gate failed with violations: {res.violations}")
        self.assertEqual(res.decision, "KEEP")
        self.assertGreater(res.net_gain, 0.5)

    def test_case_2_bad_upgrade_multi_model_consensus(self):
        """Case 2: Doraemon bloat + Approval Fatigue trap - 3 parallel LLMs with human popups."""
        proposal = {
            "proposal_id": "UPG-2026-002",
            "title": "Universal Multi-Model Consensus Engine with Human Step Approvals",
            "target_scope": "builder_core",
            "extraction_provenance": {
                "what_works": "Multi-agent consensus reduces hallucinations in critical code generation.",
                "why_it_works": "Ensemble voting aggregates diverse reasoning models.",
                "generalizable_principle": "Ensemble verification for high-risk branches.",
                "domain_specific_discarded": "Vendor-specific SDK bindings.",
                "adapted_architecture_plan": "Wrap all node executions with 3-model voting + mandatory human popup."
            },
            "evidence": {
                "benchmarks": [
                    {"metric_name": "reasoning_pass_rate", "baseline": 85, "after": 92, "source": "evals/reasoning.json"}
                ],
                "automated_tests": ["tests/test_consensus.py"],
                "measurable_metrics": [
                    {"name": "api_call_count", "delta_summary": "Calls 3 LLMs per workflow step"}
                ]
            },
            "value_deltas": {
                "power": 1.0,
                "flexibility": -0.2,
                "automation": -0.5,
                "optimization": -1.5,
                "collaboration": 0.0
            },
            "cost_deltas": {
                "token_delta_percent": 350.0,  # Blowout
                "latency_delta_percent": 600.0,  # Blowout
                "structural_complexity_delta": 1.4,  # Bloat
                "human_attention_friction": 2.0,  # Extreme fatigue
                "regression_risk": 0.4
            }
        }

        res: UpgradeEvaluationResult = evaluate_proposal(proposal)
        self.assertFalse(res.hard_gate_passed)
        self.assertEqual(res.decision, "REJECT")
        self.assertIn("APPROVAL_FATIGUE_TRAP", res.violations)
        self.assertIn("PERFORMANCE_BLOWOUT", res.violations)
        self.assertIn("DORAEMON_BLOAT_TRAP", res.violations)
        self.assertLess(res.net_gain, 0.0)

    def test_case_3_tradeoff_upgrade_rigid_prompt(self):
        """Case 3: Profitable trade-off - Sacrificing flexibility for massive automation gain."""
        proposal = {
            "proposal_id": "UPG-2026-003",
            "title": "Mandatory 4-Part Rigid Block Prompt Schema",
            "target_scope": "kit_architecture",
            "extraction_provenance": {
                "what_works": "Rigid structured blocks eliminate prompt parsing ambiguity.",
                "why_it_works": "Standardized sections allow automated deterministic linter parsing.",
                "generalizable_principle": "Enforce structural invariants to enable compile-time verification.",
                "domain_specific_discarded": "Freeform natural language variations.",
                "adapted_architecture_plan": "Update prompt-compiling and core-guardrails to enforce 4-part structure."
            },
            "evidence": {
                "benchmarks": [
                    {"metric_name": "prompt_drift_error_rate", "baseline": 18.5, "after": 0.0, "source": "evals/prompt_eval.json"}
                ],
                "automated_tests": ["tests/test_prompt_compiling.py", "tests/test_lifecycle_creation.py"],
                "measurable_metrics": [
                    {"name": "manual_debug_time", "delta_summary": "Reduced prompt debugging by 70%"}
                ]
            },
            "value_deltas": {
                "power": 0.8,
                "flexibility": -0.4,  # Intentionally sacrificed
                "automation": 1.5,   # Massive boost
                "optimization": 0.8,
                "collaboration": 0.5
            },
            "cost_deltas": {
                "token_delta_percent": -20.0,
                "latency_delta_percent": 0.0,
                "structural_complexity_delta": -0.2,
                "human_attention_friction": 0.0,
                "regression_risk": 0.1
            }
        }

        res: UpgradeEvaluationResult = evaluate_proposal(proposal)
        self.assertTrue(res.hard_gate_passed)
        self.assertIn(res.decision, ("KEEP", "ADAPT"))
        self.assertGreater(res.net_gain, 0.4)
        self.assertTrue(any("Flexibility" in t for t in res.trade_offs_identified))

    def test_case_4_goodhart_loc_attack(self):
        """Case 4: Goodhart Gaming - Claiming massive LOC reduction but 0 tests & high risk."""
        proposal = {
            "proposal_id": "UPG-2026-004",
            "title": "Aggressive One-Liner Golfing Refactor",
            "target_scope": "builder_core",
            "extraction_provenance": {
                "what_works": "Shorter code is easier to fit in context.",
                "why_it_works": "Context compression.",
                "generalizable_principle": "Code brevity.",
                "domain_specific_discarded": "None.",
                "adapted_architecture_plan": "Compress validation functions into nested list comprehensions."
            },
            "evidence": {
                "benchmarks": [],
                "automated_tests": [],  # 0 tests!
                "measurable_metrics": [
                    {"name": "loc_deleted", "delta_summary": "Deleted 500 lines of error checking"}
                ]
            },
            "value_deltas": {
                "power": 0.0,
                "flexibility": 0.0,
                "automation": 0.0,
                "optimization": 0.5,
                "collaboration": 0.0
            },
            "cost_deltas": {
                "token_delta_percent": 0.0,
                "latency_delta_percent": 0.0,
                "structural_complexity_delta": -1.0,  # Fake complexity benefit
                "human_attention_friction": 0.0,
                "regression_risk": 0.8  # Extreme risk
            }
        }

        res: UpgradeEvaluationResult = evaluate_proposal(proposal)
        self.assertFalse(res.hard_gate_passed)
        self.assertEqual(res.decision, "REJECT")
        self.assertIn("GOODHART_LOC_GAMING_TRAP", res.violations)

    def test_case_5_missing_evidence_attempt(self):
        """Case 5: Missing Evidence - Proposal has no tests, benchmarks or metrics."""
        proposal = {
            "proposal_id": "UPG-2026-005",
            "title": "Vague Optimistic Upgrade",
            "target_scope": "component",
            "extraction_provenance": {
                "what_works": "New feature works great in theoretical papers.",
                "why_it_works": "Because it uses advanced AI heuristics.",
                "generalizable_principle": "Advanced heuristics are better.",
                "domain_specific_discarded": "N/A",
                "adapted_architecture_plan": "Add heuristic helper to skills."
            },
            "evidence": {
                "benchmarks": [],
                "automated_tests": [],
                "measurable_metrics": []
            },
            "value_deltas": {
                "power": 1.0,
                "flexibility": 1.0,
                "automation": 1.0,
                "optimization": 1.0,
                "collaboration": 1.0
            },
            "cost_deltas": {
                "token_delta_percent": 0.0,
                "latency_delta_percent": 0.0,
                "structural_complexity_delta": 0.0,
                "human_attention_friction": 0.0,
                "regression_risk": 0.0
            }
        }

        res: UpgradeEvaluationResult = evaluate_proposal(proposal)
        self.assertFalse(res.hard_gate_passed)
        self.assertEqual(res.decision, "REJECT")
        self.assertIn("MISSING_EVIDENCE", res.violations)

    def test_case_6_blind_copy_rejection(self):
        """Case 6: Blind Copy Violation - Provenance fields empty or too short."""
        proposal = {
            "proposal_id": "UPG-2026-006",
            "title": "Copy pasted pattern from random repo",
            "target_scope": "component",
            "extraction_provenance": {
                "what_works": "idk",  # Too short (< 10)
                "why_it_works": "works",
                "generalizable_principle": "none",
                "domain_specific_discarded": "",
                "adapted_architecture_plan": "just copy"
            },
            "evidence": {
                "benchmarks": [{"metric_name": "speed", "baseline": 10, "after": 12, "source": "log"}],
                "automated_tests": ["test.py"],
                "measurable_metrics": []
            },
            "value_deltas": {
                "power": 0.5,
                "flexibility": 0.5,
                "automation": 0.5,
                "optimization": 0.5,
                "collaboration": 0.5
            },
            "cost_deltas": {
                "token_delta_percent": 0.0,
                "latency_delta_percent": 0.0,
                "structural_complexity_delta": 0.0,
                "human_attention_friction": 0.0,
                "regression_risk": 0.1
            }
        }

        res: UpgradeEvaluationResult = evaluate_proposal(proposal)
        self.assertFalse(res.hard_gate_passed)
        self.assertEqual(res.decision, "REJECT")
        self.assertIn("BLIND_COPY_VIOLATION", res.violations)


if __name__ == "__main__":
    unittest.main()
