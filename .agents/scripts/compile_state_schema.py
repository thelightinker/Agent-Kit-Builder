#!/usr/bin/env python3
"""Compiler module for generating state_schema.json from component and workflow contracts."""
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


def compile_state_schema(root: Path) -> dict:
    """Scan all pre/postconditions and workflow nodes to generate state_schema.json."""
    state_keys: dict[str, dict] = {}
    verdict_keys: dict[str, dict] = {}

    # 1. Scan Workflows
    for workflow_path in sorted((root / "workflows").glob("*.md")):
        fm = extract_frontmatter(workflow_path)
        if not fm:
            continue
        nodes = fm.get("nodes", {})
        if isinstance(nodes, dict):
            for node_name, node_data in nodes.items():
                if isinstance(node_data, dict):
                    outcome_key = str(node_data.get("required_outcome", "")).strip()
                    if outcome_key:
                        if outcome_key not in state_keys:
                            state_keys[outcome_key] = {
                                "type": "boolean",
                                "description": f"Outcome state for node {node_name}",
                                "written_by": [],
                                "read_by": [f"workflow:{workflow_path.stem}"],
                            }
                        else:
                            if f"workflow:{workflow_path.stem}" not in state_keys[outcome_key]["read_by"]:
                                state_keys[outcome_key]["read_by"].append(f"workflow:{workflow_path.stem}")

    # 2. Scan Agents
    for agent_path in sorted((root / "agent").glob("*.md")):
        fm = extract_frontmatter(agent_path)
        if not fm:
            continue
        agent_name = str(fm.get("name", agent_path.stem))
        caps = fm.get("capabilities", [])
        if isinstance(caps, list):
            for cap in caps:
                if not isinstance(cap, dict):
                    continue
                # Preconditions
                preconds = cap.get("preconditions", {})
                if isinstance(preconds, dict):
                    for struct in preconds.get("structural", []):
                        if isinstance(struct, dict) and "key" in struct:
                            k = str(struct["key"]).strip()
                            if k not in state_keys:
                                state_keys[k] = {
                                    "type": "any",
                                    "description": f"Precondition key read by {agent_name}",
                                    "written_by": [],
                                    "read_by": [agent_name],
                                }
                            elif agent_name not in state_keys[k]["read_by"]:
                                state_keys[k]["read_by"].append(agent_name)
                    
                    for sem in preconds.get("semantic", []):
                        if isinstance(sem, dict) and "name" in sem:
                            v_name = str(sem["name"]).strip()
                            evaluator = str(sem.get("evaluator", "judge")).strip()
                            verdict_keys[v_name] = {
                                "evaluator": evaluator,
                                "tracks_content": f"content.{v_name}",
                            }

                # Postconditions
                for post in cap.get("postconditions", []):
                    if isinstance(post, dict) and "key" in post:
                        k = str(post["key"]).strip()
                        if k not in state_keys:
                            state_keys[k] = {
                                "type": "any",
                                "description": f"Postcondition state written by {agent_name}",
                                "written_by": [agent_name],
                                "read_by": [],
                            }
                        elif agent_name not in state_keys[k]["written_by"]:
                            state_keys[k]["written_by"].append(agent_name)

    version_str = "1.0.0"
    v_file = root / "VERSION"
    if v_file.is_file():
        version_str = v_file.read_text(encoding="utf-8").strip()

    return {
        "version": version_str,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "state_keys": state_keys,
        "verdict_keys": verdict_keys,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile state schema from workflow and capability contracts")
    parser.add_argument("path", nargs="?", default=None, help="Root path of the kit (defaults to current dir)")
    parser.add_argument("--check", action="store_true", help="Check if state_schema.json is up-to-date without writing")
    args = parser.parse_args()

    root = Path(args.path).resolve() if args.path else Path.cwd()
    try:
        compiled = compile_state_schema(root)
    except Exception as exc:
        print(f"[ERROR] Compilation failed: {exc}", file=sys.stderr)
        return 1

    target_file = root / "state_schema.json"
    expected_text = canonical_json(compiled)

    if args.check:
        if not target_file.is_file():
            print("[ERROR] state_schema.json is missing.", file=sys.stderr)
            return 1
        current_text = target_file.read_text(encoding="utf-8")
        if current_text != expected_text:
            print("[ERROR] state_schema.json is stale.", file=sys.stderr)
            return 1
        print("[PASS] state_schema.json is up-to-date.")
        return 0

    target_file.write_text(expected_text, encoding="utf-8")
    print(f"[OK] Compiled {len(compiled['state_keys'])} state keys into {target_file.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
