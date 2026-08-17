# {KIT_NAME} — Memory Index (SSOT)

> Bộ nhớ phân tầng (Scoped Memory) của `{KIT_NAME}`. Giới hạn nghiêm ngặt $\le 200$ dòng. Nạp có chọn lọc để bảo vệ Attention Budget.

---

## 1. Shared Memory (`memory/shared/`)
*Dành cho toàn bộ Suite (Mọi Agent được phép đọc)*
- `brand-guidelines.md`: Quy chuẩn thương hiệu, phong cách và ngôn từ.
- `project-conventions.md`: Quy ước kiến trúc và quy chuẩn kỹ thuật chung.

---

## 2. Domain Memory (`memory/domains/`)
*Dành riêng cho từng Specialist Agent tương ứng*
- `{DOMAIN_A_NAME}.md`: Tri thức chuyên sâu và playbook của Specialist A.
- `{DOMAIN_B_NAME}.md`: Tri thức chuyên sâu và playbook của Specialist B.

---

## 3. Session & Run State (`memory/runs/`)
*Theo dõi tiến độ thực thi đa-phiên*
- `features-tracker.json`: Danh mục trạng thái các tính năng (Definition of Done ngoài context window).
- `golden-examples/`: Các mẫu output xuất sắc đạt 5/5 ⭐.
