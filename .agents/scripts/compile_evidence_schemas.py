#!/usr/bin/env python3
"""Compiler module for aggregating evidence schemas across all capabilities."""
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


def compile_evidence_schemas(root: Path) -> dict:
    """Scan all agents and skills and aggregate capability evidence schemas."""
    schemas: dict[str, dict] = {}

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
                if not cap_id:
                    continue
                evidence = cap.get("evidence_schema", {"structural": [], "semantic": []})
                if isinstance(evidence, dict):
                    schemas[cap_id] = {
                        "structural": evidence.get("structural", []),
                        "semantic": evidence.get("semantic", []),
                    }

    version_str = "1.0.0"
    v_file = root / "VERSION"
    if v_file.is_file():
        version_str = v_file.read_text(encoding="utf-8").strip()

    return {
        "version": version_str,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "schemas": schemas,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile capability evidence validation schemas")
    parser.add_argument("path", nargs="?", default=None, help="Root path of the kit (defaults to current dir)")
    parser.add_argument("--check", action="store_true", help="Check if evidence_schemas.json is up-to-date without writing")
    args = parser.parse_args()

    root = Path(args.path).resolve() if args.path else Path.cwd()
    try:
        compiled = compile_evidence_schemas(root)
    except Exception as exc:
        print(f"[ERROR] Compilation failed: {exc}", file=sys.stderr)
        return 1

    target_file = root / "evidence_schemas.json"
    expected_text = canonical_json(compiled)

    if args.check:
        if not target_file.is_file():
            print("[ERROR] evidence_schemas.json is missing.", file=sys.stderr)
            return 1
        current_text = target_file.read_text(encoding="utf-8")
        if current_text != expected_text:
            print("[ERROR] evidence_schemas.json is stale.", file=sys.stderr)
            return 1
        print("[PASS] evidence_schemas.json is up-to-date.")
        return 0

    target_file.write_text(expected_text, encoding="utf-8")
    print(f"[OK] Compiled evidence schemas for {len(compiled['schemas'])} capabilities into {target_file.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
