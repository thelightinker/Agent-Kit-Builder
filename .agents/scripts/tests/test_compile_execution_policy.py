#!/usr/bin/env python3
"""Tests for compile_execution_policy.py."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = TESTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from compile_execution_policy import compile_execution_policy


class TestCompileExecutionPolicy(unittest.TestCase):
    """Verify execution policy compiler against different kit topologies."""

    def _make_kit(self, tmp: Path, agents: list[dict], workflows: list[dict] = None):
        """Helper to create a minimal kit structure with agent/workflow frontmatter."""
        (tmp / "agent").mkdir(exist_ok=True)
        (tmp / "workflows").mkdir(exist_ok=True)
        (tmp / "skills").mkdir(exist_ok=True)
        (tmp / "VERSION").write_text("1.0.0", encoding="utf-8")
        for i, ag in enumerate(agents):
            lines = ["---"]
            for k, v in ag.items():
                if isinstance(v, list):
                    lines.append(f"{k}: [{', '.join(v)}]")
                else:
                    lines.append(f"{k}: {v}")
            lines.append("---")
            lines.append(f"\n# Agent {i}")
            (tmp / "agent" / f"agent_{i}.md").write_text("\n".join(lines), encoding="utf-8")
        for i, wf in enumerate(workflows or []):
            lines = ["---"]
            for k, v in wf.items():
                lines.append(f"{k}: {v}")
            lines.append("---")
            lines.append(f"\n# Workflow {i}")
            (tmp / "workflows" / f"wf_{i}.md").write_text("\n".join(lines), encoding="utf-8")

    def test_single_agent_produces_direct_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self._make_kit(tmp_path, [{"name": "solo-agent", "description": "test", "version": "1.0.0"}])
            result = compile_execution_policy(tmp_path)
            self.assertEqual(result["mode"], "direct")
            self.assertEqual(result["complexity_ceiling"], "L1_ROUTED")
            self.assertFalse(result["parallel"]["writes"])
            self.assertIn("repair", result["recovery"])
            self.assertEqual(result["context"], "artifact_reference")

    def test_multi_agent_with_delegates_produces_stage_machine(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self._make_kit(tmp_path, [
                {"name": "orchestrator", "description": "test", "version": "1.0.0",
                 "delegates_to": ["spec-a", "spec-b"]},
                {"name": "spec-a", "description": "test", "version": "1.0.0"},
                {"name": "spec-b", "description": "test", "version": "1.0.0"},
            ])
            result = compile_execution_policy(tmp_path)
            self.assertIn(result["mode"], ("stage_machine", "fork_join"))
            self.assertIn(result["complexity_ceiling"], ("L2_STAGED", "L3_FORK_JOIN"))
            self.assertTrue(result["parallel"]["reads"])
            self.assertFalse(result["parallel"]["writes"])

    def test_retry_max_bounded(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self._make_kit(tmp_path, [{"name": "solo", "description": "test", "version": "1.0.0"}])
            result = compile_execution_policy(tmp_path)
            self.assertLessEqual(result["retry"]["max_attempts"], 3)
            self.assertGreaterEqual(result["retry"]["same_error_limit"], 1)

    def test_recovery_cascade_max_3(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self._make_kit(tmp_path, [{"name": "solo", "description": "test", "version": "1.0.0"}])
            result = compile_execution_policy(tmp_path)
            self.assertLessEqual(len(result["recovery"]), 3)

    def test_schema_version_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self._make_kit(tmp_path, [{"name": "solo", "description": "test", "version": "1.0.0"}])
            result = compile_execution_policy(tmp_path)
            self.assertEqual(result["schemaVersion"], "1.0.0")
            self.assertIn("generated_at", result)

    def test_strict_jsonschema_conformance(self):
        """Ensure all compiler outputs strictly validate against execution-policy.schema.json."""
        import jsonschema
        schema_path = SCRIPTS_DIR.parent / "schemas" / "execution-policy.schema.json"
        self.assertTrue(schema_path.is_file(), f"Schema not found: {schema_path}")
        schema = json.loads(schema_path.read_text(encoding="utf-8"))

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            # Test direct mode
            self._make_kit(tmp_path, [{"name": "solo", "description": "test", "version": "1.0.0"}])
            res_direct = compile_execution_policy(tmp_path)
            jsonschema.validate(instance=res_direct, schema=schema)  # Raises if invalid

            # Test staged mode
            self._make_kit(tmp_path, [
                {"name": "lead", "description": "test", "version": "1.0.0", "delegates_to": ["worker"]},
                {"name": "worker", "description": "test", "version": "1.0.0"},
            ])
            res_staged = compile_execution_policy(tmp_path)
            jsonschema.validate(instance=res_staged, schema=schema)

    def test_compiler_roundtrip_and_dynamic_adaptation(self):
        """Ensure compiler adapts idempotently without SSOT drift."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            # Step 1: 1 agent -> direct
            self._make_kit(tmp_path, [{"name": "writer", "description": "test", "version": "1.0.0"}])
            policy_1 = compile_execution_policy(tmp_path)
            self.assertEqual(policy_1["mode"], "direct")
            self.assertFalse(policy_1["parallel"]["reads"])

            # Step 2: Add specialist with delegation -> stage_machine
            (tmp_path / "agent" / "editor.md").write_text(
                "---\nname: editor\ndescription: test\nversion: 1.0.0\n---\n# Editor", encoding="utf-8"
            )
            (tmp_path / "agent" / "writer.md").write_text(
                "---\nname: writer\ndescription: test\nversion: 1.0.0\ndelegates_to: [editor]\n---\n# Writer Lead", encoding="utf-8"
            )
            policy_2 = compile_execution_policy(tmp_path)
            self.assertEqual(policy_2["mode"], "stage_machine")
            self.assertTrue(policy_2["parallel"]["reads"])
            self.assertFalse(policy_2["parallel"]["writes"])

            # Step 3: Revert to 1 agent -> reverts cleanly to direct
            (tmp_path / "agent" / "agent_0.md").unlink(missing_ok=True)
            (tmp_path / "agent" / "editor.md").unlink(missing_ok=True)
            (tmp_path / "agent" / "writer.md").write_text(
                "---\nname: writer\ndescription: test\nversion: 1.0.0\n---\n# Writer Solo", encoding="utf-8"
            )
            policy_3 = compile_execution_policy(tmp_path)
            self.assertEqual(policy_3["mode"], "direct")
            self.assertFalse(policy_3["parallel"]["reads"])


if __name__ == "__main__":
    unittest.main()
