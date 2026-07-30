---
name: scaffolding-skills
description: "Use when constructing the file and folder structure for an agent's custom skill in Antigravity IDE, including SKILL.md, references, examples, and evals."
when_to_use: "Kích hoạt khi cần năng lực scaffolding-skills trong quy trình tạo hoặc kiểm định Agent Kit."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# Scaffolding Skills

## Overview
Thiết kế và cấu trúc thư mục chứa skill mới (Skills Component) theo đúng chuẩn Antigravity IDE, thiết lập các tệp SKILL.md, references, examples, và evals.json.

## When to Use
- Khi Skill Architect được yêu cầu sinh component `Skills` cho Agent Kit.
- Khi cần tạo một bộ năng lực tái sử dụng (reusable capabilities) cho Agent.

### When NOT to use
- Khi tạo các components khác như memory hoặc tools.

## Core Pattern
Mỗi skill scaffold ra phải tuân thủ cấu trúc sau:

1. **`SKILL.md` (Bắt buộc)**:
   - Chứa Frontmatter dạng YAML (name, description).
   - Description viết theo chuẩn "Use when..." (chỉ mô tả điều kiện trigger, không tóm tắt workflow).
   - Nội dung hướng dẫn dạng imperative, giải thích lý do (WHY) thay vì chỉ ra lệnh.
2. **`references/`**: Thư mục chứa tài liệu tham khảo nặng (nếu SKILL.md > 500 dòng).
3. **`examples/`**: Thư mục chứa các ví dụ chất lượng cao, có thể chạy được trực tiếp.
4. **`evals/evals.json`**: Tập hợp các test cases cùng assertions tương ứng để verify hoạt động của skill.

## Quick Reference
- Tên thư mục skill: lowercase-hyphenated.
- SKILL.md luôn là tệp entry point duy nhất.
- Luôn giữ SKILL.md tinh gọn dưới 500 dòng để tiết kiệm token khi load vào context.

## Common Mistakes
- **Lỗi**: Tạo một SKILL.md khổng lồ chứa cả nghìn dòng API reference.
  - *Khắc phục*: Tách phần API reference sang thư mục `references/` và trỏ link từ SKILL.md.
- **Lỗi**: Viết mô tả skill (description) chứa các bước thực hiện của skill.
  - *Khắc phục*: Sửa lại description chỉ mô tả bối cảnh/triệu chứng khi nào agent nên load skill đó.
