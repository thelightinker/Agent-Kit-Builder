#!/usr/bin/env python3
"""Compiler module for generating execution_policy.json from kit topology and agent declarations."""
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
            val = v.strip().strip("\"'")
            # Parse simple list syntax: [a, b, c]
            if val.startswith("[") and val.endswith("]"):
                val = [x.strip() for x in val[1:-1].split(",") if x.strip()]
            data[k.strip()] = val
    return data


def canonical_json(data: object) -> str:
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def compile_execution_policy(root: Path) -> dict:
    """Analyze kit topology and compile orchestration intent into execution_policy.json."""
    agents: list[dict] = []
    has_orchestrator = False
    has_delegates = False
    total_agents = 0

    # Scan agents
    agent_dir = root / "agent"
    if agent_dir.is_dir():
        for agent_path in sorted(agent_dir.glob("*.md")):
            fm = extract_frontmatter(agent_path)
            if not fm:
                continue
            total_agents += 1
            agents.append(fm)
            delegates = fm.get("delegates_to", [])
            if isinstance(delegates, str):
                delegates = [d.strip() for d in delegates.strip("[]").split(",") if d.strip()]
            if delegates:
                has_orchestrator = True
                has_delegates = True

    # Determine mode based on topology
    if total_agents <= 1:
        mode = "direct"
        complexity_ceiling = "L1_ROUTED"
        parallel_reads = False
    elif has_orchestrator and has_delegates:
        mode = "stage_machine"
        complexity_ceiling = "L3_FORK_JOIN"
        parallel_reads = True
    else:
        mode = "stage_machine"
        complexity_ceiling = "L2_STAGED"
        parallel_reads = True

    # Determine context strategy
    context = "artifact_reference"

    # Determine recovery cascade based on complexity
    if mode == "direct":
        recovery = ["repair"]
    else:
        recovery = ["repair", "reroute", "replan"]

    # Determine retry limits
    retry_max = 2 if mode != "direct" else 1
    same_error_limit = 1

    return {
        "schemaVersion": "1.0.0",
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "mode": mode,
        "complexity_ceiling": complexity_ceiling,
        "parallel": {
            "reads": parallel_reads,
            "writes": False,
        },
        "retry": {
            "max_attempts": retry_max,
            "same_error_limit": same_error_limit,
        },
        "recovery": recovery,
        "context": context,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile orchestration intent into execution_policy.json")
    parser.add_argument("path", nargs="?", default=None, help="Root path of the kit (defaults to current dir)")
    parser.add_argument("--check", action="store_true", help="Check if execution_policy.json is up-to-date without writing")
    args = parser.parse_args()

    root = Path(args.path).resolve() if args.path else Path.cwd()
    try:
        compiled = compile_execution_policy(root)
    except Exception as exc:
        print(f"[ERROR] Compilation failed: {exc}", file=sys.stderr)
        return 1

    target_file = root / "execution_policy.json"
    expected_text = canonical_json(compiled)

    if args.check:
        if not target_file.is_file():
            print("[ERROR] execution_policy.json is missing. Run without --check to generate.", file=sys.stderr)
            return 1
        current_text = target_file.read_text(encoding="utf-8")
        # Compare ignoring generated_at timestamp
        current_data = json.loads(current_text)
        expected_data = json.loads(expected_text)
        current_data.pop("generated_at", None)
        expected_data.pop("generated_at", None)
        if current_data != expected_data:
            print("[ERROR] execution_policy.json is stale. Run without --check to regenerate.", file=sys.stderr)
            return 1
        print("[PASS] execution_policy.json is up-to-date.")
        return 0

    target_file.write_text(expected_text, encoding="utf-8")
    print(f"[OK] Compiled execution policy (mode={compiled['mode']}) into {target_file.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
