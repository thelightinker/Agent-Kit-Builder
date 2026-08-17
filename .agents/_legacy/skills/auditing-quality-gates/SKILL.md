---
name: auditing-quality-gates
description: "Use when evaluating the generated Agent Kit against the 5-star scoring rubric, performing structural checks, and checking for jargon in the human summary."
when_to_use: "Kích hoạt khi cần năng lực auditing-quality-gates trong quy trình tạo hoặc kiểm định Agent Kit."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# Auditing Quality Gates

## Overview
Đánh giá chất lượng của Agent Kit thông qua bộ tiêu chuẩn 5 sao, chạy qua các lớp kiểm tra cấu trúc và ngữ nghĩa để đảm bảo kit đạt yêu cầu bàn giao.

## When to Use
- Khi Quality Auditor nhận output từ Kit Generator để tiến hành đánh giá chất lượng.
- Khi cần chấm điểm Agent Kit và đưa ra các yêu cầu sửa đổi (findings).

### When NOT to use
- Khi đang thiết kế hoặc sinh code mới.

## Core Pattern
Chạy quy trình đánh giá qua 2 lớp đầu tiên:

### Lớp 1: Kiểm tra cấu trúc (Structural Check)
- Check sự tồn tại của: Tóm tắt cho người dùng, 4 sections lõi của prompt, DoD (>=3 dòng), Constraints (>=2 dòng), Template đầu ra.
- Nếu thiếu bất kỳ thành phần nào -> Đánh trượt ngay lập tức (FAIL), không kiểm tra tiếp.

### Lớp 2: Kiểm tra ngữ nghĩa (Semantic Check)
- **Tóm tắt**: Đảm bảo không chứa bất kỳ thuật ngữ kỹ thuật nào (prompt, token, API, LLM, v.v.). Phải đủ 3 ý: bot làm gì, dùng khi nào, giới hạn.
- **DoD & Constraints**: Đảm bảo tính cụ thể, đo lường được, không sáo ngữ.
- **Lens Stuffing**: Tìm và chỉ ra các cơ chế thừa thãi không phục vụ mục tiêu.

## Quick Reference
- **Scoring Rubric**: Chấm điểm dựa trên 5 tiêu chí: Structural, Specificity, Relevance, Uniqueness, Usability.
- Chỉ bàn giao (PASS) khi kit đạt từ 4 sao trở lên.

## Common Mistakes
- **Lỗi**: Bỏ qua lỗi sáo ngữ trong DoD (ví dụ: "chất lượng tốt") vì nể nang hoặc muốn hoàn thành nhanh.
  - *Khắc phục*: Luôn chấm điểm khách quan theo đúng checklist nhị phân.
- **Lỗi**: Viết findings chung chung như "cần viết tốt hơn".
  - *Khắc phục*: Viết rõ: "DoD dòng 2 chứa tính từ 'chuyên nghiệp' -> thay thế bằng tiêu chí đo được."
