---
name: validate-kit
description: "Kiểm định Chất lượng Agent Kit (Validate Kit) với Audit 3 lớp và bảng điểm Rubric 5 sao."
version: 2.0.0
requires_agents: kit-architect
requires_skills: kit-verifying
artifact_outputs: audit-report
---

# Workflow: Validate Kit (Kiểm định Chất lượng)

Sử dụng để kiểm tra và đánh giá chất lượng của một Agent Kit (đầu ra của quá trình tạo mới/nâng cấp, hoặc đánh giá một bộ kit sẵn có của người dùng).

---

## Các bước thực hiện

### Bước 1: Khởi tạo Kiểm định
1. Nạp tài liệu của Agent Kit cần đánh giá.
2. Kích hoạt skill: `skills/kit-verifying/SKILL.md`.

---

### Bước 2: Chạy 3 Lớp Kiểm tra (3-Layer Audit)

#### Lớp 1: L1 Deterministic Linting
Chạy script kiểm tra cấu trúc:
```bash
python .agents/scripts/validate_kit.py ./output/<kit-name>
```
*Đạt (0 errors)*: Tiếp tục sang Lớp 2.
*Không đạt*: Dừng lại, ghi nhận lỗi cấu trúc.

#### Lớp 2: L2 Adaptive Scenario Testing
1. **Tóm tắt**: Kiểm tra 0 biệt ngữ AI, trả lời đủ 3 câu hỏi.
2. **DoD**: Kiểm tra tính nhị phân, đo lường được và 0 tính từ cảm tính.
3. **No Lens Stuffing**: Đảm bảo không nhồi cơ chế thừa.
4. **No Provider Lock-in**: Độc lập với nền tảng LLM.
5. **Kịch bản thực tế**: Thử nghiệm 2-4 kịch bản input theo domain.

#### Lớp 3: L3 Adversarial Stress Testing
1. Thử thách prompt bằng input thiếu dữ kiện hoặc cố ý gây nhiễu.
2. Tìm kẽ hở trong DoD (DoD Loophole).

---

### Bước 3: Chấm điểm & Báo cáo (Audit Report)

Chấm điểm kit dựa trên 5 tiêu chí:

| Tiêu chí | Điểm (⭐ / ❌) | Ghi chú chi tiết |
|:---|:---:|:---|
| **Structural** | | Cấu trúc file và frontmatter |
| **Specificity** | | DoD nhị phân và constraints cụ thể |
| **Relevance** | | Tính tinh gọn, không over-engineering |
| **Uniqueness** | | Độ sâu sắc đặc trưng domain |
| **Usability** | | Phần tóm tắt và trải nghiệm người dùng |

#### Kết luận đánh giá (Verdict)
- **5/5 ⭐ (EXEMPLARY)**: Xuất sắc. Bàn giao ➔ Gợi ý lưu vào `/remember-kit`.
- **4/5 ⭐ (PASS)**: Đạt chuẩn chất lượng. Bàn giao được.
- **< 4/5 ⭐ (CONDITIONAL / FAIL)**: Cần chỉnh sửa qua `/refactor-kit`.
