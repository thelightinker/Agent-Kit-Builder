---
name: kit-assembly
description: ">"
when_to_use: "Kích hoạt khi cần năng lực kit-assembly trong quy trình tạo hoặc kiểm định Agent Kit."
requires_templates: ["templates/manifest-template.json", "templates/memory-template.md"]
requires_references: ["references/suite-build-protocol.md", "references/output-format.md"]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.2.0
---

# Kit Assembly

## Overview

Tổng hợp mọi component (agent, skills, memory, workflow, tools, rules, scripts) thành một Agent Kit hoàn chỉnh. Kit Assembly đảm bảo mọi phần khớp nhau, không thừa không thiếu, không phình token lãng phí và output đúng format cho kit type đã chọn.

---

## Quy trình Assembly

### 1. Xác nhận Kit Type & Trade-off ROI Check

Kiểm tra lại kit type từ Domain Analysis và thực hiện tính toán ROI:
$$ROI = \frac{\text{Mức tăng Năng lực}}{\text{Chi phí Token \& Độ phức tạp}}$$
- **ROI >= 1.25**: Đạt chuẩn triển khai.
- **ROI < 1.0**: Over-engineered ➔ Hủy bỏ component thừa để tối ưu token.

- **Micro**: Chỉ output 1 file markdown (system prompt)
- **Standard**: Output kit folder với agent + skills/memory
- **Professional**: Output full kit với manifest, rules, scripts
- **Suite**: Output multi-agent kit với orchestrator + routing

Chi tiết mỗi type: → `references/kit-types.md`

### 2. Component Integration & Token Budgeting

Đảm bảo mọi component tương thích và tiết kiệm token:

```
□ Agent system prompt references đúng skill names
□ Skills sử dụng Selective Reading (chỉ nạp dữ liệu chi tiết khi cần)
□ Memory schema sử dụng Skeleton State (< 1KB) tránh phình context
□ Workflow states dạng Node Anatomy 5 phần
□ Tools/Scripts có instructions sử dụng rõ ràng
□ Rules không mâu thuẫn với agent instructions
```

### 3. Directory Structure (Workspace Isolation Enforcement)

> ⚠️ **HARD CONSTRAINT**: Tất cả các Agent Kit mới BẮT BỘC phải nằm trong thư mục cách ly `./output/<kit-name>/`. TUYỆT ĐỐI KHÔNG ghi trực tiếp các file/folder của kit mới vào gốc `.agents/` của Agent Kit Creator!

#### Micro Kit
```
output/[kit-name]/
└── [agent-name].md    # System prompt + TÓM TẮT
```


#### Standard Kit
```
output/
├── README.md           # TÓM TẮT + hướng dẫn sử dụng
├── agent/
│   └── [agent-name].md
├── skills/
│   ├── kit-extending/  # Meta-skill tự mở rộng Rule/Workflow/Skill chuẩn IDE
│   └── [skill-name]/
│       └── SKILL.md
└── memory/             # Nếu cần
    └── [memory-files]
```


#### Professional Kit
```
output/
├── README.md
├── ARCHITECTURE.md     # Tổng quan kiến trúc
├── manifest.json       # Component registry
├── agent/
│   └── [agents].md
├── skills/
│   └── [skill-folders]/
├── workflows/
│   └── [workflows].md
├── rules/
│   └── [rules].md
├── memory/
│   └── [memory-files]
└── scripts/            # Nếu cần
    └── [scripts]
```

#### Suite Kit
Như Professional, thêm:
```
├── agent/
│   ├── orchestrator.md   # Lead agent
│   ├── [specialist-1].md
│   └── [specialist-2].md
├── rules/
│   └── request-routing.md  # Agent routing
```

### 4. Manifest Generation (Professional/Suite)

```json
{
  "kitVersion": "1.0.0",
  "schemaVersion": "1.0.0",
  "agents": {
    "agent-name": {
      "path": "agent/agent-name.md",
      "version": "1.0.0",
      "requires": {
        "skills": { "skill-name": "^1.0.0" }
      },
      "tools": ["Read", "Write", "Edit"]
    }
  },
  "skills": {
    "skill-name": {
      "path": "skills/skill-name/SKILL.md",
      "version": "1.0.0"
    }
  },
  "rules": {},
  "workflows": {}
}
```

### 5. Dual Output Assembly

**Bắt buộc cho MỌI kit type**:

1. **TÓM TẮT CHO NGƯỜI DÙNG** (đầu file hoặc README.md)
   - 3-5 dòng đời thường
   - Trả lời: làm gì / dùng khi nào / giới hạn
   - 0 thuật ngữ kỹ thuật

2. **Nội dung kỹ thuật** (các component files)
   - Chính xác, structured
   - Ngôn ngữ kỹ thuật phù hợp

### 6. Quy tắc Độc lập Nhà cung cấp (Provider-Agnostic Rules)
- Output của kit (các file markdown, JSON) tuyệt đối KHÔNG được chứa các thuật ngữ hoặc đường dẫn đặc thù của Antigravity IDE (như `.agents/`, `GEMINI.md`) hoặc các nhà cung cấp cụ thể (Gemini, Claude, GPT) ngoại trừ trường hợp người dùng yêu cầu rõ ràng.
- Đảm bảo prompt và kit hoàn toàn có thể chạy trên mọi nền tảng AI.

---

## Component Specs

Spec cho từng loại component: → `references/component-specs.md`

---

## Output Templates

Templates cho từng kit type: → `references/output-templates.md`

---

## Self-Check trước Delivery

```
□ Kit Type đúng với complexity thực tế
□ Mọi component phục vụ outcome thực tế (không nhồi)
□ Cross-references đều hợp lệ (skill names, file paths)
□ TÓM TẮT CHO NGƯỜI DÙNG: 3-5 dòng, 0 thuật ngữ
□ Provider-agnostic (0 mention provider cụ thể, không lock-in cấu trúc file của IDE)
□ Không có file/directory rỗng
□ Ngôn ngữ khớp input user
□ Manifest chính xác (Professional/Suite)
```
