#!/usr/bin/env python3
"""Deterministic Frontmatter Renderer for AG Kit Agents.

Generates agent markdown files by combining structured JSON specifications
(kit_spec.json) with markdown body files, rendering pure YAML frontmatter
without template placeholder risks.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


def load_spec(path: Path) -> dict:
    """Load JSON kit spec file."""
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_spec(spec: dict, schema: dict) -> list[str]:
    """Validate kit_spec against required frontmatter schema rules."""
    errors: list[str] = []
    if not isinstance(spec, dict):
        return ["spec: root must be an object"]

    agents = spec.get("agents")
    if not isinstance(agents, list):
        return ["spec: missing or invalid 'agents' array"]

    required_keys = schema.get("required", ["name", "version"])

    for i, agent in enumerate(agents):
        if not isinstance(agent, dict):
            errors.append(f"agents[{i}]: agent must be an object")
            continue
        for req in required_keys:
            if req not in agent:
                errors.append(f"agents[{i}]: missing required key '{req}'")

    return errors


def render_agent_frontmatter(agent: dict) -> str:
    """Render YAML frontmatter string enclosed in --- blocks with preserve ordering and Unicode."""
    if yaml is None:
        raise RuntimeError("PyYAML is required for frontmatter rendering.")

    cleaned = {k: v for k, v in agent.items() if k != "body_file"}
    dumped = yaml.safe_dump(cleaned, sort_keys=False, allow_unicode=True)
    return f"---\n{dumped.rstrip()}\n---"


def render_agent_file(agent: dict, body: str) -> str:
    """Combine rendered frontmatter with agent body text."""
    fm = render_agent_frontmatter(agent)
    clean_body = body.lstrip("\r\n")
    if not clean_body.endswith("\n"):
        clean_body += "\n"
    return f"{fm}\n{clean_body}"


def main() -> int:
    if yaml is None:
        print("Error: PyYAML is not installed.", file=sys.stderr)
        return 3

    parser = argparse.ArgumentParser(description="Render agent frontmatter from kit_spec.json")
    parser.add_argument("spec", help="Path to kit_spec.json")
    parser.add_argument("--bodies", required=True, help="Directory containing agent body markdown files")
    parser.add_argument("--out", required=True, help="Output directory for generated agent files (<kit>/agent)")
    parser.add_argument("--schema", default=None, help="Optional path to component-frontmatter.schema.json")
    args = parser.parse_args()

    spec_path = Path(args.spec).resolve()
    if not spec_path.is_file():
        print(f"Error: Spec file not found: {spec_path}", file=sys.stderr)
        return 2

    try:
        spec = load_spec(spec_path)
    except Exception as e:
        print(f"Error reading spec file: {e}", file=sys.stderr)
        return 2

    # Load schema
    if args.schema:
        schema_path = Path(args.schema).resolve()
    else:
        schema_path = Path(__file__).resolve().parents[1] / "schemas" / "component-frontmatter.schema.json"

    schema = {}
    if schema_path.is_file():
        try:
            with schema_path.open("r", encoding="utf-8") as f:
                schema = json.load(f)
        except Exception:
            schema = {"required": ["name", "version"]}
    else:
        schema = {"required": ["name", "version"]}

    errors = validate_spec(spec, schema)
    if errors:
        for err in errors:
            print(f"Spec validation error: {err}", file=sys.stderr)
        return 2

    bodies_dir = Path(args.bodies).resolve()
    out_dir = Path(args.out).resolve()

    # Pre-check all body files exist before writing anything
    renders: list[tuple[Path, str]] = []
    for agent in spec.get("agents", []):
        name = agent.get("name")
        body_file = agent.get("body_file")
        body_path = None
        if body_file:
            candidates = [
                bodies_dir / body_file,
                bodies_dir / Path(body_file).name,
                bodies_dir.parent / body_file,
            ]
            for cand in candidates:
                if cand.is_file():
                    body_path = cand
                    break
        if body_path is None:
            cand = bodies_dir / f"{name}.md"
            if cand.is_file():
                body_path = cand

        if body_path is None or not body_path.is_file():
            print(f"Error: Body file not found for agent '{name}': {body_file or f'{name}.md'}", file=sys.stderr)
            return 2

        try:
            body_text = body_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Error reading body file {body_path}: {e}", file=sys.stderr)
            return 2

        file_content = render_agent_file(agent, body_text)
        target_path = out_dir / f"{name}.md"
        renders.append((target_path, file_content))

    # All checks passed: write rendered files
    out_dir.mkdir(parents=True, exist_ok=True)
    for target_path, content in renders:
        target_path.write_text(content, encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
