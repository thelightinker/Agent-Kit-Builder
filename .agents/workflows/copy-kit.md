---
name: copy-kit
description: "Quy trình sao chép (COPY) an toàn 1 hoặc nhiều Agent Kit từ thư mục Output sang thư mục dự án đích (mặc định: C:\\Users\\nhdcb\\OneDrive\\Desktop\\AI Project/AI Agent Kits) mà không làm di chuyển hay thay đổi file nguồn."
version: 1.0.0
requires_agents: [kit-architect]
requires_skills: [kit-exporting]
artifact_outputs: [copy_summary.md]
topology: sequential
trigger: manual
permissions: read-write
tools_allowed: [Read, Write, Bash, Glob]
safe_outputs:
  pure_copy_invariant: "Tuyệt đối sao chép (COPY), không di chuyển (MOVE) hay xóa file nguồn trong Output/."
max_retry_per_node: 2
---

# 🔄 MASTER FLOW: /copy-kit (Agent Kit Safe Copier)

> **Mục tiêu**: Cung cấp quy trình sao chép (COPY) chuẩn xác, bảo toàn 100% dữ liệu gốc từ `./Output/<kit-name>` sang thư mục quản lý dự án AI Agent (`C:\Users\nhdcb\OneDrive\Desktop\AI Project\AI Agent Kits`), hỗ trợ copy đơn lẻ, nhiều kit theo danh sách hoặc toàn bộ.

---

## 🏛️ 1. GOVERNANCE & SAFETY INVARIANTS

1. **Pure Copy Invariant (Bất biến Sao chép)**: Workflow và script thực thi CHỈ thực hiện sao chép (`shutil.copytree`), KHÔNG BAO GIỜ xóa, cắt (cut) hay di chuyển (move) thư mục nguồn tại `./Output/`.
2. **Deterministic Payload Check**: Mọi thao tác sao chép phải thống kê rõ ràng số lượng file và dung lượng trước và sau khi copy.
3. **Target Idempotency**: Cho phép copy đè an toàn khi nâng cấp kit (`dirs_exist_ok=True`) mà không làm hỏng cấu trúc thư mục đích.

---

## 🔄 2. STATE NODES & ACTION EXECUTION

### [STATE 1: SCAN_AND_SELECT] (Quét & Xác Định Kit Cần Chuyển)
- **Role Profile:** `@kit-architect` | **Skill:** `kit-exporting`
- **[Input Artifacts]:** Thư mục `./Output/` hoặc danh sách tên kit do người dùng yêu cầu.
- **[Output Artifacts]:** Danh sách kit mục tiêu đã xác thực.

- **⚡ Action Prompts & Execution Steps**:
  1. **Bước 1 (Inspect)**: Quét danh sách các kit hiện có trong `./Output/`:
     ```bash
     python .agents/scripts/copy_kit.py --list
     ```
  2. **Bước 2 (Match)**: Đối chiếu với yêu cầu của người dùng:
     - Nếu người dùng chỉ định tên cụ thể (ví dụ: `Marketing`, `content-engine`): Chọn các kit tương ứng.
     - Nếu người dùng yêu cầu copy tất cả: Kích hoạt cờ `--all`.
     - Nếu chưa rõ: Đưa ra danh sách các kit sẵn có để người dùng chọn.

- **Definition of Done (DoD - Binary Assertions)**:
  - [ ] Danh sách kit nguồn tồn tại thực tế trên đĩa trong `./Output/`.
  - [ ] Thư mục đích mặc định `C:\Users\nhdcb\OneDrive\Desktop\AI Project\AI Agent Kits` (hoặc đường dẫn tùy chỉnh) được xác định rõ ràng.

---

### [STATE 2: SAFE_COPY] (Thực Thi Sao Chép An Toàn)
- **Role Profile:** `@kit-architect` | **Skill:** `kit-exporting`
- **[Input Artifacts]:** Danh sách kit từ State 1.
- **[Output Artifacts]:** Terminal output của `copy_kit.py`.

- **⚡ Action Prompts & Execution Steps**:
  1. **Bước 1 (Execute)**: Chạy lệnh sao chép tương ứng qua script `copy_kit.py`:
     ```bash
     # Copy 1 kit:
     python .agents/scripts/copy_kit.py <kit_name>

     # Copy nhiều kit:
     python .agents/scripts/copy_kit.py <kit_1> <kit_2>

     # Copy toàn bộ:
     python .agents/scripts/copy_kit.py --all

     # Tùy chỉnh thư mục đích:
     python .agents/scripts/copy_kit.py <kit_name> --dest "D:\Custom\Path"
     ```
  2. **Bước 2 (Status Check)**: Kiểm tra exit code (0 = thành công).

- **Definition of Done (DoD)**:
  - [ ] Lệnh hoàn tất với mã thoát `0`.
  - [ ] 100% kit mục tiêu được sao chép sang thư mục đích.
  - [ ] Thư mục nguồn tại `./Output/` vẫn nguyên vẹn không đổi.

---

### [STATE 3: VERIFY_AND_SUMMARY] (Kiểm Đếm & Báo Cáo)
- **Role Profile:** `@kit-architect` | **Skill:** `kit-exporting`
- **[Input Artifacts]:** Trạng thái thư mục đích sau khi copy.
- **[Output Artifacts]:** Báo cáo tổng kết gửi người dùng.

- **⚡ Action Prompts & Execution Steps**:
  1. **Bước 1 (Verify)**: Kiểm tra sự tồn tại của thư mục kit tại đích.
  2. **Bước 2 (Summary Report)**: Báo cáo trực quan ngắn gọn 3-5 dòng cho người dùng gồm:
     - Tên kit đã sao chép.
     - Đường dẫn đích đầy đủ dạng `file:///...`.
     - Tổng số file và dung lượng đã sao chép.

- **Definition of Done (DoD)**:
  - [ ] Báo cáo hiển thị link thư mục đích rõ ràng.
  - [ ] 0 lỗi xảy ra trong quá trình copy (nếu có lỗi I/O đĩa hoặc trùng lặp không thể giải quyết ➔ `[ESCALATE_HUMAN]`).

---

## 🤝 3. HANDOFF CONTRACT

Sau khi hoàn tất sao chép, kit đã sẵn sàng để người dùng mở và sử dụng tại workspace mục tiêu:
```json
{
  "contract_version": "1.0.0",
  "source_workflow": "copy-kit",
  "target_workflow": "ready_for_use",
  "destination_path": "C:\\Users\\nhdcb\\OneDrive\\Desktop\\AI Project\\AI Agent Kits",
  "status": "COPIED"
}
```
