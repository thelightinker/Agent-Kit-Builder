---
name: domain-profiling
description: >
  Phân tích domain nghiệp vụ cho Agent Kit: trích xuất Core Verbs,
  tìm đòn bẩy 80/20 (Dynamic Enhancement Discovery), dự đoán failure modes,
  thực hiện Right Altitude Test để chọn Topology trên Spectrum (Micro/Standard/Mini-Suite/Full Suite)
  và đề xuất cấu phần tối thiểu. Luôn kích hoạt khi bắt đầu tạo kit mới hoặc đánh giá lại domain.
when_to_use: "Khi cần phân tích nghiệp vụ, hành động cốt lõi, đòn bẩy và topology cho Agent Kit mới hoặc refactor."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.2.0
---

# Domain Profiling

Kỹ năng phân tích chiều sâu miền nghiệp vụ (domain) để xây dựng nền tảng vững chắc cho Agent Kit, loại bỏ phỏng đoán và ngăn chặn over-engineering ngay từ đầu.

---

## 📚 REFERENCE KNOWLEDGE ACTIVATION (NẠP ON-DEMAND)

Khi cần tra cứu chuyên sâu trong quá trình phân tích:
- **Cây quyết định Topology & Right Altitude Test**: Đọc [workflow-topologies.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/workflow-topologies.md) để cân nhắc chi phí điều phối vs lợi ích context.
- **6 Lăng kính Thiết kế & Đòn bẩy ROI**: Đọc [outcome-lenses.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/outcome-lenses.md) để đánh giá Token Efficiency, Adaptive Flexibility, Reliable Performance...
- **Thư viện 12+ AI Failure Modes**: Đọc [failure-modes.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/failure-modes.md) để tra cứu lỗi đặc trưng theo domain.

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

Trả lời 3 câu hỏi cốt lõi — độc lập cho từng agent/specialist cần xây dựng:

1. **Outcome quan trọng nhất** của agent này là gì? *(Kết quả thực tế nào chứng minh agent thành công?)*
2. **Điểm thất vọng phổ biến nhất** của người dùng thực tế khi dùng agent này? *(Đây là đòn bẩy 80/20 ưu tiên hàng đầu).*
3. **Trade-off ROI**: Tính toán tỷ lệ $ROI = \frac{\text{Mức tăng Năng lực}}{\text{Chi phí Token \& Độ phức tạp}}$
   - ✅ **Chấp nhận ($ROI \ge 1.25$):** Tăng năng lực x1.5 mà chi phí chỉ tốn x1.2.
   - ❌ **Từ chối ($ROI < 1.0$ - Over-engineered):** Tăng năng lực x1.5 nhưng token tốn gấp đôi (x2.0).

---

## 3. THE RIGHT ALTITUDE TEST & TOPOLOGY SELECTION

Thay vì ép cứng 3 hộp, xác định vị trí tối ưu trên **Phổ Kiến trúc (Spectrum)**:

$$\mathbf{\text{Coordination Cost (Handoff + Routing)}} < \mathbf{\text{Context/Cognitive Cost Saved (Attention Rot + Confusion)}}$$

| Vị trí trên Spectrum | Điều kiện Thỏa mãn | Cấu trúc Khuyến nghị |
|:---|:---|:---|
| **Micro** | 1 tác vụ đơn lẻ, stateless, 1-shot | 1 System Prompt duy nhất (< 500 từ) |
| **Standard** | 1 domain tập trung, $\le 4-5$ skills, luồng tuyến tính | 1 Single Agent + Skills + Workflows |
| **Mini-Suite** | 2 mảng đối trọng (ví dụ: Maker & Reviewer / Coder & Auditor) | 1 Lead Orchestrator + 2 Specialist Agents |
| **Full Suite Hierarchy** | $\ge 3$ domain độc lập, $\ge 6-15$ skills, cần Scoped Memory | 1 Master Orchestrator + 3–7 Specialist Agents + Scoped Memory |

---

## 4. REPORT FORMAT

Sau khi phân tích, trả về Domain Profile theo mẫu:

```markdown
# Domain Profile: [Tên Domain / Kit]

## 1. Core Verbs Matrix
[Bảng 5-10 core verbs]

## 2. 80/20 Leverage & ROI Analysis
- Outcome cốt lõi: ...
- Điểm thất vọng lớn nhất: ...
- Đòn bẩy đề xuất (ROI >= 1.25): ...

## 3. Right Altitude Test & Topology Selection
- Vị trí Spectrum: [Micro / Standard / Mini-Suite / Full Suite]
- Rationale: Coordination Cost < Context Cost Saved vì ...
- Danh sách Specialist Agents đề xuất (nếu là Suite):
  - Specialist A: Domain X -> Cụm Skills [skill-1, skill-2]
  - Specialist B: Domain Y -> Cụm Skills [skill-3, skill-4]
```
