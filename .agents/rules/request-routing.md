---
name: request-routing
version: 1.0.0
priority: P0
trigger: always_on
description: "Tự động phân loại yêu cầu của người dùng và định tuyến đến đúng Workflow, Skill hoặc Agent tương ứng trong Agent Kit Creator."
---

# Request Routing - Agent Kit Creator

> Rule luôn luôn kích hoạt. Phân loại mọi ý tưởng/yêu cầu của người dùng và tự động định tuyến đến luồng xử lý hoặc skill tối ưu nhất.

---

## 📥 BẢNG ĐỊNH TUYẾN YÊU CẦU (REQUEST CLASSIFIER)

Mỗi khi nhận yêu cầu, phân loại và kích hoạt luồng xử lý tương ứng:

| Loại Yêu cầu | Từ khóa Trigger | Luồng xử lý / Workflow | Skill & Công cụ Cần nạp | Output mong muốn |
| :--- | :--- | :--- | :--- | :--- |
| **TẠO KIT MỚI** | "tạo kit", "viết agent", "xây dựng kit", "tạo prompt agent mới" | `/create-kit` (`workflows/create-kit.md`) | `domain-analysis` ➔ `prompt-engineering` ➔ `skill-crafting` ➔ `kit-assembly` | Agent Kit hoàn chỉnh theo Kit Type |
| **NÂNG CẤP / FIX KIT** | "nâng cấp", "refactor", "sửa kit", "thêm tính năng cho kit", "tối ưu token" | `/refactor-kit` (`workflows/refactor-kit.md`) | `kit-evolution` ➔ `prompt-engineering` / `skill-crafting` | Delta Patch & Bản tổng hợp nâng cấp |
| **KIỂM ĐỊNH / AUDIT** | "kiểm định", "kiểm tra kit", "validate", "chấm điểm kit", "đánh giá" | `/validate-kit` (`workflows/validate-kit.md`) | `quality-assurance` (Audit 3 lớp & Rubric 5 sao) | Báo cáo Đánh giá Audit Report |
| **LƯU BỘ NHỚ / BÀI HỌC** | "lưu bài học", "lưu kit mẫu", "ghi nhớ pattern", "đút rút kinh nghiệm" | `/remember-kit` (`workflows/remember-kit.md`) | Cập nhật `memory/kit-patterns.md` hoặc `memory/golden-examples/` | Bộ nhớ dài hạn được lưu vết |

---

## 🤖 QUY TRÌNH KÍCH HOẠT VÀ THÔNG BÁO SKILL (SKILL ANNOUNCEMENT PROTOCOL)

1. **Xác định Skill**: Ngay sau khi phân loại yêu cầu, chọn danh sách skill cần thiết.
2. **Thông báo công khai (MANDATORY)**: Thông báo cho người dùng trước khi thực thi:
   ```markdown
   📚 **Using skill: `@[skill-name]`...**
   ```
   *(Hoặc nạp nhiều skill: `📚 Using skills: @domain-analysis + @prompt-engineering...`)*
3. **Thực thi phân cấp (Selective Reading)**: Đọc file `SKILL.md` trước, chỉ đọc thêm các file trong `references/` khi tác vụ yêu cầu.
