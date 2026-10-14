import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
TESTS_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = TESTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))


def scan_for_names(root: Path, names: list[str]) -> dict[str, list[str]]:
    results: dict[str, list[str]] = {}
    ignored_parts = {".git", ".pytest_cache", "__pycache__", "memory", "skill-creator", ".superpowers", "up", "docs"}
    ignored_files = {
        "CHANGELOG.md",
        "manifest.lock.json",
        "DEPENDENCY_GRAPH.md",
        "test_removed_features.py",
        "preexisting_failures.txt",
        "EXPERIMENTAL.txt",
        "legacy_vocab_allowlist.txt",
    }


    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in p.parts for part in ignored_parts):
            continue
        if p.name in ignored_files:
            continue
        if p.suffix not in (".py", ".md", ".json", ".mjs", ".yml", ".yaml", ".txt", ".sh", ".html"):
            continue
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for name in names:
            if name in content:
                rel = str(p.relative_to(root)).replace("\\", "/")
                results.setdefault(name, []).append(rel)
    return results


EVOLUTION_NAMES = [
    "evolution_engine",
    "evolution_orchestrator",
    "evolution_ledger",
    "upgrade_gate_evaluator",
    "equip_evolution",
    "evolve-kit",
    "architecture-evolution",
    "architecture-mapping",
    "UPGRADE_PRINCIPLES",
    "upgrade_proposal",
    "snapshot-manifest",
    "evolution-ledger",
]


class TestEvolutionRemoved(unittest.TestCase):
    def test_no_references_to_removed_evolution_names(self):
        self.assertEqual(scan_for_names(REPO_ROOT, EVOLUTION_NAMES), {})


if __name__ == "__main__":
    unittest.main()
