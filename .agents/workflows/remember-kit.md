---
name: remember-kit
description: "Workflow lưu đúc rút kinh nghiệm, thiết kế pattern và ví dụ kit xuất sắc (5/5 ⭐) vào bộ nhớ dài hạn MEMORY.md, chuyển trạng thái sang EXEMPLAR_ARCHIVED."
version: 3.0.0
requires_agents: kit-architect
requires_skills: kit-evolving
artifact_outputs: [memory_ref, lifecycle.json]
topology: sequential
trigger: manual_or_chained
permissions: read-write
tools_allowed: [Read, Write, Edit, Glob, Grep, Bash]
---

# Workflow: Remember Kit (Cập nhật Bộ nhớ Dài hạn & Khóa Exemplar)

Sử dụng để lưu trữ các Agent Kit mẫu đạt tiêu chuẩn xuất sắc (5/5 ⭐) hoặc bài học thiết kế đắt giá vào Scoped Memory dài hạn.

> 🛡️ **HARD INVARIANT BẤT BIẾN**: `/remember-kit` **CHỈ ĐƯỢC PHÉP** thăng cấp một Agent Kit khi kit đó đã đạt trạng thái `lifecycle_state == "VALIDATED"`, `verdicts.validation.pass == true` và `score == 5/5 ⭐`. Tuyệt đối không lưu các bản thảo sơ khai (Draft) chưa qua kiểm định.

---

## 🔄 STATE MACHINE NODES

### Bước 1: Tiếp nhận Nội dung & Kiểm tra Invariant
- **Role Profile:** `@architect` | **Skill:** `kit-evolving`
- **[Input Artifacts]:** Thư mục kit (`./output/<kit-name>/`) kèm `lifecycle.json` và `audit_findings.json`.
- **[Output Artifacts]:** Quyết định tiếp nhận hoặc từ chối lưu memory.
- **[DoD]:**
  - [ ] `lifecycle_state == "VALIDATED"`
  - [ ] `verdicts.validation.pass == true`
  - [ ] `verdicts.validation.score == 5`
- **[Evaluation Loop]:** Đạt đủ điều kiện ➔ Bước 2 | Chưa đạt 5/5 ⭐ ➔ Dừng lại và yêu cầu hoàn thiện qua `/refactor-kit` (nếu có tranh chấp ➔ `[ESCALATE_HUMAN]`).

---

### Bước 2: Bóc Tách Pattern & Cập nhật Scoped Memory
- **Role Profile:** `@architect` | **Skill:** `kit-evolving`
- **[Input Artifacts]:** Kit artifacts đã được xác thực 5/5 ⭐.
- **[Output Artifacts]:** `memory/golden-examples/[kit-name].md`, `memory/kit-patterns.md`, `memory/MEMORY.md`.
- **[DoD]:**
  - [ ] Tạo file ghi chép ví dụ trong `memory/golden-examples/[kit-name].md`.
  - [ ] Cập nhật danh mục và mô tả ngắn gọn vào `memory/MEMORY.md` (giữ index $\le 200$ dòng).
  - [ ] Thêm bài học mới vào `memory/kit-patterns.md`.
- **[Evaluation Loop]:** Pass ➔ Bước 3 | Fail ➔ Bổ sung thông tin memory.

---

### Bước 3: Đóng Dấu Thăng Cấp (Lifecycle Mutation to EXEMPLAR_ARCHIVED)
- **Role Profile:** `@architect`
- **[Input Artifacts]:** Entries memory mới tạo tại Bước 2.
- **[Output Artifacts]:** `lifecycle.json` cập nhật `EXEMPLAR_ARCHIVED`.
- **[DoD]:**
  - [ ] Ghi nhận `verdicts.memory_promotion.promoted: true`.
  - [ ] Ghi nhận `verdicts.memory_promotion.memory_ref: "memory/golden-examples/[kit-name].md"`.
  - [ ] Chuyển trạng thái kit sang `lifecycle_state: "EXEMPLAR_ARCHIVED"`.
  - [ ] Cập nhật `handoff.target_workflow: "completed"`.
  - [ ] `memory/MEMORY.md` có link hợp lệ tới entry mới.
- **[Evaluation Loop]:** Hoàn tất quy trình lưu trữ exemplar.
