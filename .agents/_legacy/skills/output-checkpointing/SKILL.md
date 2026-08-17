---
name: output-checkpointing
description: "Phân tích rủi ro, kiểm định chất lượng và kích hoạt Checkpoint Envelope bảo vệ sản phẩm đầu ra (Output Artifacts) trong ./output/<kit-name>/. Sử dụng khi người dùng yêu cầu kiểm tra output, chạy checkpoint, bảo vệ file sản phẩm đầu ra khỏi state drift, hoặc khi cần xác nhận rủi ro thay đổi file."
when_to_use: "Kích hoạt khi người dùng gõ /output-checkpointing hoặc yêu cầu kiểm tra/duyệt rủi ro sản phẩm đầu ra của Agent Kit."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# Output Checkpoint Skill — Bảo vệ & Kiểm định Sản phẩm Đầu ra

> Chuyên biệt kiểm định, tính toán Blast Radius và kích hoạt Checkpoint Envelope trên các file sản phẩm đầu ra tại `./output/<kit-name>/`.

---

## ⚡ CLI Quick Start Command

Đánh giá và chạy Checkpoint Gate trên một file hoặc danh sách file Output:
```bash
python .agents/scripts/checkpoint_gate.py --node <node_name> --target <file_path> --op <create|modify|delete>
```

---

## 🛡️ Quy trình Kiểm định Output 3 Lớp

1. **Guard Check (Kiểm tra An toàn)**:
   - Tự động sinh mã SHA-256 Scoped Hash trên đúng danh sách file output được chỉ định.
   - Phát hiện State Drift và sẵn sàng khôi phục Snapshot an toàn nếu người dùng Reject.

2. **Impact Analysis (Phân tích Tác động Rủi ro)**:
   - Phân loại Ma trận Rủi ro 2 Chiều: **Path Sensitivity** x **Operation Type (`create` | `modify` | `delete`)**.
   - Mọi thao tác **`delete`** tự động leo thang **+1 Tier ➔ T3**.
   - Nén Git Diff về tối đa 15 dòng, luôn ưu tiên dòng bị xóa (`-`) và dòng tác động Core Rule lên đầu.
   - Tự động sinh Impact Summary bằng 3 câu tiếng Việt tự nhiên đơn giản.

3. **Envelope Execution (Hiển thị Lựa chọn duyệt)**:
   - Với **🟡 T2 (Rủi ro vừa)**: Hiển thị phím bấm nhanh `1` (Approve), `2` (Revise), `3` (Reject).
   - Với **🔴 T3 (Rủi ro cao/Không thể hoàn tác)**: Bắt buộc người dùng nhập đúng mã khóa xác nhận `CONFIRM <4-digit-code>` (ví dụ `CONFIRM 8492`).

---

## 📋 Bảng Phân Tầng Rủi Ro Output

| Tier | UX Indicator | Thao tác Ví dụ | Hành vi Checkpoint |
|---|---|---|---|
| **🟢 T0** | Auto-pass | Đọc file, DoD Pass 100% | Tự động Pass, ghi log ngầm |
| **🔵 T1** | Batched | Tạo draft file trong `./output/draft/` | Tự động Proceed, gom duyệt theo Phase |
| **🟡 T2** | Sync Envelope | Tạo mới/sửa file trong `./output/<kit>/` | Dừng duyệt, chìa bảng phím `1/2/3` |
| **🔴 T3** | Confirm Code | XÓA file output hoặc đè file Core Rules | Dừng duyệt bắt buộc, yêu cầu mã `CONFIRM <code4>` |
