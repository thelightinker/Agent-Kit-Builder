# .agents/scripts/tests/test_routing_validation.py
"""Tests for routing validation invariants (P0).

Validates 3 new lint rules:
- routing.empty_capabilities: Kit with ≥1 agent but 0 capabilities → error
- routing.orchestrator_missing_routing_table: Orchestrator with delegates_to but no routing table → error
- routing.agent_missing_skill_matrix: Agent with skills but no Skill Invocation Matrix → error
"""
import tempfile
import unittest
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate_kit import Finding, validate_compiler_artifacts


def _make_kit(root: Path) -> None:
    """Create minimal kit directory structure."""
    for d in ("agent", "skills", "workflows", "rules", "memory", "templates", "references", "schemas", "scripts"):
        (root / d).mkdir(parents=True, exist_ok=True)


def _write_agent(root: Path, name: str, frontmatter: str, body: str = "") -> None:
    """Write an agent .md file."""
    (root / "agent" / f"{name}.md").write_text(
        f"---\n{frontmatter}\n---\n\n# Agent: {name}\n\n{body}\n",
        encoding="utf-8",
    )


def _write_skill(root: Path, name: str) -> None:
    """Write a minimal valid skill."""
    skill_dir = root / "skills" / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f'---\nname: {name}\ndescription: "Test skill for {name}"\n'
        f'when_to_use: "When testing {name}"\nallowed-tools: Read\nversion: 1.0.0\n---\n\n'
        f"# {name}\n\n## Example\nInput: test\nOutput: result\n",
        encoding="utf-8",
    )


class TestRoutingEmptyCapabilities(unittest.TestCase):
    """routing.empty_capabilities: Kit with ≥1 agent but 0 capabilities must error."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        _make_kit(self.root)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_agent_without_capabilities_errors(self):
        _write_agent(
            self.root, "test-agent",
            'name: test-agent\ndescription: "Test agent"\ntools: Read\nmodel: inherit\nskills: [test-skill]\nversion: 1.0.0',
        )
        _write_skill(self.root, "test-skill")

        findings: list[Finding] = []
        validate_compiler_artifacts(self.root, findings)
        codes = [f.code for f in findings]
        self.assertIn("routing.empty_capabilities", codes,
                       f"Expected routing.empty_capabilities, got: {codes}")

    def test_agent_with_capabilities_no_error(self):
        cap_yaml = (
            'name: test-agent\ndescription: "Test agent"\ntools: Read\n'
            "model: inherit\nskills: [test-skill]\nversion: 1.0.0\n"
            "capabilities:\n"
            "  - id: test.domain.action\n"
            "    intent_patterns:\n"
            '      - "test intent"\n'
            "    preconditions:\n"
            "      structural: []\n"
            "    postconditions:\n"
            "      - key: test_done\n"
            "        value: true\n"
            "    evidence_schema:\n"
            "      structural:\n"
            '        - check: file_exists\n          path: "outputs/test.md"\n'
        )
        _write_agent(self.root, "test-agent", cap_yaml)
        _write_skill(self.root, "test-skill")

        findings: list[Finding] = []
        validate_compiler_artifacts(self.root, findings)
        codes = [f.code for f in findings]
        self.assertNotIn("routing.empty_capabilities", codes)

    def test_no_agents_no_error(self):
        """Kit with 0 agents should NOT trigger routing.empty_capabilities."""
        findings: list[Finding] = []
        validate_compiler_artifacts(self.root, findings)
        codes = [f.code for f in findings]
        self.assertNotIn("routing.empty_capabilities", codes)


class TestOrchestratorMissingRoutingTable(unittest.TestCase):
    """routing.orchestrator_missing_routing_table: Orchestrator with delegates_to but no routing table."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        _make_kit(self.root)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_orchestrator_without_routing_table_errors(self):
        _write_agent(
            self.root, "master-orchestrator",
            'name: master-orchestrator\ndescription: "Orchestrator"\ntools: [Read, Agent]\nmodel: inherit\nskills: []\nversion: 1.0.0\ndelegates_to: [specialist-a, specialist-b]',
            body="You are a master orchestrator. Handle tasks by delegating.",
        )

        findings: list[Finding] = []
        validate_compiler_artifacts(self.root, findings)
        codes = [f.code for f in findings]
        self.assertIn("routing.orchestrator_missing_routing_table", codes)

    def test_orchestrator_with_routing_table_no_error(self):
        _write_agent(
            self.root, "master-orchestrator",
            'name: master-orchestrator\ndescription: "Orchestrator"\ntools: [Read, Agent]\nmodel: inherit\nskills: []\nversion: 1.0.0\ndelegates_to: [specialist-a, specialist-b]',
            body="## ROUTING TABLE\n\n| Intent | Agent | Skills |\n|:---|:---|:---|\n| analyze | specialist-a | audit |",
        )

        findings: list[Finding] = []
        validate_compiler_artifacts(self.root, findings)
        codes = [f.code for f in findings]
        self.assertNotIn("routing.orchestrator_missing_routing_table", codes)


class TestAgentMissingSkillMatrix(unittest.TestCase):
    """routing.agent_missing_skill_matrix: Agent with skills but no Skill Invocation Matrix."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        _make_kit(self.root)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_agent_with_skills_but_no_matrix_errors(self):
        _write_agent(
            self.root, "specialist-a",
            'name: specialist-a\ndescription: "Specialist"\ntools: Read\nmodel: inherit\nskills: [audit-skill, optimize-skill]\nversion: 1.0.0',
            body="You are a specialist. Do your job.",
        )

        findings: list[Finding] = []
        validate_compiler_artifacts(self.root, findings)
        codes = [f.code for f in findings]
        self.assertIn("routing.agent_missing_skill_matrix", codes)

    def test_agent_with_skill_invocation_matrix_no_error(self):
        _write_agent(
            self.root, "specialist-a",
            'name: specialist-a\ndescription: "Specialist"\ntools: Read\nmodel: inherit\nskills: [audit-skill]\nversion: 1.0.0',
            body="## SKILL INVOCATION MATRIX\n\n| Scenario | Skill | Why |\n|:---|:---|:---|\n| audit needed | audit-skill | contains checklist |",
        )

        findings: list[Finding] = []
        validate_compiler_artifacts(self.root, findings)
        codes = [f.code for f in findings]
        self.assertNotIn("routing.agent_missing_skill_matrix", codes)

    def test_agent_with_strategy_matrix_variant_no_error(self):
        """Accepts 'Strategy Matrix' + 'skill' mention as an alternative anchor."""
        _write_agent(
            self.root, "specialist-a",
            'name: specialist-a\ndescription: "Specialist"\ntools: Read\nmodel: inherit\nskills: [audit-skill]\nversion: 1.0.0',
            body="## Strategy Matrix & Skill Loading Protocol\n\nWhen audit → load audit-skill.",
        )

        findings: list[Finding] = []
        validate_compiler_artifacts(self.root, findings)
        codes = [f.code for f in findings]
        self.assertNotIn("routing.agent_missing_skill_matrix", codes)

    def test_orchestrator_with_skills_not_flagged_as_missing_matrix(self):
        """Orchestrator (has delegates_to) shouldn't be checked for skill matrix — it delegates."""
        _write_agent(
            self.root, "master",
            'name: master\ndescription: "Master"\ntools: [Read, Agent]\nmodel: inherit\nskills: [coordination-skill]\nversion: 1.0.0\ndelegates_to: [specialist-a]',
            body="You are a master orchestrator.",
        )

        findings: list[Finding] = []
        validate_compiler_artifacts(self.root, findings)
        codes = [f.code for f in findings]
        self.assertNotIn("routing.agent_missing_skill_matrix", codes)


if __name__ == "__main__":
    unittest.main()
