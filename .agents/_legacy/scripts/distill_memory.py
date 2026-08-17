#!/usr/bin/env python3
"""
Automated Memory Distillation Engine for Agent Kit Creator.
Appends distilled lessons learned, design patterns, or golden examples
directly into persistent memory topic files (.agents/memory/).
"""

import sys
import os
import argparse
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def distill_memory(memory_type, title, content, target_file=None, memory_dir=None):
    if memory_dir is None:
        memory_dir = Path(__file__).resolve().parents[1] / "memory"
    else:
        memory_dir = Path(memory_dir)

    if not memory_dir.exists():
        memory_dir.mkdir(parents=True, exist_ok=True)

    if target_file is None:
        if memory_type == "example":
            target_file = memory_dir / "golden-examples" / "README.md"
        elif memory_type == "lesson":
            target_file = memory_dir / "feedback-history.md"
        else:
            target_file = memory_dir / "kit-patterns.md"
    else:
        target_file = Path(target_file)

    target_file.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry_lines = [
        f"\n### [{timestamp}] {title}",
        f"- **Type**: `{memory_type}`",
        f"- **Distilled At**: {timestamp}",
        "\n" + content.strip() + "\n"
    ]

    new_entry = "\n".join(entry_lines)

    if target_file.exists():
        text = target_file.read_text(encoding="utf-8")
        target_file.write_text(text + "\n" + new_entry, encoding="utf-8")
    else:
        header = f"# Memory Topic: {target_file.stem}\n"
        target_file.write_text(header + "\n" + new_entry, encoding="utf-8")

    print(f"[+] Distilled memory entry '{title}' saved to: {target_file}")
    return str(target_file)

def main():
    parser = argparse.ArgumentParser(description="Distill lessons and patterns into persistent memory")
    parser.add_argument("--type", choices=["pattern", "example", "lesson"], default="pattern", help="Memory entry type")
    parser.add_argument("--title", required=True, help="Title of the distilled memory entry")
    parser.add_argument("--content", required=True, help="Content text of the memory entry")
    parser.add_argument("--target-file", help="Optional explicit path to target memory file")
    parser.add_argument("--memory-dir", help="Path to .agents/memory directory")

    args = parser.parse_args()
    distill_memory(args.type, args.title, args.content, args.target_file, args.memory_dir)

if __name__ == "__main__":
    main()
