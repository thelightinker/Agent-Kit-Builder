import os
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

from kit_lint import strip_code_fences, find_placeholders
from quality_baseline import score_kit, CRITERIA

try:
    from kit_fixtures import GOOD_AGENT_BODY, GOOD_SKILL_DESC, make_kit
except ImportError:
    from tests.kit_fixtures import GOOD_AGENT_BODY, GOOD_SKILL_DESC, make_kit



class TestKitLint(unittest.TestCase):
    def test_finds_uppercase_placeholder_with_line(self):
        self.assertEqual(find_placeholders("a\nx {SKILL_NAME} y"), [(2, "{SKILL_NAME}")])

    def test_ignores_placeholder_inside_code_fence(self):
        self.assertEqual(find_placeholders("```\n{SKILL_NAME}\n```\n"), [])

    def test_ignores_lowercase_and_json_braces(self):
        self.assertEqual(find_placeholders('{"a": 1} {name}'), [])


class TestScoreKit(unittest.TestCase):
    def test_clean_kit_passes_all_machine_criteria(self):
        with tempfile.TemporaryDirectory() as t:
            s = score_kit(make_kit(Path(t)))
        machine = {k: v for k, v in s.items() if not k.startswith("M")}
        self.assertTrue(all(v is True for v in machine.values()), machine)
        self.assertIsNone(s["M7_answers_brief"])
        self.assertIsNone(s["M8_no_toolkit_vocabulary"])

    def test_placeholder_in_body_fails_q1(self):
        with tempfile.TemporaryDirectory() as t:
            s = score_kit(make_kit(Path(t), agent_body=GOOD_AGENT_BODY + "\n{DOMAIN_NAME}\n"))
        self.assertFalse(s["Q1_no_placeholders"])

    def test_broken_yaml_fails_q2_and_does_not_raise(self):
        with tempfile.TemporaryDirectory() as t:
            kit = make_kit(Path(t))
            (kit / "agent" / "demo.md").write_text("---\nname: [unclosed\n---\n# x\n", "utf-8")
            self.assertFalse(score_kit(kit)["Q2_frontmatter_parses"])

    def test_missing_skill_ref_fails_q3(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertFalse(score_kit(make_kit(Path(t), skill_ref="ghost-skill"))["Q3_skill_refs_resolve"])

    def test_short_skill_description_fails_q6(self):
        with tempfile.TemporaryDirectory() as t:
            self.assertFalse(score_kit(make_kit(Path(t), skill_description="short"))["Q6_skill_trigger_present"])


if __name__ == "__main__":
    unittest.main()
