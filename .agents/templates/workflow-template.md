---
name: {WORKFLOW_NAME}
description: {DESCRIPTION_MAX_250_CHARS}
version: 4.0.0
initial_state: {INITIAL_STATE_NAME}
terminal_states: [{TERMINAL_STATE_NAME}]
global_invariants:
  - id: {INVARIANT_ID_1}
    description: "{INVARIANT_DESCRIPTION_1}"
    check: "{STATE_CHECK_EXPRESSION_1}"
  - id: {INVARIANT_ID_2}
    description: "{INVARIANT_DESCRIPTION_2}"
    check: "{STATE_CHECK_EXPRESSION_2}"
nodes:
  {NODE_1_NAME}:
    required_outcome: "{REQUIRED_OUTCOME_KEY_1}"
    human_gate: false
    transitions:
      - to: "{NODE_2_NAME}"
        when: "{STATE_CONDITION_EXPR_1}"
  {NODE_2_NAME}:
    required_outcome: "{REQUIRED_OUTCOME_KEY_2}"
    human_gate: true
    transitions:
      - to: "{TERMINAL_STATE_NAME}"
        when: "{STATE_CONDITION_EXPR_2}"
topology: {TOPOLOGY} # [chaining | routing | sequential | parallelization | orchestrator-workers | evaluator-optimizer | autonomous-agent]
trigger: {TRIGGER_TYPE} # [manual | chained | schedule | event]
max_retry_per_node: 2
---

# 🔄 MASTER FLOW: /{WORKFLOW_NAME} ({WORKFLOW_TITLE})

> **Mục tiêu**: {Mô tả mục tiêu cốt lõi, bối cảnh thực thi, ràng buộc tuyệt đối và định nghĩa "Xong" cấp toàn hệ thống.}

---

## 🏛️ 1. GOVERNANCE & CONSTITUTIONAL INVARIANTS

Workflow này đóng vai trò là **Hiến pháp (Constitution)** của hệ thống:
1. **Zero Agent Coupling (CANON 1)**: Workflow chỉ định nghĩa trạng thái cần đạt (`required_outcome`) và các bất biến toàn cục (`global_invariants`). Thẩm quyền điều phối chọn Specialist Agent và Skill hoàn toàn thuộc về Runtime Router.
2. **No Evidence $\rightarrow$ No Transition**: Không có bất kỳ State Transition nào được kích hoạt nếu chưa có bằng chứng thực thi (`Evidence`) thỏa mãn `evidence_schema`.
3. **Verdict Staleness Gate (CANON 5)**: Mọi semantic verdict phải mang `content_version`. Nếu nội dung bị thay đổi (mutation), verdict trở thành stale và workflow bắt buộc yêu cầu re-evaluation.

---

## 🔄 2. WORKFLOW NODES & TRANSITION CONTRACTS

### [NODE 1: {NODE_1_NAME}]
- **[Required Outcome]:** `{REQUIRED_OUTCOME_KEY_1}`
- **[Input Prerequisites]:** `{PREREQUISITE_STATE_KEYS}`
- **[Expected Artifact]:** `{OUTPUT_ARTIFACT_1}`
- **[Human Gate]:** `{false | true}`

- **⚡ Action Objectives (Mục tiêu kết quả cần đạt)**:
  1. **Khảo sát & Chuẩn bị**: Xác thực các điều kiện tiền đề trong State.
  2. **Thực thi Chuyên môn**: Router tự động điều phối Capability phù hợp để hoàn thành mục tiêu `{REQUIRED_OUTCOME_KEY_1}`.
  3. **Kiểm chứng Bằng chứng**: Xác thực output theo `evidence_schema`.

- **Definition of Done (DoD - State Transition Guard)**:
  - [ ] `{STATE_CONDITION_EXPR_1}` thỏa mãn 100%.
  - [ ] Evidence Artifact tồn tại và hợp lệ trên đĩa.
- **[Transition Path]:** Thỏa mãn điều kiện ➔ Chuyển `{NODE_2_NAME}` | Thất bại ➔ Áp dụng Failure Policy.

---

### [NODE 2: {NODE_2_NAME}]
- **[Required Outcome]:** `{REQUIRED_OUTCOME_KEY_2}`
- **[Input Prerequisites]:** `{REQUIRED_OUTCOME_KEY_1} == true`
- **[Expected Artifact]:** `{OUTPUT_ARTIFACT_2}`
- **[Human Gate]:** `true (1-Touch Approval Required)`

- **⚡ Action Objectives**:
  1. **Thực thi**: Router điều phối hoàn thiện `{REQUIRED_OUTCOME_KEY_2}`.
  2. **Trình duyệt**: Xuất Decision Package / Deliverable cho Người dùng / Sếp.
- **Definition of Done (DoD)**:
  - [ ] `{STATE_CONDITION_EXPR_2}` thỏa mãn.
  - [ ] User phê duyệt qua Human Gate.
- **[Transition Path]:** Phê duyệt ➔ Chuyển `{TERMINAL_STATE_NAME}`.

---

## 🛑 3. HUMAN GATES & DECISION PACKAGES

Khi workflow đi qua Node có `human_gate: true` hoặc khi Router chạm ngưỡng `escalate_human`:
- Hệ thống xuất **Decision Package**:
  ```json
  {
    "gate_type": "human_approval",
    "current_node": "{NODE_2_NAME}",
    "required_outcome": "{REQUIRED_OUTCOME_KEY_2}",
    "evidence_summary": "{PATH_TO_EVIDENCE}",
    "options": ["APPROVE", "REVISE", "ABORT"]
  }
  ```
- Dừng an toàn chờ phản hồi, tuyệt đối không tự ý vượt rào.

---

## 🛡️ 4. TRANSACTIONAL MUTATION & ROLLBACK PATTERN (Dành cho Tác vụ Đột biến Hệ thống)

Khi workflow thực hiện các thao tác có rủi ro cao (ghi đè file, sửa code, thay đổi DB, deploy), BẮT BUỘC tuân thủ 4 bước Transactional Mutation:
1. **Snapshot**: Tạo bản sao lưu hoặc ghi nhận git commit SHA / file copy trước khi sửa đổi.
2. **Mutate**: Thực hiện thao tác thay đổi dữ liệu/cấu hình trong scoped boundary.
3. **Verify**: Chạy ngay checklist hoặc test suite xác thực kết quả.
4. **Commit / Rollback**: Nếu PASS $\rightarrow$ xác nhận Commit. Nếu FAIL $\rightarrow$ tự động hoàn nguyên (Restore Snapshot / Rollback) về trạng thái an toàn trước đó.

