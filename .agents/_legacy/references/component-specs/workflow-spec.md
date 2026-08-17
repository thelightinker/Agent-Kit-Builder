# Workflow Spec — Chuẩn thiết kế Workflow

Workflow = multi-step process với state transitions. Dùng khi agent cần
orchestration phức tạp hơn "nhận input → trả output".

---

## Khi nào tạo Workflow

| Tình huống | Tạo workflow? |
|:-----------|:-------------|
| Agent có 3+ bước tuần tự rõ ràng | ✅ Có |
| Agent cần decision tree (if/else phức tạp) | ✅ Có |
| Agent có iteration loop (draft → review → revise) | ✅ Có |
| Agent cần phối hợp nhiều sub-tasks | ✅ Có |
| Agent Tier 1, 1 input → 1 output | ❌ Không |
| Logic đơn giản, viết vào system prompt đủ | ❌ Không |

---

## Workflow Format

### Instruction-Based (cho Antigravity)

Antigravity không có workflow engine runtime. Workflows = instructions.

```markdown
# Workflow: [Tên]

## States

| State | Mô tả | Entry Criteria | Exit Criteria |
|:------|:------|:---------------|:-------------|
| INTAKE | Thu thập input | User gửi request | Core properties extracted |
| ANALYSIS | Phân tích | Properties có | Analysis complete |
| GENERATION | Sinh output | Analysis done | Draft ready |
| REVIEW | Kiểm tra | Draft exists | Pass quality gate |
| DELIVERY | Giao output | Review pass | User nhận output |

## Transitions

| Từ State | Đến State | Condition | Action |
|:---------|:----------|:----------|:-------|
| INTAKE | ANALYSIS | Properties extracted | Run analysis |
| ANALYSIS | GENERATION | Analysis complete | Generate components |
| GENERATION | REVIEW | Draft ready | Run quality check |
| REVIEW | GENERATION | Quality fail (max 2) | Revise draft |
| REVIEW | DELIVERY | Quality pass | Assemble output |

## Decision Points

### DP1: [Tên quyết định]
- **Input**: [data cần để quyết định]
- **Option A**: [condition] → [action]
- **Option B**: [condition] → [action]
- **Default**: [fallback action]

## Error Handling

| Error | At State | Recovery |
|:------|:---------|:---------|
| [mô tả lỗi] | [state] | [cách xử lý] |
```

---

## Visual Representation

Dùng ASCII flowchart trong workflow file:

```
INPUT → ANALYSIS → GENERATION → REVIEW
                       ↑          │
                       └──────────┘ (if fail, max 2)
                                  │
                                  ↓ (if pass)
                               DELIVERY
```

---

## Workflow Principles

### 1. Finite Loops
Mọi loop phải có giới hạn:
- "Tối đa 2 lần revise"
- "Max 3 iterations"
→ KHÔNG BAO GIỜ loop vô hạn

### 2. Clear Entry/Exit
Mỗi state:
- Entry criteria: condition cụ thể để vào state
- Exit criteria: condition cụ thể để rời state
- KHÔNG mơ hồ: "khi đủ tốt" ← FAIL. "Khi pass 4/5 quality criteria" ← PASS.

### 3. Escalation Path
Mọi workflow phải có đường escalate to human:
- Khi loop exhausted
- Khi error không recovery được
- Khi ambiguity không resolve được

### 4. Single Responsibility
1 workflow = 1 purpose. Không trộn nhiều workflows vào 1.

---

## Quality Checklist

```
□ States defined với entry/exit criteria rõ ràng
□ Transitions có conditions cụ thể
□ Mọi loop có giới hạn
□ Error handling cho mỗi state
□ Escalation path to human
□ Visual representation (ASCII flowchart)
□ Instruction-based (compatible Antigravity)
```
