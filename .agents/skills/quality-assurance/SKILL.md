---
name: quality-assurance
description: ">"
when_to_use: "Kích hoạt khi cần năng lực quality-assurance trong quy trình tạo hoặc kiểm định Agent Kit."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.3.0
---

# Quality Assurance

## Overview

Quy trình đánh giá chất lượng Agent Kit trước khi bàn giao. Mọi kit do Agent Kit Creator tạo ra đều phải được chấm điểm theo **Ma Trận Trọng Số 6 Chiều**:
$$\text{Total Score} = 0.25(C) + 0.25(B) + 0.20(A) + 0.15(F) + 0.10(E) + 0.05(D)$$
Kit đạt từ **8.0/10 điểm trở lên** và vượt qua 100% cả **3 Hard Fail Gates** mới được phép bàn giao.

---

## Quy trình Audit 3 Lớp

### Lớp 1: Structural Check (Kiểm tra Cấu trúc - Nhị phân)

Kiểm tra sự tồn tại và định dạng cơ bản. Nếu fail bất kỳ mục nào ở đây, trả về kết quả yêu cầu sửa đổi ngay mà không cần kiểm tra tiếp Lớp 2.

#### Agent (System Prompt)
- [ ] Có phần TÓM TẮT CHO NGƯỜI DÙNG (3-5 dòng).
- [ ] Có đầy đủ 4 phần SYSTEM PROMPT cốt lõi.
- [ ] Definition of Done có tối thiểu 3 tiêu chí.
- [ ] HARD CONSTRAINTS có tối thiểu 2 giới hạn.
- [ ] FORMAT ĐẦU RA có template hiển thị rõ ràng.

#### Skills (nếu có)
- [ ] SKILL.md tồn tại và chứa YAML Frontmatter (name + description).
- [ ] SKILL.md ngắn hơn 500 dòng.
- [ ] Có evals/evals.json với ít nhất 1 test case.

#### Memory (nếu có)
- [ ] Có mô tả cấu trúc Memory (schema).
- [ ] Xác định rõ file lưu trữ và quy trình nạp/cập nhật (áp dụng Skeleton State < 1KB).

#### Workflows & Tools (nếu có)
- [ ] Trạng thái (states) và điều kiện chuyển (transitions) theo chuẩn Node Anatomy 5 phần.
- [ ] Danh sách tham số tool, kiểu dữ liệu, và cách xử lý lỗi đầy đủ.

---

### Lớp 2: Semantic Check & 3 Hard Fail Gates

Đánh giá chất lượng thực tế và kiểm tra tính an toàn sống còn.

#### 🚨 3 HARD FAIL GATES (BẮT BUỘC PASS 100%):
1. **Gate 1 (Zero-Fabrication):** Điểm $C < 8.0/10$ (phát hiện bịa thông tin/ảo giác) ➔ **ĐÁNH FAIL NGAY LẬP TỨC**.
2. **Gate 2 (Task Completion):** Điểm $B < 8.0/10$ (bỏ dở task giữa chừng) ➔ **ĐÁNH FAIL NGAY LẬP TỨC**.
3. **Gate 3 (Token ROI):** Điểm $F$ có $ROI < 1.0$ (phình token x2 mà năng lực tăng < x1.5) ➔ **BỊ HỦY BỎ**.

---

### Lớp 3: Adversarial Test (Stress Test & Thử phá)

Tìm kẽ hở trong thiết kế của kit.
- **Edge Case Simulation**: Tạo ra 2-3 kịch bản đầu vào cực đoan, mơ hồ hoặc sai lệch. Thử xem DoD và constraints của kit có xử lý được không.
- **DoD Loophole**: Liệu agent có thể trả ra kết quả cực tệ nhưng vẫn vượt qua tất cả DoD kỹ thuật không?

---

## Chấm điểm Rubric 6 Chiều Theo Trọng Số

Tổng điểm đạt từ **8.0/10 điểm trở lên** (và 0 vi phạm Hard Fail Gate) mới được bàn giao:

1. 🔴 **C. Reliability (Độ tin cậy - 25%):** 100% Zero-Fabrication, cấm ảo giác.
2. 🔴 **B. Task Completion (Tỷ lệ hoàn thành - 25%):** Duy trì Flow State hoàn thành 100% task.
3. 🟡 **A. Output Quality (Chất lượng đầu ra - 20%):** Ngôn từ đắt giá, giàu mỏ neo hình ảnh Velcro Memory.
4. 🟡 **F. Cost & Complexity (Chi phí Token ROI - 15%):** $ROI \ge 1.25$, Selective Reading, Skeleton Memory.
5. 🟢 **E. Performance (Hiệu suất & Latency - 10%):** Right-First-Time Socratic Thinking.
6. 🟢 **D. Adaptability (Khả năng thích ứng - 5%):** Thích ứng linh hoạt bối cảnh.

---

## Proactive Improvement Flags

Đánh dấu các lỗi phát hiện chủ động khi đánh giá kit:

| Mức độ (Severity) | Tình trạng phát hiện (Condition) | Giải pháp khuyến nghị (Recommendation) |
|:---|:---|:---|
| 🔴 Critical | Lens Stuffing (cơ chế không phục vụ outcome) | Xóa cơ chế thừa, giữ prompt tinh gọn |
| 🔴 Critical | Missing Domain-Specific Mechanisms | Chạy lại phân tích domain và thiết kế đòn bẩy riêng |
| 🔴 Critical | Tóm tắt người dùng chứa thuật ngữ kỹ thuật | Viết lại bằng ngôn ngữ đời thường cho người low-tech |
| 🟡 Serious | Tính từ mơ hồ trong DoD | Thay thế bằng tiêu chí đo lường nhị phân |
| 🟡 Serious | Khóa Provider (Provider lock-in) | Chuyển đổi prompt sang định dạng agnostic |
| 🟢 Minor | Thiếu đòn bẩy nâng cao ngoài 6 lenses | Cân nhắc bổ sung đòn bẩy riêng |

---

## Chi tiết Tham khảo

- Chi tiết rubric chấm điểm: → `references/quality-rubric.md`
- Thư viện lỗi thường gặp: → `references/failure-modes.md`
