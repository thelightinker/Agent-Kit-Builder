---
name: remember-kit
description: "Workflow lưu đúc rút kinh nghiệm, thiết kế pattern và ví dụ kit xuất sắc vào bộ nhớ dài hạn MEMORY.md."
version: 1.0.0
requires_agents: master-compiler
requires_skills: memory-system
artifact_outputs: memory-entry
---

# Workflow: Remember Kit (Cập nhật Bộ nhớ Dài hạn)

Sử dụng khi một Agent Kit vừa hoàn thành đạt tiêu chuẩn xuất sắc (5/5 ⭐) hoặc khi rút ra bài học kinh nghiệm mới về thiết kế Agent/Skill/Rule.

$ARGUMENTS

---

## Các bước thực hiện

### Bước 1: Tiếp nhận Nội dung & Đánh giá Tiêu chuẩn
1. **Kiểm tra Điều kiện Lưu vết**:
   - Nếu là Agent Kit mẫu: Đảm bảo kit đã đạt kết quả **5/5 ⭐ (EXEMPLARY)** từ `/validate-kit`.
   - Nếu là Bài học / Pattern: Đảm bảo bài học có tính tổng quát, có thể tái sử dụng cho các kit sau.

---

### Bước 2: Phân loại & Cập nhật Bộ nhớ

#### Trường hợp 1: Lưu Kit mẫu Xuất sắc (Golden Examples)
1. Tạo file ghi chép ví dụ trong `memory/golden-examples/[kit-name].md`.
2. Cập nhật danh mục và mô tả ngắn vào [MEMORY.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/memory/MEMORY.md).

#### Trường hợp 2: Lưu Pattern / Bài học Thiết kế (Design Patterns)
1. Thêm bài học mới (nguyên nhân lỗi ➔ cách khắc phục ➔ quy tắc áp dụng) vào [kit-patterns.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/memory/kit-patterns.md).

---

### Bước 3: Xác nhận & Bàn giao
1. Kiểm tra lại đường dẫn file trong `memory/`.
2. Đưa phần **TÓM TẮT CHO NGƯỜI DÙNG** lên đầu kết quả phản hồi thông báo về bài học/kit mẫu đã được ghi nhớ.
