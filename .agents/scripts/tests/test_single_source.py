from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = TESTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from support import TOOLKIT, REPO_ROOT, copy_toolkit
try:
    import render_docs
except ImportError:
    render_docs = None


class TestSingleSource(unittest.TestCase):
    def setUp(self):
        self._tmp_obj = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp_obj.name)

    def tearDown(self):
        self._tmp_obj.cleanup()

    def test_generation_is_idempotent_and_lf_only(self):
        self.assertIsNotNone(render_docs, "render_docs module must exist")
        kit = copy_toolkit(self.tmp)
        (kit.parent / "README.md").write_bytes((REPO_ROOT / "README.md").read_bytes().replace(b"\n", b"\r\n"))
        render_docs.apply_generated_blocks(kit)
        self.assertEqual([], render_docs.apply_generated_blocks(kit, check=True))
        self.assertNotIn(b"\r\n", (kit / "ARCHITECTURE.md").read_bytes())

    def test_one_version_value_in_readme_and_architecture(self):
        version = (TOOLKIT / "VERSION").read_text("utf-8").strip()
        for p in (REPO_ROOT / "README.md", TOOLKIT / "ARCHITECTURE.md"):
            matches = set(re.findall(r"2026\.\d+\.\d+", p.read_text("utf-8")))
            self.assertEqual({version}, matches, f"Mismatch in {p.name}")

    def test_orchestrator_modes_are_a_subset_of_dynamic_routing_and_there_are_ten(self):
        routing = set(re.findall(r"`([A-Z_]+_TRACK)`", (TOOLKIT / "rules/dynamic-routing.md").read_text("utf-8")))
        orch = set(re.findall(r"`([A-Z_]+_TRACK)`", (TOOLKIT / "agent/kit-architect.md").read_text("utf-8")))
        self.assertEqual(10, len(routing))
        self.assertLessEqual(orch, routing)

    def test_legacy_vocab_only_in_allowlisted_files_and_allowlist_has_no_stale_entries(self):
        allowlist_path = TESTS_DIR / "legacy_vocab_allowlist.txt"
        self.assertTrue(allowlist_path.is_file(), "legacy_vocab_allowlist.txt must exist")
        allow = set(allowlist_path.read_text("utf-8").split())
        pattern = re.compile(r"\bTier [123]\b|SUITE_BUILD")
        holders = {p.relative_to(TOOLKIT).as_posix() for p in TOOLKIT.rglob("*.md") if pattern.search(p.read_text("utf-8"))}
        self.assertEqual(set(), holders - allow)
        self.assertEqual(set(), allow - holders)

    def test_failure_modes_title_has_no_stale_version(self):
        first_line = (TOOLKIT / "references/failure-modes.md").read_text("utf-8").splitlines()[0]
        self.assertNotIn("v3.0", first_line)


if __name__ == "__main__":
    unittest.main()
