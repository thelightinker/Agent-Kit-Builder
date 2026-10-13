---
name: {RULE_NAME}
version: 1.0.0
priority: P1 # [P0: Inviolable Global Core | P1: Specialized Tactical Rule | P2: Local Style/Format]
trigger: always_on # [always_on | model_decision | manual]
description: "{BRIEF_DESCRIPTION_OF_RULE_PURPOSE_FOR_MODEL_DECISION}"
tags: [{domain}, {category}]
---

# Rule: {RULE_TITLE}

> "{ONE_SENTENCE_SUMMARY_OF_INVIOLABLE_INVARIANT}"

---

## 1. Ownership & Boundaries (Ranh Giới Thẩm Quyền)

- **Sở hữu độc quyền:** {Danh mục 2-4 khía cạnh nghiệp vụ/kỹ thuật mà Rule này trực tiếp chi phối}.
- **Chỉ tham chiếu (Không định nghĩa lại):**
  - {Quy tắc nền tảng / Invariant P0} $\rightarrow$ `{P0_RULE_OR_CONSTITUTION}`.
  - {Quy chuẩn kiểm định chất lượng} $\rightarrow$ `{QUALITY_ENGINE_OR_AUDIT_RULE}`.
  - {Điều phối & chuyển giao bước} $\rightarrow$ `{ORCHESTRATOR_OR_WORKFLOW}`.

---

## 2. Các Bất Biến Cốt Lõi (Inviolable Invariants)

1. **{RULE_PREFIX}-001 · {INVARIANT_NAME_1}**:
   - {Mô tả mệnh lệnh thực thi nhị phân, 100% rõ ràng}.
   - **CẤM TUYỆT ĐỐI**: {Hành vi phủ định rõ ràng, không có ngoại lệ ngầm định}.

2. **{RULE_PREFIX}-002 · {INVARIANT_NAME_2}**:
   - {Quy chuẩn xác thực dữ kiện / kiểm chứng nhị phân}.

---

## 3. Ma Trận Hành Vi & Mẫu Đối Chiếu (Action Matrix / Contrast Rubric)

```
❌ HÀNH VI KHÔNG MONG MUỐN: {INCORRECT_BEHAVIOR_EXAMPLE}
✅ HÀNH VI CHUẨN MỰC: {CORRECT_BEHAVIOR_EXAMPLE}
```

| Trạng Thái Dữ Liệu Đầu Vào | Phản Xạ Hành Động Chuẩn Mực |
|:---|:---|
| **{TRẠNG_THÁI_1}** | ➔ {HÀNH_ĐỘNG_1}: {Mô tả chi tiết}. |
| **{TRẠNG_THÁI_2}** | ➔ {HÀNH_ĐỘNG_2}: {Mô tả chi tiết}. |

---

## 4. Giao Thức Xử Lý Vi Phạm & Vùng Mơ Hồ (Violation & Uncertainty Protocol)

- **Khi phát hiện dữ liệu thiếu hoặc vi phạm ranh giới**:
  - Dừng thực thi ngay lập tức, không tự ý đoán mò hoặc điền khuyết.
  - Báo hiệu rõ ràng: `⛔ [{RULE_PREFIX}_VIOLATION]: {Mô tả ngắn gọn lỗi hoặc dữ liệu thiếu}`.
  - Kích hoạt chế độ an toàn: {Hỏi tác giả / Yield to Interview / Fallback to Safe State}.
