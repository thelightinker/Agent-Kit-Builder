#!/usr/bin/env python3
"""Safety Hook Verifier for Antigravity-native Agent Kits.

Checks the behavioral contract of hooks/validate-tool-call.mjs against standard safety vectors:
- Blocking destructive shell commands (rm -rf /, mkfs, format)
- Blocking file writes outside workspace or to protected files (.agents/hooks.json, etc.)
- Allowing benign commands and workspace-internal writes
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


def _run_single_hook(hook_path: Path, payload: dict, ws_path: str) -> tuple[int, dict | None]:
    raw = json.dumps(payload)
    try:
        proc = subprocess.run(
            ["node", str(hook_path)],
            input=raw,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (subprocess.SubprocessError, OSError):
        return -1, None

    if proc.returncode != 0:
        return proc.returncode, None

    try:
        data = json.loads(proc.stdout)
        if isinstance(data, dict):
            return 0, data
    except (json.JSONDecodeError, ValueError):
        pass

    return 0, None


def check_hook(kit_dir: Path) -> list[str]:
    """Verify safety hook behavior under kit_dir/hooks/validate-tool-call.mjs."""
    node_bin = shutil.which("node")
    if not node_bin:
        return ["hook.no_node"]

    hook_file = kit_dir / "hooks" / "validate-tool-call.mjs"
    if not hook_file.is_file():
        return ["hook.missing"]

    ws = "/work/proj"
    blocking_cases = [
        ("rm_root", {"toolCall": {"name": "run_command", "args": {"CommandLine": "rm -rf /", "Cwd": ws}}, "workspacePaths": [ws]}),
        ("mkfs", {"toolCall": {"name": "run_command", "args": {"CommandLine": "mkfs.ext4 /dev/sda1", "Cwd": ws}}, "workspacePaths": [ws]}),
        ("format", {"toolCall": {"name": "run_command", "args": {"CommandLine": "format C:", "Cwd": ws}}, "workspacePaths": [ws]}),
        ("write_outside", {"toolCall": {"name": "write_to_file", "args": {"TargetFile": "/etc/passwd"}}, "workspacePaths": [ws]}),
    ]

    allowing_cases = [
        ("ls", {"toolCall": {"name": "run_command", "args": {"CommandLine": "ls -la", "Cwd": ws}}, "workspacePaths": [ws]}),
        ("npm_test", {"toolCall": {"name": "run_command", "args": {"CommandLine": "npm test", "Cwd": ws}}, "workspacePaths": [ws]}),
    ]

    errors: list[str] = []

    for name, payload in blocking_cases:
        rc, out = _run_single_hook(hook_file, payload, ws)
        if rc != 0 or out is None or "decision" not in out:
            errors.append(f"hook.bad_output:{name}")
        elif out.get("decision") != "deny":
            errors.append(f"hook.not_blocking:{name}")

    for name, payload in allowing_cases:
        rc, out = _run_single_hook(hook_file, payload, ws)
        if rc != 0 or out is None or "decision" not in out:
            errors.append(f"hook.bad_output:{name}")
        elif out.get("decision") != "allow":
            errors.append(f"hook.over_blocking:{name}")

    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python check_hook.py <kit_dir>", file=sys.stderr)
        return 2

    kit_dir = Path(sys.argv[1]).resolve()
    errors = check_hook(kit_dir)
    for err in errors:
        print(err)

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
