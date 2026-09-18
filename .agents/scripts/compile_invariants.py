#!/usr/bin/env python3
"""Compiler module for generating invariant_rules.json from Workflow and Agent declarations."""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


def extract_frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    raw = text[4:end]
    if yaml is not None:
        try:
            data = yaml.safe_load(raw)
            return data if isinstance(data, dict) else None
        except Exception:
            return None
    data = {}
    for line in raw.splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"\'')
    return data


def canonical_json(data: object) -> str:
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def compile_invariants(root: Path) -> dict:
    """Extract global invariants from workflows and negative scopes from agents."""
    global_invariants: list[dict] = []
    negative_boundaries: dict[str, dict] = {}

    # 1. Workflows
    for workflow_path in sorted((root / "workflows").glob("*.md")):
        fm = extract_frontmatter(workflow_path)
        if not fm:
            continue
        invariants = fm.get("global_invariants", [])
        if isinstance(invariants, list):
            for inv in invariants:
                if isinstance(inv, dict):
                    global_invariants.append({
                        "id": str(inv.get("id", "")).strip(),
                        "description": str(inv.get("description", "")).strip(),
                        "check": str(inv.get("check", "")).strip(),
                        "source_workflow": workflow_path.stem,
                    })

    # 2. Agents
    for agent_path in sorted((root / "agent").glob("*.md")):
        fm = extract_frontmatter(agent_path)
        if not fm:
            continue
        agent_name = str(fm.get("name", agent_path.stem))
        neg_scope = fm.get("negative_scope", {})
        if isinstance(neg_scope, dict):
            cannot_modify = neg_scope.get("cannot_modify", [])
            cannot_transition = neg_scope.get("cannot_trigger_state_transition", [])
            negative_boundaries[agent_name] = {
                "cannot_modify": [str(x).strip() for x in cannot_modify if str(x).strip()],
                "cannot_trigger_state_transition": [str(x).strip() for x in cannot_transition if str(x).strip()],
            }

    version_str = "1.0.0"
    v_file = root / "VERSION"
    if v_file.is_file():
        version_str = v_file.read_text(encoding="utf-8").strip()

    return {
        "version": version_str,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "global_invariants": global_invariants,
        "negative_boundaries": negative_boundaries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile invariant rules from workflows and agents")
    parser.add_argument("path", nargs="?", default=None, help="Root path of the kit (defaults to current dir)")
    parser.add_argument("--check", action="store_true", help="Check if invariant_rules.json is up-to-date without writing")
    args = parser.parse_args()

    root = Path(args.path).resolve() if args.path else Path.cwd()
    try:
        compiled = compile_invariants(root)
    except Exception as exc:
        print(f"[ERROR] Compilation failed: {exc}", file=sys.stderr)
        return 1

    target_file = root / "invariant_rules.json"
    expected_text = canonical_json(compiled)

    if args.check:
        if not target_file.is_file():
            print("[ERROR] invariant_rules.json is missing.", file=sys.stderr)
            return 1
        current_text = target_file.read_text(encoding="utf-8")
        if current_text != expected_text:
            print("[ERROR] invariant_rules.json is stale.", file=sys.stderr)
            return 1
        print("[PASS] invariant_rules.json is up-to-date.")
        return 0

    target_file.write_text(expected_text, encoding="utf-8")
    print(f"[OK] Compiled {len(compiled['global_invariants'])} invariants into {target_file.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
