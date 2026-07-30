# Golden Seed: Standard Agent Kit Example (5/5 ⭐)

> Mẫu thiết kế chuẩn mực dành cho Standard Agent Kit (System Prompt + Skills + Workflows + Memory).

---

## 1. Cấu trúc Thư mục Chuẩn (Directory Tree)

```
[kit-name]/
├── README.md                 # Tóm tắt cho người dùng (0 biệt ngữ AI)
├── agent/
│   └── [agent-name].md       # System prompt theo 4 section chuẩn
├── skills/
│   └── [skill-name]/
│       └── SKILL.md          # Skill với Selective Reading Map
├── workflows/
│   └── [workflow-name].md    # Luồng xử lý phân nhánh & fallback
└── memory/
    └── MEMORY.md             # Bộ nhớ dài hạn lưu vết bài học
```

---

## 2. Các điểm sáng Kỹ thuật (5-Star Design Patterns)

1. **System Prompt 4 Sections**:
   - `Section 1: Role & Purpose` - Vai trò rõ ràng.
   - `Section 2: Core Principles` - Nguyên tắc hành động.
   - `Section 3: Boundaries` - Ranh giới cấm kỵ nhị phân.
   - `Section 4: Output Format & DoD` - Tiêu chuẩn hoàn thành đo lường được.

2. **3-Trigger Rules**:
   - `always_on`, `manual`, `model_decision` được khai báo chính xác ở YAML Frontmatter.

3. **Progressive Disclosure**:
   - System Prompt dưới 1500 tokens, chuyển toàn bộ kiến thức chuyên sâu vào `skills/`.
