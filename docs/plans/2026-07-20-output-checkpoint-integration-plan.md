# Output Checkpoint System Integration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the 3-Tier Checkpoint architecture by embedding `checkpoint_gate.py` contracts into Core Rules, Workflow Master Template, `kit-extending` skill, and creating a dedicated `@output-checkpointing` skill.

**Architecture:** Contract & Skill extension across `.agents/rules/`, `.agents/templates/`, and `.agents/skills/` to enforce `decided_by: orchestrator` and automatic execution of `checkpoint_gate.py` on all output artifacts.

**Tech Stack:** Antigravity IDE Agent Kit Standard (YAML Frontmatter, Markdown Contracts, Manifest Generator).

## Global Constraints

- **Trigger Rule**: Only 3 valid triggers allowed for Rules (`always_on`, `manual`, `model_decision`).
- **Orchestration Rule**: Workflow checkpoint nodes MUST use `decided_by: orchestrator`.
- **DoD Rule**: Binary, measurable DoD assertions with zero vague adjectives.

---

### Task 1: Update Rule Standards (`.agents/rules/file-standards.md`)

**Files:**
- Modify: `.agents/rules/file-standards.md`
- Test: `python -m unittest discover -s .agents/scripts/tests -p "test_toolkit.py"`

- [ ] **Step 1: Inspect `file-standards.md`**
- [ ] **Step 2: Add Workflow Checkpoint Contract schema to `file-standards.md`**

```markdown
### 2.4 Workflow Checkpoint Schema (`risk_tier`, `reason_code`)
Mọi Node trong Workflow có bước `[Evaluation Loop]` cho Output BẮT BỘC khai báo:
- `risk_tier`: T0 | T1 | T2 | T3
- `reason_code`: IRREVERSIBLE_ACTION | POLICY_BOUNDARY | EXTERNAL_WRITE | INTERNAL_DRAFT | DETERMINISTIC_PASS
- `decided_by`: orchestrator  # BẮT BỘC, không bao giờ dùng "model"
- `checkpoint_cmd`: `python .agents/scripts/checkpoint_gate.py --node <node_id> --target <output_files> --op <create|modify|delete>`
```

- [ ] **Step 3: Run validation tests**

Run: `python -m unittest discover -s .agents/scripts/tests -p "test_toolkit.py"`
Expected: PASS

---

### Task 2: Update Workflow Master Template (`.agents/templates/workflow-template.md`)

**Files:**
- Modify: `.agents/templates/workflow-template.md`
- Test: `python -m unittest discover -s .agents/scripts/tests -p "test_toolkit.py"`

- [ ] **Step 1: Add Checkpoint Gate parameters to `workflow-template.md`**

Update `[Evaluation Loop]` in `workflow-template.md`:
```markdown
- **Evaluation Loop & Checkpoint Gate**: 
  - Checkpoint Command: `python .agents/scripts/checkpoint_gate.py --node {NODE_ID} --target {OUTPUT_ARTIFACT} --op {OP}`
  - Risk Tier: `{RISK_TIER}` | Reason: `{REASON_CODE}` | Decided By: `orchestrator`
  - Evaluate output ➔ Pass ➔ Transition sang `[STATE: {NEXT_STATE}]`
  - Fail ➔ Revise (Tối đa `{MAX_RETRY}` lần) ➔ Vượt ngưỡng ➔ Escalate sang `[ESCALATE_HUMAN]`
```

- [ ] **Step 2: Run self-validation**

Run: `python .agents/scripts/validate_kit.py`
Expected: PASS

---

### Task 3: Update Self-Extension Skill (`.agents/skills/kit-extending/SKILL.md`)

**Files:**
- Modify: `.agents/skills/kit-extending/SKILL.md`
- Test: `python -m unittest discover -s .agents/scripts/tests -p "test_toolkit.py"`

- [ ] **Step 1: Add Section 4 "Output Checkpoint Integration Contract" to `kit-extending/SKILL.md`**

```markdown
## 4. Output Checkpoint Integration Contract

Khi tạo mới hoặc refactor bất kỳ Workflow hay Kit nào:
1. Đảm bảo mọi Output Artifact được ghi ra `./output/<kit-name>/` đều gắn với một Checkpoint Gate.
2. Gọi script `checkpoint_gate.py` để đánh giá `risk_tier` và `reason_code` trước khi hoàn tất node.
3. Không cho phép LLM tự hủy hoặc tự duyệt checkpoint (`decided_by: orchestrator`).
```

- [ ] **Step 2: Run validation**

Run: `python .agents/scripts/validate_kit.py`
Expected: PASS

---

### Task 4: Create Dedicated Skill (`.agents/skills/output-checkpointing/SKILL.md`)

**Files:**
- Create: `.agents/skills/output-checkpointing/SKILL.md`
- Test: `python -m unittest discover -s .agents/scripts/tests -p "test_toolkit.py"`

- [ ] **Step 1: Create `.agents/skills/output-checkpointing/SKILL.md`**

```markdown
---
name: output-checkpointing
description: "Phân tích rủi ro, kiểm định chất lượng và kích hoạt Checkpoint Envelope bảo vệ sản phẩm đầu ra (Output Artifacts) trong ./output/<kit-name>/. Sử dụng khi người dùng yêu cầu kiểm tra output, chạy checkpoint, hoặc bảo vệ file được sinh ra khỏi state drift."
when_to_use: "Kích hoạt khi người dùng gõ /output-checkpointing hoặc yêu cầu kiểm tra/duyệt rủi ro sản phẩm đầu ra của Agent Kit."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# Output Checkpoint Skill — Bảo vệ & Kiểm định Sản phẩm Đầu ra

> Chuyên biệt kiểm định, tính toán Blast Radius và kích hoạt Checkpoint Envelope trên các file đầu ra tại `./output/<kit-name>/`.

## Quick Start Command

Đánh giá và chạy Checkpoint Gate trên một file Output:
```bash
python .agents/scripts/checkpoint_gate.py --node <node_name> --target <file_path> --op <create|modify|delete>
```

## Quy trình Kiểm định Output 3 Lớp:

1. **Guard Check**: Sinh SHA-256 Scoped Hash trên file output, phát hiện state drift và sẵn sàng Rollback snapshot nếu người dùng Reject.
2. **Impact Analysis**: Phân loại Ma trận Rủi ro 2D (Path x Operation), nén Git Diff ≤ 15 dòng ưu tiên dòng bị xóa (`-`), viết Impact Summary tiếng Việt.
3. **Envelope Execution**:
   - Với **T2**: Hiển thị phím bấm `1` (Approve), `2` (Revise), `3` (Reject).
   - Với **T3**: Bắt buộc nhập mã `CONFIRM <4-digit-code>` (ví dụ `CONFIRM 8492`).
```

- [ ] **Step 2: Run validation**

Run: `python .agents/scripts/validate_kit.py`
Expected: PASS

---

### Task 5: Regenerate Manifest & Lock Files

**Files:**
- Modify: `.agents/manifest.json`
- Modify: `.agents/manifest.lock.json`
- Test: `python -m unittest discover -s .agents/scripts/tests -p "test_*.py"`

- [ ] **Step 1: Regenerate manifest**

Run: `python .agents/scripts/generate_manifest.py`

- [ ] **Step 2: Run full regression test suite**

Run: `python -m unittest discover -s .agents/scripts/tests -p "test_*.py"`
Expected: 17/17 PASS
