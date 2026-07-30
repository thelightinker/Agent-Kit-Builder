# Failure Modes — Thư viện Lỗi thường gặp

Danh sách các phản mẫu (anti-patterns) và lỗi thiết kế thường gặp khi xây dựng Agent Kit, phân loại theo mức độ nghiêm trọng.

---

## 🔴 Critical — Lỗi nghiêm trọng (Không thể bàn giao)

### 1. Lens Stuffing (Nhồi cơ chế)
*   **Triệu chứng**: System Prompt phình to quá mức, chứa nhiều hướng dẫn kiểm soát ngữ cảnh, an toàn, hoặc I/O phức tạp dù agent chỉ làm tác vụ đơn giản.
*   **Nguyên nhân**: Người tạo cố gắng đưa tất cả các lens/quy tắc vào prompt mà không chọn lọc.
*   **Khắc phục**: Chạy quy trình YAGNI, xóa mọi dòng không trực tiếp tạo ra chất lượng đầu ra.

### 2. Human Summary Failure (Lỗi Tóm tắt)
*   **Triệu chứng**: Người dùng không chuyên môn đọc Tóm tắt vẫn không hiểu agent dùng để làm gì hoặc dùng khi nào.
*   **Nguyên nhân**: Lạm dụng thuật ngữ kỹ thuật (prompt, LLM, context, token, model...).
*   **Khắc phục**: Viết lại tóm tắt bằng ngôn ngữ đời thường, trả lời rõ 3 câu hỏi (Làm gì? Khi nào dùng? Giới hạn?).

### 3. Provider Lock-in (Khóa Nhà cung cấp)
*   **Triệu chứng**: Prompt chứa các chỉ dẫn phụ thuộc cụ thể vào tính năng hoặc cú pháp của một bên (ví dụ: Claude Artifacts, Gemini system instruction format...).
*   **Khắc phục**: Chuyển đổi prompt sang định dạng Markdown chuẩn, trung lập (provider-agnostic).

### 4. Template-Replaceable (Chung chung)
*   **Triệu chứng**: Kit chỉ là một khung sườn trống được điền tên domain vào.
*   **Khắc phục**: Tìm kiếm và áp dụng các cơ chế đòn bẩy đặc thù của domain (domain-specific levers).

---

## 🟡 Serious — Lỗi đáng ngại (Giảm chất lượng kit)

### 1. Vague DoD (DoD mơ hồ)
*   **Triệu chứng**: Sử dụng các tính từ cảm tính như "đầy đủ", "chất lượng", "sạch sẽ".
*   **Khắc phục**: Thay thế bằng tiêu chí đo lường được (số lượng từ, định dạng JSON/Markdown, sự tồn tại của file).

### 2. Over-engineered Micro Kit
*   **Triệu chứng**: Micro Kit (Tier 1) nhưng dài hơn 500 từ và chứa nhiều file phụ trợ không cần thiết.
*   **Khắc phục**: Gom tất cả vào 1 file system prompt duy nhất và rút gọn.

### 3. Tone Mixing (Lẫn lộn giọng văn)
*   **Triệu chứng**: Sử dụng giọng văn giải thích, thân thiện trong phần system prompt kỹ thuật dành cho LLM, hoặc dùng ngôn ngữ code trong phần tóm tắt cho người dùng.
*   **Khắc phục**: Tách biệt rõ ràng 2 phần. Phần kỹ thuật: lạnh lùng, chính xác. Phần người dùng: thân thiện, đời thường.

---

## Failure Modes đặc trưng của Suite Kit

### 1. Infinite Handoff Loop (Vòng lặp vô hạn)
*   **Triệu chứng**: Agent A chuyển việc cho Agent B, B chuyển cho C, C chuyển ngược lại cho A và chạy mãi không dừng.
*   **Khắc phục**: Phải chỉ định duy nhất một Lead Agent làm chủ luồng quyết định cuối cùng và phân bổ rõ ràng điểm dừng.

### 2. Merge Conflict (Xung đột kết quả)
*   **Triệu chứng**: Hai agent specialist làm việc song song tạo ra hai kết quả mâu thuẫn nhau và không có cơ chế hợp nhất.
*   **Khắc phục**: Thiết lập vai trò hợp nhất dữ liệu (synthesis) cho Lead Agent.

### 3. Context Drift (Lệch ngữ cảnh)
*   **Triệu chứng**: Mỗi agent hiểu yêu cầu của nhiệm vụ theo một hướng khác nhau do thiếu brief đồng nhất.
*   **Khắc phục**: Yêu cầu Lead Agent luôn viết và gửi một bản Brief hướng dẫn thống nhất cho các sub-agents trước khi dispatch.

### 4. Overhead > Value (Quá tải thủ tục)
*   **Triệu chứng**: Chia nhỏ quá nhiều agent cho một tác vụ đơn giản, gây lãng phí tokens và latency.
*   **Khắc phục**: Chạy YAGNI check: Nếu 1 agent multi-state có thể làm tốt tác vụ đó, không chia nhỏ thành Suite Kit.

### 5. Dead Letter (Thư chết)
*   **Triệu chứng**: Agent gửi handoff nhưng không có agent nào tiếp nhận hoặc xử lý.
*   **Khắc phục**: Bắt buộc mapping rõ ràng luồng handoff đến định danh agent cụ thể trong `manifest.json`.
