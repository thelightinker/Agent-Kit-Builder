# Component Specs — Tất cả loại component

Spec cho từng loại component trong Agent Kit. Kit Generator dùng tài liệu
này để sinh component đúng format.

---

## Agent (System Prompt)

**Bắt buộc trong**: Mọi kit type.
**Spec chi tiết**: Xem `skills/prompt-engineering/SKILL.md`

Cấu trúc tối thiểu:
```markdown
# [TÊN AGENT]
## TÓM TẮT CHO NGƯỜI DÙNG
## 1. VAI TRÒ & OUTCOME ĐÍCH (+ DoD)
## 2. NGUYÊN TẮC VẬN HÀNH
## 3. HARD CONSTRAINTS
## 4. FORMAT ĐẦU RA
```

---

## Skill

**Bắt buộc trong**: Standard+ (khi agent cần reusable capabilities).
**Spec chi tiết**: Xem `skills/skill-crafting/SKILL.md`

Cấu trúc tối thiểu:
```
skill-name/
├── SKILL.md (frontmatter: name + description)
└── references/ (nếu body > 300 dòng)
```

---

## Memory

**Khi cần**: Agent cần persistent knowledge hoặc cross-session context.

### Schema Types

| Type | Mô tả | Khi nào |
|:-----|:-------|:--------|
| **Key-Value** | Cặp key=value đơn giản | Preferences, settings, flags |
| **Document** | Markdown files có cấu trúc | Knowledge base, conventions |
| **Tiered** | Hot/Warm/Cold layers | Agent xử lý nhiều context |

### Memory File Structure

```markdown
## MEMORY ARCHITECTURE

### Schema
[Key-value / Document / Tiered]

### Files
| File | Mục đích | Update frequency |
|:-----|:---------|:----------------|
| MEMORY.md | Index — trỏ tới memory files | Mỗi session |
| [topic].md | [mô tả] | [khi nào] |

### Load Rules
- Đọc MEMORY.md ở đầu mỗi session
- Load file cụ thể khi task cần

### Update Rules
- Cập nhật khi user provide preference mới
- Cập nhật khi project convention thay đổi
- Format: append, không xoá entry cũ trừ khi outdated
```

### Ví dụ Memory Files

```markdown
# MEMORY.md
> Persistent project memory. Read at session start.

## Project Conventions
→ See `project-conventions.md`

## User Preferences
→ See `user-preferences.md`

## Tech Decisions
→ See `tech-decisions.md`
```

---

## Workflow

**Khi cần**: Agent cần multi-step orchestration có state transitions.

### Workflow Format

```markdown
## WORKFLOW: [TÊN]

### Trigger
[Khi nào workflow bắt đầu]

### States
| State | Mô tả | Entry Criteria | Exit Criteria |
|:------|:------|:---------------|:-------------|
| [name] | [mô tả] | [điều kiện vào] | [điều kiện ra] |

### Transitions
| Từ | Đến | Condition | Action |
|:---|:----|:----------|:-------|
| [state A] | [state B] | [condition] | [action] |

### Error Handling
| Error | State | Recovery |
|:------|:------|:---------|
| [error] | [state xảy ra] | [cách xử lý] |
```

### Quy tắc
- Mỗi state có entry + exit criteria rõ ràng
- Không có dead-end state (mọi state có exit path)
- Error handling cho mỗi transition có thể fail
- Tối đa 7 states — quá nhiều thì chia workflow nhỏ hơn

---

## Tools (MCP/API)

**Khi cần**: Agent cần tương tác với external services.

### Tool Format

```markdown
## TOOLS

### [Tool Name]
- **Purpose**: [1 câu mô tả]
- **Type**: [MCP Server / API Call / CLI / File I/O]
- **Parameters**:
  | Param | Type | Required | Description |
  |:------|:-----|:---------|:------------|
  | [name] | [type] | [yes/no] | [mô tả] |
- **Returns**: [output format]
- **Error Handling**: [khi fail → action]
```

---

## Rules

**Khi cần**: Professional/Suite kit cần rules binding cho toàn workspace.

### Rule Format

```markdown
---
name: rule-name
version: 1.0.0
priority: P0/P1/P2
trigger: always_on / manual / model_decision
---

# [Rule Name]

[Nội dung rule]
```

### Rule Priorities
| Priority | Meaning | Example |
|:---------|:--------|:--------|
| P0 | Luôn enforce, không skip | Core protocol, routing |
| P1 | Enforce khi agent activated | Agent-specific rules |
| P2 | Reference, enforce khi cần | Quick reference, style guides |

---

## Scripts

**Khi cần**: Professional/Suite kit cần automated validation hoặc tooling.

### Common Scripts

| Script | Purpose | Kit Type |
|:-------|:--------|:---------|
| `validate_kit.py` | Self-check versions, links, refs | Professional+ |
| `generate_manifest.py` | Generate/check manifest | Professional+ |
| `validate_kit.py` | Fast validation during dev | Professional+ |
| Domain-specific scripts | Audit, lint, check domain rules | Tuỳ domain |
