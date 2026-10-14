---
name: {WORKFLOW_NAME}
description: {DESCRIPTION_MAX_250_CHARS}
version: 1.0.0
requires_skills: [{SKILL_1}, {SKILL_2}]
artifact_outputs: [{ARTIFACT_1}, {ARTIFACT_2}]
topology: {TOPOLOGY} # [chaining | routing | sequential | parallelization | orchestrator-workers | evaluator-optimizer]
trigger: {TRIGGER_TYPE} # [manual | chained | schedule | event]
max_retry_per_node: 2
global_invariants:
  - id: inv.{WORKFLOW_NAME}.no_corruption
    description: Cannot overwrite valid outputs without verification
    check: check_no_corruption
nodes:
  step_1:
    role: {AGENT_ROLE}
    skill: {SKILL_1}
    required_outcome: outcome.{WORKFLOW_NAME}.step1
    transitions:
      - to: step_2
  step_2:
    role: {AUDITOR_ROLE}
    skill: {SKILL_2}
    required_outcome: outcome.{WORKFLOW_NAME}.final
    transitions: []
---

# Workflow: /{WORKFLOW_NAME} ({WORKFLOW_TITLE})

> **Mục tiêu**: {Mô tả mục tiêu cốt lõi và định nghĩa "Xong" cấp toàn workflow.}

---

## 1. INVARIANTS (Ràng buộc bất biến)

1. **No Evidence → No Transition**: Mọi state transition đòi hỏi evidence artifact hợp lệ trên đĩa.
2. **Sequential Agent Isolation**: Mỗi Node có đúng 1 Active Role và 1 Assigned Skill. Chuyển Role bắt buộc context reset. Node Audit/Review: `Auditor ≠ Author`.
3. {DOMAIN_SPECIFIC_INVARIANT}

---

## 2. STATE MACHINE NODES

### Bước 1: {NODE_1_TITLE}
- **Role:** `{agent-role}` | **Skill:** `{skill-name}`
- **[Input Artifacts]:** {Mô tả input cần thiết}.
- **[Output Artifacts]:** {Mô tả output sinh ra}.
- **[DoD]:**
  - [ ] {Tiêu chí nhị phân 1}.
  - [ ] {Tiêu chí nhị phân 2}.
- **[Transition]:** Pass → Bước 2 | Fail → {Failure handling}.

---

### Bước 2: {NODE_2_TITLE}
- **Role:** `{agent-role}` (khác Role Bước 1 nếu là Audit)
- **Skill:** `{skill-name}`
- **[Input Artifacts]:** Output từ Bước 1.
- **[Output Artifacts]:** {Deliverable}.
- **[Human Gate]:** `true` — Xuất Decision Package, dừng chờ phê duyệt.
- **[DoD]:**
  - [ ] {Tiêu chí nhị phân}.
  - [ ] User phê duyệt qua Human Gate.
- **[Transition]:** Approve → Hoàn tất | Revise → Quay lại Bước 1.

---

## 3. FAILURE & ESCALATION

- **Retry**: Mỗi node tối đa `max_retry_per_node` lần.
- **Escalate**: Nếu retry hết → `[ESCALATE_HUMAN]` với evidence log.

---

## 4. TRANSACTIONAL MUTATION (Chỉ dùng khi workflow thay đổi file/state có rủi ro)

1. **Snapshot**: Lưu trạng thái trước khi sửa.
2. **Mutate**: Thực hiện thay đổi trong scoped boundary.
3. **Verify**: Chạy validation ngay.
4. **Commit / Rollback**: PASS → xác nhận. FAIL → hoàn nguyên.
