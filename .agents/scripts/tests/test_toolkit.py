from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

TOOLKIT = Path(__file__).resolve().parents[2]
SCRIPTS = TOOLKIT / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


validate_kit = load_module("agkit_validate_kit", SCRIPTS / "validate_kit.py")
eval_runner = load_module("agkit_eval_runner", SCRIPTS / "eval_runner.py")
export_kit = load_module("agkit_export_kit", SCRIPTS / "export_kit.py")
component_registry = sys.modules["component_registry"]
dependency_graph = sys.modules["dependency_graph"]




class ToolkitRegressionTests(unittest.TestCase):
    def test_toolkit_self_validation_passes(self):
        findings = validate_kit.validate(TOOLKIT)
        errors = [item for item in findings if item.severity == "error"]
        self.assertEqual([], errors)

    def test_mcp_config_is_valid_json(self):
        data = json.loads((TOOLKIT / "mcp_config.json").read_text("utf-8"))
        self.assertIn("mcpServers", data)

    def test_all_components_use_strict_semver(self):
        manifest = component_registry.build_manifest(TOOLKIT)
        for group in ("agents", "skills", "workflows", "rules"):
            with self.subTest(group=group):
                invalid = {
                    name: data["version"]
                    for name, data in manifest[group].items()
                    if not component_registry.is_semver(data["version"])
                }
                self.assertEqual({}, invalid)

    def test_manifest_is_synchronized(self):
        manifest = component_registry.build_manifest(TOOLKIT)
        self.assertEqual(manifest, json.loads((TOOLKIT / "manifest.json").read_text("utf-8")))

    def test_dependency_graph_is_synchronized(self):
        expected = dependency_graph.render(TOOLKIT)
        self.assertEqual(expected, (TOOLKIT / "DEPENDENCY_GRAPH.md").read_text("utf-8"))

    def test_workflow_dependencies_resolve(self):
        manifest = component_registry.build_manifest(TOOLKIT)
        agents = set(manifest["agents"])
        skills = set(manifest["skills"])
        for name, workflow in manifest["workflows"].items():
            with self.subTest(workflow=name):
                self.assertLessEqual(set(workflow["requires"]["agents"]), agents)
                self.assertLessEqual(set(workflow["requires"]["skills"]), skills)
                self.assertTrue(workflow["artifactOutputs"])

    def test_caret_semver_resolution(self):
        self.assertTrue(component_registry.version_satisfies("1.4.2", "^1.2.0"))
        self.assertFalse(component_registry.version_satisfies("2.0.0", "^1.2.0"))
        self.assertTrue(component_registry.version_satisfies("0.3.5", "^0.3.1"))
        self.assertFalse(component_registry.version_satisfies("0.4.0", "^0.3.1"))

    def test_memory_topics_are_present(self):
        topics = {
            "project-conventions.md",
            "user-preferences.md",
            "tech-decisions.md",
            "feedback-history.md",
        }
        self.assertLessEqual(topics, {path.name for path in (TOOLKIT / "memory").glob("*.md")})
        self.assertLessEqual(len((TOOLKIT / "memory/MEMORY.md").read_text("utf-8").splitlines()), 200)


class TestEvalRunner(unittest.TestCase):
    def test_eval_runner_suite_execution(self):
        eval_file = TOOLKIT / "evals" / "eval_suite_example.json"
        report = eval_runner.run_eval_suite(str(eval_file), str(TOOLKIT))
        self.assertEqual(report["failed"], 0)
        self.assertEqual(report["passed"], 2)
        self.assertEqual(report["score_pct"], 100.0)


class TestExportKit(unittest.TestCase):
    def test_export_kit_multi_platform(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            res = export_kit.export_kit(str(TOOLKIT), tmpdir, target="all")
            self.assertIn("cursor", res)
            self.assertIn("claude", res)
            self.assertIn("openai", res)
            self.assertTrue(Path(res["cursor"]).exists())
            self.assertTrue((Path(res["claude"]) / "claude_instructions.txt").exists())
            self.assertTrue(Path(res["openai"]).exists())


if __name__ == "__main__":
    unittest.main()



