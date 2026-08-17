---
name: kit-exporting
description: >
  Đóng gói và xuất bản Agent Kit sang nhiều định dạng nền tảng:
  Cursor (.cursorrules), Claude Desktop (claude_instructions.txt),
  OpenAI Custom GPTs (gpt_instructions.txt). Kích hoạt khi cần phân phối kit.
when_to_use: "Khi người dùng yêu cầu export hoặc chuyển đổi Agent Kit sang Cursor, Claude, hoặc OpenAI."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.0.0
---

# Kit Exporting

Kỹ năng xuất bản và chuyển đổi Agent Kit sang các nền tảng IDE và AI Assistant phổ biến hiện nay.

---

## 1. CÁC NỀN TẢNG HỖ TRỢ

| Nền tảng | File đầu ra chính | Đặc điểm kỹ thuật |
|:---|:---|:---|
| **Cursor IDE** | `.cursorrules` | Đặt tại thư mục gốc workspace, dạng flat markdown |
| **Claude Desktop / Projects** | `claude_instructions.txt` | Chỉ dẫn hệ thống gộp, hỗ trợ XML tagging |
| **OpenAI Custom GPTs** | `gpt_instructions.txt` | Chỉ dẫn gộp cho GPT Builder, tối ưu hóa text |

---

## 2. QUY TRÌNH XUẤT BẢN TỰ ĐỘNG

Sử dụng script `export_kit.py` tích hợp sẵn:

```bash
# Export sang tất cả nền tảng
python .agents/scripts/export_kit.py ./output/<kit-name> ./dist/<kit-name> --target all

# Export riêng cho Cursor
python .agents/scripts/export_kit.py ./output/<kit-name> ./dist/<kit-name> --target cursor

# Export riêng cho Claude
python .agents/scripts/export_kit.py ./output/<kit-name> ./dist/<kit-name> --target claude

# Export riêng cho OpenAI
python .agents/scripts/export_kit.py ./output/<kit-name> ./dist/<kit-name> --target openai
```

---

## 3. KIỂM TRA ĐẦU RA SAU KHI EXPORT

Sau khi xuất bản, kiểm tra:
1. File đích tồn tại trong thư mục `./dist/<kit-name>/`.
2. Nội dung không bị cắt ngắn hoặc mất các Hard Constraints cốt lõi.
3. Hướng dẫn người dùng cách copy/paste hoặc nạp vào công cụ tương ứng.
