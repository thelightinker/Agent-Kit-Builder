---
name: kit-extending
description: "Self-extension skill for Agent Kits. Use ALWAYS whenever creating, adding, refactoring, or extending rules (.agents/rules/), workflows (.agents/workflows/), or skills (.agents/skills/) in this workspace to guarantee 100% Antigravity IDE contract compliance."
when_to_use: "Kích hoạt khi người dùng yêu cầu tạo mới hoặc bổ sung Rule, Workflow, hoặc Skill vào Agent Kit hiện tại."
requires_templates: ["templates/rule-template.md", "templates/workflow-template.md", "templates/skill-template.md"]
requires_references: ["references/file-standards.md"]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# Kit Extending — Self-Extension Skill for Antigravity IDE Agent Kits

> Enables any Agent Kit to create new Rules, Workflows, or Skills for itself in target workspaces with 100% Antigravity IDE compliance.

---

## 1. Rule Creation Contract (`.agents/rules/<rule-name>.md`)

Khi người dùng yêu cầu tạo hoặc sửa một **Rule**:
1. Đặt file tại đường dẫn: `.agents/rules/<rule-name>.md` (tên dạng kebab-case).
2. **BẮT BỘC** sử dụng đúng cớ chế YAML Frontmatter:

```yaml
---
name: rule-name
version: 1.0.0
priority: P0 # P0: Hệ thống | P1: Cấp Agent | P2: Cấp Skill
trigger: always_on # BẮT BỘC chỉ dùng 1 trong 3 giá trị: [always_on | manual | model_decision]
description: Mô tả ngắn gọn mục đích và điều kiện áp dụng rule.
---
```

3. **Chỉ dùng 3 loại Trigger chính thức**:
   - `always_on`: Luôn nạp và áp dụng trong mọi lượt chat.
   - `manual`: Chỉ chạy khi gọi tên rule (ví dụ: `@rule-name` hoặc `/rule-name`).
   - `model_decision`: AI tự động chọn nạp dựa vào `description` và bối cảnh.

---

## 2. Workflow Creation Contract (`.agents/workflows/<workflow-name>.md`)

Khi người dùng yêu cầu tạo hoặc sửa một **Workflow**:
1. Đặt file tại đường dẫn: `.agents/workflows/<workflow-name>.md`.
2. **BẮT BỘC** sử dụng YAML Frontmatter đầy đủ:

```yaml
---
name: workflow-name
description: "Mô tả ngắn gọn mục đích workflow."
version: 1.0.0
requires_agents: [master-compiler]
requires_skills: [domain-analysis, kit-assembly]
artifact_outputs: [agent-kit-spec]
topology: chaining # [chaining | routing | parallelization | orchestrator-workers | evaluator-optimizer | autonomous-agent]
trigger: manual
permissions: read-only
tools_allowed: [Read, Write, Edit, Glob, Grep, Bash]
safe_outputs:
  write_file: "Chỉ được phép ghi file trong thư mục dự án"
max_retry_per_node: 2
---
```

3. **BẮT BỘC** tuân thủ cấu trúc State Machine 5 phần cho từng Node:

```markdown
# Workflow: [TÊN WORKFLOW]

## [STATE: INIT]
[Input Artifacts]: <khoá dữ liệu đầu vào>
[Output Artifacts]: <khoá dữ liệu đầu ra>
[DoD]
- [ ] <Điều kiện nhị phân 1: Pass/Fail rõ ràng>
- [ ] <Điều kiện nhị phân 2: Đo được từ Output Artifact>
- [ ] <Điều kiện nhị phân 3: 0 tính từ sáo ngữ>
[Evaluation Loop]: Evaluate ➔ Pass ➔ Transition sang [STATE: KẾ TIẾP] / Fail ➔ Revise (Tối đa max_retry_per_node lần) ➔ Escalate sang [ESCALATE_HUMAN]

## [STATE: STEP_1]
...

## [ESCALATE_HUMAN]
Kích hoạt khi: Node fail DoD quá số lần retry quy định.
Output: Log lý do fail + needs_human_review: true. KHÔNG tự publish.
```

---

## 3. Skill Creation Contract (`.agents/skills/<skill-name>/SKILL.md`)

Khi người dùng yêu cầu tạo hoặc bổ sung một **Skill**:
1. Đặt file tại đường dẫn: `.agents/skills/<skill-name>/SKILL.md`.
2. **BẮT BỘC** sử dụng YAML Frontmatter pushy trigger:

```yaml
---
name: skill-name
description: "Mô tả năng lực skill. Sử dụng từ khóa định hướng kích hoạt pushy trigger để LLM nạp đúng lúc."
when_to_use: "Kích hoạt khi..."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---
```

3. **Nội dung SKILL.md**:
   - Viết ngắn gọn (dưới 500 dòng).
   - Đưa câu lệnh CLI Quick Start trực tiếp.
   - Phân cấp thông tin (Progressive Disclosure) nếu có tài liệu tham chiếu sâu (`references/`).

---

## 4. Output Checkpoint Integration Contract

Khi tạo mới hoặc refactor bất kỳ Workflow hay Agent Kit nào:
1. Đảm bảo mọi sản phẩm Output được ghi ra `./output/<kit-name>/` đều được bảo vệ bởi Checkpoint Gate.
2. Khai báo và gọi script điều phối: `python .agents/scripts/checkpoint_gate.py --node <node_id> --target <output_file> --op <create|modify|delete>`.
3. BẮT BỘC tuân thủ `decided_by: orchestrator`. Tuyệt đối KHÔNG cho phép LLM tự bỏ qua hoặc tự duyệt Checkpoint.

