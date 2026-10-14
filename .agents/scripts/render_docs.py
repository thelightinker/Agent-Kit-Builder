#!/usr/bin/env python3
"""Single Source of Truth (SSOT) renderer for documentation blocks.

Generates and synchronizes dynamic blocks in Markdown documentation:
- <!-- GENERATED:version -->...<!-- /GENERATED:version -->
- <!-- GENERATED:inventory -->...<!-- /GENERATED:inventory -->
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def resolve_roots(root: Path) -> tuple[Path, Path]:
    root = root.resolve()
    if (root / "VERSION").is_file() and root.name == ".agents":
        toolkit = root
        repo_root = root.parent
    elif (root / ".agents" / "VERSION").is_file():
        toolkit = root / ".agents"
        repo_root = root
    elif (root / "VERSION").is_file():
        toolkit = root
        repo_root = root.parent
    else:
        toolkit = root
        repo_root = root.parent
    return toolkit, repo_root


def render_version(root: Path) -> str:
    toolkit, _ = resolve_roots(root)
    version_file = toolkit / "VERSION"
    if not version_file.is_file():
        raise FileNotFoundError(f"VERSION file not found in {toolkit}")
    return version_file.read_text("utf-8").strip()


def render_inventory(root: Path) -> str:
    toolkit, _ = resolve_roots(root)
    agents_count = len(list((toolkit / "agent").glob("*.md")))
    skills_count = len(list((toolkit / "skills").glob("*/SKILL.md")))
    workflows_count = len(list((toolkit / "workflows").glob("*.md")))
    skill_scripts_count = len(list((toolkit / "skills").glob("*/scripts/*.py")))
    rules_count = len(list((toolkit / "rules").glob("*.md")))

    lines = [
        "| Metric | Value |",
        "| --- | --- |",
        f"| **Total Agents** | {agents_count} |",
        f"| **Total Skills** | {skills_count} |",
        f"| **Total Workflows** | {workflows_count} |",
        f"| **Total Skill Scripts** | {skill_scripts_count} |",
        f"| **Total Rules** | {rules_count} |",
        "| **Top-level Utilities** | 14 user-facing + 2 internal engine modules |",
        "| **Coverage** | Domain analysis, prompt compilation, skill architecture, context compression, visual design intelligence, assembly, 3-layer verification, export, evolution, closed-loop convergence, unified lifecycle |",
        "| **Token Efficiency** | Always-on rules <= 3KB (giảm >=75% context overhead) |",
    ]
    return "\n".join(lines)


def apply_generated_blocks(root: Path, check: bool = False) -> list[str]:
    toolkit, repo_root = resolve_roots(root)

    # Candidate files to scan
    candidate_files: set[Path] = set()
    if (repo_root / "README.md").is_file():
        candidate_files.add(repo_root / "README.md")
    if (toolkit / "ARCHITECTURE.md").is_file():
        candidate_files.add(toolkit / "ARCHITECTURE.md")

    # Also scan any other markdown files under toolkit containing generated markers
    for md_path in toolkit.rglob("*.md"):
        try:
            sample = md_path.read_text("utf-8", errors="ignore")
            if "<!-- GENERATED:" in sample:
                candidate_files.add(md_path)
        except Exception:
            pass

    # Filter to files that actually contain generated markers
    active_files: list[Path] = []
    for f in sorted(candidate_files):
        try:
            content = f.read_bytes()
            if b"<!-- GENERATED:" in content:
                active_files.append(f)
        except Exception:
            pass

    if not active_files:
        return []

    version_file = toolkit / "VERSION"
    version = version_file.read_text("utf-8").strip() if version_file.is_file() else ""
    inventory = render_inventory(toolkit)

    ver_re = re.compile(r"<!-- GENERATED:version -->.*?<!-- /GENERATED:version -->", re.DOTALL)
    inv_re = re.compile(r"<!-- GENERATED:inventory -->.*?<!-- /GENERATED:inventory -->", re.DOTALL)

    modified: list[str] = []

    for file_path in active_files:
        original_bytes = file_path.read_bytes()
        text = original_bytes.decode("utf-8", errors="replace")

        new_text = ver_re.sub(f"<!-- GENERATED:version -->{version}<!-- /GENERATED:version -->", text)
        new_text = inv_re.sub(f"<!-- GENERATED:inventory -->\n{inventory}\n<!-- /GENERATED:inventory -->", new_text)

        # Normalize line endings to LF only
        new_text = new_text.replace("\r\n", "\n")
        new_bytes = new_text.encode("utf-8")

        if new_bytes != original_bytes:
            rel_name = file_path.name
            try:
                rel_name = str(file_path.relative_to(repo_root))
            except ValueError:
                rel_name = file_path.name
            modified.append(rel_name)
            if not check:
                file_path.write_bytes(new_bytes)

    return modified


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render generated documentation blocks")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent, help="Toolkit root path (.agents)")
    parser.add_argument("--check", action="store_true", help="Exit 1 if any generated block is stale")
    args = parser.parse_args(argv)

    modified = apply_generated_blocks(args.root, check=args.check)
    if args.check:
        if modified:
            print(f"[ERROR] Stale documentation blocks found in {len(modified)} file(s):")
            for m in modified:
                print(f"  - {m}")
            print("Run 'python .agents/scripts/render_docs.py' to update them.")
            return 1
        print("[PASS] All generated documentation blocks are up to date.")
        return 0

    if modified:
        print(f"[OK] Updated generated blocks in {len(modified)} file(s):")
        for m in modified:
            print(f"  - {m}")
    else:
        print("[OK] All generated blocks already up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
