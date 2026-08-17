# Advanced Agent Prompt Patterns

> Cẩm nang thiết kế Prompt kiến trúc chuyên sâu: 3-Tier Autonomy Gate, Domain-Aware Anti-Defaults, Velcro Memory, Reality Check và Context Engineering.

---

## 1. 3-TIER AUTONOMY GATE (CHỐNG TÊ LIỆT TỰ CHỦ)

Quy tắc cốt lõi: **Chỉ dừng lại hỏi khi sự không chắc chắn làm thay đổi đáng kể outcome hoặc rủi ro.**

| Mức rủi ro | Đặc điểm tác vụ | Hành động của Agent | Ví dụ |
|:---|:---|:---|:---|
| **Tier A** (Low Risk / Reversible) | Tinh chỉnh UI nhỏ, sửa lỗi cú pháp, lệnh rõ ràng | **THỰC THI NGAY.** 0 câu hỏi thừa. | *"Đổi màu nút bấm sang Dawn"* ➔ Thực thi ngay. |
| **Tier B** (Medium Risk / Defaults Exist) | Triển khai tính năng chuẩn đã có mẫu sẵn | **TỰ CHỦ THỰC HIỆN.** Áp dụng sensible defaults + ghi rõ giả định vào kết quả. | *"Viết REST API cho User Profile"* ➔ Tạo schema chuẩn + liệt kê giả định. |
| **Tier C** (High Risk / Irreversible) | Đổi kiến trúc lớn, xóa dữ liệu, tác vụ tốn kém | **DỪNG LẠI & HỎI.** Chỉ hỏi tối đa 1-3 câu trọng tâm nhất. | *"Chuyển database từ Postgres sang Mongo"* ➔ Hỏi xác nhận phạm vi migration. |

---

## 2. DOMAIN-AWARE ANTI-DEFAULT THINKING

Tránh sự rập khuôn theo từng lĩnh vực chuyên môn:
- **UI / Frontend**: Phá vỡ các layout mặc định phẳng lì, cliché; ưu tiên thiết kế có phân cấp thị giác rõ ràng, micro-animations và styling hiện đại.
- **Backend / Infra**: Ưu tiên giải pháp ổn định, đơn giản, "Boring & Stable Tech First" (YAGNI); không tự ý đưa vào kiến trúc phân tán quá phức tạp khi chưa cần thiết.
- **Tư duy cốt lõi**: Thách thức các giả định lười biếng (defaults), nhưng luôn tôn trọng sự ổn định của hệ thống.

---

## 3. VELCRO MEMORY & REALITY CHECK

### Velcro Memory (Mỏ neo Trực quan):
Sử dụng các khái niệm hình ảnh hoặc thuật ngữ trực quan mạnh mẽ để giúp LLM ghi nhớ và tuân thủ các quy tắc quan trọng xuyên suốt phiên làm việc.

### Reality Check Protocol (Thực tế hơn Checklist):
- Bắt buộc kiểm chứng bằng bằng chứng thực tế (Empirical Evidence) từ file hoặc kết quả chạy lệnh.
- Sửa tận gốc nguyên nhân (Root Cause Fix) thay vì vá tạm bề mặt.
- Không dùng placeholder (`TODO`, `TBD`, `[INSERT HERE]`) trong output bàn giao.

---

## 4. CONTEXT ENGINEERING GUIDELINES

- **Attention Budget**: Nhồi quá nhiều context "cho chắc ăn" làm tăng bậc hai tương tác pairwise giữa các tokens $\rightarrow$ gây Context Rot và giảm chất lượng output.
- **Just-In-Time Retrieval**: Giữ context sạch bằng cách chỉ nạp full reference khi bước hiện tại thật sự yêu cầu.
- **Right Altitude**: System Prompt phải ở mức cao độ phù hợp — đủ cụ thể cho các hành vi cốt lõi, nhưng đủ không gian heuristic cho các trường hợp biến thiên.
