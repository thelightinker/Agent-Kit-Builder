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
    @classmethod
    def setUpClass(cls):
        import tempfile
        from support import copy_toolkit
        cls._tmp = tempfile.TemporaryDirectory()
        cls.kit_copy = copy_toolkit(Path(cls._tmp.name))

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_toolkit_self_validation_passes(self):
        findings = validate_kit.validate(self.kit_copy)
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


class TestUnifiedValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import tempfile
        from support import copy_toolkit
        cls._tmp = tempfile.TemporaryDirectory()
        cls.kit_copy = copy_toolkit(Path(cls._tmp.name))

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_validate_quick(self):
        findings = validate_kit.validate_quick(self.kit_copy)
        errors = [item for item in findings if item.severity == "error"]
        self.assertEqual([], errors)

    def test_sync_registry(self):
        count, files = validate_kit.sync_registry(self.kit_copy)
        self.assertGreaterEqual(count, 3)
        self.assertIn("manifest.json", files)
        self.assertIn("manifest.lock.json", files)
        self.assertIn("DEPENDENCY_GRAPH.md", files)
        self.assertIn("execution_policy.json", files)


class TestMachineActionableContract(unittest.TestCase):
    def test_finding_has_fix_strategy_fields(self):
        f = validate_kit.Finding(
            severity="error",
            code="manifest.stale",
            file="manifest.json",
            line=1,
            message="Registry differs from component frontmatter",
            evidence="actual_hash != expected_hash",
            fix_strategy="deterministic",
            retryable=True,
        )
        self.assertEqual(f.fix_strategy, "deterministic")
        self.assertTrue(f.retryable)
        self.assertIn("evidence", f.__dict__)

    def test_finding_json_serializable(self):
        f = validate_kit.Finding(
            severity="error",
            code="manifest.stale",
            file="manifest.json",
            line=1,
            message="test",
            evidence="hash_mismatch",
            fix_strategy="deterministic",
            retryable=True,
        )
        payload = json.dumps(f.__dict__)
        roundtrip = json.loads(payload)
        self.assertEqual(roundtrip["fix_strategy"], "deterministic")


class TestBehavioralCapabilities(unittest.TestCase):
    def test_dynamic_routing_and_dag_safety(self):
        benchmark_mod = load_module("agkit_benchmark", SCRIPTS / "benchmark_behavior.py")
        for tc in benchmark_mod.TEST_VECTORS:
            mode = benchmark_mod.classify_prompt(tc.user_prompt)
            self.assertEqual(tc.expected_mode, mode, f"Failed routing for {tc.name}")
        
        dag = benchmark_mod.analyze_dag_conflict_safety()
        self.assertFalse(dag["write_conflict_detected"])
        self.assertEqual(4, dag["dag_stages"])

    def test_backward_compatibility(self):
        benchmark_mod = load_module("agkit_benchmark", SCRIPTS / "benchmark_behavior.py")
        compat = benchmark_mod.verify_backward_compatibility()
        for wf, info in compat.items():
            self.assertTrue(info["present"], f"Missing workflow {wf}")
            self.assertTrue(info["valid_requires"], f"Invalid requirements in {wf}")


class TestDeterministicFixer(unittest.TestCase):
    def test_fix_stale_manifest(self):
        import tempfile, shutil
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir) / ".agents"
            shutil.copytree(TOOLKIT, tmp_root)
            manifest_path = tmp_root / "manifest.json"
            manifest_path.write_text('{"broken": true}', "utf-8")
            findings = validate_kit.validate(tmp_root, auto_heal=False)
            det_findings = [f for f in findings if f.fix_strategy == "deterministic"]
            self.assertTrue(len(det_findings) > 0)
            det_fixer = load_module("agkit_det_fixer", SCRIPTS / "deterministic_fixer.py")
            report = det_fixer.fix(tmp_root, det_findings)
            self.assertTrue(len(report["fixed"]) > 0)
            self.assertEqual(len(report["failed"]), 0)
            re_findings = validate_kit.validate(tmp_root, auto_heal=False)
            det_remaining = [f for f in re_findings if f.fix_strategy == "deterministic"]
            self.assertEqual(len(det_remaining), 0)


class TestConvergenceEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import tempfile
        from support import copy_toolkit
        cls._tmp = tempfile.TemporaryDirectory()
        cls.kit_copy = copy_toolkit(Path(cls._tmp.name))

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_converge_on_healthy_kit(self):
        conv_mod = load_module("agkit_conv", SCRIPTS / "convergence_engine.py")
        report = conv_mod.converge(self.kit_copy, max_iterations=3)
        self.assertTrue(report["converged"])
        self.assertEqual(report["iterations"], 0)
        self.assertEqual(report["auto_fixed_count"], 0)
        self.assertEqual(report["escalated_count"], 0)
        self.assertFalse(report["oscillation_detected"])

    def test_converge_detects_oscillation(self):
        conv_mod = load_module("agkit_conv", SCRIPTS / "convergence_engine.py")
        history = [{"manifest.stale"}, {"manifest.stale"}]
        self.assertTrue(conv_mod._detect_oscillation(history))

    def test_max_iterations_bounded(self):
        conv_mod = load_module("agkit_conv", SCRIPTS / "convergence_engine.py")
        report = conv_mod.converge(self.kit_copy, max_iterations=1)
        self.assertLessEqual(report["iterations"], 1)


class TestConvergenceBenchmark(unittest.TestCase):
    def test_oscillation_detection_accuracy(self):
        conv_mod = load_module("agkit_conv", SCRIPTS / "convergence_engine.py")
        self.assertTrue(conv_mod._detect_oscillation([{"a"}, {"b"}, {"a"}]))
        self.assertFalse(conv_mod._detect_oscillation([{"a"}, {"b"}, {"c"}]))
        self.assertTrue(conv_mod._detect_oscillation([{"a", "b"}, {"a", "b"}]))
        self.assertFalse(conv_mod._detect_oscillation([set()]))


class TestChaosRecoveryScenarios(unittest.TestCase):
    def test_chaos_multi_fault_recovery(self):
        import tempfile, shutil
        conv_mod = load_module("agkit_conv", SCRIPTS / "convergence_engine.py")
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir) / ".agents"
            shutil.copytree(TOOLKIT, tmp_root)
            
            # Inject 5 faults
            (tmp_root / "manifest.json").write_text('{"corrupted": true}', "utf-8")
            if (tmp_root / "manifest.lock.json").exists():
                (tmp_root / "manifest.lock.json").unlink()
            if (tmp_root / "DEPENDENCY_GRAPH.md").exists():
                (tmp_root / "DEPENDENCY_GRAPH.md").unlink()
            if (tmp_root / "VERSION").exists():
                (tmp_root / "VERSION").unlink()
            
            report = conv_mod.converge(tmp_root, max_iterations=3)
            self.assertTrue(report["converged"])
            self.assertLessEqual(report["iterations"], 2)
            self.assertGreaterEqual(report["first_pass_errors"], 3)
            self.assertGreaterEqual(report["auto_fixed_count"], 3)

    def test_chaos_fatal_syntax_trap_escalates(self):
        import tempfile, shutil
        conv_mod = load_module("agkit_conv", SCRIPTS / "convergence_engine.py")
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir) / ".agents"
            shutil.copytree(TOOLKIT, tmp_root)
            
            # Inject fatal syntax error
            (tmp_root / "scripts" / "bad_syntax.py").write_text("def broken(:\n  pass", "utf-8")
            
            report = conv_mod.converge(tmp_root, max_iterations=3)
            self.assertFalse(report["converged"])
            self.assertGreater(report["escalated_count"], 0)
            self.assertEqual(1, report["iterations"])


if __name__ == "__main__":
    unittest.main()



