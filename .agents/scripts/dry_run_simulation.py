#!/usr/bin/env python3
"""Compiler simulation tool for validating Graph Reachability, Cycle Detection, and Capability Coverage."""
from __future__ import annotations

import argparse
import json
import sys
from collections import deque
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
import fnmatch
import re


def matches_outcome(post_key: str, workflow_outcome: str) -> bool:
    """Flexible matching between capability postcondition key and workflow required outcome."""
    if not post_key or not workflow_outcome:
        return False
    if post_key == workflow_outcome:
        return True
    norm_post = re.sub(r"\{[a-zA-Z0-9_-]+\}", "*", post_key)
    norm_out = re.sub(r"\{[a-zA-Z0-9_-]+\}", "*", workflow_outcome)
    if fnmatch.fnmatch(workflow_outcome, norm_post) or fnmatch.fnmatch(post_key, norm_out):
        return True
    if post_key.startswith(workflow_outcome + ".") or workflow_outcome.startswith(post_key + "."):
        return True
    return False


def simulate_workflow_graph(root: Path) -> dict:
    """Run reachability, cycle detection, dead state detection, and capability coverage simulations."""
    unreachable_nodes: list[str] = []
    dead_states: list[str] = []
    uncovered_outcomes: list[str] = []
    cycles_detected: list[list[str]] = []
    all_workflows: dict[str, dict] = {}

    # 1. Gather all capability postconditions
    available_postconditions: set[str] = set()
    precondition_graph: dict[str, set[str]] = {}

    for agent_path in sorted((root / "agent").glob("*.md")):
        fm = extract_frontmatter(agent_path)
        if not fm:
            continue
        caps = fm.get("capabilities", [])
        if isinstance(caps, list):
            for cap in caps:
                if not isinstance(cap, dict):
                    continue
                cap_id = str(cap.get("id", "")).strip()
                precond_keys = set()
                preconds = cap.get("preconditions", {})
                if isinstance(preconds, dict):
                    for st in preconds.get("structural", []):
                        if isinstance(st, dict) and "key" in st:
                            precond_keys.add(str(st["key"]).strip())
                
                post_keys = set()
                for po in cap.get("postconditions", []):
                    if isinstance(po, dict) and "key" in po:
                        k = str(po["key"]).strip()
                        post_keys.add(k)
                        available_postconditions.add(k)

                for p_key in post_keys:
                    if p_key not in precondition_graph:
                        precondition_graph[p_key] = set()
                    precondition_graph[p_key].update(precond_keys)

    # Check for cycles in precondition graph (DFS cycle detection)
    visited: dict[str, int] = {}  # 0: unvisited, 1: visiting, 2: visited

    def find_cycle(node: str, path: list[str]) -> None:
        visited[node] = 1
        path.append(node)
        for neighbor in precondition_graph.get(node, []):
            if neighbor not in visited or visited[neighbor] == 0:
                find_cycle(neighbor, path)
            elif visited[neighbor] == 1:
                cycle_start = path.index(neighbor)
                cycles_detected.append(path[cycle_start:] + [neighbor])
        path.pop()
        visited[node] = 2

    for key in list(precondition_graph.keys()):
        if visited.get(key, 0) == 0:
            find_cycle(key, [])

    # 2. Analyze Workflows
    for workflow_path in sorted((root / "workflows").glob("*.md")):
        fm = extract_frontmatter(workflow_path)
        if not fm:
            continue
        wf_name = workflow_path.stem
        nodes = fm.get("nodes", {})
        if not isinstance(nodes, dict):
            continue

        initial_state = str(fm.get("initial_state", "")).strip()
        terminal_states = fm.get("terminal_states", [])
        if isinstance(terminal_states, str):
            terminal_states = [terminal_states]
        terminal_set = {str(t).strip() for t in terminal_states}

        # Build adjacency graph
        adj: dict[str, list[str]] = {}
        for node_name, node_data in nodes.items():
            adj[node_name] = []
            if isinstance(node_data, dict):
                # Check capability coverage
                outcome = str(node_data.get("required_outcome", "")).strip()
                is_human_gate = bool(node_data.get("human_gate", False))
                if outcome and not is_human_gate:
                    # Check flexible matching against all available postconditions
                    covered = any(matches_outcome(pk, outcome) for pk in available_postconditions)
                    if not covered:
                        uncovered_outcomes.append(outcome)

                transitions = node_data.get("transitions", [])
                if isinstance(transitions, list):
                    for trans in transitions:
                        if isinstance(trans, dict) and "to" in trans:
                            adj[node_name].append(str(trans["to"]).strip())

                # Check dead state (non-terminal state with 0 transitions)
                if node_name not in terminal_set and not adj[node_name]:
                    dead_states.append(f"{wf_name}:{node_name}")

        # Check reachability via BFS from initial_state
        reachable_set: set[str] = set()
        if initial_state and initial_state in nodes:
            queue = deque([initial_state])
            reachable_set.add(initial_state)
            while queue:
                curr = queue.popleft()
                for neighbor in adj.get(curr, []):
                    if neighbor not in reachable_set:
                        reachable_set.add(neighbor)
                        if neighbor in nodes:
                            queue.append(neighbor)
            
            for node_name in nodes.keys():
                if node_name not in reachable_set:
                    unreachable_nodes.append(f"{wf_name}:{node_name}")

        all_workflows[wf_name] = {
            "total_nodes": len(nodes),
            "reachable_nodes": len(reachable_set.intersection(nodes.keys())),
            "terminal_states": list(terminal_set),
        }

    passed = not (unreachable_nodes or dead_states or uncovered_outcomes or cycles_detected)
    return {
        "passed": passed,
        "unreachable_nodes": unreachable_nodes,
        "dead_states": dead_states,
        "uncovered_outcomes": uncovered_outcomes,
        "cycles_detected": cycles_detected,
        "workflows": all_workflows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Dry-run simulation for workflow reachability, cycles, and capability coverage")
    parser.add_argument("path", nargs="?", default=None, help="Root path of the kit (defaults to current dir)")
    parser.add_argument("--coverage", action="store_true", help="Print full coverage and simulation details")
    args = parser.parse_args()

    root = Path(args.path).resolve() if args.path else Path.cwd()
    report = simulate_workflow_graph(root)

    if args.coverage or not report["passed"]:
        print("=== DRY RUN SIMULATION REPORT ===")
        print(f"Status: {'[PASS]' if report['passed'] else '[FAIL]'}")
        if report["unreachable_nodes"]:
            print(f"- Unreachable nodes ({len(report['unreachable_nodes'])}): {', '.join(report['unreachable_nodes'])}")
        if report["dead_states"]:
            print(f"- Dead states ({len(report['dead_states'])}): {', '.join(report['dead_states'])}")
        if report["uncovered_outcomes"]:
            print(f"- Uncovered outcomes ({len(report['uncovered_outcomes'])}): {', '.join(report['uncovered_outcomes'])}")
        if report["cycles_detected"]:
            print(f"- Precondition cycles detected ({len(report['cycles_detected'])}): {report['cycles_detected']}")
        for wf, stats in report["workflows"].items():
            print(f"- Workflow '{wf}': {stats['reachable_nodes']}/{stats['total_nodes']} reachable nodes")
    else:
        print("[PASS] Workflow graph is fully reachable, cycle-free, and covered by capabilities.")

    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
