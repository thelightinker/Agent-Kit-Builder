---
name: evolve-kit
description: "Quy trình tiến hóa tự động 1 lệnh duy nhất tại Engine: Ingest Inbox -> Ledger SSOT -> Freeze Full-Kit Snapshot -> Validate L1-L3 -> Tier 2 Human Gate -> Release SemVer -> Sync Test Workspace."
version: 2.0.0
requires_agents: [kit-architect]
requires_skills: [kit-evolving, kit-verifying]
artifact_outputs: [EVOLUTION_LEDGER.json, snapshot_manifest.json, EVOLUTION_HISTORY.json]
topology: sequential
trigger: manual
permissions: read-write
tools_allowed: [Read, Write, Edit, Glob, Grep, Bash]
safe_outputs:
  evidence_integrity: "Không bao giờ ghi đè bản duy nhất; luôn đóng băng snapshot trước khi release vNext."
max_retry_per_node: 2
---

# 🔄 MASTER FLOW: /evolve-kit (Unified Single-Command Evolution Orchestrator)

> **Mục tiêu**: Điều phối toàn diện chu trình tiến hóa từ phản hồi thực chiến sang phiên bản mới: Đọc inbox, ghi nhận Sổ Cái Quyền Lực (SSOT Ledger), đóng băng Full-Kit Snapshot, kiểm định 3 lớp, duyệt rủi ro phân tầng, tăng SemVer và đồng bộ an toàn sang Test Workspace.

---

## 🏛️ 1. GOVERNANCE & THE 4 INVARIANTS

1. **Never Mutate The Only Copy**: Mọi đợt tiến hóa BẮT BUỘC chụp snapshot đóng băng toàn bộ thư mục Kit (Full Root Scope) kèm bảng mã băm SHA-256 trước khi áp dụng thay đổi.
2. **Every Change Must Have An Identity**: Mọi patch phải có `run_id`, `snapshot_ref`, danh sách `feedbacks_addressed` và hash diff cụ thể.
3. **Every Feedback Must Have A Status**: Di chuyển chuẩn mực qua 6 pha (`RECEIVED` ➔ `TRIAGED` ➔ `DIAGNOSED` ➔ `PATCHED` ➔ `VERIFIED` ➔ `RELEASED`).
4. **Every RESOLVED Claim Must Have Verification Evidence**: Chỉ release khi có bằng chứng thực thi xác thực từ `validate_kit.py` (Linter Pass, Score 5/5 ⭐).

---

## 🔄 2. STATE NODES & ACTION EXECUTION

### [STATE 1: INGEST_AND_LEDGER] (Nạp Batch & Khởi Tạo Sổ Cái)
- **Role Profile:** `kit-architect` | **Skill:** `kit-evolving`
- **[Input Artifacts]:** Batches trong `evolution/inbox/`.
- **[Output Artifacts]:** Entry cập nhật trong `evolution/state/kits/<kit-name>-ledger.json`.
- **[DoD]:**
  - [ ] 100% feedback items được chuyển sang trạng thái `RECEIVED` và `TRIAGED`.
  - [ ] Batch gốc được chuyển sang `evolution/completed/` để tránh xử lý trùng.
- **[Evaluation Loop]:** Pass ➔ Chuyển sang State 2; Fail ➔ [ESCALATE_HUMAN].

- **⚡ Action Prompts & Execution Steps**:
  ```bash
  python .agents/scripts/evolution_orchestrator.py <kit-name> --bump minor
  ```

---

### [STATE 2: FREEZE_SNAPSHOT] (Đóng Băng Phiên Bản Cũ)
- **Role Profile:** `kit-architect` | **Skill:** `kit-evolving`
- **[Input Artifacts]:** Thư mục Kit hiện tại (Full Root Scope).
- **[Output Artifacts]:** `evolution/snapshots/<kit-name>/v<old_version>-<hash>/` kèm `snapshot_manifest.json`.
- **[DoD]:**
  - [ ] Thư mục snapshot chứa toàn bộ file của kit kèm `snapshot_manifest.json`.
  - [ ] Root hash và tree checksum được tính toán chính xác 100%.
- **[Evaluation Loop]:** Pass ➔ Chuyển sang State 3; Fail ➔ Rollback & [ESCALATE_HUMAN].

---

### [STATE 3: VALIDATE_AND_GATE] (Kiểm Định 3 Lớp & Human Approval Gate)
- **Role Profile:** `kit-architect` | **Skill:** `kit-verifying`
- **[Input Artifacts]:** Codebase kit đã vá trong Staging/Output.
- **[Output Artifacts]:** Verification Evidence Log (Linter Score $\ge 4/5$, 0 errors).
- **[Risk-Tier Handling]:**
  - **Tier 0/1**: Tự động thông qua nếu 100% L1-L3 test pass.
  - **Tier 2 (Architectural)**: Dừng lại, trình bày diff và yêu cầu Human Sign-off.
- **[DoD]:**
  - [ ] `validate_kit.py` trả về `0 error(s)`.
  - [ ] Bằng chứng kiểm định được lưu vào Ledger.
- **[Evaluation Loop]:** Pass ➔ Chuyển sang State 4; Fail ➔ Repair Cycle (Tối đa 3 lần) ➔ [ESCALATE_HUMAN].

---

### [STATE 4: RELEASE_AND_SYNC] (Tăng SemVer & Đồng Bộ Test Workspace)
- **Role Profile:** `kit-architect` | **Skill:** `kit-evolving`
- **[Input Artifacts]:** Release metadata.
- **[Output Artifacts]:** `VERSION`, `manifest.json`, `lifecycle.json` cập nhật `vNext`; `EVOLUTION_HISTORY.json` mirror được ghi vào Kit.
- **[DoD]:**
  - [ ] SemVer được tăng đúng quy chuẩn (`patch`/`minor`/`major`).
  - [ ] Toàn bộ feedback items liên quan chuyển sang trạng thái `RELEASED`.
  - [ ] Code sạch được sync sang Test Workspace (bảo toàn test data).
- **[Evaluation Loop]:** Pass ➔ Hoàn tất quy trình; Fail ➔ [ESCALATE_HUMAN].

---

## 🤝 3. HANDOFF CONTRACT

```json
{
  "contract_version": "2.0.0",
  "source_workflow": "evolve-kit",
  "target_workflow": "test-execution",
  "status": "RELEASED",
  "evidence_refs": ["EVOLUTION_LEDGER.json", "snapshot_manifest.json", "EVOLUTION_HISTORY.json"]
}
```

---

## 🚨 4. ESCALATE HUMAN CHECKPOINT ([ESCALATE_HUMAN])

- **Kích hoạt khi**: Lỗi snapshot, sai lệch checksum, hoặc linter fail quá 3 vòng sửa chữa.
- **Hành động**: Dừng tiến trình, khôi phục snapshot an toàn và báo cáo trực tiếp cho sếp.
