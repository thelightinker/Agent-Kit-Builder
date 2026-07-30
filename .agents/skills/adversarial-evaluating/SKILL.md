---
name: adversarial-evaluating
description: "Use when stress-testing the generated prompt with edge cases, searching for loopholes in the Definition of Done, and verifying constraint boundaries."
when_to_use: "Kích hoạt khi cần năng lực adversarial-evaluating trong quy trình tạo hoặc kiểm định Agent Kit."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# Adversarial Evaluating

## Overview
Đóng vai trò kẻ phá bĩnh (adversarial tester) để tìm kiếm kẽ hở trong DoD, các điểm mập mờ trong Constraints, và giả lập các tình huống edge-case nhằm tối đa hóa độ tin cậy của Agent Kit.

## When to Use
- Ở lớp kiểm tra thứ 3 (Adversarial Test) của Quality Gate workflow.
- Khi cần đảm bảo Agent Kit không bị "bẻ lái" hoặc thực hiện sai lệch dưới áp lực input lạ.

### When NOT to use
- Khi kit chưa vượt qua lớp kiểm tra cấu trúc cơ bản.

## Core Pattern

### 1. Tìm kẽ hở trong DoD (DoD Loophole Check)
- Đặt câu hỏi: "LLM có thể trả về một kết quả tệ nhưng vẫn khớp với checklist DoD này không?"
- *Ví dụ*: DoD yêu cầu "Nội dung >= 500 từ" -> LLM chỉ cần viết lặp đi lặp lại 1 câu 500 lần là pass.
- *Khắc phục*: Thêm tiêu chí về nội dung không lặp hoặc có cấu trúc logic.

### 2. Giả lập Edge Cases
- Đưa ra 2-3 tình huống giả định:
  - Input rỗng hoặc chỉ chứa ký tự đặc biệt.
  - Yêu cầu vượt quá giới hạn an toàn của bot.
  - Yêu cầu mâu thuẫn trực tiếp với nhau.
- Kiểm tra xem prompt hiện tại có cơ chế dừng an toàn (escalation) hoặc báo lỗi hợp lý không.

### 3. Kiểm tra tính mập mờ của Constraints
- Constraint "KHÔNG làm việc quá khả năng" -> mơ hồ.
- Thay bằng: "KHÔNG thực hiện tính toán tài chính — nếu gặp, dừng lại và hướng dẫn user gọi công cụ phù hợp."

## Quick Reference
- Suy nghĩ như một kẻ tấn công hoặc một người dùng cố tình phá hoại hệ thống.
- Thắt chặt các điều kiện biên của prompt.

## Common Mistakes
- **Lỗi**: Tin tưởng tuyệt đối vào khả năng "tự hiểu" của LLM.
  - *Khắc phục*: Luôn giả định LLM sẽ lách mọi kẽ hở nếu có thể để giảm tải công việc của nó.
- **Lỗi**: Thiết kế constraints quá cứng nhắc làm bot không hoạt động được trong thực tế.
  - *Khắc phục*: Cân bằng giữa an toàn và tính hữu dụng của bot.
