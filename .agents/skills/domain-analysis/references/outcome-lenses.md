# Outcome Lens Library

Tài liệu tham khảo chi tiết về 6 Outcome Lenses dùng để định hình các cơ chế của Agent Kit dựa trên độ phức tạp (Complexity Tiers).

---

## Lenses A-F: Chi tiết & Ví dụ Cơ chế

### Lens A — Token Efficiency (Tối ưu hóa Chi phí & Latency)
*   **Outcome**: Vận hành Agent Kit với số lượng token tối thiểu mà không làm giảm độ chính xác.
*   **Ví dụ cơ chế**:
    *   *Delta-Only output*: Chỉ yêu cầu agent patch/diff thay vì viết lại toàn bộ file.
    *   *System prompt budget*: Giới hạn kích thước prompt theo Kit Type.
*   **Anti-patterns**: Nhồi toàn bộ tài liệu hướng dẫn vào system prompt thay vì dùng link/JIT load.

### Lens B — Adaptive Flexibility (Độ Linh hoạt Thích ứng)
*   **Outcome**: Agent hoạt động ổn định trước các định dạng đầu vào bất ngờ hoặc mơ hồ.
*   **Ví dụ cơ chế**:
    *   *State-switch*: Agent tự chuyển đổi chế độ hành vi dựa trên việc phân tích đầu vào.
    *   *Graceful degradation*: Trả ra kết quả tốt nhất có thể kèm cảnh báo thay vì báo lỗi dừng chạy.
*   **Anti-patterns**: Chỉ lập trình cho kịch bản thuận lợi (happy path), thiếu cơ chế xử lý khi dữ liệu thiếu hoặc sai định dạng.

### Lens C — Reliable Performance (Độ Tin cậy & Chính xác)
*   **Outcome**: Đảm bảo thông tin chính xác, triệt tiêu ảo tưởng (hallucination).
*   **Ví dụ cơ chế**:
    *   *Binary Definition of Done*: Tiêu chí đo lường rõ ràng, kiểm tra được bằng code hoặc nhị phân.
    *   *Source check*: Đánh dấu [CHƯA XÁC MINH] cho các thông tin chưa có nguồn kiểm chứng rõ ràng.
*   **Anti-patterns**: Sử dụng tính từ mơ hồ ("chuyên nghiệp", "tối ưu") để đặt yêu cầu chất lượng cho agent.

### Lens D — Lean Context (Tinh gọn Ngữ cảnh)
*   **Outcome**: Tránh quá tải attention budget của mô hình bằng cách nạp context theo tầng.
*   **Ví dụ cơ chế**:
    *   *Core/Module/Reference layer*: Phân chia ngữ cảnh thành 3 lớp và nạp JIT (Just-In-Time) khi cần.
*   **Anti-patterns**: Nạp toàn bộ kho tri thức (knowledge base) vào context của mỗi lượt hội thoại.

### Lens E — Interoperability (Khả năng Giao tiếp & Ghép nối)
*   **Outcome**: Cho phép ghép nối agent vào một hệ thống hoặc pipeline nhiều agent.
*   **Ví dụ cơ chế**:
    *   *Input/Output Schema*: Định nghĩa cấu trúc JSON/Markdown cố định cho đầu vào và đầu ra.
    *   *Handoff protocol*: Định rõ điều kiện trigger, payload và format gửi sang agent tiếp theo.
*   **Anti-patterns**: Handoff bằng ngôn ngữ tự nhiên không cấu trúc dẫn đến sai lệch thông tin.

### Lens F — Safety & Escalation (Độ An toàn & Điểm dừng Hỏi người)
*   **Outcome**: Agent biết dừng lại để hỏi ý kiến con người khi vượt quá thẩm quyền hoặc gặp lỗi lặp vô hạn.
*   **Ví dụ cơ chế**:
    *   *Confidence threshold*: Ngưỡng tin cậy thấp -> kích hoạt hỏi người.
    *   *Giới hạn tự sửa (Self-correction limits)*: Giới hạn tối đa N lần tự sửa lỗi, nếu vẫn fail thì escalate.
*   **Anti-patterns**: Agent tự đoán bừa tham số hoặc lặp vô hạn khi kiểm tra code lỗi.

---

## Phân bổ theo Tiers

| Tier | Kit Type | Lenses bắt buộc | Lenses tùy chọn |
|:-----|:---------|:----------------|:----------------|
| **1 — Micro** | Micro Kit | A + C | F (mức cơ bản) |
| **2 — Multi-state** | Standard Kit | A + C + B | D, F (nâng cao) |
| **3 — System/Suite** | Professional/Suite | A + C + B + E | D + F (toàn phần) |
