---
name: skill-architecting
description: >
  Thiết kế cấu trúc thư mục skill chuẩn Antigravity IDE, viết SKILL.md
  tuân thủ Progressive Disclosure, và đặc tả chuẩn Frontmatter cho mọi cấu phần
  (Agent, Skill, Workflow, Rule, Memory). Kích hoạt khi tạo skill mới hoặc chuẩn hóa cấu trúc kit.
when_to_use: "Khi cần tạo mới skill folder, viết SKILL.md hoặc chuẩn hóa YAML frontmatter cho Agent Kit."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.1.0
---

# Skill Architecting

Kỹ năng thiết kế cấu trúc thư mục skill và đặc tả chuẩn kỹ thuật cho hệ thống Agent Kit, tối ưu hóa Context Window thông qua Progressive Disclosure.

---

## 📚 REFERENCE KNOWLEDGE ACTIVATION (NẠP ON-DEMAND)

Khi cần tra cứu chuẩn kỹ thuật và cấu trúc nâng cao:
- **Chuẩn Contract & Tool ACI Design**: Đọc [component-contracts.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/component-contracts.md) để tra cứu chuẩn YAML frontmatter, namespacing và permissions.
- **Cây quyết định Topology Workflow & Scale-Out Trigger**: Đọc [workflow-topologies.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/workflow-topologies.md) khi chọn 6 khối kiến trúc workflow và xác định ranh giới tách agent.
- **Cấu trúc 5 thành phần State Node**: Đọc [state-machine-nodes.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/state-machine-nodes.md) khi viết node state machine.
- **Scaffolding Templates**: Sử dụng [templates/skill-template.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/templates/skill-template.md) hoặc [templates/workflow-template.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/templates/workflow-template.md).

---

## 1. CẤU TRÚC THƯ MỤC SKILL CHUẨN

```
skills/<skill-name>/
├── SKILL.md              # BẮT BUỘC — Frontmatter + chỉ dẫn chính (< 500 dòng)
├── references/            # Tài liệu tra cứu nạp on-demand (tùy chọn)
│   └── [topic].md
├── examples/              # Ví dụ mẫu minh họa đầu vào/đầu ra (tùy chọn)
│   └── [example].md
├── evals/                 # Test cases đánh giá tự động (tùy chọn)
│   └── evals.json
└── scripts/               # Script hỗ trợ thực thi lặp lại (tùy chọn)
    └── [script].py
```

---

## 2. NGUYÊN TẮC PROGRESSIVE DISCLOSURE (3 TẦNG)

| Tầng | Nội dung | Thời điểm nạp | Token Budget |
|:---|:---|:---|:---|
| **1. Metadata** | `name` + `description` trong Frontmatter | Luôn luôn có trong context | ~50-100 từ |
| **2. Body** | Nội dung markdown trong `SKILL.md` | Khi skill được kích hoạt | < 500 dòng |
| **3. References** | Tài liệu chi tiết trong `references/` | Chỉ khi body chỉ dẫn cần đọc | Không giới hạn |

*Quy tắc phân tách:* Nếu một phần tài liệu dài > 300 dòng hoặc là bảng tra cứu chi tiết, BẮT BỘC tách sang `references/<name>.md`.

---

## 3. CHUẨN YAML FRONTMATTER CHO CÁC THÀNH PHẦN

### A. Skills (`skills/<name>/SKILL.md`)
```yaml
---
name: kebab-case-name
description: >
  Mô tả năng lực và điều kiện trigger. Viết rõ ràng, bao quát các từ khóa
  và bối cảnh người dùng sẽ đề cập.
when_to_use: "Điều kiện cụ thể khi nào agent cần nạp skill này."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---
```

### B. Rules (`rules/<name>.md`)
```yaml
---
name: kebab-case-name
version: 1.0.0
priority: P0 # [P0: Invariant | P1: System | P2: Guideline]
trigger: always_on # [always_on | manual | model_decision]
description: "Mô tả mục đích và phạm vi áp dụng của rule."
---
```

### C. Workflows (`workflows/<name>.md`)
```yaml
---
name: kebab-case-name
description: "Mô tả mục đích của workflow."
version: 1.0.0
requires_agents: kit-architect
requires_skills: [skill-a, skill-b]
artifact_outputs: [output-name]
---
```

### D. Agents (`agent/<name>.md`)
```yaml
---
name: kebab-case-name
description: "Vai trò và năng lực của agent."
tools: Read, Grep, Glob, Edit, Write, Bash
model: inherit
skills: [skill-a, skill-b]
version: 1.0.0
---
```

---

## 4. PHONG CÁCH VIẾT CHỈ DẪN TRONG SKILL.MD

- **Giải thích Lý do (WHY over MUST)**: Giải thích tại sao một quy tắc là cần thiết thay vì chỉ áp đặt các lệnh cấm cứng nhắc.
- **Mẫu định dạng cụ thể**: Luôn cung cấp template output rõ ràng.
- **Tập trung vào 1 năng lực cốt lõi**: Tránh biến skill thành "God Skill" ôm đồm quá nhiều nghiệp vụ không liên quan.
