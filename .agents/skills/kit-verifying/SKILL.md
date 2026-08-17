---
name: kit-verifying
description: >
  Kiểm định chất lượng Agent Kit theo 3 lớp: L1 Deterministic Linting
  (validate_kit.py, eval_runner.py), L2 Adaptive Scenario Testing (sinh test cases theo domain),
  và L3 Adversarial Stress Testing. Kích hoạt khi kiểm thử, chấm điểm hoặc nghiệm thu Agent Kit.
when_to_use: "Khi cần kiểm định chất lượng, chạy test suite hoặc chấm điểm Agent Kit mới/refactor."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.1.0
---

# Kit Verifying

Kỹ năng kiểm định chất lượng toàn diện cho Agent Kit, kết hợp giữa công cụ tự động hóa tất định (Deterministic) và đánh giá ngữ nghĩa thích ứng (Adaptive Evaluation).

---

## 📚 REFERENCE KNOWLEDGE ACTIVATION (NẠP ON-DEMAND)

Khi thực hiện kiểm thử và đánh giá chuyên sâu:
- **Danh mục Lỗi AI để Stress-test L3**: Đọc [failure-modes.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/failure-modes.md) để thử thách các kẽ hở DoD và Hard Constraints.
- **Quy chuẩn Xử lý Lỗi & Escalation**: Đọc [error-resilience.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/error-resilience.md) để kiểm tra cơ chế dừng và hỏi người dùng.
- **Tiêu chuẩn Hợp đồng Kỹ thuật**: Đọc [component-contracts.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/component-contracts.md) để đối soát frontmatter và ACI tool.

---

## 1. QUY TRÌNH KIỂM ĐỊNH 3 LỚP (3-LAYER AUDIT)

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: L1 Deterministic Linting (validate_kit.py)     │ -> 0 errors bắt buộc
├─────────────────────────────────────────────────────────┤
│ Layer 2: L2 Adaptive Scenario Testing (Domain-Specific) │ -> 2-4 Test cases
├─────────────────────────────────────────────────────────┤
│ Layer 3: L3 Adversarial Stress Testing (Loopholes/Edge) │ -> DoD & Constraints
└─────────────────────────────────────────────────────────┘
```

---

## 2. LAYER 1: DETERMINISTIC LINTING

Sử dụng script để kiểm tra các thuộc tính cấu trúc cứng:

```bash
# Kiểm tra toàn vẹn cấu trúc và tham chiếu
python .agents/scripts/validate_kit.py ./output/<kit-name>

# Chạy eval suite (nếu có)
python .agents/scripts/eval_runner.py evals/eval_suite_example.json ./output/<kit-name>
```

**Tiêu chí Pass Layer 1:** 0 error. Nếu có warning, phải giải trình lý do hợp lý.

---

## 3. LAYER 2: ADAPTIVE SCENARIO TESTING

Thay vì dùng test case cố định, sinh kịch bản kiểm thử thích ứng theo domain và tier:

- **Micro Kit**: 1 Happy-path + 1 Edge-case input.
- **Standard Kit**: 2 Happy-path + 2 Edge-case inputs.
- **Professional / Suite Kit**: 3 Happy-path + 3 Adversarial + 1 Cross-component flow.

### Kiểm tra Ngữ nghĩa Cốt lõi:
1. **TÓM TẮT CHO NGƯỜI DÙNG**:
   - 0 thuật ngữ AI/kỹ thuật (prompt, LLM, token, schema, context).
   - Trả lời đủ 3 câu: Làm gì? Dùng khi nào? Giới hạn gì?
2. **Definition of Done**: 100% nhị phân, đo lường được, 0 tính từ cảm tính.
3. **No Lens Stuffing / Over-Engineering**: Mọi cơ chế đều phục vụ outcome thực tế.
4. **No Provider Lock-in**: Chạy tốt trên các LLM khác nhau.

---

## 4. LAYER 3: ADVERSARIAL STRESS TESTING

- Thử nghiệm input thiếu dữ kiện $\rightarrow$ Agent có hỏi lại hoặc gắn nhãn `[CHƯA XÁC MINH]` không?
- Thử nghiệm input sai lệch/cố ý lừa $\rightarrow$ Hard Constraints có chặn đứng không?
- Tìm kẽ hở DoD $\rightarrow$ Có thể trả output tồi mà vẫn "pass" checklist không?

---

## 5. THANG ĐIỂM RUBRIC 5 SAO & KẾT LUẬN

| Tiêu chí | Trọng số | Yêu cầu đạt |
|:---|:---:|:---|
| **Structural** | 20% | Đủ cấu phần theo Tier, frontmatter hợp lệ |
| **Specificity** | 25% | DoD nhị phân, Constraints rõ ràng, 0 mơ hồ |
| **Relevance** | 20% | Đúng trọng tâm, không over-engineered |
| **Uniqueness** | 15% | Thể hiện sâu sắc đặc trưng domain, 0 generic |
| **Usability** | 20% | Tóm tắt dễ hiểu, hướng dẫn rõ ràng |

### Verdict:
- **5/5 ⭐ (EXEMPLARY)**: Xuất sắc. Bàn giao + Gợi ý lưu vào Golden Examples (`/remember-kit`).
- **4/5 ⭐ (PASS)**: Đạt chuẩn chất lượng. Đủ điều kiện bàn giao.
- **< 4/5 ⭐ (CONDITIONAL / FAIL)**: Cần chỉnh sửa qua `/refactor-kit`.
