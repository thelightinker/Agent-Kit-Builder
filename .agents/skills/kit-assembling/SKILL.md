---
name: kit-assembling
description: >
  Lắp ráp các cấu phần thành Agent Kit hoàn chỉnh trong thư mục cách ly
  ./output/<kit-name>/, sinh manifest.json, và đóng gói theo chuẩn Kit Type.
  Luôn kích hoạt ở bước hoàn thiện của quy trình tạo kit.
when_to_use: "Khi hoàn tất các cấu phần và cần lắp ráp thành thư mục Agent Kit hoàn chỉnh."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.0.0
---

# Kit Assembling

Kỹ năng tổng hợp, tổ chức thư mục và đóng gói Agent Kit hoàn chỉnh, tuân thủ nghiêm ngặt ranh giới cách ly không gian làm việc.

---

## 1. WORKSPACE ISOLATION (BẤT BIẾN)

- Mọi file của Agent Kit mới **BẮT BỘC** được tạo tại:
  `./output/<kit-name>/` (ví dụ: `./output/copywriting-pro-kit/`)
- **TUYỆT ĐỐI KHÔNG** ghi đè hoặc tạo trực tiếp vào `.agents/` của Agent Kit Creator.

---

## 2. CẤU TRÚC ĐÓNG GÓI THEO KIT TYPE

### A. Micro Kit
```
output/<kit-name>/
└── [kit-name].md             # System prompt duy nhất có Tóm tắt + Kỹ thuật
```

### B. Standard Kit
```
output/<kit-name>/
├── agent/
│   └── [kit-name].md         # System prompt chính
├── skills/
│   └── [skill-name]/
│       └── SKILL.md          # Skill chuyên biệt
└── workflows/
    └── [workflow-name].md    # Workflow điều phối
```

### C. Professional Kit
```
output/<kit-name>/
├── agent/
├── skills/
├── workflows/
├── memory/
│   └── MEMORY.md             # Bộ nhớ dài hạn
└── manifest.json             # Danh mục cấu phần & version
```

---

## 3. QUY TRÌNH LẮP RÁP

1. **Kiểm tra đầu vào**: Xác nhận đầy đủ các file đã sinh từ các bước trước.
2. **Khởi tạo thư mục đích**: Tạo `./output/<kit-name>/` và các thư mục con tương ứng.
3. **Ghi nhận file**: Tạo từng file Markdown/JSON vào đúng vị trí với frontmatter hợp lệ.
4. **Tạo manifest.json (nếu là Professional/Suite)**: Khai báo danh mục agent, skills, workflows, rules.
5. **Kiểm tra tính toàn vẹn (Integrity Check)**: Đảm bảo không có broken relative links giữa các file.
