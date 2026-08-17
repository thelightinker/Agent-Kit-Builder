---
name: kit-assembling
description: >
  Lắp ráp các cấu phần thành Agent Kit hoàn chỉnh trong thư mục cách ly
  ./output/<kit-name>/, sinh manifest.json chuẩn SSOT (khai báo topology,
  delegatesTo, ownedSkills, memoryScope), và đóng gói theo chuẩn Kit Type.
  Luôn kích hoạt ở bước hoàn thiện của quy trình tạo kit.
when_to_use: "Khi hoàn tất các cấu phần và cần lắp ráp thành thư mục Agent Kit hoàn chỉnh."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.2.0
---

# Kit Assembling

Kỹ năng tổng hợp, tổ chức thư mục và đóng gói Agent Kit hoàn chỉnh, tuân thủ nghiêm ngặt ranh giới cách ly không gian làm việc và chuẩn hóa `manifest.json` làm Single Source of Truth (SSOT).

---

## 1. WORKSPACE ISOLATION (BẤT BIẾN)

- Mọi file của Agent Kit mới **BẮT BỘC** được tạo tại:
  `./output/<kit-name>/` (ví dụ: `./output/marketing-growth-suite/`)
- **TUYỆT ĐỐI KHÔNG** ghi đè hoặc tạo trực tiếp vào `.agents/` của Agent Kit Creator.

---

## 2. CẤU TRÚC ĐÓNG GÓI THEO TOPOLOGY

### A. Single Agent Kit (Micro / Standard)
```
output/<kit-name>/
├── agent/
│   └── [kit-name].md         # System prompt chính
├── skills/
│   └── [skill-name]/SKILL.md # Skills trực thuộc
├── workflows/
└── manifest.json
```

### B. Multi-Agent Suite Kit (Mini-Suite / Full Suite)
```
output/<suite-name>/
├── agent/
│   ├── [orchestrator-name].md # Master Orchestrator
│   ├── [specialist-a].md      # Real Specialist Agent A
│   └── [specialist-b].md      # Real Specialist Agent B
├── skills/                    # Domain skills mapped to Specialists
│   ├── [skill-a1]/SKILL.md
│   └── [skill-b1]/SKILL.md
├── workflows/
├── memory/
│   ├── MEMORY.md
│   ├── shared/
│   └── domains/
└── manifest.json              # Khai báo SSOT phân cấp
```

---

## 3. SINH MANIFEST.JSON CHUẨN SSOT

Khai báo đầy đủ trường `topology`, `role`, `delegatesTo`, `ownedSkills`, `memoryScope`:

```json
{
  "name": "kit-name",
  "kitVersion": "1.0.0",
  "topology": {
    "type": "hierarchical-multi-agent",
    "orchestrator": "master-orchestrator",
    "spectrumPosition": "full-suite",
    "rightAltitudeRationale": "Decoupled domains with independent skill clusters."
  },
  "agents": {
    "master-orchestrator": {
      "role": "master-orchestrator",
      "tools": ["Read", "Grep", "Glob", "Agent"],
      "delegatesTo": ["specialist-a", "specialist-b"]
    },
    "specialist-a": {
      "role": "domain-specialist",
      "domain": "domain-a",
      "tools": ["Read", "Grep", "Glob", "Edit", "Write"],
      "ownedSkills": ["skill-a1", "skill-a2"],
      "memoryScope": ["shared", "domains/domain-a"]
    }
  },
  "skills": { ... },
  "workflows": { ... }
}
```
