---
name: kit-exporting
description: >
  Đóng gói và xuất bản Agent Kit sang nhiều định dạng nền tảng:
  Antigravity Plugin bundle (dist/antigravity-plugin), Cursor (.cursorrules),
  Claude Desktop (claude_instructions.txt), OpenAI Custom GPTs (gpt_instructions.txt).
  Kích hoạt khi cần phân phối hoặc đóng gói plugin cho kit.
when_to_use: "Khi người dùng yêu cầu export hoặc chuyển đổi Agent Kit sang Antigravity Plugin, Cursor, Claude, hoặc OpenAI."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.1.0
---

# Kit Exporting

Kỹ năng xuất bản và chuyển đổi Agent Kit sang các nền tảng IDE, AI Assistant và đóng gói Antigravity Plugin bundle.

---

## 1. CÁC NỀN TẢNG HỖ TRỢ

| Nền tảng | File đầu ra chính | Đặc điểm kỹ thuật |
|:---|:---|:---|
| **Antigravity Plugin** | `dist/antigravity-plugin/` | Gói plugin hoàn chỉnh kèm `gemini-extension.json`, commands TOML và `PLUGIN_CONTENTS.json` (bảng mã băm SHA-256). |
| **Cursor IDE** | `.cursorrules` | Đặt tại thư mục gốc workspace, dạng flat markdown. |
| **Claude Desktop / Projects** | `claude_instructions.txt` | Chỉ dẫn hệ thống gộp, hỗ trợ XML tagging. |
| **OpenAI Custom GPTs** | `gpt_instructions.txt` | Chỉ dẫn gộp cho GPT Builder, tối ưu hóa text. |

---

## 2. QUY TRÌNH XUẤT BẢN TỰ ĐỘNG

Sử dụng script `export_kit.py` tích hợp sẵn:

```bash
# Export sang tất cả nền tảng (kèm Antigravity Plugin)
python .agents/scripts/export_kit.py ./output/<kit-name> ./dist/<kit-name> --target all

# Đóng gói Antigravity Plugin bundle
python .agents/scripts/export_kit.py ./output/<kit-name> ./dist/<kit-name> --target plugin

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
1. File/Folder đích tồn tại trong thư mục `./dist/<kit-name>/`.
2. Đối với Antigravity Plugin: Xác thực `PLUGIN_CONTENTS.json` chứa đầy đủ danh mục file và mã băm SHA-256.
3. Nội dung không bị cắt ngắn hoặc mất các Hard Constraints cốt lõi.

---

## 4. SAO CHÉP KIT AN TOÀN SANG THƯ MỤC DỰ ÁN (SAFE COPY)

Khi cần copy kit sang thư mục quản lý dự án đích (`C:\Users\nhdcb\OneDrive\Desktop\AI Project\AI Agent Kits`), sử dụng script `copy_kit.py`:

```bash
# Xem danh sách kit sẵn có
python .agents/scripts/copy_kit.py --list

# Copy 1 kit cụ thể (an toàn, không di chuyển/xóa nguồn)
python .agents/scripts/copy_kit.py <kit-name>

# Copy nhiều kit
python .agents/scripts/copy_kit.py <kit_1> <kit_2>

# Copy toàn bộ kit trong Output/
python .agents/scripts/copy_kit.py --all

# Xem trước kết quả (Dry Run)
python .agents/scripts/copy_kit.py <kit-name> --dry-run
```

