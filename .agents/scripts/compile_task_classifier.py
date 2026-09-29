#!/usr/bin/env python3
"""Compiler module for generating task_classifier_index.json to classify tasks into workflow-bound vs ad-hoc."""
from __future__ import annotations

import argparse
import datetime
import json
import re
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


import fnmatch


def matches_outcome(post_key: str, workflow_outcome: str) -> bool:
    """Flexible matching between capability postcondition key and workflow required outcome."""
    if not post_key or not workflow_outcome:
        return False
    if post_key == workflow_outcome:
        return True
    # Support wildcard / parameterized matching (e.g. chapter_draft.{id} -> chapter_draft.*)
    norm_post = re.sub(r"\{[a-zA-Z0-9_-]+\}", "*", post_key)
    norm_out = re.sub(r"\{[a-zA-Z0-9_-]+\}", "*", workflow_outcome)
    if fnmatch.fnmatch(workflow_outcome, norm_post) or fnmatch.fnmatch(post_key, norm_out):
        return True
    # Support namespace / prefix matching (e.g. chapter_draft.ch1 matches chapter_draft)
    if post_key.startswith(workflow_outcome + ".") or workflow_outcome.startswith(post_key + "."):
        return True
    return False


def compile_task_classifier(root: Path) -> dict:
    """Classify capability intents into workflow-bound (satisfying required outcomes) vs ad-hoc."""
    workflow_outcomes: set[str] = set()
    workflow_nodes_map: dict[str, list[str]] = {}

    # 1. Collect workflow required outcomes
    for workflow_path in sorted((root / "workflows").glob("*.md")):
        fm = extract_frontmatter(workflow_path)
        if not fm:
            continue
        nodes = fm.get("nodes", {})
        if isinstance(nodes, dict):
            for node_name, node_data in nodes.items():
                if isinstance(node_data, dict):
                    outcome = str(node_data.get("required_outcome", "")).strip()
                    if outcome:
                        workflow_outcomes.add(outcome)
                        if outcome not in workflow_nodes_map:
                            workflow_nodes_map[outcome] = []
                        workflow_nodes_map[outcome].append(f"{workflow_path.stem}:{node_name}")

    workflow_bound_intents: dict[str, dict] = {}
    ad_hoc_intents: dict[str, dict] = {}

    # 2. Match capability postconditions against workflow outcomes
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
                intents = [str(p).strip().lower() for p in cap.get("intent_patterns", []) if str(p).strip()]
                post_keys = {str(post.get("key", "")).strip() for post in cap.get("postconditions", []) if isinstance(post, dict)}
                
                # Check flexible matching with workflow outcomes
                explicit_satisfies = set(cap.get("satisfies_outcomes", []))
                matched_outcomes = set()
                for wf_out in workflow_outcomes:
                    if wf_out in explicit_satisfies:
                        matched_outcomes.add(wf_out)
                    elif any(matches_outcome(pk, wf_out) for pk in post_keys):
                        matched_outcomes.add(wf_out)
                
                if matched_outcomes:
                    for intent in intents:
                        workflow_bound_intents[intent] = {
                            "capability_id": cap_id,
                            "workflow_outcomes": sorted(matched_outcomes),
                            "target_nodes": sorted([node for out in matched_outcomes for node in workflow_nodes_map.get(out, [])]),
                        }
                else:
                    for intent in intents:
                        ad_hoc_intents[intent] = {
                            "capability_id": cap_id,
                            "postcondition_keys": sorted(post_keys),
                        }

    version_str = "1.0.0"
    v_file = root / "VERSION"
    if v_file.is_file():
        version_str = v_file.read_text(encoding="utf-8").strip()

    return {
        "version": version_str,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "workflow_bound_intents": workflow_bound_intents,
        "ad_hoc_intents": ad_hoc_intents,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile task classifier index")
    parser.add_argument("path", nargs="?", default=None, help="Root path of the kit (defaults to current dir)")
    parser.add_argument("--check", action="store_true", help="Check if task_classifier_index.json is up-to-date without writing")
    args = parser.parse_args()

    root = Path(args.path).resolve() if args.path else Path.cwd()
    try:
        compiled = compile_task_classifier(root)
    except Exception as exc:
        print(f"[ERROR] Compilation failed: {exc}", file=sys.stderr)
        return 1

    target_file = root / "task_classifier_index.json"
    expected_text = canonical_json(compiled)

    if args.check:
        if not target_file.is_file():
            print("[ERROR] task_classifier_index.json is missing.", file=sys.stderr)
            return 1
        current_text = target_file.read_text(encoding="utf-8")
        if current_text != expected_text:
            print("[ERROR] task_classifier_index.json is stale.", file=sys.stderr)
            return 1
        print("[PASS] task_classifier_index.json is up-to-date.")
        return 0

    target_file.write_text(expected_text, encoding="utf-8")
    print(f"[OK] Compiled task classifier ({len(compiled['workflow_bound_intents'])} workflow, {len(compiled['ad_hoc_intents'])} ad-hoc) into {target_file.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
