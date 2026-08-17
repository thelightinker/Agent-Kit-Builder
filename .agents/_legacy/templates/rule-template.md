---
name: {RULE_NAME}
version: 1.0.0
priority: P0 # P0: Toàn hệ thống | P1: Cấp Agent | P2: Cấp Skill
trigger: always_on # [always_on | manual | model_decision]
description: {BRIEF_DESCRIPTION_OF_RULE_PURPOSE_FOR_MODEL_DECISION}
# Bổ sung linh hoạt nếu cần:
# tags: [security, code-style]
# domain: {TARGET_DOMAIN}
---

# Rule: {RULE_TITLE}

> {ONE_SENTENCE_SUMMARY_OF_RULE}

---

## 📌 Phân loại Trigger (Rule Trigger Type)
- **`always_on`**: Luôn luôn tự động chạy trong mọi lượt chat.
- **`manual`**: Chỉ kích hoạt khi được gọi đích danh (`@{RULE_NAME}`).
- **`model_decision`**: AI tự đọc `description` ở frontmatter và quyết định kích hoạt dựa trên ngữ cảnh.

---

## 1. Triết lý & Nguyên tắc Cốt lõi (Core Guidelines)

1. **{GUIDELINE_1_NAME}**: {GUIDELINE_1_DESCRIPTION}
2. **{GUIDELINE_2_NAME}**: {GUIDELINE_2_DESCRIPTION}

---

## 2. Xử lý Linh hoạt & Trường hợp Ngoại lệ (Adaptive Handling)

```
❌ HÀNH VI KHÔNG MONG MUỐN: {INCORRECT_BEHAVIOR_EXAMPLE}
✅ HÀNH VI CHUẨN MỰC: {CORRECT_BEHAVIOR_EXAMPLE}
```

- **Ranh giới bất biến (Hard Boundaries)**: {MUST_NEVER_VIOLATE}
- **Khả năng thích ứng (Adaptive Flexibility)**: {WHEN_AND_HOW_TO_CUSTOMIZE}
