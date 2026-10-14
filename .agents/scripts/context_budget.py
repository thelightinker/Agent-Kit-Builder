#!/usr/bin/env python3
"""Context budget enforcement module for always-on rules and orchestrator prompts.

Ensures always-on context stays strictly within budget:
- RULES_BUDGET_BYTES: 8,192 bytes
- ORCHESTRATOR_BUDGET_BYTES: 10,240 bytes
"""
from __future__ import annotations

import os
from pathlib import Path

RULES_BUDGET_BYTES = 8192
ORCHESTRATOR_BUDGET_BYTES = 10240

P0_INVARIANTS: tuple[str, ...] = (
    "Workspace Isolation",
    "Topology & Node-Contract Reconciliation",
    "Verification Feasibility",
    "Sequential Context Isolation",
    "Legacy Intake & Tri-Bucket Scope",
    "Executable Script Smoke Test",
    "Targeted Grounding",
    "Worker Briefing",
    "Verification Abstraction",
    "Universal Filesystem & Workspace Contract",
)


def _load_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    raw = text[4:end]
    try:
        import yaml
        data = yaml.safe_load(raw)
        return data if isinstance(data, dict) else {}
    except Exception:
        pass
    data = {}
    for line in raw.splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"\'')
    return data


def measure(root: Path) -> dict:
    """Measure total always-on rules bytes and orchestrator bytes."""
    rules_bytes = 0
    always_on_files: list[str] = []

    rules_dir = root / "rules"
    if rules_dir.is_dir():
        for r_path in sorted(rules_dir.glob("*.md")):
            fm = _load_frontmatter(r_path)
            if fm.get("trigger") == "always_on":
                rules_bytes += r_path.stat().st_size
                always_on_files.append(str(r_path.relative_to(root)).replace("\\", "/"))

    orchestrator_bytes = 0
    agent_dir = root / "agent"
    if agent_dir.is_dir():
        for a_path in sorted(agent_dir.glob("*.md")):
            fm = _load_frontmatter(a_path)
            if fm.get("routing_exempt") is True:
                orchestrator_bytes += a_path.stat().st_size
                always_on_files.append(str(a_path.relative_to(root)).replace("\\", "/"))

    return {
        "rules_bytes": rules_bytes,
        "orchestrator_bytes": orchestrator_bytes,
        "files": always_on_files,
    }
