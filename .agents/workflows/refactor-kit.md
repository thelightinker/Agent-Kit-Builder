---
name: refactor-kit
description: "Cải tiến & Nâng cấp Agent Kit đã có sẵn theo chuẩn Delta Patch (Refactor Kit), tiêu thụ audit_findings.json và quản lý hạn ngạch repair cycle."
version: 3.0.0
requires_agents: kit-architect
requires_skills: [kit-evolving, kit-verifying]
artifact_outputs: [gap_analysis.md, delta_patch]
topology: evaluator-optimizer
trigger: chained_from_validation_or_manual
permissions: read-write
tools_allowed: [Read, Write, Edit, Glob, Grep, Bash]
safe_outputs:
  apply_delta_patch: Sửa đổi trong thư mục kit chỉ định (<kit-dir>, mặc định ./output/<kit-name>/)
max_retry_per_node: 2
---

# Workflow: /refactor-kit (Bản Vá Delta Patch & Quản Lý Chu Trình Sửa Lỗi)

Quy trình cải tiến, nâng cấp hoặc tối ưu hóa Agent Kit thông qua việc tiêu thụ trực tiếp `audit_findings.json`, lập `gap_analysis.md` và thực thi bản vá tối giản Delta Patch.

> 🚫 **NEGATIVE CONSTRAINT BẤT BIẾN**: `/refactor-kit` **TUYỆT ĐỐI KHÔNG** được phép tự cập nhật `lifecycle_state: "VALIDATED"`. Sau khi sửa chữa xong, workflow CHỈ được chuyển trạng thái sang `READY_FOR_VALIDATION` và bàn giao lại cho `/validate-kit`.

---

## 🚦 BƯỚC 0: ENTRY GUARD & SCOPE DETERMINATION

**Entry Path A — Chained from `/validate-kit` (Auto Repair):**
- Kit ở trạng thái `lifecycle_state == "NEEDS_REFACTOR"`.
- `audit_findings.json` đã có sẵn từ handoff payload → skip feedback hub audit, tiến thẳng vào Bước 1.

**Entry Path B — Manual Refactor (Feature/Improvement):**
- Người dùng yêu cầu refactor tính năng hoặc nâng cấp.
- **Central Feedback Hub Audit**: Chạy `python .agents/scripts/feedback_hub.py --audit <kit-name>` để nạp feedback chưa giải quyết.
- **Brainstorming**: Nếu scope chưa rõ hoặc thay đổi có ảnh hưởng kiến trúc → invoke `superpowers:brainstorming`.
- Nếu scope đã rõ → tiến vào Bước 1.

---

## 🔄 STATE MACHINE NODES

### Bước 1: Phân tích Sai lệch theo Bằng chứng (Targeted Gap Analysis)
- **Skill:** `kit-evolving`
- **[Input Artifacts]:** `audit_findings.json` từ handoff payload + Thư mục kit (`<kit-dir>`, mặc định `./output/<kit-name>/` hoặc đường dẫn chỉ định).
- **[Output Artifacts]:** `gap_analysis.md` (Mapping trực tiếp từ từng mã lỗi `error.code` sang chính xác file và dòng cần sửa).
- **[DoD]:** 
  - [ ] Liệt kê 100% các lỗi từ `audit_findings.json`.
  - [ ] Xác định nguyên nhân gốc rễ (Root Cause) và danh sách file cụ thể.
- **[Evaluation Loop]:** Pass ➔ Chuyển Bước 2.

---

### Bước 2: Thực hiện Bản vá & Tái Biên Dịch (Delta Patch & Recompilation)
- **Role Profile:** `@compiler` (nếu sửa prompt) hoặc `@architect` (nếu sửa skill/memory/workflow)
- **[Mandatory Grounding Template & Prerequisites]:** 
  - Chỉ nạp đúng template của loại component đang được refactor (ví dụ: refactor workflow $\rightarrow$ đọc `templates/workflow-template.md`).
  - **Đặc biệt với Skill**: Nếu tạo mới hoặc sửa đổi `skills/*/SKILL.md`, BẮT BUỘC phải nạp / kích hoạt `skill-creator` (`.agents/skills/skill-creator/SKILL.md`) kết hợp với `templates/skill-template.md`.
- **[Input Artifacts]:** `gap_analysis.md`
- **[Output Artifacts]:** Các file được sửa đổi trong thư mục kit (`<kit-dir>`) và các decision artifacts được tái biên dịch (`routing_index.json`, `invariant_rules.json`, `state_schema.json`, `task_classifier_index.json`, `evidence_schemas.json`).
- **[DoD]:**
  - [ ] Chỉ sửa đúng các khối lỗi (Delta Patch), giữ nguyên 100% các phần đang chạy tốt.
  - [ ] Thỏa mãn Evidence Gate của component được refactor.
  - [ ] Tự động chạy lại các script Compiler để cập nhật `routing_index.json`, `invariant_rules.json`, `state_schema.json`, `task_classifier_index.json`, `evidence_schemas.json` và `manifest.lock.json`.
  - [ ] Nâng SemVer patch trong YAML Frontmatter và `manifest.json` nếu có thay đổi logic.
- **[Evaluation Loop]:** Pass ➔ Chuyển Bước 3.


---

### Bước 3: Đóng Gói Handoff & Tái Thẩm Định (Handoff to Re-validation)
- **Role Profile:** `@architect` / `@compiler`
- **[Input Artifacts]:** Các file đã sửa đổi + `gap_analysis.md`.
- **[Output Artifacts]:** `lifecycle.json` cập nhật trạng thái + Handoff contract.
- **[DoD]:**
  - [ ] Ghi nhận `repair_cycle_count += 1` trong `lineage` của `lifecycle.json`.
  - [ ] Cập nhật `lifecycle_state: "READY_FOR_VALIDATION"`.
  - [ ] Thiết lập Handoff payload:
    ```json
    {
      "contract_version": "1.0.0",
      "source_workflow": "refactor-kit",
      "target_workflow": "validate-kit",
      "payload_file": "gap_analysis.md",
      "evidence_refs": ["audit_findings.json", "gap_analysis.md"],
      "notes": "Delta patch applied. Handing off for re-validation."
    }
    ```
- **[Evaluation Loop]:** Chuyển giao sang `/validate-kit` để chạy kiểm tra 3 lớp (nếu vượt quá 3 vòng repair cycle ➔ `[ESCALATE_HUMAN]`).
