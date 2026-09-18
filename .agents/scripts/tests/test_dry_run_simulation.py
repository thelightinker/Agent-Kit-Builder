#!/usr/bin/env python3
import unittest
import tempfile
import shutil
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dry_run_simulation import simulate_workflow_graph

class TestDryRunSimulation(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.workflows_dir = self.temp_dir / "workflows"
        self.agents_dir = self.temp_dir / "agent"
        self.workflows_dir.mkdir(parents=True)
        self.agents_dir.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_valid_reachable_graph_with_coverage(self):
        (self.workflows_dir / "book.md").write_text(
            """---
name: book
initial_state: GENESIS
terminal_states: [PUBLISHED]
nodes:
  GENESIS:
    required_outcome: profile_done
    transitions:
      - to: PUBLISHED
        when: profile_done == true
---
# Book Workflow
""",
            encoding="utf-8",
        )
        (self.agents_dir / "planner.md").write_text(
            """---
name: planner
capabilities:
  - id: writing.genesis.profile
    postconditions:
      - key: profile_done
        value: true
---
# Planner Agent
""",
            encoding="utf-8",
        )
        report = simulate_workflow_graph(self.temp_dir)
        self.assertTrue(report["passed"])
        self.assertEqual(len(report["unreachable_nodes"]), 0)
        self.assertEqual(len(report["uncovered_outcomes"]), 0)
        self.assertEqual(len(report["dead_states"]), 0)

    def test_unreachable_node_detected(self):
        (self.workflows_dir / "book.md").write_text(
            """---
name: book
initial_state: GENESIS
terminal_states: [PUBLISHED]
nodes:
  GENESIS:
    required_outcome: profile_done
    transitions:
      - to: PUBLISHED
        when: profile_done == true
  ORPHAN_NODE:
    required_outcome: orphan_done
    transitions:
      - to: PUBLISHED
        when: orphan_done == true
---
# Book Workflow
""",
            encoding="utf-8",
        )
        report = simulate_workflow_graph(self.temp_dir)
        self.assertFalse(report["passed"])
        self.assertIn("book:ORPHAN_NODE", report["unreachable_nodes"])

    def test_uncovered_outcome_detected(self):
        (self.workflows_dir / "book.md").write_text(
            """---
name: book
initial_state: GENESIS
terminal_states: [PUBLISHED]
nodes:
  GENESIS:
    required_outcome: profile_done
    transitions:
      - to: PUBLISHED
        when: profile_done == true
---
# Book Workflow
""",
            encoding="utf-8",
        )
        report = simulate_workflow_graph(self.temp_dir)
        self.assertFalse(report["passed"])
        self.assertIn("profile_done", report["uncovered_outcomes"])

if __name__ == "__main__":
    unittest.main()
