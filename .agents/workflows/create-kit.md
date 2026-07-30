---
name: create-kit
description: "Quy trình tạo Agent Kit mới từ đầu (Create Kit)."
version: 1.0.0
requires_agents: master-compiler, domain-analyst, kit-generator
requires_skills: domain-analysis, prompt-engineering, kit-assembly
artifact_outputs: agent-kit-spec
---

# Workflow: Create Kit (Tạo Agent Kit Mới)

Sử dụng khi người dùng yêu cầu xây dựng một Agent Kit mới từ đầu.

---

## Các bước thực hiện

### Bước 1: Tiếp nhận thông tin (Input Processing)
1.  **Xác định Trình độ kỹ thuật của User**:
    *   *Low-tech*: Hỏi 2-3 câu đơn giản bằng ngôn ngữ đời thường về mục tiêu và giới hạn.
    *   *Tech User*: Sử dụng trực tiếp các yêu cầu/spec từ user prompt.
2.  **Xác định North Star & Constraints**: Trích xuất mục tiêu cốt lõi và các điều kiện tuyệt đối không được vi phạm.

---

### Bước 2: Phân tích Domain (Domain Analysis)
1.  Kích hoạt và nạp skill: `skills/domain-analysis/SKILL.md`.
2.  Thực hiện phân tích:
    *   Core Verbs (Hành động cốt lõi).
    *   Domain-Specific Discovery (Tìm đòn bẩy 80/20).
    *   Predicted Failure Modes (Dự đoán lỗi).
3.  **Xác định Kit Type**: Chọn Micro, Standard, Professional hoặc Suite.
4.  Lập danh sách component cần tạo.

---

### Bước 3: Tạo các thành phần (Component Generation)
Duyệt qua danh sách components được khuyến nghị ở Bước 2 để tạo:

#### 1. Agent (System Prompt) - Luôn có
*   Kích hoạt skill: `skills/prompt-engineering/SKILL.md`.
*   Viết System Prompt hoàn chỉnh theo đúng cấu trúc 4 section (Vai trò, Nguyên tắc, Constraints, Format đầu ra).
*   Thiết lập Definition of Done nhị phân, đo lường được, không sáo ngữ.

#### 2. Skills (nếu cần)
*   Kích hoạt skill: `skills/skill-crafting/SKILL.md`.
*   Tạo cấu trúc thư mục skill, viết SKILL.md với Frontmatter pushy và phân cấp progressive disclosure.

#### 3. Memory / Workflow / Tools (nếu cần)
*   Kích hoạt skill: `skills/kit-assembly/SKILL.md`.
*   Thiết kế cấu trúc dữ liệu lưu trữ, chuyển trạng thái và định nghĩa tham số tool theo spec chuẩn.

---

### Bước 4: Tổng hợp & Lắp ráp (Assembly)
1.  Kích hoạt skill: `skills/kit-assembly/SKILL.md`.
2.  Lắp ráp các thành phần thành cấu trúc thư mục hoàn chỉnh phù hợp với Kit Type đã chọn **bắt buộc nằm trong thư mục cách ly `./output/<kit-name>/`** (tuyệt đối KHÔNG ghi trực tiếp vào `.agents/` của Agent Kit Creator).
3.  Tạo file `manifest.json` (đối với Professional/Suite Kit).
4.  Ghép phần TÓM TẮT CHO NGƯỜI DÙNG lên đầu kết quả đầu ra.

---

### Bước 5: Kiểm tra chất lượng (Quality Check)
1.  Chạy workflow: `workflows/validate-kit.md` để tự kiểm định kết quả trong thư mục `./output/<kit-name>/`.
2.  Đảm bảo kit đạt tối thiểu **4/5 sao**.
3.  Nếu không đạt:
    *   Phân tích các lỗi từ bảng kiểm tra.
    *   Thực hiện chỉnh sửa và tái kiểm định (tối đa 2 lần).
    *   Nếu vẫn fail: Dừng lại và trình bày bản thảo kèm lý do cho người dùng quyết định.

---

### Bước 6: Bàn giao (Delivery)
Bàn giao Agent Kit hoàn chỉnh tại đường dẫn `./output/<kit-name>/` cho người dùng theo đúng mẫu cấu trúc.

