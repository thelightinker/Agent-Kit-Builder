---
name: discovering-enhancements
description: "Use when looking for 80/20 leverage points and custom mechanisms that go beyond standard prompt frameworks to address the most likely point of user failure."
when_to_use: "Kích hoạt khi cần năng lực discovering-enhancements trong quy trình tạo hoặc kiểm định Agent Kit."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# Discovering Enhancements

## Overview
Tìm kiếm đòn bẩy 80/20 và thiết kế các cơ chế tuỳ chỉnh (ngoài 6 Outcome Lens tiêu chuẩn) để giải quyết điểm yếu lớn nhất của Agent trong thực tế.

## When to Use
- Trong bước phân tích domain của Domain Analyst.
- Khi muốn Agent Kit có tính độc bản và hiệu quả vượt trội so với các template có sẵn trên mạng.

### When NOT to use
- Khi đang thiết kế các micro-agent siêu đơn giản không cần tuỳ chỉnh.

## Core Pattern
Chạy quy trình **Dynamic Enhancement Discovery** qua 3 câu hỏi tự vấn:

1. **Outcome thực tế quan trọng nhất là gì?**
   - Tìm kiếm khía cạnh cốt lõi tạo nên giá trị của agent. Nó có nằm ngoài 6 lens thông thường không?
   - *Ví dụ*: Đối với bot viết sách, đó là "Nhất quán giọng văn".
2. **Điểm thất vọng/lỗi lớn nhất mà user có thể gặp?**
   - Dự đoán hành vi sai lệch của LLM hoặc sự không hài lòng của user.
   - *Ví dụ*: Bot tự ý bịa trích dẫn (hallucination) hoặc đổi giọng văn giữa chừng.
3. **2-3 đòn bẩy thực sự đáng làm là gì?**
   - Thiết kế cơ chế cụ thể để giải quyết 2 vấn đề trên.
   - *Ví dụ*: Đòn bẩy "Claim accuracy" (Constraint chặt) và "Nhất quán giọng văn" (Đòn bẩy riêng với Voice Profile).

## Quick Reference
- Không cố nhồi nhét tất cả 6 lenses.
- Tập trung vào tối đa 2-3 đòn bẩy mang lại hiệu quả cao nhất (quy luật 80/20).

## Common Mistakes
- **Lỗi**: Thiết kế đòn bẩy quá chung chung, không giải quyết vấn đề cụ thể của domain.
  - *Khắc phục*: Quy đòn bẩy về một cơ chế kỹ thuật rõ ràng trong System Prompt.
- **Lỗi**: Nhồi nhét cả 6 lenses làm phình prompt vô ích (Lens Stuffing).
  - *Khắc phục*: Chỉ chọn những gì thực sự cần thiết dựa trên phân tích rủi ro.
