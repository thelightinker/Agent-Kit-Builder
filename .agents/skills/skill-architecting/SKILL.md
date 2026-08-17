---
name: skill-architecting
description: >
  Thiết kế cấu trúc thư mục skill chuẩn Antigravity IDE, cấu trúc Scoped Memory
  (shared, domains, runs) và ánh xạ kỹ năng theo cụm Specialist Agents.
  Kích hoạt khi tạo skill mới hoặc chuẩn hóa kiến trúc kit.
when_to_use: "Khi cần thiết kế cấu trúc thư mục skill, memory schema hoặc mapping Specialist -> Skills."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.2.0
---

# Skill Architecting

Kỹ năng thiết kế cấu trúc thư mục skill, kiến trúc Scoped Memory và ánh xạ cụm năng lực cho hệ thống Agent Kit.

---

## 📚 REFERENCE KNOWLEDGE ACTIVATION (NẠP ON-DEMAND)

Khi cần tra cứu chuẩn kỹ thuật và cấu trúc nâng cao:
- **Chuẩn Contract & Tool ACI Design**: Đọc [component-contracts.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/component-contracts.md) để tra cứu chuẩn YAML frontmatter, namespacing và permissions.
- **Cây quyết định Topology Workflow & Scale-Out Trigger**: Đọc [workflow-topologies.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/workflow-topologies.md).
- **Cấu trúc 5 thành phần State Node**: Đọc [state-machine-nodes.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/state-machine-nodes.md).

---

## 1. CẤU TRÚC THƯ MỤC SKILL CHUẨN

```
skills/<skill-name>/
├── SKILL.md              # BẮT BUỘC — Frontmatter + chỉ dẫn chính (< 500 dòng)
├── references/            # Tài liệu tra cứu nạp on-demand (tùy chọn)
│   └── [topic].md
├── examples/              # Ví dụ mẫu minh họa đầu vào/đầu ra (tùy chọn)
└── scripts/               # Script hỗ trợ thực thi (tùy chọn)
```

---

## 2. NGUYÊN TẮC ÁNH XẠ SPECIALIST ➔ SKILLS

Trong hệ thống Suite Kit:
- **Mỗi Specialist Agent** sở hữu một cụm kỹ năng chuyên sâu (`ownedSkills: [skill-a, skill-b]`).
- **Không tạo Skill mồ côi (No Orphan Skills)**: Mọi skill trong `skills/` phải thuộc quyền sở hữu của ít nhất một Specialist hoặc Master Orchestrator.
- **Giảm thiểu Cross-reference**: Các skills trong cùng một cụm domain tương tác chặt chẽ; skills giữa 2 domain khác nhau chỉ phối hợp thông qua Workflow.

---

## 3. KIẾN TRÚC SCOPED MEMORY

Khi tạo bộ nhớ cho Suite Kit:

```
memory/
├── MEMORY.md                 # Chỉ mục bộ nhớ (SSOT index ≤ 200 dòng)
├── shared/                   # Dành cho toàn bộ Suite (brand voice, conventions)
├── domains/                  # Dành riêng cho từng Specialist
└── runs/                     # Dành cho phiên thực thi dài hạn (feature trackers)
```
