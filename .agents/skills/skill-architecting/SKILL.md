---
name: skill-architecting
description: >
  Thiết kế cấu trúc thư mục skill chuẩn Anthropic Skill Creator & Antigravity IDE,
  cấu trúc Scoped Memory (shared, domains, runs), conditional loading và ánh xạ kỹ năng theo cụm Specialist Agents.
  Kích hoạt khi tạo skill mới hoặc chuẩn hóa kiến trúc kit.
when_to_use: "Khi cần thiết kế cấu trúc thư mục skill theo chuẩn Skill Creator, memory schema hoặc mapping Specialist -> Skills."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.6.0
---

# Skill Architecting

Kỹ năng thiết kế cấu trúc thư mục skill theo tiêu chuẩn **Anthropic Skill Creator**, kết hợp với kiến trúc Scoped Memory và ánh xạ cụm năng lực cho hệ thống Agent Kit.

---

## 🚨 MANDATORY HARD GATE: KÍCH HOẠT SKILL CREATOR TRƯỚC TIÊN (ZERO-TOLERANCE)

Trước khi khởi tạo hoặc chỉnh sửa bất kỳ file `skills/<name>/SKILL.md` nào:
- **BẮT BUỘC** kích hoạt và đọc [skill-creator/SKILL.md](file:///C:/Users/nhdcb/.gemini/config/plugins/anthropic-skills/skills/skill-creator/SKILL.md) (global plugin — nếu path không tồn tại, tìm trong `plugins/anthropic-skills/skills/skill-creator/` của user config).
- **TUYỆT ĐỐI KHÔNG** sinh file `SKILL.md` từ trí nhớ mà chưa nạp `skill-creator`.
- Tuân thủ quy trình chuẩn: Capture Intent $\rightarrow$ Pushy Description $\rightarrow$ 3-Tier Progressive Disclosure $\rightarrow$ Imperative / Why-driven style $\rightarrow$ Concrete Input/Output Examples $\rightarrow$ Evals.

---

## 📚 REFERENCE KNOWLEDGE ACTIVATION (NẠP ON-DEMAND)

Khi cần tra cứu chuẩn kỹ thuật và cấu trúc mở rộng:
- **Chuẩn Contract & Tool ACI Design**: Đọc [component-contracts.md](../../references/component-contracts.md).
- **Cây quyết định Topology Workflow & Scale-Out Trigger**: Đọc [workflow-topologies.md](../../references/workflow-topologies.md).
- **5-Part Node Anatomy & Artifacts Isolation**: Đọc [state-machine-nodes.md](../../references/state-machine-nodes.md) khi thiết kế Workflow State Machine.

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
├── scripts/                  # Code thực thi các tác vụ tất định (Deterministic tasks / Verification)
└── assets/                   # Templates, schemas, static assets
```

### 3 Tầng Progressive Disclosure:
1. **Metadata** (`name` + `description` + `when_to_use` trong YAML frontmatter): Luôn nạp vào context (~100 từ).
2. **Body `SKILL.md`**: Nạp khi skill được kích hoạt (< 500 dòng).
3. **Bundled Resources (`references/`, `scripts/`, `assets/`)**: Chỉ nạp on-demand khi có chỉ dẫn.

---

## 2. QUY CHUẨN SOẠN THẢO SKILL THEO SKILL CREATOR

1. **Pushy Trigger Description & when_to_use**:
   - `description` trong YAML frontmatter là cơ chế kích hoạt chính. Phải viết "pushy" (nêu rõ cả năng lực lẫn các từ khóa/ngữ cảnh trigger) để chống hiện tượng LLM under-triggering.
   - Thêm trường `when_to_use` nêu rõ cả trường hợp NÊN DÙNG và trường hợp KHÔNG DÙNG (Exclusions) để tối ưu hóa nạp có điều kiện (Conditional Loading).
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
