---
name: kit-evolution
description: ">"
when_to_use: "Kích hoạt khi cần năng lực kit-evolution trong quy trình tạo hoặc kiểm định Agent Kit."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# Kit Evolution

## Overview

Quy trình bảo trì, refactor và nâng cấp Agent Kit có sẵn. Đảm bảo tính kế thừa, tối ưu
token bằng phương pháp sửa đổi chọn lọc (delta-only patch), tránh viết lại toàn bộ hệ thống
khi không thực sự cần thiết.

---

## Nguyên tắc Refactor

### 1. Audit-First (Đánh giá trước)
- Trước khi thực hiện bất kỳ chỉnh sửa nào, hãy chạy quy trình `workflows/validate-kit.md` để xác định điểm yếu của kit hiện tại.
- Lập danh sách cụ thể các phần cần sửa đổi (thừa, thiếu, sai lệch).

### 2. Delta-Only Editing (Chỉ sửa phần lệch)
- Tuyệt đối tránh việc viết lại toàn bộ System Prompt hoặc các file skills lớn từ đầu.
- Chỉ chỉnh sửa hoặc bổ sung những dòng/khối thực sự cần cập nhật.
- Điều này giúp tiết kiệm token, bảo vệ các cơ chế cũ đang hoạt động ổn định và giảm thiểu rủi ro phát sinh lỗi mới.

### 3. Quy chuẩn Đánh phiên bản (Version Bumping)
Sử dụng chuẩn SemVer (Semantic Versioning) cho tất cả các thành phần trong kit:
- **Patch (x.x.Y)**: Sửa lỗi chính tả, làm rõ câu chữ trong prompt mà không thay đổi logic hoạt động.
- **Minor (x.Y.0)**: Bổ sung skill mới, thêm constraint hoặc DoD mới vào agent.
- **Major (Y.0.0)**: Tái cấu trúc toàn bộ (ví dụ: chuyển từ Standard Kit lên Professional Kit), thay đổi hoàn toàn kiến trúc I/O hoặc workflow.

---

## Quy trình Thực hiện

```
Kit hiện tại ──> Audit (Validate) ──> Lập danh sách Delta ──> Patch sửa đổi ──> Re-Audit
```

### Bước 1: Phân tích Sự lệch pha (Gap Analysis)
Xác định sự khác biệt giữa kit hiện tại và yêu cầu mới của người dùng:
- Agent có hoạt động sai logic không? (Sửa đổi logic trong prompt).
- Có thiếu năng lực chuyên biệt nào không? (Thêm Skill mới).
- Có gặp lỗi lặp vô hạn hay context phình to không? (Áp dụng các Lens tối ưu).

### Bước 2: Viết mã delta và áp dụng
- Cập nhật phiên bản của các file được chỉnh sửa trong frontmatter.
- Nếu chỉnh sửa Professional Kit, chạy cập nhật file `manifest.json`.

### Bước 3: Đảm bảo tính tương thích ngược (Backward Compatibility)
- Đảm bảo các agent khác trong hệ thống vẫn giao tiếp được với agent vừa được nâng cấp (không thay đổi cấu trúc I/O schema hoặc handoff protocol trừ khi nâng cấp Major).
