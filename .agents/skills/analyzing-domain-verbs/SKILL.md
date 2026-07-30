---
name: analyzing-domain-verbs
description: "Use when analyzing a target domain to identify the core actions (verbs) that occur most frequently and determine their precision and knowledge requirements."
when_to_use: "Kích hoạt khi cần năng lực analyzing-domain-verbs trong quy trình tạo hoặc kiểm định Agent Kit."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# Analyzing Domain Verbs

## Overview
Phân tích các động từ cốt lõi (core verbs) của một lĩnh vực để thiết kế các cơ chế điều khiển tương ứng trong System Prompt, đảm bảo agent hoạt động chính xác trong thực tế.

## When to Use
- Khi tiến hành phân tích domain cho Agent Kit mới hoặc Refactor.
- Khi cần xác định đâu là hành động quan trọng nhất cần kiểm soát rủi ro.

### When NOT to use
- Khi domain quá hẹp hoặc tác vụ quá đơn giản (Tier 1) không có nhiều quy trình nghiệp vụ.

## Core Pattern
Mỗi domain được đặc trưng bởi các hành động lặp đi lặp lại. Phân tích chúng theo 4 tiêu chí:

1. **Động từ cốt lõi**: Hành động thực tế (ví dụ: `Trích dẫn`, `Dịch`, `Viết bản thảo`).
2. **Yêu cầu Chính xác vs. Sáng tạo**:
   - *Chính xác (Precision)*: Cần cơ chế kiểm soát chặt chẽ, DoD rõ ràng.
   - *Sáng tạo (Creativity)*: Cần cho LLM không gian tự do, hướng dẫn mang tính gợi mở.
3. **Yêu cầu Kiến thức chuyên môn**: Agent có cần nạp tài liệu tham khảo (references) để thực hiện không?
4. **Mức độ rủi ro khi thất bại (Failure Severity)**:
   - *Critical/High*: Bắt buộc có Hard Constraints và cơ chế an toàn (Giao thức an toàn).
   - *Medium/Low*: Kiểm soát bằng DoD thông thường.

## Quick Reference
Ví dụ phân tích cho domain **Lập trình**:
- `Viết code` -> Sáng tạo -> General -> Medium Risk
- `Viết Unit Test` -> Chính xác -> General -> High Risk
- `Deploy` -> Chính xác -> Specialized -> Critical Risk (cần Giao thức an toàn)

## Common Mistakes
- **Lỗi**: Xác định các động từ quá chung chung như "Làm việc", "Xử lý", "Hỗ trợ".
  - *Khắc phục*: Thay bằng hành động cụ thể: "Trích xuất dữ liệu", "Đối chiếu hóa đơn".
- **Lỗi**: Đánh giá sai mức độ rủi ro dẫn đến thiếu Hard Constraints cho các tác vụ nguy hiểm.
  - *Khắc phục*: Luôn hỏi "Nếu bước này lỗi, hệ thống/user có bị ảnh hưởng nghiêm trọng không?".
