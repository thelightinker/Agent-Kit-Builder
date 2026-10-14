#!/usr/bin/env python3
"""Readset Report Utility.

Calculates context footprint (in raw bytes) for each generation mode defined in readsets.json.
Modes: micro, standard, mini_suite, full_suite.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def readset_bytes(root: Path, mode: str) -> int:
    """Calculate total size in bytes of all files associated with a given mode in readsets.json."""
    readsets_file = root / "readsets.json"
    if not readsets_file.is_file():
        raise FileNotFoundError(f"Missing readsets.json at {readsets_file}")

    with readsets_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if mode not in data:
        raise KeyError(f"Unknown mode '{mode}'. Available modes: {list(data.keys())}")

    files = data[mode]
    total_bytes = 0
    for rel_path in files:
        p = root / rel_path
        if not p.is_file():
            raise FileNotFoundError(f"File listed in readset does not exist: {p}")
        total_bytes += p.stat().st_size

    return total_bytes


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    if len(sys.argv) > 1:
        root = Path(sys.argv[1]).resolve()

    readsets_file = root / "readsets.json"
    if not readsets_file.is_file():
        print(f"Error: {readsets_file} not found", file=sys.stderr)
        return 1

    with readsets_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    for mode in data:
        size = readset_bytes(root, mode)
        print(f"{mode}\t{size}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
