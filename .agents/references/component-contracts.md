# Component Contracts & Technical Specifications

> Đặc tả kỹ thuật, cấu trúc YAML Frontmatter, định dạng SSOT `manifest.json` và chuẩn thiết kế Tool / ACI cho toàn bộ các thành phần trong Agent Kit.

---

## 1. MANIFEST.JSON (SINGLE SOURCE OF TRUTH - SSOT)

`manifest.json` là nguồn sự thật duy nhất khai báo cấu trúc Topology, quan hệ sở hữu và ranh giới phân quyền:

```json
{
  "name": "growth-marketing-suite",
  "kitVersion": "1.0.0",
  "topology": {
    "type": "hierarchical-multi-agent",
    "orchestrator": "growth-orchestrator",
    "spectrumPosition": "full-suite",
    "rightAltitudeRationale": "Decoupled 3 domains with independent skill clusters and scoped memory."
  },
  "agents": {
    "growth-orchestrator": {
      "role": "master-orchestrator",
      "tools": ["Read", "Grep", "Glob", "Agent"],
      "delegatesTo": ["seo-specialist", "copy-specialist"]
    },
    "seo-specialist": {
      "role": "domain-specialist",
      "domain": "seo",
      "tools": ["Read", "Grep", "Glob", "Edit", "Write"],
      "ownedSkills": ["seo-audit", "ai-seo-optimizer"],
      "memoryScope": ["shared", "domains/seo-playbook"]
    }
  },
  "skills": { ... },
  "workflows": { ... }
}
```

---

## 2. AGENT CONTRACTS

### A. Master Orchestrator (`agent/<name>.md`)
```yaml
---
name: kebab-orchestrator-name
description: "Master Orchestrator điều phối toàn bộ Suite."
tools: Read, Grep, Glob, Agent
model: inherit
delegates_to: [specialist-a, specialist-b]
version: 1.0.0
---
```

### B. Specialist Agent (`agent/<name>.md` - Real Agent)
```yaml
---
name: kebab-specialist-name
description: "Specialist chịu trách nhiệm chuyên môn domain X."
tools: Read, Grep, Glob, Edit, Write
model: inherit
domain: domain-name
skills: [skill-a, skill-b]
version: 1.0.0
---
```

---

## 3. SKILL CONTRACT (`skills/<name>/SKILL.md`)

```yaml
---
name: kebab-case-name
description: >
  Mô tả năng lực và bối cảnh trigger. Viết pushy và cụ thể.
when_to_use: "Điều kiện khi nào cần nạp skill này."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---
```

*Progressive Disclosure:* `SKILL.md` giữ dưới 500 dòng. Chi tiết tra cứu dài > 300 dòng bắt buộc tách sang `references/`.

---

## 4. WORKFLOW CONTRACT (`workflows/<name>.md`)

```yaml
---
name: kebab-case-name
description: "Mô tả mục đích của workflow."
version: 1.0.0
requires_agents: [orchestrator-name, specialist-a]
requires_skills: [skill-a, skill-b]
artifact_outputs: [output-name]
---
```

---

## 5. SCOPED MEMORY CONTRACT (`memory/`)

- `MEMORY.md`: File chỉ mục chính, giới hạn nghiêm ngặt **$\le 200$ dòng**.
- `shared/`: Tri thức dùng chung toàn bộ suite (ví dụ: `brand-guidelines.md`).
- `domains/`: Tri thức chuyên biệt của từng Specialist.
- `runs/`: Trạng thái thực thi (`features-tracker.json`).
