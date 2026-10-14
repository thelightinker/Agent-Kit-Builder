from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from kit_fixtures import GOOD_AGENT_BODY, GOOD_SKILL_DESC
from kit_lint import find_placeholders
from quality_baseline import score_kit

try:
    from render_frontmatter import (
        load_spec,
        render_agent_file,
        render_agent_frontmatter,
        validate_spec,
    )
except ImportError:
    render_agent_file = None

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
SPEC_MIN = FIXTURES_DIR / "kit_spec_min.json"
SCHEMA_FILE = Path(__file__).resolve().parents[2] / "schemas" / "component-frontmatter.schema.json"
RENDER_CLI = SCRIPTS_DIR / "render_frontmatter.py"

with open(SPEC_MIN, encoding="utf-8") as f:
    SPEC_DATA = json.load(f)

AGENT = SPEC_DATA["agents"][0]
BODY = """# Writer Agent
Chuyên gia soạn thảo tài liệu.

## Negative Boundaries & Scope
- Cấm sửa đổi ngoài scope.

## Definition of Done (DoD)
1. 100% tests pass.
"""


class TestRenderer(unittest.TestCase):
    def setUp(self):
        if render_agent_file is None:
            self.skipTest("render_frontmatter module not implemented yet")
        with open(SCHEMA_FILE, encoding="utf-8") as f:
            self.schema = json.load(f)

    def test_render_is_byte_identical_on_second_run(self):
        a = render_agent_file(AGENT, BODY)
        b = render_agent_file(AGENT, BODY)
        self.assertEqual(a, b)

    def test_rendered_file_parses_and_has_no_placeholders(self):
        text = render_agent_file(AGENT, BODY)
        fm_part = text.split("\n---\n", 1)[0].lstrip("-\n")
        fm = yaml.safe_load(fm_part)
        self.assertIsInstance(fm, dict)
        self.assertEqual(find_placeholders(text), [])

    def test_vietnamese_diacritics_survive(self):
        text = render_agent_file(AGENT, BODY)
        self.assertIn("viết", text.lower())
        self.assertNotIn("\\u", text)

    def test_missing_required_key_reports_path(self):
        spec = {"agents": [{k: v for k, v in AGENT.items() if k != "name"}]}
        errors = validate_spec(spec, self.schema)
        self.assertTrue(any("agents[0]: missing required key 'name'" in e for e in errors))

    def test_cli_exits_2_and_writes_nothing_on_invalid_spec(self):
        with tempfile.TemporaryDirectory() as t:
            out_dir = Path(t) / "agent"
            out_dir.mkdir()
            bad_spec = Path(t) / "bad_spec.json"
            bad_spec.write_text(json.dumps({"agents": [{"version": "1.0.0"}]}), encoding="utf-8")
            bodies_dir = Path(t) / "bodies"
            bodies_dir.mkdir()

            res = subprocess.run(
                [sys.executable, str(RENDER_CLI), str(bad_spec), "--bodies", str(bodies_dir), "--out", str(out_dir)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(res.returncode, 2)
            self.assertEqual(list(out_dir.iterdir()), [])

    def test_rendered_agent_passes_quality_baseline_machine_criteria(self):
        with tempfile.TemporaryDirectory() as t:
            kit_dir = Path(t)
            agent_dir = kit_dir / "agent"
            agent_dir.mkdir()
            rendered_text = render_agent_file(AGENT, BODY)
            (agent_dir / "writer.md").write_text(rendered_text, encoding="utf-8")

            # Add valid skill for agent
            skill_dir = kit_dir / "skills" / "doc-skill"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                f"---\nname: doc-skill\ndescription: \"{GOOD_SKILL_DESC}\"\nwhen_to_use: \"When drafting docs\"\n---\n# Doc Skill\n",
                encoding="utf-8",
            )

            scores = score_kit(kit_dir)
            self.assertTrue(scores.get("Q1_no_placeholders"), "Q1 must pass")
            self.assertTrue(scores.get("Q2_frontmatter_parses"), "Q2 must pass")


if __name__ == "__main__":
    unittest.main()
