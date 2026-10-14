"""Tests for Antigravity Doctor Hooks Diagnostic Phase.

CLI Contract & Usage:
- Command: `node .agents/templates/antigravity-doctor.mjs --root <dir> [--json] [--strict]`
- Exit codes: 0 (passed), 1 (failed with errors), 2 (runtime/argument crash)
- Findings output format (JSON): { "findings": [ { "phase": "hooks", "severity": "error"|"warning", "code": "...", "file": "...", "message": "..." } ] }
- Known hook finding codes:
  - `hooks.missing`: warning when kit has no agents, error when kit has agent/*.md
  - `hooks.invalid_json`: error when hooks.json is not valid JSON
  - `hooks.invalid_entry`: error when a top-level hook entry is not an object
  - `hooks.enabled`: error when an entry has an invalid non-boolean 'enabled' field
"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

DOCTOR_MJS = Path(__file__).resolve().parents[2] / "templates" / "antigravity-doctor.mjs"


def run_doctor(kit_root: Path) -> dict:
    proc = subprocess.run(
        ["node", str(DOCTOR_MJS), "--root", str(kit_root), "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as err:
        raise RuntimeError(f"Doctor failed to produce JSON output (exit {proc.returncode}):\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}") from err


@unittest.skipUnless(shutil.which("node"), "node required")
class TestAntigravityDoctorHooks(unittest.TestCase):
    def test_valid_official_schema_has_no_hooks_error(self):
        with tempfile.TemporaryDirectory() as t:
            kit = Path(t)
            agents_dir = kit / ".agents"
            agents_dir.mkdir()
            hooks_file = agents_dir / "hooks.json"
            hooks_file.write_text(
                json.dumps({
                    "agent-kit-safety-gate": {
                        "event": "PreToolUse",
                        "matcher": "run_command|write_to_file",
                        "handler": {
                            "type": "command",
                            "command": "node .agents/hooks/validate-tool-call.mjs",
                            "timeout": 10,
                        },
                    }
                }),
                encoding="utf-8",
            )
            report = run_doctor(kit)
            hook_errors = [
                f for f in report.get("findings", [])
                if f.get("phase") == "hooks" and f.get("severity") == "error"
            ]
            self.assertEqual(hook_errors, [])

    def test_non_object_hook_entry_is_error(self):
        with tempfile.TemporaryDirectory() as t:
            kit = Path(t)
            agents_dir = kit / ".agents"
            agents_dir.mkdir()
            hooks_file = agents_dir / "hooks.json"
            hooks_file.write_text(
                json.dumps({
                    "my-hook": "not_an_object"
                }),
                encoding="utf-8",
            )
            report = run_doctor(kit)
            hook_errors = [
                f for f in report.get("findings", [])
                if f.get("phase") == "hooks" and f.get("code") == "hooks.invalid_entry"
            ]
            self.assertTrue(len(hook_errors) > 0, "Expected hooks.invalid_entry error finding")

    def test_missing_hooks_json_is_error_for_kit_with_agents(self):
        with tempfile.TemporaryDirectory() as t:
            kit = Path(t)
            agent_dir = kit / "agent"
            agent_dir.mkdir()
            (agent_dir / "writer.md").write_text(
                "---\nname: writer\ndescription: writes docs\n---\n# Writer\n",
                encoding="utf-8",
            )
            report = run_doctor(kit)
            missing_errors = [
                f for f in report.get("findings", [])
                if f.get("phase") == "hooks" and f.get("code") == "hooks.missing" and f.get("severity") == "error"
            ]
            self.assertTrue(
                len(missing_errors) > 0,
                "Expected hooks.missing with severity 'error' when agent/*.md exists",
            )


if __name__ == "__main__":
    unittest.main()
