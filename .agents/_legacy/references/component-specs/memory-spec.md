# Memory Spec — Chuẩn thiết kế Memory

Memory = persistent knowledge cho agent. Giúp agent nhớ context, patterns,
preferences qua các session.

---

## Khi nào tạo Memory

| Tình huống | Tạo memory? |
|:-----------|:-----------|
| Agent cần nhớ context qua sessions | ✅ Có |
| Agent cần voice/style profile | ✅ Có |
| Agent cần accumulated domain knowledge | ✅ Có |
| Agent cần user preferences | ✅ Có |
| Agent Tier 1, mỗi request độc lập | ❌ Không |
| Context nhỏ, fit trong system prompt | ❌ Không |

---

## Memory Types

### 1. Static Reference Memory
Knowledge không thay đổi — domain facts, templates, guidelines.

```
memory/
└── references/
    ├── domain-glossary.md       # Thuật ngữ domain
    ├── style-guide.md           # Hướng dẫn style
    └── templates/               # Output templates
```

**Load rule**: Luôn load khi agent start session.

### 2. Dynamic Session Memory
Context tích luỹ qua mỗi session — preferences, decisions, history.

```
memory/
└── session/
    ├── user-preferences.md      # Sở thích user
    ├── decision-log.md          # Quyết định đã đưa ra
    └── context-history.md       # Context từ sessions trước
```

**Load rule**: Load khi start session.
**Update rule**: Update sau mỗi session (append, không overwrite).

### 3. Working Memory
Context trong 1 session — draft hiện tại, state hiện tại.

```
memory/
└── working/
    ├── current-state.md         # State hiện tại
    └── draft/                   # Draft đang làm việc
```

**Load rule**: Load khi resume work.
**Update rule**: Update real-time trong session.

---

## Memory Schema

Mỗi memory file cần header:

```markdown
# [Tên Memory]
**Type**: [Static Reference / Dynamic Session / Working]
**Updated**: [timestamp]
**Load when**: [condition]
**Update when**: [condition]

---

[Nội dung]
```

---

## Memory trong System Prompt

Agent system prompt tham chiếu memory:

```markdown
## MEMORY

### Trước mỗi session
Đọc các file sau trước khi bắt đầu:
- `memory/references/style-guide.md` — hướng dẫn style
- `memory/session/user-preferences.md` — sở thích user

### Sau mỗi session
Cập nhật nếu phát hiện thông tin mới:
- Preferences user thay đổi → update `user-preferences.md`
- Quyết định quan trọng → append vào `decision-log.md`
```

---

## Storage Strategy (Antigravity)

Antigravity IDE: file-based, markdown.

| Aspect | Strategy |
|:-------|:---------|
| Format | Markdown (.md) |
| Location | Trong project directory |
| Persistence | File system — persist qua sessions |
| Access | Agent đọc/ghi file bằng built-in tools |
| Concurrency | Single agent — không cần locking |

---

## Quality Checklist

```
□ Mỗi memory file có header (type, load/update rules)
□ Load rules rõ ràng — agent biết khi nào nạp
□ Update rules rõ ràng — agent biết khi nào cập nhật
□ Không nhồi static content vào system prompt
□ Memory phục vụ outcome thực tế — không tạo "cho đủ"
□ File-based, Antigravity-compatible
```
