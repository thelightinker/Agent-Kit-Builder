# .agents/scripts/tests/test_structural_anchors.py
import tempfile
import unittest
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate_kit import Finding, validate_structural_anchors


class TestStructuralAnchors(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "skills").mkdir(parents=True, exist_ok=True)
        (self.root / "workflows").mkdir(parents=True, exist_ok=True)
        (self.root / "agent").mkdir(parents=True, exist_ok=True)
        (self.root / "memory").mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_valid_skill_passes(self):
        skill_dir = self.root / "skills" / "demo-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(
            """---
name: demo-skill
description: "Comprehensive trigger description for demo skill with context"
when_to_use: "Use when the user requests demo processing. Do not use for other tasks."
allowed-tools: Read, Write
version: 1.0.0
---

# Demo Skill

Instructions for demo processing.

## Guidelines
- Follow imperative commands.

## Examples
### Example 1
Input: Process input data.
Output: Processed output data.
""",
            encoding="utf-8",
        )

        findings: list[Finding] = []
        validate_structural_anchors(self.root, findings)
        skill_errors = [f for f in findings if f.code.startswith("skill.")]
        self.assertEqual(skill_errors, [])

    def test_invalid_skill_missing_examples(self):
        skill_dir = self.root / "skills" / "no-example-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(
            """---
name: no-example-skill
description: "Comprehensive trigger description without any examples"
when_to_use: "Use when testing missing examples."
allowed-tools: Read, Write
version: 1.0.0
---

# No Example Skill

Just instructions without any example section or input output.
""",
            encoding="utf-8",
        )

        findings: list[Finding] = []
        validate_structural_anchors(self.root, findings)
        codes = [f.code for f in findings]
        self.assertIn("skill.missing_examples", codes)

    def test_valid_workflow_passes(self):
        wf_file = self.root / "workflows" / "demo-wf.md"
        wf_file.write_text(
            """---
name: demo-wf
description: "Demo workflow description"
version: 1.0.0
requires_agents: [demo-agent]
requires_skills: [demo-skill]
artifact_outputs: [output.md]
---

# Workflow: demo-wf

## State Machine Nodes

### Bước 1: Khởi tạo
- **[Input Artifacts]:** input.md
- **[Output Artifacts]:** intermediate.md
- **[DoD]:**
  - [ ] Validated schema
- **[Evaluation Loop]:** Pass -> Bước 2 | Fail -> [ESCALATE_HUMAN]

### Bước 2: Hoàn tất
- **[Input Artifacts]:** intermediate.md
- **[Output Artifacts]:** output.md
- **[DoD]:**
  - [ ] Final output ready
- **[Evaluation Loop]:** Pass -> Done
""",
            encoding="utf-8",
        )

        findings: list[Finding] = []
        validate_structural_anchors(self.root, findings)
        wf_errors = [f for f in findings if f.code == "workflow.missing_node_anatomy"]
        self.assertEqual(wf_errors, [])

    def test_invalid_workflow_missing_node_anatomy(self):
        wf_file = self.root / "workflows" / "broken-wf.md"
        wf_file.write_text(
            """---
name: broken-wf
description: "Broken workflow"
version: 1.0.0
requires_agents: [demo-agent]
requires_skills: [demo-skill]
artifact_outputs: [output.md]
---

# Workflow: broken-wf

### Bước 1: Do something
Just free-form text without Input, Output, DoD, or Evaluation loop.
""",
            encoding="utf-8",
        )

        findings: list[Finding] = []
        validate_structural_anchors(self.root, findings)
        codes = [f.code for f in findings]
        self.assertIn("workflow.missing_node_anatomy", codes)

    def test_valid_agent_passes(self):
        agent_file = self.root / "agent" / "demo-agent.md"
        agent_file.write_text(
            """---
name: demo-agent
description: "Demo agent description"
tools: Read, Write
model: inherit
skills: [demo-skill]
version: 1.0.0
---

# Demo Agent

## 1. Vai trò & Outcome
Core responsibilities and outcomes.

## 2. Quy trình Thực thi
State machine and execution steps.

## 3. Hard Constraints & Negative Boundaries
- Never do X.

## 4. Format Đầu Ra & Definition of Done
Binary DoD:
- [ ] Output exists
""",
            encoding="utf-8",
        )

        findings: list[Finding] = []
        validate_structural_anchors(self.root, findings)
        agent_errors = [f for f in findings if f.code == "agent.missing_role_blocks"]
        self.assertEqual(agent_errors, [])

    def test_invalid_agent_missing_blocks(self):
        agent_file = self.root / "agent" / "incomplete-agent.md"
        agent_file.write_text(
            """---
name: incomplete-agent
description: "Incomplete agent description"
tools: Read
model: inherit
skills: []
version: 1.0.0
---

# Incomplete Agent

Only some random notes without standard 4 blocks or constraints.
""",
            encoding="utf-8",
        )

        findings: list[Finding] = []
        validate_structural_anchors(self.root, findings)
        codes = [f.code for f in findings]
        self.assertIn("agent.missing_role_blocks", codes)

    def test_orchestrator_worker_briefing_check(self):
        orch_file = self.root / "agent" / "demo-orchestrator.md"
        orch_file.write_text(
            """---
name: demo-orchestrator
description: "Master orchestrator agent"
tools: Read, Write
model: inherit
skills: []
version: 1.0.0
---

# Demo Orchestrator

## 1. Vai trò & Outcome
Orchestrator brain.

## 2. Quy trình & Worker Briefing Protocol
- Goal & Context: Specific objective
- What was ruled out: Exclusions
- Specific file scope: Files
- Negative boundaries: Limits
- Verification evidence: Criteria

## 3. Hard Constraints
- Must not delegate understanding.

## 4. Format Đầu Ra & Definition of Done
- [ ] Done
""",
            encoding="utf-8",
        )

        findings: list[Finding] = []
        validate_structural_anchors(self.root, findings)
        orch_errors = [f for f in findings if f.code == "agent.missing_worker_briefing"]
        self.assertEqual(orch_errors, [])

    def test_agent_filesystem_contract_check(self):
        # Incompliant agent without filesystem contract
        agent_file = self.root / "agent" / "no-fs-agent.md"
        agent_file.write_text(
            """---
name: no-fs-agent
description: "Agent without filesystem contract"
tools: Read
model: inherit
skills: []
version: 1.0.0
---

# No FS Agent

## 1. Vai trò & Outcome
Worker.

## 2. Quy trình & Process
Step 1, step 2.

## 3. Hard Constraints
Do not fail.

## 4. Format Đầu Ra & Definition of Done
- [ ] Done
""",
            encoding="utf-8",
        )

        findings: list[Finding] = []
        validate_structural_anchors(self.root, findings)
        codes = [f.code for f in findings]
        self.assertIn("agent.missing_filesystem_contract", codes)

        # Compliant agent with filesystem contract
        agent_file.write_text(
            """---
name: compliant-agent
description: "Agent with filesystem contract"
tools: Read
model: inherit
skills: []
version: 1.0.0
---

# Compliant Agent

## 1. Vai trò & Outcome
Worker.

## 2. Quy trình & Process
Step 1, step 2.

## 3. Hard Constraints
Do not fail.

### 🔒 FILESYSTEM & WORKSPACE CONTRACT (BẤT BIẾN)
- Inputs: inputs/
- Kitchen: .workspace/
- Deliverables: outputs/

## 4. Format Đầu Ra & Definition of Done
- [ ] Done
""",
            encoding="utf-8",
        )

        findings.clear()
        validate_structural_anchors(self.root, findings)
        fs_errors = [f for f in findings if f.code == "agent.missing_filesystem_contract"]
        self.assertEqual(fs_errors, [])

    def test_outputs_sanitizer_violation(self):
        outputs_dir = self.root / "outputs"
        outputs_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Inject forbidden temporary and cache files
        (outputs_dir / "dirty_log.tmp").write_text("temp", encoding="utf-8")
        (outputs_dir / "raw_chunk.chunk").write_text("chunk", encoding="utf-8")
        (outputs_dir / ".hidden_intermediate").write_text("hidden", encoding="utf-8")
        (outputs_dir / "clean_book.epub").write_text("clean", encoding="utf-8")

        findings: list[Finding] = []
        validate_structural_anchors(self.root, findings)
        sanitizer_errors = [f for f in findings if f.code == "output.sanitizer_violation"]
        self.assertEqual(len(sanitizer_errors), 3)

        # 2. Clean up forbidden files, leaving only valid deliverable
        (outputs_dir / "dirty_log.tmp").unlink()
        (outputs_dir / "raw_chunk.chunk").unlink()
        (outputs_dir / ".hidden_intermediate").unlink()

        findings.clear()
        validate_structural_anchors(self.root, findings)
        sanitizer_errors_after = [f for f in findings if f.code == "output.sanitizer_violation"]
        self.assertEqual(len(sanitizer_errors_after), 0)


if __name__ == "__main__":
    unittest.main()
