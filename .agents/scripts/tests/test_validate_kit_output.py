from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from kit_fixtures import GOOD_AGENT_BODY, make_kit
from validate_kit import validate, validate_compiler_artifacts


class TestValidateKitOutput(unittest.TestCase):
    def test_invalid_yaml_in_agent_does_not_crash_compiler_validation(self):
        with tempfile.TemporaryDirectory() as t:
            kit = make_kit(Path(t))
            (kit / "agent" / "demo.md").write_text("---\nname: {A}.{B}\n---\n# x\n", encoding="utf-8")
            findings: list = []
            validate_compiler_artifacts(kit, findings)  # không ném lỗi

    def test_placeholder_reported_with_real_line(self):
        with tempfile.TemporaryDirectory() as t:
            kit = make_kit(Path(t), agent_body=GOOD_AGENT_BODY + "\n{DOMAIN_NAME}\n")
            f = [x for x in validate(kit, auto_heal=False, kit_output=True) if x.code == "placeholder.unfilled"]
            self.assertTrue(f)
            self.assertEqual(f[0].severity, "error")
            self.assertGreater(f[0].line, 1)

    def test_placeholder_rule_off_by_default(self):
        with tempfile.TemporaryDirectory() as t:
            kit = make_kit(Path(t), agent_body=GOOD_AGENT_BODY + "\n{DOMAIN_NAME}\n")
            self.assertFalse([x for x in validate(kit, auto_heal=False) if x.code == "placeholder.unfilled"])

    def test_placeholder_in_code_fence_not_reported(self):
        with tempfile.TemporaryDirectory() as t:
            kit = make_kit(Path(t), agent_body=GOOD_AGENT_BODY + "\n```\n{DOMAIN_NAME}\n```\n")
            self.assertFalse([x for x in validate(kit, auto_heal=False, kit_output=True) if x.code == "placeholder.unfilled"])


if __name__ == "__main__":
    unittest.main()
