---
name: domain-profiling
description: >
  Phân tích domain nghiệp vụ cho Agent Kit: trích xuất Core Verbs,
  tìm đòn bẩy 80/20 (Dynamic Enhancement Discovery), dự đoán failure modes,
  xác định Complexity Tier (Micro/Standard/Professional/Suite) và đề xuất
  cấu phần tối thiểu. Luôn kích hoạt khi bắt đầu tạo kit mới hoặc đánh giá lại domain.
when_to_use: "Khi cần phân tích nghiệp vụ, hành động cốt lõi và đòn bẩy cho Agent Kit mới hoặc refactor."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.0.0
---

# Domain Profiling

Kỹ năng phân tích chiều sâu miền nghiệp vụ (domain) để xây dựng nền tảng vững chắc cho Agent Kit, loại bỏ phỏng đoán và ngăn chặn over-engineering ngay từ đầu.

---

## 1. PHÂN TÍCH CORE VERBS

Xác định 5-10 hành động xảy ra thường xuyên nhất trong domain. Mỗi verb đánh giá theo 4 tiêu chí:

| Tiêu chí | Câu hỏi kiểm định | Giá trị |
|:---|:---|:---|
| **Precision vs Creativity** | Cần chính xác tuyệt đối hay cần sáng tạo/linh hoạt? | Precision / Creativity |
| **Knowledge Type** | Cần tri thức chuyên sâu đặc thù hay tư duy logic chung? | Specialized / General |
| **Failure Severity** | Hậu quả nếu Agent thực hiện sai hành động này? | Low / Medium / Critical |
| **Automation Feasibility** | Có thể kiểm chứng tự động bằng script/pattern không? | Deterministic / Semantic |

*Nguyên tắc:* Các verb có `Critical` severity hoặc `Precision` cao bắt buộc phải có Hard Constraints và cơ chế Reality Check bảo vệ.

---

## 2. DYNAMIC ENHANCEMENT DISCOVERY (ĐÒN BẨY 80/20)

Trả lời 3 câu hỏi cốt lõi — độc lập cho từng agent cần xây dựng:

1. **Outcome quan trọng nhất** của agent này là gì? *(Kết quả thực tế nào chứng minh agent thành công?)*
2. **Điểm thất vọng phổ biến nhất** của người dùng thực tế khi dùng agent này? *(Đây là đòn bẩy 80/20 ưu tiên hàng đầu).*
3. **Trade-off ROI**: Tính toán tỷ lệ $ROI = \frac{\text{Mức tăng Năng lực}}{\text{Chi phí Token \& Độ phức tạp}}$
   - ✅ **Chấp nhận ($ROI \ge 1.25$):** Tăng năng lực x1.5 mà chi phí chỉ tốn x1.2.
   - ❌ **Từ chối ($ROI < 1.0$ - Over-engineered):** Tăng năng lực x1.5 nhưng token tốn gấp đôi (x2.0).

---

## 3. DỰ ĐOÁN FAILURE MODES

Dự đoán 3-5 lỗi sai nghiêm trọng nhất mà mô hình AI thường mắc phải trong domain này:

```markdown
| Failure Mode | Xác suất | Mức độ | Cơ chế phòng ngừa cụ thể |
|:---|:---:|:---:|:---|
| [Mô tả lỗi cụ thể] | High/Med/Low | Critical/High | [Ràng buộc phủ định hoặc cơ chế kiểm tra] |
```

---

## 4. PHÂN LOẠI COMPLEXITY TIER & ĐỀ XUẤT CẤU PHẦN

| Tier | Tiêu chí | Cấu phần khuyến nghị |
|:---|:---|:---|
| **Tier 1 (Micro)** | 1 tác vụ đơn lẻ, stateless, 1-shot | 1 System Prompt duy nhất (< 500 từ) |
| **Tier 2 (Standard)** | Quy trình nhiều bước, có trạng thái ngắn hạn | System Prompt + 1-2 Skills + Workflows |
| **Tier 3 (Professional)** | Hệ thống nghiệp vụ phức tạp, context lớn | System Prompt + Multi-skills + Memory + `manifest.json` |
| **Tier 4 (Suite)** | Nhiều agent phối hợp có lead/worker | Lead Orchestrator + Sub-agent Kits độc lập |

---

## 5. REPORT FORMAT

Sau khi phân tích, trả về Domain Profile theo mẫu:

```markdown
# Domain Profile: [Tên Domain / Agent]

## 1. Core Verbs Matrix
[Bảng 5-10 core verbs]

## 2. 80/20 Leverage & ROI Analysis
- Outcome cốt lõi: ...
- Điểm thất vọng lớn nhất: ...
- Đòn bẩy đề xuất (ROI >= 1.25): ...

## 3. Predicted Failure Modes
[Bảng failure modes & phòng ngừa]

## 4. Tier Classification & Components
- Phân loại: [Tier 1 / 2 / 3 / 4]
- Cấu phần cần sinh: [Danh sách file cụ thể]
```
