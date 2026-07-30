---
name: optimizing-progressive-disclosure
description: "Use when managing context window optimization by splitting information into metadata, main instructions, and heavy reference sub-files to minimize token usage."
when_to_use: "Kích hoạt khi cần năng lực optimizing-progressive-disclosure trong quy trình tạo hoặc kiểm định Agent Kit."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# Optimizing Progressive Disclosure

## Overview
Tối ưu hóa dung lượng token và bối cảnh hoạt động (context window) của Agent bằng cách phân cấp thông tin thành 3 tầng: Metadata, Body (SKILL.md), và References.

## When to Use
- Khi Skill Architect thiết kế skill và phát hiện tài liệu hướng dẫn/dữ liệu quá nặng.
- Khi muốn giảm thiểu độ trễ và chi phí vận hành Agent Kit.

### When NOT to use
- Khi tài liệu hướng dẫn cực kỳ ngắn gọn và đơn giản (< 100 từ).

## Core Pattern
Phân bổ thông tin theo đúng 3 lớp:

1. **Lớp 1: Metadata (Tên + Mô tả trong Frontmatter)**:
   - *Mục tiêu*: Giúp LLM nhận biết và quyết định xem có nên load skill này không mà không cần mở file.
   - *Token budget*: ~100 từ.
2. **Lớp 2: Body (SKILL.md body)**:
   - *Mục tiêu*: Hướng dẫn quy trình cốt lõi và các nguyên tắc chính khi skill được nạp.
   - *Token budget*: < 500 dòng.
3. **Lớp 3: References (Tệp tin trong references/)**:
   - *Mục tiêu*: Lưu trữ các chi tiết kỹ thuật chuyên sâu, API Spec, bảng tra cứu. Chỉ đọc JIT (Just-In-Time) khi bước trong SKILL.md yêu cầu.
   - *Token budget*: Không giới hạn.

## Quick Reference
- Không bao giờ copy nguyên một file documentation từ bên ngoài vào SKILL.md.
- Luôn sử dụng relative links để trỏ đến các file references.
- Cập nhật định kỳ để loại bỏ các thông tin trùng lặp.

## Common Mistakes
- **Lỗi**: Load toàn bộ thư viện tài liệu tham khảo ngay từ đầu cuộc hội thoại.
  - *Khắc phục*: Thiết kế chỉ dẫn rõ ràng trong SKILL.md: "Khi gặp lỗi X, hãy đọc file `references/error-codes.md` để sửa."
- **Lỗi**: Để mô tả Frontmatter quá ngắn hoặc quá dài, làm mất đi khả năng auto-discovery.
  - *Khắc phục*: Tối ưu hóa description tập trung vào keyword mà agent sẽ tìm kiếm.
