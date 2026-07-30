# Dynamic Checkpoint System — Architecture & Design Spec v1.1 (Production-Ready)

## 0. Purpose & Low-Tech Philosophy

### Purpose
Bổ sung hệ thống Checkpoint phân tầng rủi ro, tiết kiệm token, được điều phối bởi Orchestrator vào cơ chế `[Evaluation Loop]` ➔ `[ESCALATE_HUMAN]` của Workflow Contract.

### Triết lý "Cực mạnh bên dưới — Cực dễ bên trên" (Low-Tech / Zero-Touch UX)
1. **Zero-Configuration Defaults**: Hệ thống tự động phân loại rủi ro (Risk Tiering) dựa trên ma trận 2 chiều: **Vị trí file (Path)** x **Hành động (Operation: create | modify | delete)**.
2. **Human-Readable Envelope**: Khi cần con người duyệt (T2/T3), giao diện hiển thị dạng Markdown trực quan với Emoji chỉ báo rủi ro (🟢 T0 | 🔵 T1 | 🟡 T2 | 🔴 T3).
3. **Risk-Appropriate Decision Guard**:
   - Với **T2**: Duyệt nhanh bằng 1 phím (`1` Approve | `2` Revise | `3` Reject).
   - Với **T3**: Chống ấn nhầm phản xạ bằng mã xác nhận động (**CONFIRM <4-digit-code>** hoặc gõ tên node).

---

## 1. Kiến trúc 3 Engine Độc lập (Modular Engine Architecture)

```
Orchestrator Node ([Evaluation Loop])
       │
       ▼
checkpoint_gate.py ───┬──► GuardEngine (Scoped SHA-256 Hash, Staleness Guard, Rollback)
                      ├──► ImpactEngine (2D Blast Radius, Risk-Prioritized Diff ≤ 15 dòng)
                      └──► TrustEngine (Log history, Trust Score, Proposal Hạ Tier, Batcher)
```

### 1.1 GuardEngine (`guard_engine.py`)
- **Scoped State Hashing (Sửa lỗi Hash Scope)**: Chỉ mã hóa SHA-256 đối với **các file/artifact cụ thể mà Node đó được phép đọc/ghi** (dựa theo khai báo `[Input Artifacts]` và `[Output Artifacts]`). KHÔNG hash toàn bộ thư mục output để tránh Auto-Invalidate nhầm khi có tiến trình song song.
- **Dual-Hash Staleness Guard**:
  - Sinh `state_hash_pause` trước khi tạm dừng.
  - Khi resume, sinh `state_hash_resume`. Nếu các file mục tiêu bị thay đổi bên ngoài, checkpoint tự động **Auto-Invalidate** và rollback về snapshot an toàn.
- **State Snapshot**: Lưu bản sao lưu khẩn cấp của các file mục tiêu trước khi mở Envelope.

### 1.2 ImpactEngine (`impact_engine.py`)
- **Ma trận Rủi ro 2 Chiều (2D Blast Radius Matrix)**:
  Tính toán Risk Tier kết hợp giữa **Vị trí File** và **Loại Thao tác (Operation)**:

  | Operation \ Path | LOW (File tạm / Log / Draft) | MEDIUM (Output Kit artifacts) | HIGH (`.agents/rules/`, `manifest.json`, `ARCHITECTURE.md`) |
  |---|---|---|---|
  | **`create`** | 🟢 T0 / 🔵 T1 | 🔵 T1 / 🟡 T2 | 🟡 T2 |
  | **`modify`** | 🔵 T1 | 🟡 T2 | 🔴 T3 |
  | **`delete`** | 🟡 T2 *(Auto +1 Tier)* | 🔴 T3 *(Auto +1 Tier)* | 🔴 T3 *(Crucial Lock)* |

- **Thuật toán Nén Diff theo Độ Nguy Hiểm (Risk-Prioritized Diff Truncation)**:
  Khi nén Git Diff về tối đa 15 dòng, hệ thống sắp xếp ưu tiên hiển thị:
  1. **Priority 1**: Các dòng bị xóa (`-`) và các dòng tác động vào file cấu hình Core (HIGH path).
  2. **Priority 2**: Các dòng bổ sung cấu trúc mới (`+`).
  3. **Priority 3**: Các dòng ngữ cảnh xung quanh để lấp đầy ngân sách 15 dòng.

### 1.3 TrustEngine (`trust_engine.py`)
- **Bảng Ánh Xạ Lý Do (Reason Code Mapping Table)**:
  Ánh xạ cố định giữa Ma trận Rủi ro ➔ `reason_code` để TrustEngine có key space nhất quán ghi log:

  | Blast Radius & Op | Reason Code | Default Tier |
  |---|---|---|
  | HIGH Path hoặc Operation = `delete` | `IRREVERSIBLE_ACTION` / `POLICY_BOUNDARY` | 🔴 T3 |
  | MEDIUM Path & Op = `modify`/`create` | `EXTERNAL_WRITE` / `SCHEMA_AMBIGUOUS` | 🟡 T2 |
  | LOW Path & Op = `modify`/`create` | `INTERNAL_DRAFT` / `LOW_CONFIDENCE` | 🔵 T1 |
  | Script Pass 100% / Read-only | `DETERMINISTIC_PASS` | 🟢 T0 |

- **Trust Proposal System**: Đề xuất hạ tier (T2 ➔ T1) công khai khi `reason_code` đạt tỉ lệ Approve > 95% sau 20 lượt chạy (KHÔNG tự ý hạ ngầm).
- **Compounding Risk Batcher**: Gom nhóm T1 theo Phase. Nếu có ≥ 3 file bị tác động trong cùng 1 Phase, tự động nâng Batch đó lên T2.

---

## 2. Standard Decision Envelopes

### 2.1 Mẫu Envelope T2 (Rủi ro Vừa phải — Phím tắt 1/2/3)

```markdown
====================================================================
🚨 CHECKPOINT REVIEW [Tier: 🟡 T2 - Moderate Risk]
--------------------------------------------------------------------
📍 Node: [kit-assembly] | Lý do: EXTERNAL_WRITE (Modify manifest.json)

📝 Tóm tắt tác động (Impact Summary):
- Bổ sung 2 Skill mới vào manifest: @domain-analysis và @skill-crafting.

🔍 Core Delta (Risk-Prioritized - 3 dòng):
+ "skills": ["domain-analysis", "skill-crafting"]

--------------------------------------------------------------------
👉 LỰA CHỌN CỦA BẠN (Gõ 1, 2 hoặc 3):
[1] Approve (Đồng ý & Tiếp tục)
[2] Revise  (Yêu cầu chỉnh sửa thêm)
[3] Reject  (Hủy bỏ & Rollback)
====================================================================
```

### 2.2 Mẫu Envelope T3 (Rủi ro Cao / Unreversible — Mã Khóa Xác Nhận)

```markdown
====================================================================
⛔ CRITICAL CHECKPOINT REVIEW [Tier: 🔴 T3 - HIGH RISK / IRREVERSIBLE]
--------------------------------------------------------------------
📍 Node: [refactor-rules] | Lý do: IRREVERSIBLE_ACTION (Delete .agents/rules/legacy.md)
⚠️ CẢNH BÁO: Thao tác XÓA file cấu hình hệ thống!

📝 Tóm tắt tác động (Impact Summary):
- Thao tác XÓA vĩnh viễn quy tắc legacy.md khỏi hệ thống core.

🔍 Core Delta (Risk-Prioritized Deletions):
- rule: legacy-workflow-v0
- trigger: always_on

--------------------------------------------------------------------
🔒 XÁC NHẬN AN TOÀN (Chống bấm nhầm):
Để thực thi thao tác nguy hiểm này, vui lòng nhập chính xác chuỗi sau:

   CONFIRM 8492

(Hoặc nhập "cancel" để Từ chối & Rollback an toàn)
====================================================================
```

---

## 3. Ghi Chú Quyết Định Thiết Kế (Architectural Decision Records)

1. **`ttl` Field Scope**: Trạng thái `ttl` trong Workflow Contract Schema được giữ lại làm **Reserved Field** cho Phase 2 (Async Orchestration). Trong phiên bản v1.1 CLI Sync hiện tại, checkpoint sẽ dừng đợi người dùng vô thời hạn hoặc cho đến khi bấm cancel.
2. **Idempotency Key Scope**: Đã chủ động đơn giản hóa trong v1.1 CLI. Hệ thống tập trung 100% vào **Scoped Dual-Hash Staleness Guard** để kiểm soát drift. Idempotency key chuẩn distributed queue được chuyển sang reserved cho Phase 2.

---

## 4. Definition of Done (DoD Kiểm định v1.1)

- [ ] `guard_engine.py`: Đạt 100% unit tests kiểm tra Scoped Hash (chỉ hash target artifacts) & Staleness Rollback.
- [ ] `impact_engine.py`: Ma trận 2D phân loại chính xác thao tác `delete` ➔ T3; Nén Git Diff ưu tiên dòng bị xóa (`-`) lên đầu.
- [ ] `trust_engine.py`: Map chuẩn `reason_code` theo Bảng Ánh Xạ Cố Định và lưu log `decision_history.json`.
- [ ] Interface T3: Bắt buộc người dùng nhập đúng mã `CONFIRM <code4>` mới cho phép pass.
- [ ] `validate_kit.py`: Reject bất kỳ node nào có `decided_by: model`.
