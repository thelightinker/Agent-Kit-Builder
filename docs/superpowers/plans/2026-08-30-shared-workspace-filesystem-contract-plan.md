# Shared Workspace & Universal Artifact Lifecycle Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Nâng cấp Agent Kit Builder (`.agents`) để tự động áp dụng và kiểm định Universal Filesystem & Workspace Contract (Dropzone/Shared/Projects 3-Zone Hierarchy, Artifact Lifecycle Model, Closed Kitchen `.workspace/`) trên mọi Agent Kit sinh ra.

**Architecture:** Bổ sung khối ràng buộc phủ định bất biến (Filesystem Contract) vào agent templates, chuẩn hóa schema `artifact_contracts` trong manifest template, cung cấp card README 4 dòng trong kit-assembling, và thiết lập deterministic validation anchor trong `validate_kit.py` cùng bộ kiểm thử TDD.

**Tech Stack:** Python 3.12 (unittest, json, re, pathlib), Markdown Frontmatter/Content, JSON Schema (Draft 2020-12).

## Global Constraints

- **Workspace Isolation:** Mọi kit mẫu hoặc output kiểm thử PHẢI cách ly, không ghi đè bất kỳ file nào ngoài scope.
- **Zero Ungrounded Generation:** Tuân thủ nghiêm ngặt rule `collaboration-protocol.md`.
- **TDD First:** Mỗi task đều có failing test trước khi viết implementation.
- **Binary Definition of Done:** Kiểm thử tự động phải PASS 100% trước khi kết thúc task.
- **No Hardcoded Tool Paths:** Dùng `Path(__file__).resolve()` hoặc tham số CLI `root`.

---

### Task 1: Update Agent and Orchestrator Templates with Filesystem Contract Anchors

**Files:**
- Modify: `.agents/templates/agent-template.md`
- Modify: `.agents/templates/orchestrator-template.md`
- Test: `.agents/scripts/tests/test_templates.py`

**Interfaces:**
- Consumes: Spec `docs/superpowers/specs/2026-08-30-shared-workspace-filesystem-contract-design.md` §6.1
- Produces: Anchors in templates:
  - `### 🔒 FILESYSTEM & WORKSPACE CONTRACT (BẤT BIẾN)`
  - `Inputs Authority (inputs/ | Shared/)`
  - `Closed Kitchen (.workspace/)`
  - `Clean Deliverables (outputs/)`
  - `Controlled Promotion`
  - `Zero-Pollution Discovery`

- [ ] **Step 1: Write the failing test in `test_templates.py`**

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python .agents/scripts/tests/test_templates.py`  
Expected: FAIL with `AssertionError: 'FILESYSTEM & WORKSPACE CONTRACT' not found`

- [ ] **Step 3: Add Filesystem & Workspace Contract section to `agent-template.md` and `orchestrator-template.md`**

In `.agents/templates/agent-template.md` (under Section 4 Ranh giới Phủ định / Hard Constraints):
```markdown
### 🔒 FILESYSTEM & WORKSPACE CONTRACT (BẤT BIẾN)
1. **Inputs Authority (`inputs/` | `Shared/`)**: Chỉ đọc dữ liệu từ đây. Tuyệt đối KHÔNG ghi file tạm hoặc nháp vào thư mục này.
2. **Closed Kitchen (`.workspace/`)**: Mọi dữ liệu trung gian (chunks, split audio, temp json, embeddings, logs) BẮT BUỘC ghi vào `.workspace/`. Cấm xả rác ra root.
3. **Clean Deliverables (`outputs/`)**: Chỉ ghi vào `outputs/` khi file đã hoàn chỉnh 100%, sẵn sàng cho người dùng sử dụng.
4. **Controlled Promotion**: Không tự ý đẩy file lên `Shared/`. Chỉ promote khi người dùng xác nhận hoặc workflow có chỉ thị rõ ràng.
5. **Zero-Pollution Discovery**: Khi tìm kiếm tài nguyên từ kit khác, ưu tiên quét `Shared/`, sau đó mới đến `outputs/`. Không bao giờ scan `.workspace/`.
```

In `.agents/templates/orchestrator-template.md` (under Strict Domain Boundary Matrix / Orchestration Invariants):
```markdown
### 🔒 FILESYSTEM & WORKSPACE CONTRACT (BẤT BIẾN)
1. **Inputs Authority (`inputs/` | `Shared/`)**: Điều phối worker đọc dữ liệu từ `inputs/` hoặc `Shared/`. Không cho phép ghi đè source.
2. **Closed Kitchen (`.workspace/`)**: Cưỡng chế mọi Specialist Agent nhốt toàn bộ intermediate, logs, cache vào `.workspace/`.
3. **Clean Deliverables (`outputs/`)**: Đích đến duy nhất cho sản phẩm cuối cùng của dự án là `outputs/`.
4. **Controlled Promotion**: Chỉ hỗ trợ promote deliverables từ `outputs/` sang `Shared/` khi có sự phê duyệt của người dùng.
5. **Zero-Pollution Discovery**: Khi routing hoặc tìm kiếm tài nguyên chéo giữa các agent, chỉ quét `Shared/` và `Projects/*/outputs/`. Cấm quét `.workspace/`.
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python .agents/scripts/tests/test_templates.py`  
Expected: PASS

- [ ] **Step 5: Commit changes**

```bash
git add .agents/templates/agent-template.md .agents/templates/orchestrator-template.md .agents/scripts/tests/test_templates.py
git commit -m "feat(templates): add filesystem and workspace contract anchors to agent templates"
```

---

### Task 2: Update Manifest Schema and Manifest Template with `artifact_contracts`

**Files:**
- Modify: `.agents/schemas/manifest.schema.json`
- Modify: `.agents/templates/manifest-template.json`
- Test: `.agents/scripts/tests/test_templates.py`

**Interfaces:**
- Consumes: Spec `docs/superpowers/specs/2026-08-30-shared-workspace-filesystem-contract-design.md` §6.2
- Produces: Schema property `artifact_contracts` in `manifest.schema.json` and concrete template block in `manifest-template.json`.

- [ ] **Step 1: Write the failing test in `test_templates.py`**

```python
    def test_manifest_template_artifact_contracts(self):
        manifest_template = self.templates_dir / "manifest-template.json"
        self.assertTrue(manifest_template.is_file(), "manifest-template.json must exist")
        data = json.loads(manifest_template.read_text(encoding="utf-8"))
        self.assertIn("artifact_contracts", data)
        contracts = data["artifact_contracts"]
        self.assertIn("consumes", contracts)
        self.assertIn("produces", contracts)
        self.assertEqual(contracts.get("workspace_dir"), ".workspace")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python .agents/scripts/tests/test_templates.py`  
Expected: FAIL with `AssertionError: 'artifact_contracts' not found in dict`

- [ ] **Step 3: Update `manifest.schema.json` and `manifest-template.json`**

In `.agents/schemas/manifest.schema.json`, add `artifact_contracts` to properties:
```json
    "artifact_contracts": {
      "type": "object",
      "properties": {
        "consumes": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["type"],
            "properties": {
              "type": { "type": "string" },
              "preferred_sources": { "type": "array", "items": { "type": "string" } }
            }
          }
        },
        "produces": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["type", "path_pattern"],
            "properties": {
              "type": { "type": "string" },
              "default_scope": { "type": "string", "enum": ["project", "shared"] },
              "path_pattern": { "type": "string" },
              "promotable_to": { "type": "string" }
            }
          }
        },
        "workspace_dir": { "type": "string", "default": ".workspace" }
      }
    }
```

In `.agents/templates/manifest-template.json`, add:
```json
  "artifact_contracts": {
    "consumes": [
      {
        "type": "{CONSUMED_ARTIFACT_TYPE}",
        "preferred_sources": ["Shared/{TARGET_SHARED_DIR}", "inputs"]
      }
    ],
    "produces": [
      {
        "type": "{PRODUCED_ARTIFACT_TYPE}",
        "default_scope": "project",
        "path_pattern": "outputs/{OUTPUT_FILENAME_PATTERN}",
        "promotable_to": "Shared/{TARGET_SHARED_DIR}"
      }
    ],
    "workspace_dir": ".workspace"
  }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python .agents/scripts/tests/test_templates.py`  
Expected: PASS

- [ ] **Step 5: Commit changes**

```bash
git add .agents/schemas/manifest.schema.json .agents/templates/manifest-template.json .agents/scripts/tests/test_templates.py
git commit -m "feat(schemas): add artifact_contracts to manifest schema and template"
```

---

### Task 3: Add README Card Template & Update `kit-assembling` Skill

**Files:**
- Create: `.agents/templates/readme-card-template.md`
- Modify: `.agents/skills/kit-assembling/SKILL.md`
- Test: `.agents/scripts/tests/test_templates.py`

**Interfaces:**
- Consumes: Spec `docs/superpowers/specs/2026-08-30-shared-workspace-filesystem-contract-design.md` §6.3 & §6.4
- Produces:
  - Card 4 dòng chuẩn: Input, Output, Share, Working Files
  - Scaffolding guidelines trong `kit-assembling/SKILL.md`

- [ ] **Step 1: Write the failing test in `test_templates.py`**

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python .agents/scripts/tests/test_templates.py`  
Expected: FAIL with `AssertionError: readme-card-template.md must exist`

- [ ] **Step 3: Create `.agents/templates/readme-card-template.md` and update `kit-assembling/SKILL.md`**

Create `.agents/templates/readme-card-template.md`:
```markdown
> 📥 **Input:** Thả tài liệu vào `inputs/` (hoặc `Shared Workspace/Shared/`, `_Dropzone/`)  
> ✨ **Output:** Thành phẩm sạch của dự án nằm tại `outputs/`  
> 📤 **Share:** Chỉ publish lên `Shared/` khi muốn các Agent khác cùng tái sử dụng  
> ⚙️ **Working Files:** Nằm ẩn trong `.workspace/` (Thoải mái xóa để giải phóng ổ cứng)
```

Update `.agents/skills/kit-assembling/SKILL.md`:
Add a section:
```markdown
## 4. UNIVERSAL FILESYSTEM & ARTIFACT CONTRACT GENERATION
Mọi kit khi sinh ra phải tuân thủ chuẩn 3-Zone Workspace:
1. Đảm bảo System Prompt chứa đủ 5 điều khoản Filesystem Contract (Inputs, .workspace, outputs, promotion, zero-pollution discovery).
2. Manifest khai báo `artifact_contracts` với `workspace_dir: ".workspace"`.
3. Sinh sẵn card README 4 dòng từ `templates/readme-card-template.md` vào README của kit.
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python .agents/scripts/tests/test_templates.py`  
Expected: PASS

- [ ] **Step 5: Commit changes**

```bash
git add .agents/templates/readme-card-template.md .agents/skills/kit-assembling/SKILL.md .agents/scripts/tests/test_templates.py
git commit -m "feat(templates): add readme card template and update kit-assembling skill"
```

---

### Task 4: Implement Deterministic Validator Anchor in `validate_kit.py`

**Files:**
- Modify: `.agents/scripts/validate_kit.py`
- Modify: `.agents/scripts/tests/test_structural_anchors.py`

**Interfaces:**
- Consumes: Rule registry and agent validation loop in `validate_kit.py`
- Produces: Error code `agent.missing_filesystem_contract` (`llm_patch`, True) emitted when agent prompts lack filesystem contract anchors.

- [ ] **Step 1: Write the failing test in `test_structural_anchors.py`**

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python .agents/scripts/tests/test_structural_anchors.py`  
Expected: FAIL with `AssertionError: 'agent.missing_filesystem_contract' not found in codes`

- [ ] **Step 3: Implement `agent.missing_filesystem_contract` in `validate_kit.py`**

In `RULE_REGISTRY` of `.agents/scripts/validate_kit.py`, register:
```python
    "agent.missing_filesystem_contract": ("llm_patch", True),
```

In `validate_structural_anchors()` under `# 3. Agent Anchors`:
```python
        has_fs_contract = bool(
            re.search(r"(?i)(filesystem\s*&\s*workspace\s*contract|\.workspace.*outputs\/|inputs\/.*\.workspace)", text)
        )
        if not has_fs_contract:
            add(findings, "warning", "agent.missing_filesystem_contract", rel, "Agent prompt lacks Filesystem & Workspace Contract anchors (inputs/, outputs/, .workspace/)")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python .agents/scripts/tests/test_structural_anchors.py`  
Expected: PASS

- [ ] **Step 5: Commit changes**

```bash
git add .agents/scripts/validate_kit.py .agents/scripts/tests/test_structural_anchors.py
git commit -m "feat(validator): add agent.missing_filesystem_contract deterministic check"
```

---

### Task 5: End-to-End Validation & Decision Graph Recompilation

**Files:**
- Run: `.agents/scripts/generate_manifest.py`
- Run: `.agents/scripts/dependency_graph.py`
- Run: `.agents/scripts/validate_kit.py .agents`

**Interfaces:**
- Consumes: All updated templates, schemas, skills, and scripts
- Produces: Clean validation report and synchronized `manifest.lock.json` & `DEPENDENCY_GRAPH.md`.

- [ ] **Step 1: Run all test suites**

Run: `python .agents/scripts/tests/test_structural_anchors.py`  
Run: `python .agents/scripts/tests/test_templates.py`  
Expected: All tests PASS.

- [ ] **Step 2: Regenerate manifest and dependency graph**

Run: `python .agents/scripts/generate_manifest.py`  
Run: `python .agents/scripts/dependency_graph.py`  
Expected: `manifest.json`, `manifest.lock.json`, and `DEPENDENCY_GRAPH.md` updated without errors.

- [ ] **Step 3: Validate `.agents` with `validate_kit.py`**

Run: `python .agents/scripts/validate_kit.py .agents`  
Expected: Zero fatal errors.

- [ ] **Step 4: Commit registry synchronization**

```bash
git add .agents/manifest.json .agents/manifest.lock.json .agents/DEPENDENCY_GRAPH.md
git commit -m "chore(registry): recompile manifest and dependency graph after filesystem contract upgrade"
```
