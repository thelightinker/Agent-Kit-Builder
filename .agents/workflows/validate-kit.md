---
name: validate-kit
description: "Kiểm định Chất lượng Agent Kit (Validate Kit) với Audit 3 lớp và bảng điểm Rubric 5 sao."
version: 1.0.0
requires_agents: quality-auditor
requires_skills: quality-assurance, auditing-quality-gates, adversarial-evaluating
artifact_outputs: audit-report
---

# Workflow: Validate Kit (Kiểm định Chất lượng)

Sử dụng để kiểm tra và đánh giá chất lượng của một Agent Kit (đầu ra của quá trình tạo mới/nâng cấp, hoặc đánh giá một bộ kit sẵn có của người dùng).

---

## Các bước thực hiện

### Bước 1: Khởi tạo Kiểm định
1. Nạp tài liệu của Agent Kit cần đánh giá.
2. Kích hoạt skill: `skills/quality-assurance/SKILL.md`.

---

### Bước 2: Chạy 3 Lớp Kiểm tra (3-Layer Audit)

#### Lớp 1: Structural Check (Kiểm tra Cấu trúc)
Đối chiếu kit với checklist nhị phân trong `skills/quality-assurance/SKILL.md`:
* *Đạt*: Tiếp tục sang Lớp 2.
* *Không đạt*: Dừng lại, đánh giá **1/5 sao** (hoặc fail tiêu chí Structural) và ghi nhận các lỗi thiếu cấu trúc.

#### Lớp 2: Semantic Check (Kiểm tra Ngữ nghĩa)
Đánh giá chất lượng chiều sâu:
1. **Tóm tắt**: Kiểm tra xem có chứa biệt ngữ AI hoặc thiếu thông tin 3 câu hỏi không.
2. **DoD**: Kiểm tra tính nhị phân, đo lường được và không có tính từ cảm tính.
3. **Lens Stuffing**: Phát hiện cơ chế thừa không phục vụ mục tiêu đầu ra.
4. **Provider Lock-in**: Tìm các từ khóa lock-in nhà cung cấp (Gemini, Claude...).
5. **Template Replaceable**: Thử nghiệm đổi tên domain để kiểm tra tính đặc trưng của kit.

#### Lớp 3: Adversarial Test (Thử thách & Thử phá)
1. Giả lập 2 kịch bản đầu vào khó khăn hoặc sai lệch để kiểm tra tính linh hoạt (Adaptive Flexibility) và an toàn (Safety & Escalation).
2. Tìm kẽ hở trong DoD (DoD Loophole): Đảm bảo agent không thể lách luật để trả ra kết quả kém chất lượng.

---

### Bước 3: Chấm điểm & Đưa ra Kết luận

Chấm điểm kit dựa trên 5 tiêu chí của rubric trong `skills/quality-assurance/references/quality-rubric.md`.

#### Bảng điểm Rubric
| Tiêu chí | Điểm (⭐ / ❌) | Ghi chú chi tiết |
|:---|:---:|:---|
| Structural | | |
| Specificity | | |
| Relevance | | |
| Uniqueness | | |
| Usability | | |

#### Kết luận đánh giá (Verdict)
- **5/5 ⭐ (EXEMPLARY)**: Đạt tiêu chuẩn tối cao. Sẵn sàng bàn giao ➔ Kích hoạt workflow `/remember-kit` để lưu vào Golden Examples!
- **4/5 ⭐ (PASS)**: Đạt tiêu chuẩn chất lượng. Bàn giao được.
- **3/5 ⭐ (CONDITIONAL)**: Cần chỉnh sửa các lỗi cụ thể trước khi bàn giao (chạy `/refactor-kit`).
- **≤ 2/5 ⭐ (FAIL)**: Vi phạm nghiêm trọng các lỗi cấu trúc hoặc chất lượng. Cần làm lại phần lớn.

---

### Bước 4: Lập Báo cáo Kết quả (Audit Report)
Trả kết quả dưới dạng Báo cáo Đánh giá cho luồng xử lý chính:

```markdown
# Audit Report: [Tên Agent Kit]

## Score: [N]/5 ⭐
## Verdict: [PASS / CONDITIONAL / FAIL]

## Findings
- **Structural**: [Đạt / Không đạt - lý do]
- **Specificity**: [Chi tiết các DoD/Constraints mơ hồ]
- **Relevance**: [Chi tiết các cơ chế thừa, over-engineer]
- **Uniqueness**: [Đánh giá tính đặc trưng domain]
- **Usability**: [Đánh giá phần Tóm tắt dành cho người dùng]

## Required Fixes (Yêu cầu sửa đổi bắt buộc nếu Score < 4)
1. [Hành động sửa đổi cụ thể 1]
2. [Hành động sửa đổi cụ thể 2]
```
