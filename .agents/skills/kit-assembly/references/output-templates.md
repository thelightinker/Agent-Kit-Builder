# Output Templates — Mẫu output cho từng Kit Type

---

## Micro Kit Output

```markdown
# [TÊN AGENT]

## TÓM TẮT CHO NGƯỜI DÙNG
[3-5 dòng: làm gì / dùng khi nào / giới hạn]

---

# SYSTEM PROMPT: [TÊN AGENT]

## 1. VAI TRÒ & OUTCOME ĐÍCH

Bạn là **[vai trò]** — [mô tả 1 câu].

### Definition of Done
- [ ] [Tiêu chí nhị phân, đo được 1]
- [ ] [Tiêu chí 2]
- [ ] [Tiêu chí 3]

## 2. NGUYÊN TẮC VẬN HÀNH

**[Outcome 1]** → [Cơ chế đạt outcome]

**[Outcome 2]** → [Cơ chế đạt outcome]

## 3. HARD CONSTRAINTS

- KHÔNG [constraint cụ thể, verifiable 1]
- KHÔNG [constraint 2]

## 4. FORMAT ĐẦU RA

[Template output mà agent dùng để trả kết quả]
```

---

## Standard Kit Output

```markdown
# [TÊN KIT]

## TÓM TẮT CHO NGƯỜI DÙNG
[3-5 dòng: hệ thống này làm gì / gồm gì / khi nào dùng / giới hạn]

## DANH SÁCH THÀNH PHẦN
| Component | Mô tả | Path |
|:----------|:------|:-----|
| Agent | [1 câu] | agent/[name].md |
| Skills | [nếu có] | skills/[name]/ |
| Memory | [nếu có] | memory/ |

---

[NỘI DUNG TỪNG COMPONENT]
```

---

## Professional Kit Output

### README.md
```markdown
# [TÊN KIT]

## TÓM TẮT CHO NGƯỜI DÙNG
[3-5 dòng đời thường]

## Cài đặt & Sử dụng
1. Copy thư mục kit vào project
2. [Hướng dẫn cụ thể]

## Thành phần
| Component | Số lượng | Mô tả |
|:----------|:---------|:------|
| Agents | [N] | [tổng quan] |
| Skills | [N] | [tổng quan] |
| Workflows | [N] | [tổng quan] |
| Rules | [N] | [tổng quan] |
```

### ARCHITECTURE.md
```markdown
# [TÊN KIT] Architecture

## Overview
[Mô tả kiến trúc tổng quan]

## Agents ([N])
| Agent | Focus | Skills Used |
|:------|:------|:-----------|
| [name] | [focus] | [skills] |

## Skills ([N])
| Skill | Description |
|:------|:-----------|
| [name] | [desc] |

## Workflows ([N])
| Command | Description |
|:--------|:-----------|
| [cmd] | [desc] |

## Directory Structure
[Cây thư mục]
```

### manifest.json
```json
{
  "kitVersion": "1.0.0",
  "schemaVersion": "1.0.0",
  "agents": {
    "[agent-name]": {
      "path": "agent/[agent-name].md",
      "version": "1.0.0",
      "requires": {
        "skills": {
          "[skill-name]": "^1.0.0"
        }
      },
      "tools": ["Read", "Write", "Edit", "Grep", "Glob"]
    }
  },
  "skills": {
    "[skill-name]": {
      "path": "skills/[skill-name]/SKILL.md",
      "version": "1.0.0"
    }
  },
  "rules": {
    "[rule-name]": {
      "path": "rules/[rule-name].md",
      "version": "1.0.0",
      "priority": "P0",
      "trigger": "always_on"
    }
  },
  "workflows": {
    "[workflow-name]": {
      "path": "workflows/[workflow-name].md",
      "version": "1.0.0"
    }
  }
}
```

---

## Suite Kit — Thêm routing

### rules/request-routing.md
```markdown
---
name: request-routing
version: 1.0.0
priority: P0
trigger: always_on
---

# Request Routing

## Request Classifier
| Request Type | Trigger | Route To |
|:-------------|:--------|:---------|
| [type 1] | [keywords/patterns] | [agent-name] |
| [type 2] | [keywords/patterns] | [agent-name] |

## Agent Routing Protocol
1. Analyze request → detect domain
2. Select agent(s)
3. Announce: "🤖 Applying knowledge of @[agent-name]..."
4. Apply agent's persona and rules

## Handoff Protocol
| From | To | Trigger | Payload |
|:-----|:---|:--------|:--------|
| [agent A] | [agent B] | [condition] | [data format] |
```

---

## Frontmatter Templates

### Agent Frontmatter
```yaml
---
name: agent-name
description: [Vai trò + khi nào activate]
tools: Read, Grep, Glob, Bash, Write, Edit
version: 1.0.0
skills: skill-1, skill-2
---
```

### Skill Frontmatter
```yaml
---
name: skill-name
description: >
  [Trigger conditions — pushy, specific, include edge cases]
when_to_use: "[When to activate. NOT for X.]"
allowed-tools: Read, Grep, Glob
version: 1.0.0
---
```

### Rule Frontmatter
```yaml
---
name: rule-name
version: 1.0.0
priority: P0
trigger: always_on
---
```

### Workflow Frontmatter
```yaml
---
name: workflow-name
version: 1.0.0
trigger: "/command-name"
---
```
