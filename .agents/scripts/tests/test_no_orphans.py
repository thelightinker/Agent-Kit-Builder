from __future__ import annotations

import unittest
from pathlib import Path

AGENTS_ROOT = Path(__file__).resolve().parents[2]

IGNORED_SCAN_FILES = {
    "manifest.json",
    "manifest.lock.json",
    "DEPENDENCY_GRAPH.md",
}

TEXT_EXTENSIONS = {".md", ".py", ".json", ".mjs", ".txt", ".yaml", ".yml"}


def find_orphans(agents_root: Path) -> list[str]:
    """Find files in templates/ and references/ whose basename is not referenced in any other file under agents_root."""
    candidates: list[Path] = []
    for sub in ("templates", "references"):
        sub_dir = agents_root / sub
        if sub_dir.is_dir():
            for p in sub_dir.iterdir():
                if p.is_file():
                    candidates.append(p)

    search_files: list[tuple[str, str]] = []
    for p in agents_root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(agents_root).as_posix()
        if p.name in IGNORED_SCAN_FILES:
            continue
        if p.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        if rel.startswith("scripts/tests/"):
            continue
        try:
            content = p.read_text(encoding="utf-8")
            search_files.append((rel, content))
        except (UnicodeDecodeError, OSError):
            continue

    orphans: list[str] = []
    for cand in candidates:
        cand_rel = cand.relative_to(agents_root).as_posix()
        cand_name = cand.name
        is_referenced = False
        for search_rel, content in search_files:
            if search_rel == cand_rel:
                continue
            if cand_name in content:
                is_referenced = True
                break
        if not is_referenced:
            orphans.append(cand_rel)

    return sorted(orphans)


class TestNoOrphans(unittest.TestCase):
    def test_every_template_and_reference_is_referenced(self):
        orphans = find_orphans(AGENTS_ROOT)
        self.assertEqual(orphans, [])


if __name__ == "__main__":
    unittest.main()
