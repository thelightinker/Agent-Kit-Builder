---
name: domain-analysis
description: ">"
when_to_use: "Kích hoạt khi cần năng lực domain-analysis trong quy trình tạo hoặc kiểm định Agent Kit."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# Domain Analysis

## Overview

Phân tích domain mục tiêu để trích xuất yêu cầu, tìm cơ chế domain-specific,
dự đoán failure modes, và khuyến nghị kit type + components. Đây là bước
đầu tiên khi tạo kit mới — thiếu bước này, kit sẽ generic và vô giá trị.

---

## Quy trình

### 1. Core Verbs — Hành động cốt lõi

Xác định **5-10 hành động xảy ra thường nhất** trong domain.

Mỗi verb phải trả lời 3 câu:

| Câu hỏi                                    | Mục đích                                    |
| :------------------------------------------- | :--------------------------------------------- |
| Precision hay Creativity?                    | Quyết định mức kiểm soát output          |
| Specialized Knowledge hay General Reasoning? | Quyết định cần skill/memory không         |
| Failure Severity nếu làm sai?              | Quyết định cần constraint/safeguard không |

**Ví dụ** (domain: phân tích tài chính):

| Verb                   | P/C        | Knowledge   | Severity |
| :--------------------- | :--------- | :---------- | :------- |
| Tính toán chỉ số   | Precision  | Specialized | Critical |
| Dự báo xu hướng    | Creativity | Specialized | High     |
| Giải thích kết quả | Creativity | General     | Medium   |
| Đọc báo cáo        | Precision  | Specialized | High     |

Nếu core verbs áp dụng cho domain nào cũng được → phân tích chưa đủ sâu.

### 2. Domain-Specific Discovery

3 câu hỏi — trả lời RIÊNG cho agent đang build:

**Câu 1: Outcome quan trọng nhất?**
Agent này tồn tại để đạt outcome gì? Outcome đó có cần cơ chế đặc biệt
nào mà agent thông thường không có?

**Câu 2: Điểm thất vọng phổ biến nhất?**
Nếu user thực tế dùng agent này, đâu là lúc họ sẽ nói "agent này không
hiểu tôi"? Đây là đòn bẩy 80/20 cần ưu tiên.

**Câu 3: Tối đa 2-3 đòn bẩy đáng làm**

- Không cố nặn ra nhiều cơ chế cho đủ
- Mỗi đòn bẩy phải có: outcome → cơ chế → kích hoạt
- Nếu đòn bẩy áp dụng cho domain nào cũng được → nó không domain-specific

### 3. Failure Mode Prediction

Dự đoán 3-5 failure modes đặc trưng:

| Failure Mode       | Xác suất   | Severity              | Phòng ngừa        |
| :----------------- | :----------- | :-------------------- | :------------------ |
| [mô tả cụ thể] | High/Med/Low | Critical/High/Med/Low | [cơ chế cụ thể] |

Failure modes phải domain-specific. "Agent hallucinate" là generic — không đếm.
"Agent bịa số liệu tài chính" là domain-specific — đếm.

### 4. Kit Type Classification

Dựa trên phân tích, phân loại:

### 4. Kit Type Classification & Outcome Lenses

Dựa trên phân tích, phân loại Kit Type và áp dụng các Outcome Lenses (A-F) tương ứng:

- **Micro Kit (Tier 1)**: 1 tác vụ đơn giản, không state. Lenses: **A (Token Efficiency)** + **C (Reliable Performance)** + F (Safety - mức tối giản).
- **Standard Kit (Tier 2)**: Nhiều state, context động hoặc cần capability phức tạp. Lenses: **A** + **C** + **B (Adaptive Flexibility)**, cân nhắc **D (Lean Context)**.
- **Professional Kit (Tier 3)**: Hệ thống đa thành phần, có validation/scripts. Lenses: **A** + **C** + **B** + **E (Interoperability)**, cân nhắc **D** + **F**.
- **Suite Kit (Tier 3+)**: Nhiều agent phối hợp. Lenses: **Bắt buộc cả 6 Lenses (E là bắt buộc toàn phần)**.

Chi tiết về 6 Lenses và cơ chế: → `references/outcome-lenses.md`

### 5. Domain Pattern Lookup

Trước khi đưa ra các đòn bẩy và failure modes riêng, hãy tra cứu các mẫu thiết kế có sẵn cho 4 lĩnh vực lớn (Phần mềm, Viết sách, Chiến lược kinh doanh, Nghiên cứu tri thức):
→ `references/domains.md`

### 6. Component Selection

Khuyến nghị components cần — MỖI khuyến nghị kèm lý do cụ thể:

```
□ Agent (system prompt) — [luôn cần]
□ Skills — [cần/không] — lý do: [...]
□ Memory — [cần/không] — lý do: [...]
□ Workflow — [cần/không] — lý do: [...]
□ Tools — [cần/không] — lý do: [...]
□ Rules — [cần/không] — lý do: [...]
□ Scripts — [cần/không] — lý do: [...]
```

---

## Output Format

```markdown
# Domain Analysis: [Tên Domain]

## Kit Type: [Micro/Standard/Professional/Suite]
## Applied Lenses: [Ví dụ: A + C + B]

## Core Verbs
[Bảng core verbs]

## Domain-Specific Discovery
1. Outcome quan trọng nhất: [...]
2. Điểm thất vọng phổ biến: [...]
3. Đòn bẩy đáng làm: [...]

## Predicted Failure Modes
[Bảng failure modes]

## Component Recommendation
[Checklist components với lý do]

## Domain-Specific Mechanisms
[Cơ chế riêng cần đưa vào kit]
```

---

## Quality Check

Phân tích thất bại nếu:

- Core verbs quá generic (áp cho domain nào cũng được)
- Discovery chỉ lặp lại nguyên tắc chung
- Failure modes copy từ template, không đặc trưng domain
- Component recommendation không có lý do cụ thể
- Kit Type và Applied Lenses không khớp với complexity thực tế
