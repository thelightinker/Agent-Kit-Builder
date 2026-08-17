---
name: exporting-kits
description: "Multi-platform Agent Kit export engine. Use ALWAYS whenever the user asks to convert, export, package, or build an Agent Kit for Cursor (.cursorrules), Claude Desktop / Anthropic Projects, OpenAI Custom GPTs, or multi-platform distribution."
when_to_use: "Kích hoạt khi người dùng muốn đóng gói và xuất bản Agent Kit sang các định dạng tương thích với Cursor, Claude Desktop hoặc OpenAI Custom GPTs."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# Exporting Kits Skill

## Overview
Cung cấp năng lực đóng gói tự động một Agent Kit chuẩn Antigravity thành các bundle tương thích 100% với các nền tảng AI Agent phổ biến:
- **Cursor**: File `.cursorrules` chứa System Prompts và Rules tổng hợp.
- **Claude Desktop / Anthropic Project**: File `claude_instructions.txt` (được đóng tag XML) và `tools.json` (định nghĩa schema công cụ).
- **OpenAI Custom GPTs**: File `gpt_instructions.txt` (được tối ưu dưới 8000 ký tự).

## Directives & Execution Pattern
Khi được yêu cầu export kit:
1. Đã xác định thư mục nguồn Agent Kit (`--kit-dir`).
2. Thực thi script `export_kit.py` với nền tảng đích tương ứng.

### Command Variations
Xuất bản toàn bộ nền tảng (All Platforms):

```bash
python .agents/scripts/export_kit.py --kit-dir .agents --output-dir dist/my_bundle --target all
```

Xuất bản cho từng nền tảng cụ thể:

```bash
python .agents/scripts/export_kit.py --kit-dir .agents --output-dir dist/cursor_bundle --target cursor
python .agents/scripts/export_kit.py --kit-dir .agents --output-dir dist/claude_bundle --target claude
python .agents/scripts/export_kit.py --kit-dir .agents --output-dir dist/openai_bundle --target openai
```

## Output Structure Guidelines
- **Cursor**: Cung cấp file `dist/<bundle>/cursor/.cursorrules` để người dùng copy trực tiếp vào gốc dự án.
- **Claude**: Cung cấp file `dist/<bundle>/claude/claude_instructions.txt` cho phần Project Custom Instructions và `tools.json` cho phần Tool definitions.
- **OpenAI**: Cung cấp `dist/<bundle>/openai/gpt_instructions.txt` cho phần GPT Instructions.
