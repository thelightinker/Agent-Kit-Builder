from __future__ import annotations

import argparse
import sys
from pathlib import Path

REQUIRED_FILES: tuple[str, ...] = (
    "skills/skill-creator/SKILL.md",
    "templates/workflow-template.md",
    "templates/orchestrator-template.md",
    "templates/agent-template.md",
    "templates/skill-template.md",
    "templates/rule-template.md",
    "templates/memory-template.md",
    "templates/manifest-template.json",
    "templates/design-spec-template.md",
)


def check_preflight(root: Path) -> list[str]:
    """Check that all required files and templates exist under root."""
    missing: list[str] = []
    for rel in REQUIRED_FILES:
        target = root / rel
        if not target.is_file():
            missing.append(rel)
    return missing


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Preflight check for Agent Kit Builder prerequisites.")
    parser.add_argument("path", nargs="?", default=".agents", help="Path to toolkit root (default: .agents)")
    args = parser.parse_args(argv)

    root = Path(args.path).resolve()
    if not root.exists():
        # Maybe current directory itself is the toolkit
        if (root / "manifest.json").exists():
            pass
        elif (Path.cwd() / ".agents").exists():
            root = Path.cwd() / ".agents"

    missing = check_preflight(root)
    if missing:
        print("[-] Preflight Check FAILED! Missing required files:")
        for item in missing:
            print(f"  - {item}")
        return 1

    print("[+] Preflight Check PASSED: All required templates and vendored skills present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
