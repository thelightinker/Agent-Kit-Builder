---
name: refactor-kit
description: "Cải tiến & Nâng cấp Agent Kit đã có sẵn (Refactor Kit)."
version: 1.0.0
requires_agents: master-compiler, quality-auditor, kit-generator
requires_skills: kit-evolution, quality-assurance
artifact_outputs: refactored-kit-spec
---

# Workflow: Refactor Kit (Cải tiến & Nâng cấp Kit)

Sử dụng khi người dùng yêu cầu nâng cấp, sửa đổi hoặc thêm tính năng cho một Agent Kit đã có sẵn.

---

## Các bước thực hiện

### Bước 1: Tiếp nhận & Đánh giá hiện trạng
1.  Đọc toàn bộ file cấu trúc của Agent Kit hiện tại.
2.  Chạy workflow: `workflows/validate-kit.md` trên kit hiện tại để tìm điểm yếu, lỗi cấu trúc hoặc sự thiếu hụt.
3.  Xác định yêu cầu nâng cấp của user:
    *   Bổ sung năng lực mới (Thêm Skill/Tool).
    *   Khắc phục lỗi chạy sai (Sửa logic prompt/workflow).
    *   Tối ưu hóa token (Rút gọn prompt, chuyển cấu trúc sang progressive disclosure).

---

### Bước 2: Phân tích sự lệch pha (Gap Analysis)
1.  Kích hoạt skill: `skills/kit-evolution/SKILL.md`.
2.  Phân tích phần cần sửa đổi. Xác định xem thay đổi thuộc mức độ nào:
    *   *Patch* (Sửa lỗi nhỏ/câu chữ).
    *   *Minor* (Thêm tính năng/skill phụ).
    *   *Major* (Thay đổi cấu trúc/thay đổi cách giao tiếp/nâng cấp Kit Type).

---

### Bước 3: Thực hiện chỉnh sửa chọn lọc (Delta Patch)
1.  **Chỉ sửa đổi phần cần thiết**: Không viết lại toàn bộ các file lớn nếu không được yêu cầu. Chỉ áp dụng các thay đổi delta để bảo vệ các logic cũ đang ổn định.
2.  **Nạp Selective Context theo Hydration Matrix**: Tra cứu `rules/request-routing.md` và nạp tài liệu chẩn đoán lỗi (`references/failure-modes.md`, `references/outcome-lenses.md`) cùng Template tương ứng của cấu phần cần refactor trước khi sửa code.
3.  Nếu thêm Skill mới: Kích hoạt `skills/skill-crafting/SKILL.md` để tạo skill folder.
4.  Nếu cập nhật System Prompt: Kích hoạt `skills/prompt-engineering/SKILL.md` để sửa đổi chọn lọc.
4.  Cập nhật số phiên bản (Version) trong frontmatter của các thành phần bị ảnh hưởng theo chuẩn SemVer.
5.  Cập nhật file `manifest.json` (nếu có).

---

### Bước 4: Kiểm tra & Tái đánh giá (Re-Audit)
1.  Chạy lại workflow: `workflows/validate-kit.md` trên kit mới sau khi chỉnh sửa.
2.  So sánh điểm số trước và sau khi refactor. Đảm bảo kit mới đạt ít nhất **4/5 sao** và không vi phạm bất kỳ lỗi nghiêm trọng (Critical Failure Modes) nào.
3.  Kiểm tra tính tương thích ngược (Backward Compatibility): Đảm bảo các component không bị sửa đổi vẫn tương tác tốt với các component mới.

---

### Bước 5: Bàn giao (Delivery)
Trả kết quả bàn giao cho user kèm theo:
- Bản tóm tắt các thay đổi (Changelog/Delta summary).
- Nội dung chi tiết các file được cập nhật.
