---
name: core-protocol
version: 1.0.0
priority: P0
trigger: always_on
description: "Hướng dẫn cốt lõi về giao thức tải Skill, thông báo Skill và đọc hiểu trước khi thực thi cho Agent."
---

# Core Protocol - Agent Kit Standard

> Quy định ưu tiên cao nhất về cách LLM Agent nạp skill, đọc tài liệu và thực thi công việc.

---

## 1. Giao thức Nạp Skill Phân cấp (Modular Skill Loading Protocol)

Khi kích hoạt một Agent hoặc Workflow:
1. Đọc **Frontmatter** của Agent/Workflow để xác định danh sách `skills` cần thiết.
2. Đọc file `SKILL.md` (chỉ mục chính) của skill tương ứng.
3. Chỉ đọc tiếp các tài liệu chuyên sâu trong thư mục `references/` hoặc `scripts/` khi có yêu cầu cụ thể từ tác vụ (Selective Reading).

### 1.1 Thông báo Kích hoạt Skill (Skill Announcement - bắt buộc)
Mỗi khi kích hoạt và áp dụng một skill, Agent **BẮT BUỘC** thông báo cho người dùng trước khi thực thi:

```markdown
📚 **Using skill: `@[skill-name]`...**
```

- Nếu áp dụng nhiều skill: `📚 Using skills: @skill-a + @skill-b...`
- Không được âm thầm sử dụng skill mà không thông báo.

### 1.2 Selective Progressive Disclosure & Token Budgeting
- **Lazy Frontmatter Loading**: Nạp YAML Frontmatter trước (< 50 tokens) để duy trì Context Window tối ưu.
- **On-Demand Loading**: Chỉ nạp toàn bộ body `SKILL.md` khi tác vụ được kích hoạt.

### 1.3 80/20 System Automation Tooling
- **Auto-Healing Lockfile**: Script `validate_kit.py` tự động đồng bộ `manifest.lock.json` khi phát hiện biến động component file.
- **1-Click Workspace Sync**: Script `export_kit.py --sync <target_dir>` phân phối trực tiếp bundle `.cursorrules`, `.claude/instructions.txt`, `.gpts/instructions.txt`.
- **Memory Distillation**: Script `distill_memory.py` hỗ trợ tự động ghi nhận bài học kinh nghiệm và pattern vào `.agents/memory/`.

---

## 2. Thứ tự Ưu tiên Quy tắc (Rule Priority)

1. **P0 (Universal Rules)**: Các file trong `.agents/rules/`
2. **P1 (Agent System Prompt)**: File cấu hình Agent trong `.agents/agent/` hoặc System Prompt
3. **P2 (Skill Instructions)**: Các file `SKILL.md` trong `.agents/skills/`

---

## 3. Quy trình "Read → Understand → Apply"

```
❌ SAI: Đọc yêu cầu → Viết code / Viết prompt ngay lập tức
✅ ĐÚNG: Đọc tài liệu → Phân tích tiêu chí DoD → Áp dụng Nguyên tắc → Thực thi
```

Trước khi sinh ra bất kỳ file hay cấu phần nào trong Agent Kit, Agent phải trả lời:
1. **Mục tiêu cốt lõi** của cấu phần này là gì?
2. **Định dạng chuẩn Frontmatter** có đầy đủ không?
3. **Definition of Done (DoD)** có đạt tính nhị phân (Đạt / Không đạt) không?
