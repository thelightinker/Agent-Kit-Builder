#!/usr/bin/env python3
import unittest
from pathlib import Path
import json
import re

class TestTemplates(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[2]
        self.templates_dir = self.root / "templates"
        self.references_dir = self.root / "references"
        
        self.agent_template = self.templates_dir / "agent-template.md"
        self.workflow_template = self.templates_dir / "workflow-template.md"
        self.antigravity_template = self.templates_dir / "antigravity-template.json"
        self.manifest_template = self.templates_dir / "manifest-template.json"

        self.role_profiles_doc = self.references_dir / "role-profiles.md"
        self.component_contracts_doc = self.references_dir / "component-contracts.md"
        self.verification_abstraction_doc = self.references_dir / "verification-abstraction.md"

    def test_agent_template_structure(self):
        self.assertTrue(self.agent_template.is_file(), "agent-template.md must exist")
        content = self.agent_template.read_text(encoding="utf-8")
        self.assertIn("capabilities:", content)
        self.assertIn("negative_scope:", content)
        self.assertIn("failure_policy:", content)
        self.assertIn("checkpoint_resume_policy:", content)
        self.assertTrue(bool(re.search(r"(?i)##.*negative boundaries", content)))

    def test_agent_and_orchestrator_filesystem_contract(self):
        # Test agent-template.md
        agent_content = self.agent_template.read_text(encoding="utf-8")
        self.assertIn("FILESYSTEM & WORKSPACE CONTRACT", agent_content)
        self.assertIn(".workspace", agent_content)
        self.assertIn("outputs/", agent_content)
        self.assertIn("inputs/", agent_content)

        # Test orchestrator-template.md
        orch_template = self.templates_dir / "orchestrator-template.md"
        self.assertTrue(orch_template.is_file(), "orchestrator-template.md must exist")
        orch_content = orch_template.read_text(encoding="utf-8")
        self.assertIn("FILESYSTEM & WORKSPACE CONTRACT", orch_content)
        self.assertIn(".workspace", orch_content)


    def test_workflow_template_structure(self):
        self.assertTrue(self.workflow_template.is_file(), "workflow-template.md must exist")
        content = self.workflow_template.read_text(encoding="utf-8")
        self.assertIn("global_invariants:", content)
        self.assertIn("nodes:", content)
        self.assertIn("required_outcome:", content)
        self.assertIn("transitions:", content)
        self.assertNotIn("requires_agents:", content)
        self.assertNotIn("role_profile:", content.lower())

    def test_json_templates_validity(self):
        for template_path in [
            self.antigravity_template,
            self.manifest_template,
        ]:
            self.assertTrue(template_path.is_file(), f"{template_path.name} must exist")
            content = template_path.read_text(encoding="utf-8")
            data = json.loads(content)
            self.assertIsInstance(data, (dict, list), f"{template_path.name} must be valid JSON")

    def test_reference_guides_presence(self):
        for doc_path in [
            self.role_profiles_doc,
            self.component_contracts_doc,
            self.verification_abstraction_doc,
        ]:
            self.assertTrue(doc_path.is_file(), f"{doc_path.name} must exist")
            content = doc_path.read_text(encoding="utf-8")
            self.assertGreater(len(content), 100, f"{doc_path.name} must have substantive content")

    def test_manifest_template_artifact_contracts(self):
        manifest_template = self.templates_dir / "manifest-template.json"
        self.assertTrue(manifest_template.is_file(), "manifest-template.json must exist")
        data = json.loads(manifest_template.read_text(encoding="utf-8"))
        self.assertIn("artifact_contracts", data)
        contracts = data["artifact_contracts"]
        self.assertIn("consumes", contracts)
        self.assertIn("produces", contracts)
        self.assertEqual(contracts.get("workspace_dir"), ".workspace")

    def test_readme_card_template_and_assembling_skill(self):
        readme_card = self.templates_dir / "readme-card-template.md"
        self.assertTrue(readme_card.is_file(), "readme-card-template.md must exist")
        content = readme_card.read_text(encoding="utf-8")
        self.assertIn("Input:", content)
        self.assertIn("Output:", content)
        self.assertIn("Share:", content)
        self.assertIn("Working Files:", content)

        assembling_skill = self.root / "skills" / "kit-assembling" / "SKILL.md"
        self.assertTrue(assembling_skill.is_file(), "kit-assembling/SKILL.md must exist")
        skill_text = assembling_skill.read_text(encoding="utf-8")
        self.assertIn("FILESYSTEM & WORKSPACE CONTRACT", skill_text)
        self.assertIn(".workspace", skill_text)

if __name__ == "__main__":
    unittest.main()
