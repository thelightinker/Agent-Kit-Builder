---
name: remember-kit
description: "Workflow lưu đúc rút kinh nghiệm, thiết kế pattern và ví dụ kit xuất sắc vào bộ nhớ dài hạn MEMORY.md."
version: 2.0.0
requires_agents: kit-architect
requires_skills: kit-evolving
artifact_outputs: memory-entry
---

# Workflow: Remember Kit (Cập nhật Bộ nhớ Dài hạn)

Sử dụng khi một Agent Kit vừa hoàn thành đạt tiêu chuẩn xuất sắc (5/5 ⭐) hoặc khi rút ra bài học kinh nghiệm mới về thiết kế Agent/Skill/Rule.

---

## Các bước thực hiện

### Bước 1: Tiếp nhận Nội dung & Đánh giá Tiêu chuẩn
1. **Kiểm tra Điều kiện Lưu vết**:
   - Nếu là Agent Kit mẫu: Đảm bảo kit đã đạt kết quả **5/5 ⭐ (EXEMPLARY)** từ `/validate-kit`.
   - Nếu là Bài học / Pattern: Đảm bảo bài học có tính tổng quát, tái sử dụng được.

---

### Bước 2: Phân loại & Cập nhật Bộ nhớ
1. Kích hoạt skill: `skills/kit-evolving/SKILL.md`.
2. **Lưu Kit mẫu (Golden Examples)**:
   - Tạo file ghi chép ví dụ trong `memory/golden-examples/[kit-name].md`.
   - Cập nhật danh mục và mô tả ngắn vào `memory/MEMORY.md`.
3. **Lưu Pattern / Bài học (Design Patterns)**:
   - Thêm bài học mới vào `memory/kit-patterns.md`.

---

### Bước 3: Xác nhận & Bàn giao
1. Kiểm tra lại đường dẫn liên kết trong `memory/MEMORY.md`.
2. Đưa phần **TÓM TẮT CHO NGƯỜI DÙNG** lên đầu kết quả thông báo bài học/kit đã được ghi nhớ.
