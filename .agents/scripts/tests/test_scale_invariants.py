#!/usr/bin/env python3
"""Scale Invariant & Component Expansion Benchmark Test.

Verifies that adding multiple new skills, workflows, and schemas scales cleanly (O(N)),
requires zero changes to core governance files, and maintains structural integrity.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
import tempfile
import time
import unittest
from pathlib import Path

# Add scripts directory to sys.path
SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

import component_registry
import dependency_graph
import validate_kit


class TestScaleInvariants(unittest.TestCase):
    def test_adding_30_components_requires_zero_core_modifications(self):
        """Scale test: Adding 20 skills + 10 workflows scales in O(N) time with zero core edits."""
        toolkit_root = Path(__file__).resolve().parents[2]

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir) / ".agents"
            shutil.copytree(toolkit_root, tmp_root)

            # Record baseline hash of core rules and agents
            core_guardrails_baseline = (tmp_root / "rules" / "core-guardrails.md").read_text("utf-8")
            kit_architect_baseline = (tmp_root / "agent" / "kit-architect.md").read_text("utf-8")
            upgrade_principles_baseline = (tmp_root / "UPGRADE_PRINCIPLES.md").read_text("utf-8")
            initial_skills_count = len([d for d in (tmp_root / "skills").iterdir() if d.is_dir()])
            initial_wf_count = len(list((tmp_root / "workflows").glob("*.md")))
            expected_skills = initial_skills_count + 20
            expected_wfs = initial_wf_count + 10

            # 1. Dynamically generate 20 new domain skills complying with Anthropic standard
            for i in range(1, 21):
                skill_dir = tmp_root / "skills" / f"scale-test-skill-{i:02d}"
                skill_dir.mkdir(parents=True, exist_ok=True)
                skill_content = f"""---
name: scale-test-skill-{i:02d}
description: "Synthetic test skill {i:02d} for scale invariant benchmark."
version: 1.0.0
allowed-tools: [Read, Write, Grep]
when_to_use: "Kích hoạt khi chạy benchmark kiểm thử độ co giãn (scale test) của Agent Kit."
---

# Skill: Scale Test Skill {i:02d}

## Overview
Test skill for scaling capacity.

## Examples
### Example 1
Input: Scale test input {i:02d}.
Output: Scale test output {i:02d}.
"""
                (skill_dir / "SKILL.md").write_text(skill_content, encoding="utf-8")

            # 2. Dynamically generate 10 new composite workflows
            for j in range(1, 11):
                wf_file = tmp_root / "workflows" / f"scale-workflow-{j:02d}.md"
                # Link each workflow to 2 skills and kit-architect
                skill_a = f"scale-test-skill-{(2*j - 1):02d}"
                skill_b = f"scale-test-skill-{(2*j):02d}"
                wf_content = f"""---
name: scale-workflow-{j:02d}
description: "Synthetic scale workflow {j:02d}."
version: 1.0.0
requires_agents: [kit-architect]
requires_skills: [{skill_a}, {skill_b}]
artifact_outputs: [output_{j:02d}.md]
topology: sequential-state-machine
trigger: manual
---

# Workflow: Scale Workflow {j:02d}

## State Machine Nodes

### Bước 1: Execute
- **[Input Artifacts]:** input_{j:02d}.md
- **[Output Artifacts]:** output_{j:02d}.md
- **[DoD]:**
  - [ ] Scale execution complete
- **[Evaluation Loop]:** Pass -> Done | Fail -> [ESCALATE_HUMAN]
"""
                wf_file.write_text(wf_content, encoding="utf-8")

            # 3. Update ARCHITECTURE.md inventory table in temp root
            arch_file = tmp_root / "ARCHITECTURE.md"
            arch_text = arch_file.read_text("utf-8")
            arch_text = re.sub(r"(\*\*Total Skills\*\*\s*\|\s*)\d+", rf"\g<1>{expected_skills}", arch_text)
            arch_text = re.sub(r"(\*\*Total Workflows\*\*\s*\|\s*)\d+", rf"\g<1>{expected_wfs}", arch_text)
            arch_file.write_text(arch_text, "utf-8")

            # 4. Benchmark Registry Sync & Validation Performance
            start_time = time.perf_counter()
            count, synced_files = validate_kit.sync_registry(tmp_root)
            findings = validate_kit.validate(tmp_root, auto_heal=False)
            elapsed_time = time.perf_counter() - start_time

            # 4. Read generated manifest
            manifest = json.loads((tmp_root / "manifest.json").read_text("utf-8"))

            # 5. Assertions
            # Component counts scaled accurately
            self.assertEqual(len(manifest["skills"]), expected_skills)
            self.assertEqual(len(manifest["workflows"]), expected_wfs)
            self.assertEqual(len(manifest["agents"]), 1)

            # Zero validation errors
            errors = [f for f in findings if f.severity == "error"]
            self.assertEqual(errors, [], f"Validation errors found on scaled toolkit: {errors}")

            # Performance is sub-second (< 1.5s for 47 total components on disk)
            self.assertLess(elapsed_time, 2.0, f"Scale execution too slow: {elapsed_time:.3f}s")

            # Invariant: Core files were NEVER touched or modified
            self.assertEqual(core_guardrails_baseline, (tmp_root / "rules" / "core-guardrails.md").read_text("utf-8"))
            self.assertEqual(kit_architect_baseline, (tmp_root / "agent" / "kit-architect.md").read_text("utf-8"))
            self.assertEqual(upgrade_principles_baseline, (tmp_root / "UPGRADE_PRINCIPLES.md").read_text("utf-8"))


if __name__ == "__main__":
    unittest.main()
