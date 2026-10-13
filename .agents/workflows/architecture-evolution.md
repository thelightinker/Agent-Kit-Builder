---
name: architecture-evolution
description: "Quy trình tiến hóa & nâng cấp kiến trúc an toàn cho Agent Kit dựa trên Bản đồ Kiến trúc Sống (Living Map): Đọc Map → Định vị Layer → Đánh giá Tác động → Duyệt Đề xuất → Thực thi → Tái kiểm định → Đồng bộ Map."
version: 1.0.0
requires_agents: [kit-architect]
requires_skills: [architecture-mapping, kit-evolving, kit-verifying]
artifact_outputs: [impact_assessment.md, change_proposal.md, validation_report.md, map.md]
topology: sequential-state-machine
trigger: manual
permissions: read-write
tools_allowed: [Read, Grep, Glob, Edit, Write, Bash]
safe_outputs:
  map_synchronization_lock: "Bản đồ map.md bắt buộc phải được đồng bộ và 100% test PASS trước khi hoàn tất tiến hóa kiến trúc"
max_retry_per_node: 2
recovery:
  idempotent: true
  resume_from_last_valid_state: true
  prevent_duplicate_artifacts: true
  prevent_infinite_handoff: true
---

# Workflow: Architecture Evolution (Giao Thức Tiến Hóa Kiến Trúc)

> **Mục tiêu**: Hướng dẫn quy trình tiến hóa kiến trúc an toàn, có kiểm soát dựa trên Bản đồ Kiến trúc Sống (`map.md`), ngăn chặn sự thoái hóa kiến trúc (*Architectural Drift*) và vỡ ma trận phụ thuộc khi nâng cấp.

---

## 🏛️ 1. GOVERNANCE LAYER (HÀNG RÀO PHÁP LÝ & AN TOÀN)

1. **Change Gate Protocol**: Khi bắt đầu, mở `active_change_gate: "architecture_evolution"` trong `lifecycle.json`. Khi kết thúc, bắt buộc đóng gate `active_change_gate: null`.
2. **Map-First Enforcement**: Mọi hành động sửa đổi cấu phần kiến trúc đều phải bắt đầu từ việc đọc và phân tích `map.md`. Nếu `map.md` chưa tồn tại, invoke `architecture-mapping` skill để sinh map ban đầu trước khi tiếp tục.
3. **Blast Radius Gate**: Bắt buộc lượng hóa phạm vi tác động (Direct, Indirect, Invariant Risks) trong `impact_assessment.md` trước khi can thiệp code.
4. **Zero-Degradation Guarantee**: Sau khi nâng cấp, toàn bộ test suite hiện có phải đạt 100% PASS và không làm tổn hại các Invariants bất biến.
5. **Mandatory Map Sync & Re-validation**: `map.md` phải được cập nhật phản ánh đúng trạng thái thực tế mới nhất, chuyển trạng thái `lifecycle_state: "READY_FOR_VALIDATION"` và bàn giao cho `/validate-kit`.

---

## 🏗️ 2. ORCHESTRATION LAYER & TRANSITION MATRIX

### 2.1. Shared State Schema (SSOT via lifecycle.json)
```json
{
  "lifecycle_state": "READY_FOR_VALIDATION",
  "active_change_gate": "architecture_evolution | null",
  "handoff": {
    "source_workflow": "architecture-evolution",
    "target_workflow": "validate-kit",
    "payload_file": "impact_assessment.md",
    "evidence_refs": ["map.md", "impact_assessment.md", "change_proposal.md"],
    "notes": "Architecture evolution completed. Handing off to validate-kit for regression test."
  }
}
```

### 2.2. Evidence-Gated Transition Matrix
| Current State | Target State | Required Evidence / Artifact | Transition Assertion Guard | Allowed Epistemic Status | Remediation Path (On Fail) | Max Retries |
|:---|:---|:---|:---|:---|:---|:---|
| `INIT` | `READ_MAP` | `map.md` exists | `file_exists(map.md) == true` | `[CONFIRMED]` | Invoke `architecture-mapping` skill để sinh map ban đầu | 1 |
| `READ_MAP` | `LOCATE_LAYER` | Map Invariants read | `map_context_loaded == true` | `[CONFIRMED]` | Re-read map.md | 1 |
| `LOCATE_LAYER` | `ASSESS_IMPACT` | Target Component Identified | `target_layer_defined == true` | `[CONFIRMED]` | Clarify target layer | 2 |
| `ASSESS_IMPACT` | `[GATE: Proposal_Approval]` | `impact_assessment.md` | `file_exists(impact_assessment.md) == true` | `[CONFIRMED]` | Re-evaluate dependencies | 2 |
| `[GATE: Proposal_Approval]` | `IMPLEMENT` | User Signoff | `proposal.approved == true` | `[CONFIRMED]` | Revise change scope | — |
| `IMPLEMENT` | `VALIDATE` | Modified files | `files_modified == true` | `[CONFIRMED]` | Rollback & re-implement | 2 |
| `VALIDATE` | `UPDATE_MAP` | `validation_report.md` | `tests_passed == 100% && lint_errors == 0` | `[CONFIRMED]` | Fix regression bugs | 2 |
| `UPDATE_MAP` | `VERIFIED` | Updated `map.md` | `map_synced == true` | `[CONFIRMED]` | Sync missing components | 1 |

---

## 🔄 3. INTELLIGENCE LAYER & NODE EXECUTION (5-Part Node Anatomy)

### [STATE: READ_MAP & LOCATE_LAYER]
- **Responsible Agent / Role**: `kit-architect` | `architecture-mapping`
- **Input Artifacts**: `map.md`
- **Output Artifacts & Contract**:
  ```yaml
  artifact:
    name: architecture_context
    type: in_memory_context
    schema: map_context_schema
    mutability: read_only
    provenance: living_map
  ```
- **Decision Policy**:
  ```yaml
  mode: deterministic_reader
  objective: Định vị chính xác tầng trong 7 tầng quyền lực (Author/Constitution/Craft/Writer/Sensor/Editor/Release)
  stop_when: layer_and_component_identified
  ```
- **DoD**: Xác định đúng danh tính component và tầng kiến trúc tương ứng.

---

### [STATE: ASSESS_IMPACT & PROPOSE_CHANGE]
- **Responsible Agent / Role**: `kit-architect` | `architecture-mapping` + `kit-evolving`
- **Input Artifacts**: `map.md`, Yêu cầu nâng cấp mới
- **Output Artifacts & Contract**:
  ```yaml
  artifacts:
    - name: impact_assessment.md
      type: design_doc
      schema: templates/gap-analysis-schema
      mutability: draft
      provenance: blast_radius_analysis
    - name: upgrade_proposal.json
      type: data_payload
      schema: schemas/upgrade_proposal.schema.json
      mutability: draft
      provenance: evidence_extraction
  ```
- **Decision Policy & Automated Gate**:
  ```yaml
  mode: evaluator-optimizer
  objective: Lượng hóa Blast Radius và tạo upgrade_proposal.json
  scope_routing:
    small_change: "Quick impact check in-chat (≤2 components affected) — skip upgrade_gate_evaluator.py"
    large_change: "Full automated gate: python .agents/scripts/upgrade_gate_evaluator.py upgrade_proposal.json"
  stop_when: impact_assessed_and_proposal_ready
  ```
- **DoD**: 
  - [ ] `impact_assessment.md` nêu rõ Layer cần sửa, Blast Radius và Rủi ro.
  - [ ] `upgrade_proposal.json` hợp lệ theo schema và vượt qua `upgrade_gate_evaluator.py` (Decision: `KEEP` hoặc `ADAPT`).


---

### [STATE: IMPLEMENT & VALIDATE]
- **Responsible Agent / Role**: `kit-architect` | `kit-evolving` + `kit-verifying`
- **Input Artifacts**: `impact_assessment.md` (Đã duyệt)
- **Output Artifacts**: Mã nguồn đã chỉnh sửa, `validation_report.md`
- **Decision Policy**:
  ```yaml
  mode: test-driven-execution
  objective: Triển khai theo nguyên tắc Delta Patch tối thiểu, chạy toàn bộ test suite để đảm bảo không gãy regression
  stop_when: all_tests_pass
  ```
- **DoD**: 100% tests trong bộ kiểm thử tự động PASS, không có lỗi linting.

---

### [STATE: UPDATE_MAP]
- **Responsible Agent / Role**: `kit-architect` | `architecture-mapping`
- **Input Artifacts**: Cấu phần mới được cập nhật, `validation_report.md`
- **Output Artifact**: `map.md` (Phiên bản mới)
- **Decision Policy**:
  ```yaml
  mode: map_synchronization
  objective: Cập nhật danh mục component, dependencies, contracts và version trong map.md
  stop_when: map_fully_synced
  ```
- **DoD**: `map.md` phản ánh 100% đúng trạng thái mới của hệ thống.

---

## 🛑 4. FIRST-CLASS HUMAN GATES

| Gate ID | Tên Điểm Chốt | Vị Trí Kích Hoạt | Đầu Vào Thẩm Định | Quyền Quyết Định | Hành Động Khi APPROVE | Hành Động Khi REVISE |
|:---|:---|:---|:---|:---|:---|:---|
| **Gate: Evolution Signoff** | Duyệt Đề Xuất Tiến Hóa | Sau Bước ASSESS_IMPACT | `impact_assessment.md`<br>`upgrade_proposal.json`<br>(Đã qua `upgrade_gate_evaluator.py`) | User / Tác giả | Cho phép tiến hành sửa mã nguồn | Thu hẹp phạm vi hoặc hủy nâng cấp |


---

## 🚨 5. ESCALATE HUMAN CHECKPOINT

- **Kích hoạt khi**: Phát hiện nguy cơ vi phạm các Invariants bất biến (*Truth > Thesis, Asset Loss, Fake Passes*) hoặc test regression không thể giải quyết sau 2 lần retry.
- **Output Artifact**: `evolution_escalation.md`.
- **Constraint**: Đóng băng mọi thay đổi, khôi phục trạng thái gần nhất từ git/backup.
