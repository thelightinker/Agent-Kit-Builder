# Antigravity IDE Patterns

Patterns chuẩn khi tạo Agent Kit cho Antigravity IDE.
Kit Generator và Skill Architect dùng tài liệu này để đảm bảo output
tương thích và tận dụng tối đa hệ sinh thái Antigravity.

---

## 1. Cấu trúc Workspace Antigravity

Antigravity IDE tổ chức customizations qua 2 root:

### Global Customizations
```
~/.gemini/config/
├── GEMINI.md              # Global rules (bắt buộc)
├── skills/
│   └── [skill-name]/
│       ├── SKILL.md
│       ├── references/
│       ├── examples/
│       └── evals/
└── skills.json            # Optional: skill registration
```

### Workspace Customizations
```
[project-root]/
├── GEMINI.md              # Project-scoped rules (alternative to .agents/rules/GEMINI.md)
├── .agents/
│   ├── rules/
│   │   ├── GEMINI.md      # Project-scoped rules (bắt buộc)
│   │   └── [other].md     # Additional rules
│   └── skills/
│       └── [skill-name]/
│           └── SKILL.md
```

---

## 2. Skills trong Antigravity

### Auto-Discovery
- Skills đặt trong customization roots → tự discovered
- Không cần registration nếu đặt đúng chỗ
- Cần `skills.json` chỉ khi đặt ở non-standard location

### SKILL.md Requirements
- **Frontmatter (YAML)**: `name` + `description` (required)
- **Body (Markdown)**: < 500 dòng
- **Triggering**: Dựa trên `description` — viết "pushy" để LLM trigger đúng

### Progressive Disclosure
| Tầng | Luôn load | Token |
|:-----|:----------|:------|
| Metadata (name + desc) | ✅ | ~100 từ |
| SKILL.md body | Khi trigger | < 500 dòng |
| references/ | Khi body chỉ dẫn | Không giới hạn |

### Bundled Resources
```
skill-name/
├── scripts/       # Executable code
├── references/    # Docs loaded as needed
├── examples/      # Reference implementations
├── assets/        # Templates, icons, fonts
└── evals/         # Test cases
```

---

## 3. Agents trong Antigravity

### Agent Files
- Đặt trong `.agents/` hoặc dự án riêng
- Format: Markdown (.md)
- Mỗi agent 1 file — vai trò rõ ràng, không overlap

### Rules (GEMINI.md)
- Global: `~/.gemini/config/GEMINI.md` (chứa global rules cho mọi workspace, bắt buộc)
- Project: `[project]/.agents/rules/GEMINI.md` hoặc `[project]/GEMINI.md` (chứa các rules đặc thù cho workspace hiện tại ở thư mục gốc, bắt buộc)
- Style guidelines, behavioral constraints, general instructions

---

## 4. Memory trong Antigravity

### File-Based Memory
Antigravity không có built-in persistence layer. Memory = files.

**Patterns phổ biến**:

#### Knowledge Files
```
memory/
├── domain-patterns/     # Domain-specific knowledge
│   └── [domain].md
├── user-preferences/    # User settings/preferences
│   └── preferences.md
└── session-context/     # Accumulated session context
    └── current.md
```

#### Referencing Memory
Trong Agent system prompt:
```markdown
## MEMORY
Trước mỗi session, đọc:
- `memory/user-preferences/preferences.md` — sở thích user
- `memory/domain-patterns/[domain].md` — patterns domain hiện tại

Sau mỗi session, cập nhật nếu có thông tin mới.
```

---

## 5. Workflows trong Antigravity

### Không có built-in workflow engine
Workflows trong Antigravity = **instructions trong markdown files**.
Agent follow instructions, không có state machine runtime.

**Pattern**: Viết workflow dạng decision tree / checklist:

```markdown
## Workflow: [Tên]

### Step 1: [Tên bước]
- Kiểm tra: [condition]
- Nếu CÓ → [action]
- Nếu KHÔNG → [action khác]

### Step 2: [Tên bước]
[...]
```

---

## 6. Tools (MCP) trong Antigravity

### MCP Integration
Antigravity hỗ trợ MCP (Model Context Protocol) servers.

**Pattern khi tạo tool spec cho Agent Kit**:

```markdown
## TOOLS

### [Tool Name]
- **MCP Server**: [server-name]
- **Tool**: [tool-name]
- **Parameters**: [params]
- **Returns**: [output]
- **When to use**: [condition]
```

### Built-in Tools (không cần MCP)
Agent trong Antigravity đã có sẵn:
- File read/write
- Terminal commands
- Web search
- Browser automation
- Image generation

→ KHÔNG cần tạo MCP tool cho các khả năng này.

---

## 7. Naming Conventions

| Item | Convention | Ví dụ |
|:-----|:-----------|:------|
| Skill name | lowercase-hyphenated | `book-writing-assistant` |
| Agent file | lowercase-hyphenated.md | `domain-analyst.md` |
| Reference file | lowercase-hyphenated.md | `outcome-lenses.md` |
| Directory | lowercase-hyphenated | `component-specs` |
| Memory file | lowercase-hyphenated.md | `user-preferences.md` |

---

## 8. Anti-Patterns trong Antigravity

| Anti-pattern | Vấn đề | Sửa |
|:-------------|:-------|:----|
| Skill > 500 dòng | Token overhead mỗi lần trigger | Tách sang references/ |
| Memory trong system prompt | Token lãng phí, không update được | File-based memory |
| Workflow cần runtime | Antigravity không có workflow engine | Viết dạng instructions |
| MCP cho file I/O | Antigravity đã có built-in | Dùng built-in tools |
| Skills.json khi đặt đúng chỗ | Không cần registration | Chỉ dùng khi non-standard path |
