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
        
        self.routing_index_template = self.templates_dir / "routing-index-template.json"
        self.state_schema_template = self.templates_dir / "state-schema-template.json"
        self.evidence_schema_template = self.templates_dir / "evidence-schema-template.json"
        self.invariant_rules_template = self.templates_dir / "invariant-rules-template.json"
        
        self.capability_guide = self.references_dir / "capability-declaration-guide.md"
        self.runtime_routing_doc = self.references_dir / "runtime-routing-model.md"
        self.state_verdict_doc = self.references_dir / "state-verdict-protocol.md"

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
            self.routing_index_template,
            self.state_schema_template,
            self.evidence_schema_template,
            self.invariant_rules_template,
        ]:
            self.assertTrue(template_path.is_file(), f"{template_path.name} must exist")
            content = template_path.read_text(encoding="utf-8")
            data = json.loads(content)
            self.assertIsInstance(data, (dict, list), f"{template_path.name} must be valid JSON")

    def test_reference_guides_presence(self):
        for doc_path in [
            self.capability_guide,
            self.runtime_routing_doc,
            self.state_verdict_doc,
        ]:
            self.assertTrue(doc_path.is_file(), f"{doc_path.name} must exist")
            content = doc_path.read_text(encoding="utf-8")
            self.assertGreater(len(content), 100, f"{doc_path.name} must have substantive content")

if __name__ == "__main__":
    unittest.main()
