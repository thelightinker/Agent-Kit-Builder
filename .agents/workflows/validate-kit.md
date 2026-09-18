---
name: validate-kit
description: "Kiểm định Chất lượng Agent Kit (Validate Kit) với Audit 3 lớp, xuất audit_findings.json và quản lý State Transition trong lifecycle.json."
version: 3.0.0
requires_agents: kit-architect
requires_skills: kit-verifying
artifact_outputs: [audit_findings.json, validation_report.md]
topology: evaluator
trigger: manual_or_chained
permissions: read-write
tools_allowed: [Read, Write, Edit, Glob, Grep, Bash]
---

# Workflow: Validate Kit (Kiểm định Chất lượng & Điều Phối State Lifecycle)

Sử dụng để kiểm tra, đánh giá và đóng dấu trạng thái chính thức (`VALIDATED` / `NEEDS_REFACTOR` / `NEEDS_HUMAN_INTERVENTION`) cho Agent Kit thông qua **Evidence Gate**.

> 🛡️ **INVARIANT TOÀN HỆ THỐNG**: `/validate-kit` là workflow **DUY NHẤT** sở hữu thẩm quyền chuyển đổi trạng thái sang `VALIDATED` dựa trên bằng chứng máy đọc được `audit_findings.json`.

---

## 🔄 STATE MACHINE NODES

### Bước 1: Khởi tạo Kiểm định & Tải State
- **Role Profile:** `@auditor` | **Skill:** `kit-verifying`
- **[Input Artifacts]:** Thư mục kit (`./output/<kit-name>/`) kèm `lifecycle.json`.
- **[Output Artifacts]:** Bối cảnh thẩm định sẵn sàng.
- **[DoD]:**
  - [ ] `lifecycle_state == "READY_FOR_VALIDATION"`.
  - [ ] Tải đầy đủ metadata và kiểm tra file inventory.
- **[Evaluation Loop]:** Pass ➔ Bước 2 | Fail ➔ Dừng lại và yêu cầu chuẩn bị kit (`[ESCALATE_HUMAN]`).

---

### Bước 2: Chạy 3 Lớp Kiểm tra (3-Layer Audit) & Xuất Bằng Chứng
- **Role Profile:** `@auditor` | **Skill:** `kit-verifying`
- **[Input Artifacts]:** Toàn bộ component files của kit.
- **[Output Artifacts]:** `audit_findings.json`, `validation_report.md`.
- **[DoD]:**
  - [ ] Lớp 1 (L1 Deterministic Linting & Compiler Gates): `validate_kit.py` chạy qua 100% structural anchors, frontmatter, và 9 compile-time checks (reachability, cycle, coverage, dead states, state keys, namespace, negative scope, evidence schema, artifact freshness).
  - [ ] Chạy `dry_run_simulation.py` đạt 100% PASS (0 deadlocks, 0 unreachable nodes).
  - [ ] Lớp 2 (L2 Adaptive Scenario Testing): Tóm tắt đời thường (3-5 dòng), DoD 100% nhị phân.
  - [ ] Lớp 3 (L3 Adversarial Stress Testing): Giả lập edge cases, kiểm tra độ bền vững DoD.
- **[Evaluation Loop]:** Pass ➔ Bước 3.


---

### Bước 3: Đóng Dấu Verdict & Chuyển Giao Handoff (Authority Matrix)
- **Role Profile:** `@auditor`
- **[Input Artifacts]:** `audit_findings.json`, `lifecycle.json`.
- **[Output Artifacts]:** `lifecycle.json` cập nhật verdict mới + Handoff payload.
- **[DoD]:**
  - [ ] Nhánh A (PASS - `errors == 0`): Cập nhật `lifecycle_state: "VALIDATED"`, `verdicts.validation.pass: true`, điểm $\ge 4/5$ ⭐.
  - [ ] Nhánh B (FAIL - `errors > 0`): Nếu `repair_cycle_count < 3` ➔ Cập nhật `lifecycle_state: "NEEDS_REFACTOR"` và handoff sang `/refactor-kit`; nếu `repair_cycle_count >= 3` ➔ Cập nhật `lifecycle_state: "NEEDS_HUMAN_INTERVENTION"`.
- **[Evaluation Loop]:** PASS ➔ Hoàn tất (hoặc chuyển sang `/remember-kit` nếu 5/5 ⭐) | FAIL ➔ Chuyển giao sang `/refactor-kit` (nếu vượt quá 3 cycles ➔ `[ESCALATE_HUMAN]`).
