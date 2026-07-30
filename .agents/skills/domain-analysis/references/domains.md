# Domain Pattern Database

Thư viện mẫu thiết kế domain-specific levers, core verbs, và failure modes phổ biến cho 4 lĩnh vực chính.

---

## 1. Lĩnh vực: Phát triển Phần mềm (Software Development)

*   **Core Verbs**: implement, write-tests, lint, refactor, debug, compile, validate, document.
*   **Outcome Patterns**:
    *   *Developer*: Tạo mã nguồn và ca kiểm thử (unit tests).
    *   *Quality Engineer*: Kiểm tra chất lượng, chạy linter, validate biên dịch.
    *   *Debugger*: Phân tích logs, tìm lỗi tận gốc (root cause).
*   **Typical Lenses**: C (Reliability), A (Efficiency), F (Safety - no destructive commands).
*   **Quality Signals**: Mã nguồn compile không lỗi; test coverage đạt ngưỡng target; không có lỗi bảo mật tĩnh (static analysis pass).
*   **Common Failure Modes**:
    *   *Code breaks on run*: Agent viết code trông đúng nhưng không chạy được.
        *   *Đòn bẩy (Lever)*: **Verification Script** - Chạy mã thực tế và kiểm tra output trước khi xác nhận hoàn thành.
    *   *Over-engineered patterns*: Viết code quá phức tạp cho các tác vụ đơn giản.
        *   *Đòn bẩy (Lever)*: Siết chặt Hard Constraints về cấu trúc thư mục và dependencies.

---

## 2. Lĩnh vực: Viết sách phi hư cấu (Book Writing - Non-Fiction)

*   **Core Verbs**: outline, draft, review, revise, research, cite, maintain-voice, edit.
*   **Outcome Patterns**:
    *   *Co-Author / Drafter*: Mở rộng dàn ý thành các chương sách chi tiết.
    *   *Editor / Reviewer*: Đánh giá sự mạch lạc của lập luận và độ thống nhất giọng văn.
    *   *Researcher*: Xác minh tuyên bố, kiểm tra tính đúng đắn của số liệu.
*   **Typical Lenses**: B (Flexibility), C (Reliability), D (Lean Context for long chapters).
*   **Quality Signals**: Giọng văn đồng nhất; lập luận chặt chẽ; trích dẫn nguồn số liệu rõ ràng.
*   **Common Failure Modes**:
    *   *Voice Drift*: Thay đổi giọng văn giữa các chương sách.
        *   *Đòn bẩy (Lever)*: **Voice Profile Document** - Tài liệu quy ước mẫu văn, mức độ trang trọng và từ vựng đặc trưng nạp ở đầu session.
    *   *Citation Hallucination*: Tự bịa số liệu hoặc trích dẫn không có thật.
        *   *Đòn bẩy (Lever)*: Hard constraint bắt buộc đánh dấu [CHƯA XÁC MINH] nếu không đối chiếu được nguồn.

---

## 3. Lĩnh vực: Quản lý & Chiến lược Kinh doanh (Business & Strategy)

*   **Core Verbs**: analyze, audit, forecast, plan, pitch, manage-risk, evaluate.
*   **Outcome Patterns**:
    *   *Business Analyst*: Phân tích SWOT, tìm đòn bẩy thị trường.
    *   *Strategist*: Lập kế hoạch hành động ngắn hạn và dài hạn.
    *   *Financial Risk Evaluator*: Dự báo và cảnh báo rủi ro dòng tiền/chi phí.
*   **Typical Lenses**: B (Flexibility), C (Reliability), F (Escalation on high-risk actions).
*   **Quality Signals**: Gợi ý có tính khả thi cao; lập luận chiến lược đi kèm số liệu thực tế; kịch bản rủi ro toàn diện.
*   **Common Failure Modes**:
    *   *Generic advice*: Đưa ra các gợi ý kinh doanh quá chung chung như sách giáo khoa.
        *   *Đòn bẩy (Lever)*: **Strategic Alignment Matrix** - Bản phân tích đối chiếu chiến lược đề xuất trực tiếp với 3 rào cản lớn nhất của doanh nghiệp.
    *   *Unrealistic growth numbers*: Dự báo doanh số phi thực tế mà không phân tích chi phí đi kèm.
        *   *Đòn bẩy (Lever)*: Định nghĩa DoD yêu cầu kiểm chứng dòng tiền tối thiểu.

---

## 4. Lĩnh vực: Nghiên cứu & Tổng hợp Tri thức (Research & Synthesis)

*   **Core Verbs**: search, screen, extract, synthesize, evaluate-evidence, summarize.
*   **Outcome Patterns**:
    *   *Academic Researcher*: Đọc và tổng hợp các nghiên cứu khoa học.
    *   *Fact-Checker*: Kiểm chứng tin đồn hoặc tuyên bố dựa trên bằng chứng khoa học.
*   **Typical Lenses**: C (Reliability), D (Lean Context for paper abstracts).
*   **Quality Signals**: Báo cáo có phân cấp độ tin cậy của bằng chứng (Evidence level ranking); nguồn rõ ràng.
*   **Common Failure Modes**:
    *   *Cherry-Picking*: Chỉ trích dẫn các tài liệu ủng hộ luận điểm của agent, bỏ qua các nghiên cứu đối lập.
        *   *Đòn bẩy (Lever)*: **Balanced Literature Protocol** - Cơ chế yêu cầu bắt buộc tìm kiếm và đối chiếu ít nhất 2 nghiên cứu có kết quả ngược lại.
