---
name: guided-intaking
description: "Use when the user request is low-tech, brief, or lacks technical prompt engineering terminology, and needs clarification of core properties before building an agent."
when_to_use: "Kích hoạt khi cần năng lực guided-intaking trong quy trình tạo hoặc kiểm định Agent Kit."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# Guided Intaking

## Overview
Dùng để thu thập thông tin từ người dùng phổ thông (low-tech) bằng ngôn ngữ tự nhiên, tránh thuật ngữ AI, nhằm xác định đúng mục tiêu của Agent.

## When to Use
- User gửi yêu cầu ngắn gọn ("tạo con bot dịch thuật", "bot trả lời mail").
- User không có kiến thức về Prompt Engineering, System Prompts, hay System Tier.
- Khi cần làm rõ mục tiêu mà không gây áp lực kỹ thuật cho user.

### When NOT to use
- User có spec kỹ thuật rõ ràng hoặc là prompt engineer chuyên nghiệp.
- Khi các thuộc tính cốt lõi (North Star, Constraints) đã rõ ràng 100% trong bối cảnh.

## Core Pattern
Thay vì hỏi trực tiếp các câu hỏi kỹ thuật, hãy chuyển dịch sang ngôn ngữ đời thường:

| Thuật ngữ kỹ thuật | Câu hỏi đời thường tương ứng |
|:-------------------|:-----------------------------|
| **North Star** | "Bạn muốn con bot này giải quyết công việc gì cụ thể cho bạn?" |
| **Hard Constraints** | "Có điều gì con bot này tuyệt đối KHÔNG bao giờ được làm không?" |
| **Definition of Done** | "Khi bot làm xong việc, kết quả như thế nào thì bạn hài lòng?" |
| **Complexity Tier** | Không hỏi. Tự suy ra từ độ phức tạp của công việc user mô tả. |

## Quick Reference
- **Tối đa 2-3 câu hỏi** trong một lượt tương tác.
- **Luôn dùng ví dụ** cụ thể để minh họa nếu user khó hình dung.
- **Giọng điệu**: Thân thiện, hỗ trợ, không phán xét.

## Common Mistakes
- **Lỗi**: Hỏi "North Star của bot là gì?" hoặc "Bạn muốn dùng tier mấy?"
  - *Khắc phục*: Thay bằng "Mục tiêu lớn nhất của bot..."
- **Lỗi**: Hỏi quá nhiều câu hỏi trong 1 lượt làm user ngợp.
  - *Khắc phục*: Chia nhỏ, chỉ hỏi những thông tin quan trọng nhất trước.
