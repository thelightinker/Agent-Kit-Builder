# Domain References

Mỗi file trong thư mục này chứa domain pattern cho 1 lĩnh vực cụ thể.
Builder dùng để tham khảo khi build Agent Kit cho domain tương ứng.

---

## Cấu trúc mỗi domain file

| Section | Mô tả |
|:--------|:------|
| **Core Verbs** | 5–10 hành động chính của domain |
| **Outcome Patterns** | Các vai trò / chức năng outcome-driven phổ biến |
| **Typical Lenses** | Lens nào thường áp dụng cho domain này (tham khảo) |
| **Quality Signals** | Cách đo "agent đang làm tốt" |
| **Common Failure Modes** | Lỗi hay gặp + đòn bẩy khắc phục |

---

## Available Domains

- `book-writing.md` — Viết sách phi hư cấu
- `business.md` — Quản lý kinh doanh, chiến lược
- `research.md` — Nghiên cứu, tổng hợp tri thức
- `software.md` — Phát triển phần mềm

---

## Cách dùng

1. Xác định domain của Agent Kit đang build
2. Load domain file tương ứng
3. Dùng Core Verbs để xác định cơ chế cần thiết
4. Dùng Typical Lenses như gợi ý — KHÔNG áp dụng máy móc
5. Dùng Failure Modes để chạy Dynamic Enhancement Discovery
