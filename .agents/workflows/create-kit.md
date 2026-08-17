---
name: create-kit
description: "Quy trình tạo Agent Kit mới từ đầu (Create Kit)."
version: 2.0.0
requires_agents: kit-architect
requires_skills: domain-profiling, prompt-compiling, skill-architecting, kit-assembling, kit-verifying
artifact_outputs: agent-kit-spec
---

# Workflow: Create Kit (Tạo Agent Kit Mới)

Sử dụng khi người dùng yêu cầu xây dựng một Agent Kit mới từ đầu theo quy trình Deep Track.

---

## Các bước thực hiện

### Bước 1: Tiếp nhận thông tin & Phân loại
1. **Xác định Trình độ kỹ thuật**:
   - *Low-tech*: Dùng `superpowers:brainstorming` phỏng vấn 2-3 câu đơn giản bằng ngôn ngữ đời thường.
   - *Tech User*: Sử dụng trực tiếp spec từ prompt.
2. **Xác định North Star & Constraints**: Trích xuất mục tiêu cốt lõi và các điều kiện bắt buộc.

---

### Bước 2: Phân tích Domain (`@analyst`)
1. Kích hoạt skill: `skills/domain-profiling/SKILL.md`.
2. Phân tích:
   - Core Verbs (Hành động cốt lõi).
   - Dynamic Enhancement Discovery (Tìm đòn bẩy 80/20 với ROI $\ge 1.25$).
   - Predicted Failure Modes (Dự đoán lỗi và cơ chế phòng ngừa).
3. **Xác định Kit Type**: Micro, Standard, Professional hoặc Suite.
4. Lập danh sách component tối thiểu cần tạo.

---

### Bước 3: Biên dịch System Prompt (`@compiler`)
1. Kích hoạt skill: `skills/prompt-compiling/SKILL.md`.
2. Nạp template: `templates/agent-template.md` (hoặc `templates/orchestrator-template.md` nếu là Suite Kit).
3. Viết System Prompt 4 khối (Vai trò & DoD nhị phân, Quy trình, Hard Constraints phủ định, Format đầu ra).

---

### Bước 4: Thiết kế Skills & Cấu phần Bổ trợ (`@architect`)
1. Nếu cần Skill: Kích hoạt `skills/skill-architecting/SKILL.md` và dùng `templates/skill-template.md`.
2. Nếu cần Memory/Workflow: Thiết kế theo `templates/memory-template.md` hoặc `templates/workflow-template.md`.

---

### Bước 5: Lắp ráp & Đóng gói (`kit-assembling`)
1. Kích hoạt skill: `skills/kit-assembling/SKILL.md`.
2. Tạo thư mục cách ly bắt buộc tại `./output/<kit-name>/`.
3. Ghi toàn bộ các files vào đúng cấu trúc thư mục. Sinh `manifest.json` nếu là Professional/Suite.

---

### Bước 6: Kiểm định Chất lượng (`@auditor` + `kit-verifying`)
1. Chạy workflow: `workflows/validate-kit.md` trên thư mục `./output/<kit-name>/`.
2. Thực hiện 3 lớp kiểm định (L1 Linting $\rightarrow$ L2 Scenario $\rightarrow$ L3 Adversarial).
3. Đảm bảo kit đạt tối thiểu **4/5 ⭐**. Nếu chưa đạt, revise trước khi bàn giao.

---

### Bước 7: Bàn giao (Delivery)
Bàn giao Agent Kit hoàn chỉnh tại `./output/<kit-name>/` kèm phần **TÓM TẮT CHO NGƯỜI DÙNG** (0 thuật ngữ AI) ở đầu output.
