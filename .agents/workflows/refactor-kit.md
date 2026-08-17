---
name: refactor-kit
description: "Cải tiến & Nâng cấp Agent Kit đã có sẵn theo chuẩn Delta Patch (Refactor Kit)."
version: 2.1.0
requires_agents: kit-architect
requires_skills: [kit-evolving, kit-verifying]
artifact_outputs: [gap_analysis, delta_patch, validation_report]
---

# Workflow: /refactor-kit

Quy trình cải tiến, nâng cấp hoặc tối ưu hóa Agent Kit đã có sẵn thông qua Gap Analysis và Delta Patch, có bảo vệ bởi Superpowers Process Gate.

---

## 🚦 BƯỚC 0: SUPERPOWERS PROCESS & SKILL GATE (BẮT BUỘC)

Trước khi chỉnh sửa bất kỳ file nào trong `./output/<kit-name>/`:

1. **Invoke Brainstorming:** BẮT BUỘC invoke `superpowers:brainstorming`.
2. **Khóa Refactor Scope:** Thống nhất với User: Điểm cần sửa, Nguyên nhân gốc rễ, Phạm vi ảnh hưởng và SemVer bump (`patch` hay `minor`).
3. **Approval Gate:** Nhận sự phê duyệt (`APPROVED`) từ User cho Refactor Plan trước khi sửa code.
   - 🚫 **HARD CONSTRAINT:** Không tự ý sửa file kit khi chưa xác định rõ Gap Analysis và nhận được sự đồng thuận.
   - ⚠️ **Quy tắc Bypass:** Chỉ cho phép bypass khi chạy script tự động (như `export_kit.py` hay `generate_manifest.py`) không làm thay đổi logic nghiệp vụ.

---

## 🔄 STATE MACHINE NODES

### Bước 1: Phân tích Sai lệch (Gap Analysis)
- **Skill:** `kit-evolving`
- **[Input Artifacts]:** Thư mục kit hiện tại (`./output/<kit-name>/`) + Feedback/Yêu cầu mới.
- **[Output Artifacts]:** `gap_analysis.md` (Liệt kê chính xác điểm thiếu sót hoặc cần tối ưu).
- **[DoD]:** 
  - [ ] Chỉ ra đúng nguyên nhân gốc rễ (Root Cause).
  - [ ] Liệt kê danh sách file cụ thể bị tác động.
- **[Evaluation Loop]:** Pass ➔ Chuyển Bước 2.

---

### Bước 2: Thực hiện Bản vá (Delta Patch)
- **Role Profile:** `@compiler` (nếu sửa prompt) hoặc `@architect` (nếu sửa skill/memory)
- **[Input Artifacts]:** `gap_analysis.md`
- **[Output Artifacts]:** Các file được sửa đổi trong `./output/<kit-name>/`.
- **[DoD]:**
  - [ ] Chỉ sửa các khối cần thiết (Delta Patch), giữ nguyên 100% các phần đang chạy tốt.
  - [ ] Nâng version trong YAML Frontmatter và `manifest.json` theo chuẩn SemVer.
- **[Evaluation Loop]:** Pass ➔ Chuyển Bước 3.

---

### Bước 3: Tái kiểm định & Nghiệm thu (Re-verification)
- **Role Profile:** `@auditor` | **Skill:** `kit-verifying`
- **[Input Artifacts]:** Kit sau khi refactor.
- **[Output Artifacts]:** `validation_report.md`
- **[DoD]:**
  - [ ] `validate_kit.py` trả về `0 error(s)`.
  - [ ] Regression test không bị gãy bất kỳ tiêu chí nào trước đó.
- **[Evaluation Loop]:** Pass ➔ Hoàn tất & Bàn giao.
