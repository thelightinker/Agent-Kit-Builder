---
name: skill-architecting
description: >
  Thiết kế cấu trúc thư mục skill chuẩn Anthropic Skill Creator & Antigravity IDE,
  cấu trúc Scoped Memory (shared, domains, runs) và ánh xạ kỹ năng theo cụm Specialist Agents.
  Kích hoạt khi tạo skill mới hoặc chuẩn hóa kiến trúc kit.
when_to_use: "Khi cần thiết kế cấu trúc thư mục skill theo chuẩn Skill Creator, memory schema hoặc mapping Specialist -> Skills."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.3.0
---

# Skill Architecting

Kỹ năng thiết kế cấu trúc thư mục skill theo tiêu chuẩn **Anthropic Skill Creator**, kết hợp với kiến trúc Scoped Memory và ánh xạ cụm năng lực cho hệ thống Agent Kit.

---

## 📚 REFERENCE KNOWLEDGE ACTIVATION (NẠP ON-DEMAND)

Khi cần tra cứu chuẩn kỹ thuật và cấu trúc nâng cao:
- **Chuẩn Anthropic Skill Creator**: Đọc [skill-creator/SKILL.md](file:///C:/Users/nhdcb/.gemini/config/plugins/anthropic-skills/skills/skill-creator/SKILL.md) để áp dụng quy trình tạo skill, trigger optimization và anatomy chuẩn.
- **Chuẩn Contract & Tool ACI Design**: Đọc [component-contracts.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/component-contracts.md).
- **Cây quyết định Topology Workflow & Scale-Out Trigger**: Đọc [workflow-topologies.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/workflow-topologies.md).

---

## 1. ANTHROPIC SKILL CREATOR ANATOMY

Mọi skill tạo ra trong Output Kit bắt buộc tuân theo cấu trúc 3 tầng:

```
skills/<skill-name>/
├── SKILL.md                  # BẮT BUỘC — Frontmatter + chỉ dẫn chính (< 500 dòng)
├── references/               # Tài liệu tra cứu nạp on-demand (> 300 dòng cần Table of Contents)
│   └── [topic].md
├── examples/                 # Ví dụ mẫu Input -> Output (Few-shot patterns)
│   └── [example].md
├── scripts/                  # Code thực thi các tác vụ tất định (Deterministic tasks)
└── assets/                   # Templates, schemas, static assets
```

### 3 Tầng Progressive Disclosure:
1. **Metadata** (`name` + `description` trong YAML frontmatter): Luôn nạp vào context (~100 từ).
2. **Body `SKILL.md`**: Nạp khi skill được kích hoạt (< 500 dòng).
3. **Bundled Resources (`references/`, `scripts/`, `assets/`)**: Chỉ nạp on-demand khi có chỉ dẫn.

---

## 2. QUY CHUẨN SOẠN THẢO SKILL THEO SKILL CREATOR

1. **Pushy Trigger Description**:
   - `description` trong YAML frontmatter là cơ chế kích hoạt chính. Phải viết "pushy" (nêu rõ cả năng lực lẫn các từ khóa/ngữ cảnh trigger) để chống hiện tượng LLM under-triggering.
   - *Ví dụ:* `"Tối ưu hóa SEO On-Page. BẮT BUỘC sử dụng kỹ năng này khi người dùng nhắc đến audit SEO, meta tags, schema markup, hoặc muốn cải thiện thứ hạng tìm kiếm, ngay cả khi họ không nói rõ từ khóa 'SEO'."`
2. **Writing Style (Phong cách Soạn thảo)**:
   - Dùng câu mệnh lệnh (Imperative).
   - Giải thích lý do **"Why"** đằng sau các chỉ dẫn thay vì dùng các từ cấm võ đoán ("MUST", "ALWAYS").
   - Cung cấp ít nhất 1-2 ví dụ cụ thể theo mẫu:
     ```markdown
     **Example 1:**
     Input: ...
     Output: ...
     ```
3. **Principle of Lack of Surprise**:
   - Skill không chứa mã độc hại, không can thiệp trái phép, minh bạch và an toàn.

---

## 3. NGUYÊN TẮC ÁNH XẠ SPECIALIST ➔ SKILLS

- **Specialist Ownership**: Mỗi Specialist Agent sở hữu cụm kỹ năng chuyên sâu tương ứng (`ownedSkills`).
- **No Orphan Skills**: Mọi skill trong `skills/` phải thuộc quyền sở hữu của ít nhất một Specialist hoặc Master Orchestrator.

---

## 4. KIẾN TRÚC SCOPED MEMORY

```
memory/
├── MEMORY.md                 # Chỉ mục bộ nhớ (SSOT index ≤ 200 dòng)
├── shared/                   # Dành cho toàn bộ Suite (brand voice, conventions)
├── domains/                  # Dành riêng cho từng Specialist
└── runs/                     # Dành cho phiên thực thi dài hạn (feature trackers, golden runs)
```
