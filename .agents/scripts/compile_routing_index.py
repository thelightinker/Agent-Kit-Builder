#!/usr/bin/env python3
"""Compiler module for generating routing_index.json from capability declarations."""
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

NAMESPACE_PATTERN = re.compile(r"^[a-z0-9_-]+\.[a-z0-9_-]+\.[a-z0-9_-]+$")


def validate_capability_namespace(cap_id: str) -> bool:
    """Validate that capability ID strictly follows domain.component.action format (CANON 9)."""
    return bool(NAMESPACE_PATTERN.match(str(cap_id).strip()))


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
    # Fallback simple parser
    data = {}
    for line in raw.splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"\'')
    return data


def canonical_json(data: object) -> str:
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def compile_routing_index(root: Path) -> dict:
    """Scan all agents and skills, extracting and normalizing capability declarations."""
    capabilities: dict[str, dict] = {}
    intent_map: dict[str, list[str]] = {}

    # Scan agents
    for agent_path in sorted((root / "agent").glob("*.md")):
        fm = extract_frontmatter(agent_path)
        if not fm:
            continue
        agent_name = str(fm.get("name", agent_path.stem))
        owned_skills = fm.get("skills", [])
        if isinstance(owned_skills, str):
            owned_skills = [s.strip() for s in owned_skills.strip("[]").split(",") if s.strip()]
        
        caps = fm.get("capabilities", [])
        if isinstance(caps, list):
            for cap in caps:
                if not isinstance(cap, dict):
                    continue
                cap_id = str(cap.get("id", "")).strip()
                if not cap_id:
                    continue
                if not validate_capability_namespace(cap_id):
                    raise ValueError(f"Capability '{cap_id}' in {agent_path.name} violates namespace format (CANON 9: domain.component.action)")
                
                normalized_cap = {
                    "id": cap_id,
                    "owner_agent": agent_name,
                    "owned_skills": owned_skills,
                    "intent_patterns": [str(p).strip() for p in cap.get("intent_patterns", []) if str(p).strip()],
                    "satisfies_outcomes": [str(o).strip() for o in cap.get("satisfies_outcomes", []) if str(o).strip()],
                    "preconditions": cap.get("preconditions", {"structural": [], "semantic": []}),
                    "postconditions": cap.get("postconditions", []),
                    "evidence_schema": cap.get("evidence_schema", {"structural": [], "semantic": []}),
                    "failure_policy": cap.get("failure_policy", {
                        "on_structural_failure": "retry(max=2) → escalate_human",
                        "on_semantic_rejection": "escalate_human",
                        "on_no_capability_match": "escalate_human",
                    }),
                    "checkpoint_resume_policy": cap.get("checkpoint_resume_policy", {
                        "checkpoint_supported": True,
                        "resume_condition": "checkpoint_valid",
                    }),
                    "negative_scope": cap.get("negative_scope", {
                        "cannot_modify": [],
                        "cannot_trigger_state_transition": [],
                    }),
                    "tags": [str(t).strip() for t in cap.get("tags", []) if str(t).strip()],
                }
                capabilities[cap_id] = normalized_cap

                for pattern in normalized_cap["intent_patterns"]:
                    pattern_key = pattern.lower().strip()
                    if pattern_key not in intent_map:
                        intent_map[pattern_key] = []
                    if cap_id not in intent_map[pattern_key]:
                        intent_map[pattern_key].append(cap_id)

    # Scan skills (if skill declares standalone capabilities)
    for skill_path in sorted((root / "skills").glob("*/SKILL.md")):
        fm = extract_frontmatter(skill_path)
        if not fm:
            continue
        skill_name = skill_path.parent.name
        caps = fm.get("capabilities", [])
        if isinstance(caps, list):
            for cap in caps:
                if not isinstance(cap, dict):
                    continue
                cap_id = str(cap.get("id", "")).strip()
                if not cap_id:
                    continue
                if not validate_capability_namespace(cap_id):
                    raise ValueError(f"Capability '{cap_id}' in skill {skill_name} violates namespace format (CANON 9)")
                if cap_id not in capabilities:
                    capabilities[cap_id] = {
                        "id": cap_id,
                        "owner_agent": "autonomous_router",
                        "owned_skills": [skill_name],
                        "intent_patterns": [str(p).strip() for p in cap.get("intent_patterns", []) if str(p).strip()],
                        "preconditions": cap.get("preconditions", {"structural": [], "semantic": []}),
                        "postconditions": cap.get("postconditions", []),
                        "evidence_schema": cap.get("evidence_schema", {"structural": [], "semantic": []}),
                        "failure_policy": cap.get("failure_policy", {}),
                        "checkpoint_resume_policy": cap.get("checkpoint_resume_policy", {}),
                        "negative_scope": cap.get("negative_scope", {}),
                    }
                    for pattern in capabilities[cap_id]["intent_patterns"]:
                        pattern_key = pattern.lower().strip()
                        if pattern_key not in intent_map:
                            intent_map[pattern_key] = []
                        if cap_id not in intent_map[pattern_key]:
                            intent_map[pattern_key].append(cap_id)

    manifest_version = "1.0.0"
    version_file = root / "VERSION"
    if version_file.is_file():
        manifest_version = version_file.read_text(encoding="utf-8").strip()

    return {
        "version": manifest_version,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "capabilities": capabilities,
        "intent_map": intent_map,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile capability declarations into routing_index.json")
    parser.add_argument("path", nargs="?", default=None, help="Root path of the kit (defaults to current dir)")
    parser.add_argument("--check", action="store_true", help="Check if routing_index.json is up-to-date without writing")
    args = parser.parse_args()

    root = Path(args.path).resolve() if args.path else Path.cwd()
    try:
        compiled = compile_routing_index(root)
    except Exception as exc:
        print(f"[ERROR] Compilation failed: {exc}", file=sys.stderr)
        return 1

    target_file = root / "routing_index.json"
    expected_text = canonical_json(compiled)

    if args.check:
        if not target_file.is_file():
            print("[ERROR] routing_index.json is missing. Run without --check to generate.", file=sys.stderr)
            return 1
        current_text = target_file.read_text(encoding="utf-8")
        if current_text != expected_text:
            print("[ERROR] routing_index.json is stale. Run without --check to regenerate.", file=sys.stderr)
            return 1
        print("[PASS] routing_index.json is up-to-date.")
        return 0

    target_file.write_text(expected_text, encoding="utf-8")
    cap_count = len(compiled['capabilities'])
    agent_count = len(list((root / "agent").glob("*.md"))) if (root / "agent").is_dir() else 0
    if agent_count > 0 and cap_count == 0:
        print(f"[WARN] Compiled 0 capabilities but found {agent_count} agent(s). "
              f"Routing will be blind. Populate 'capabilities:' in agent frontmatter.", file=sys.stderr)
    print(f"[OK] Compiled {cap_count} capabilities into {target_file.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
