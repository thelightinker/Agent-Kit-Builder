---
name: {WORKFLOW_NAME}
description: {DESCRIPTION_OF_WORKFLOW_PURPOSE_AND_TRIGGERS}
version: 1.0.0
requires_agents: [{REQUIRED_AGENT_1}]
requires_skills: [{REQUIRED_SKILL_1}, {REQUIRED_SKILL_2}]
artifact_outputs: [{OUTPUT_1}, {OUTPUT_2}]
# === MASTER FRAMEWORK EXTENSIONS (Compile-Time) ===
topology: {TOPOLOGY} # [chaining | routing | parallelization | orchestrator-workers | evaluator-optimizer | autonomous-agent]
trigger: {TRIGGER_TYPE} # [manual | schedule | event]
permissions: {PERMISSIONS} # mặc định: read-only
tools_allowed: [{TOOL_1}, {TOOL_2}] # namespaced & consolidated tools
safe_outputs:
  {SAFE_ACTION}: {RANG_BUOC_CU_THE}
max_retry_per_node: 2
---

# Workflow Master Template: {WORKFLOW_TITLE}

> **Mục tiêu**: {Mô tả mục tiêu bằng ngôn ngữ tự nhiên như giải thích cho đồng nghiệp mới: bối cảnh dự án, constraint tuyệt đối, định nghĩa "xong" cấp toàn workflow.}

---

## 🏗️ [WORKFLOW META & TOPOLOGY]

- **Topology Selected**: `{TOPOLOGY}` (Đã qua kiểm tra Complexity Ladder - chọn giải pháp tối giản nhất)
- **Shared State Schema**:
  ```json
  {
    "workflow_state": {
      "session_id": "string",
      "input_artifacts": "object",
      "output_artifacts": "object",
      "status": "pending | running | needs_human_review | completed"
    }
  }
  ```
- **Context & Tool Strategy**: Just-in-Time retrieval + Namespaced/Consolidated Tools (không pre-load thừa).

---

## 🔄 State Machine & Node Execution (5-Part Node Anatomy)

### [STATE: INIT]
- **Input Artifacts**: `{INITIAL_INPUT_ARTIFACTS}` (Artifacts Isolation - chỉ nạp đúng khoá dữ liệu cần thiết)
- **Output Artifacts**: `workflow_state.{INIT_KEY}`
- **Definition of Done (DoD - 3 Kiểm định nhị phân)**:
  - [ ] `{DOD_COND_1}` (Binary: Pass/Fail rõ ràng)
  - [ ] `{DOD_COND_2}` (Measurable: Đo trực tiếp từ Output Artifact)
  - [ ] `{DOD_COND_3}` (Concrete: Không dùng tính từ sáo ngữ "chuyên nghiệp/đầy đủ")
- **Evaluation Loop & Checkpoint Gate**:
  - Checkpoint Command: `python .agents/scripts/checkpoint_gate.py --node {INIT_KEY} --target {TARGET_OUTPUT} --op {OP}`
  - Risk Tier: `{RISK_TIER}` | Reason: `{REASON_CODE}` | Decided By: `orchestrator`
  - Evaluate output ➔ Pass ➔ Transition sang `[STATE: {STEP_1_NAME}]`
  - Fail ➔ Revise (Tối đa `{MAX_RETRY}` lần) ➔ Vượt ngưỡng ➔ Escalate sang `[ESCALATE_HUMAN]`


---

### [STATE: {STEP_1_NAME}]
- **Input Artifacts**: `workflow_state.{INIT_KEY}`
- **Output Artifacts**: `workflow_state.{STEP_1_OUTPUT_KEY}`
- **Definition of Done (DoD)**:
  - [ ] `{STEP_1_DOD_1}`
  - [ ] `{STEP_1_DOD_2}`
- **Evaluation Loop & Transition**: 
  - Evaluate output ➔ Pass ➔ Transition sang `[STATE: {STEP_2_NAME}]`
  - Fail ➔ Revise ➔ Retry ➔ (Transition ngược nếu phát hiện mâu thuẫn evidence: ➔ `[STATE: INIT]`)

---

### [STATE: NODE_FINALIZE]
- **Input Artifacts**: Toàn bộ `workflow_state`
- **Output Artifacts**: `{DELIVERABLE_CUOI_CUNG}`
- **Definition of Done (DoD)**:
  - [ ] Không mâu thuẫn chéo giữa các Output Artifacts của các node.
  - [ ] Mọi Safe Outputs đã qua độc lập validation gate trước khi áp dụng thật.
- **Evaluation Loop**: Evaluate ➔ Pass ➔ Done ➔ `[*]`. Fail ➔ Revise ➔ `[ESCALATE_HUMAN]`.

---

## 🚨 [ESCALATE_HUMAN] (Human Checkpoint)

- **Kích hoạt khi**: Node bất kỳ fail DoD vượt quá `max_retry_per_node` hoặc chạm Tool Risk Tier cao.
- **Output Artifact**: Draft hiện tại + Log lý do fail mỗi lần Evaluation + `needs_human_review: true`.
- **Constraint**: KHÔNG tự động publish khi ở trạng thái này.

---

## ⏳ [SESSION HANDOFF] (Chỉ áp dụng cho Long-running Workflows nhiều phiên)

- **Progress File**: `memory/progress-notes.md`
- **Feature List**: `memory/feature_list.json` (`{"category": "...", "description": "...", "passes": false}`)
- **Nghi thức đầu phiên**: 
  1. `pwd` ➔ Xác nhận phạm vi thư mục được phép sửa.
  2. Read progress & git log ➔ Nắm bối cảnh công việc phiên trước.
  3. Read `feature_list.json` ➔ Chọn 1 feature `passes: false` ưu tiên cao nhất.
  4. Run `init.sh` ➔ Kiểm tra môi trường còn chạy tốt trước khi code tiếp.

---

## 📋 Quy trình Tự kiểm trước khi Publish (Pre-Publish Audit Checklist)

- [ ] **Complexity Ladder**: Xác nhận giải pháp đơn giản nhất KHÔNG giải quyết được task này?
- [ ] **Multi-Agent Check**: Nếu có sub-agents song song, đã xác nhận sub-tasks hoàn toàn độc lập (breadth-first)?
- [ ] **5-Part Node Anatomy**: Tất cả các node đều đủ `[STATE]`, `[Input Artifacts]`, `[Output Artifacts]`, `[DoD]`, `[Evaluation Loop]`?
- [ ] **3-Check DoD**: DoD có tính nhị phân, đo được từ Output Artifact, 0 tính từ sáo ngữ?
- [ ] **Context & ACI**: Áp dụng Just-in-Time retrieval và Tool Namespacing/Consolidation?
- [ ] **Escalate Path**: Đã khai báo tường minh đường dẫn `[ESCALATE_HUMAN]`?
