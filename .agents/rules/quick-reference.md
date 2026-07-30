---
name: quick-reference
version: 1.0.0
priority: P2
trigger: model_decision
description: "Tra cứu nhanh toàn bộ danh mục Workflows, Skills, Rules, Schemas và Templates có sẵn trong Agent Kit Creator."
---

# Quick Reference - Agent Kit Creator

> Chỉ mục tra cứu nhanh toàn bộ tài nguyên trong workspace `Agent Kit Creator`.

---

## 🔄 Workflows (`.agents/workflows/`)
- `/create-kit` ([create-kit.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/workflows/create-kit.md)): Quy trình tạo Agent Kit mới từ đầu.
- `/refactor-kit` ([refactor-kit.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/workflows/refactor-kit.md)): Cải tiến, nâng cấp & vá lỗi Agent Kit sẵn có.
- `/validate-kit` ([validate-kit.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/workflows/validate-kit.md)): Kiểm định chất lượng 3 lớp & chấm điểm Rubric 5 sao.
- `/remember-kit` ([remember-kit.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/workflows/remember-kit.md)): Lưu bài học kinh nghiệm và kit mẫu 5 sao vào bộ nhớ dài hạn.

---

## 📚 Specialized Skills (`.agents/skills/`)
- `domain-analysis`: Phân tích lĩnh vực, tìm đòn bẩy 80/20, dự đoán lỗi & chọn Kit Type.
- `prompt-engineering`: Thiết kế System Prompt 4 phần chuẩn mực, binary DoD & constraints.
- `skill-crafting`: Viết thư mục skill, SKILL.md với pushy frontmatter & progressive disclosure.
- `kit-assembly`: Lắp ráp thư mục kit, tạo manifest.json & dual-output.
- `quality-assurance`: Đánh giá 3 lớp (Structural, Semantic, Adversarial) & bảng điểm Rubric.
- `kit-evolution`: Phân tích sự lệch pha (Gap Analysis) & thực hiện Delta Patch.

---

## 📐 Standard Templates (`.agents/templates/`)
- [agent-template.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/templates/agent-template.md): Mẫu System Prompt / Agent.
- [skill-template.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/templates/skill-template.md): Mẫu thư mục Skill & SKILL.md.
- [workflow-template.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/templates/workflow-template.md): Mẫu luồng xử lý Workflow.
- [rule-template.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/templates/rule-template.md): Mẫu quy tắc Rule (3 loại trigger).
- [manifest-template.json](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/templates/manifest-template.json): Mẫu file Manifest.
- [memory-template.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/templates/memory-template.md): Mẫu bộ nhớ dài hạn MEMORY.md.
