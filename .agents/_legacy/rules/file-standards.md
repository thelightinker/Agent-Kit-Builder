---
name: file-standards
version: 1.2.0
priority: P0
trigger: always_on
description: "Tiêu chuẩn cấu trúc file linh hoạt, 3 loại trigger của Rule và quy tắc mở rộng cho Agent Kit."
---

# File Standards & Rule Triggers

> Quy định chuẩn hóa định dạng file: Giữ nguyên các bất biến kỹ thuật nhưng tối đa hóa tính linh động.

---

## 1. 3 Loại Trigger Chuẩn cho Rules (`trigger:`)

Tất cả các Rule trong Agent Kit chỉ sử dụng **3 loại Trigger chính thức** sau đây:

1. **`manual`**: Chỉ chạy khi người dùng hoặc Agent gọi trực tiếp bằng tên rule (ví dụ: `@rule-name` hoặc `/rule-name`).
2. **`always_on`**: Luôn luôn được nạp và áp dụng trong mọi lượt chat.
3. **`model_decision`**: AI tự động đọc `description` và bối cảnh để tự quyết định có sử dụng rule hay không.

### 1.1 Cú pháp Frontmatter chuẩn cho Rules (`.agents/rules/*.md`)
```yaml
---
name: kebab-case-name
version: 1.0.0
priority: P0 # P0: Toàn hệ thống | P1: Cấp Agent | P2: Cấp Skill
trigger: always_on # [always_on | manual | model_decision]
description: Mô tả ngắn gọn về mục đích và điều kiện áp dụng rule.
# Các trường mở rộng tùy chọn:
tags: [security, code-style]
domain: backend
---
```

---

## 2. Frontmatter Chuẩn cho các Thành phần khác

### 2.1 Workflows (`.agents/workflows/*.md`)
```yaml
---
name: workflow-name
description: Mô tả mục đích và kịch bản sử dụng workflow.
version: 1.0.0
requires_skills: [skill-a, skill-b]
requires_agents: [agent-x]
---
```

### 2.2 Skills (`.agents/skills/<skill-name>/SKILL.md`)
```yaml
---
name: skill-name
description: Mô tả năng lực với các từ khóa trigger linh hoạt.
when_to_use: "Điều kiện cụ thể khi nào agent cần nạp skill này."
version: 1.0.0
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---
```

### 2.3 Agents (`.agents/agent/<agent-name>.md`)
```yaml
---
name: agent-name
description: Vai trò và phạm vi trách nhiệm của agent.
tools: [Read, Write, Edit, Glob, Grep, Bash, Agent]
model: inherit
version: 1.0.0
skills: [skill-a, skill-b]
---
```

### 2.4 Workflow Output Checkpoint Contract (`[Evaluation Loop]`)
Mọi Node trong Workflow sản sinh file tại `./output/<kit-name>/` BẮT BỘC khai báo Checkpoint Gate:
```yaml
risk_tier: T0 | T1 | T2 | T3
reason_code: IRREVERSIBLE_ACTION | POLICY_BOUNDARY | EXTERNAL_WRITE | INTERNAL_DRAFT | DETERMINISTIC_PASS
decided_by: orchestrator  # BẮT BỘC, KHÔNG BAO GIỜ dùng "model"
checkpoint_cmd: python .agents/scripts/checkpoint_gate.py --node <node_id> --target <output_files> --op <create|modify|delete>
```


---

## 3. Triết lý Thiết kế: "Khung Cứng - Nội dung Mềm"

- **Khung cứng (Rigid Frame)**: 
  - Cú pháp YAML Frontmatter nằm giữa 2 cặp `---`.
  - Cú pháp JSON chuẩn (không lỗi trailing comma).
  - 3 Loại Trigger cho Rule: `always_on`, `manual`, `model_decision`.
- **Nội dung mềm (Soft Content)**:
  - Tùy biến tiêu đề các mục theo domain.
  - Tự do bổ sung các trường mở rộng (`tags`, `metadata`, `domain`, `hooks`, `inputs`).
  - Hỗ trợ xử lý phân nhánh, fallback và đa luồng.
