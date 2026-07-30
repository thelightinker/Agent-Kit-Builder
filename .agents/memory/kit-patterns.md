# Kit Design Patterns — Các khuôn mẫu thiết kế Agent Kit xuất sắc

Tổng hợp các khuôn mẫu thiết kế và kỹ thuật tối ưu hóa được đúc rút từ thực tiễn phát triển các Agent Kit sản xuất (production-grade), tiêu biểu là hệ thống demo kit.

---

## 1. Mẫu Thiết kế Kỹ thuật (Technical Design Patterns)

### A. Modular Skill Loading Protocol (Conditional Loading)
*   **Bối cảnh**: Hệ thống Agent Kit có hàng chục kỹ năng khác nhau nhưng mỗi task của user chỉ cần dùng 1-2 kỹ năng.
*   **Giải pháp**: Thiết lập frontmatter `when_to_use` trong mỗi SKILL.md. Agent chỉ đọc/nạp kỹ năng khi context khớp với mô tả trigger của kỹ năng đó.
*   **Lợi ích**: Giảm 50-80% hao phí token, duy trì độ tập trung (attention budget) của mô hình.

### B. Core Protocol (Read → Understand → Apply)
*   **Bối cảnh**: Agent thường bỏ qua các chỉ dẫn quan trọng của skill/rules và thực thi trực tiếp (nhảy cóc).
*   **Giải pháp**: Thiết lập Rule bắt buộc (P0 - priority cao nhất). Yêu cầu agent phải:
    1.  Công bố (announce) kỹ năng/agent đang áp dụng trước khi trả lời.
    2.  Tự vấn 3 câu hỏi trước khi thực thi: Mục tiêu là gì? Nguyên lý cốt lõi nào cần áp dụng? Cách này khác biệt gì so với output chung chung?
*   **Ví dụ thông báo bắt buộc**: `🤖 Applying knowledge of @[agent-name]...` hoặc `📚 Using skill: @[skill-name]...`.

### C. Agent Boundary Enforcement
*   **Bối cảnh**: Trong hệ đa agent, các agent chuyên biệt thường lấn sân nhiệm vụ của nhau hoặc đùn đẩy trách nhiệm.
*   **Giải pháp**: Định nghĩa rõ phạm vi (scope) và danh sách các agent bị cấm (banned agents) trong từng ngữ cảnh. Ví dụ: Trong Agent Kit Viết sách, chỉ cho phép `book-researcher` đảm nhận khâu tra cứu, cấm `book-editor` tự ý sửa outline khi chưa có sự đồng ý.

---

## 2. Quy chuẩn Hợp đồng I/O & Manifest

### A. manifest.json & manifest.lock.json
*   Professional Kit cần có file manifest làm nguồn thông tin duy nhất (source of truth) đăng ký phiên bản, đường dẫn và các dependency của từng agent/skill/rule.
*   Hỗ trợ quản lý cập nhật đồng bộ thông qua các script tự động.

### B. Schema Validation
*   Định nghĩa sẵn các JSON contract schema (ví dụ: `manifest.schema.json`, `memory.schema.json`) để kiểm tra tính toàn vẹn cấu trúc thông qua script validation.

---

## 3. Các Bài học Tối ưu hóa (Optimization Levers)

### A. Tránh Giả lập Multi-Agent trong cùng 1 Context
*   **Bài học**: Việc cố tạo ra 5 "agent giả lập" chuyển tiếp việc cho nhau trong cùng 1 luồng trò chuyện đơn (như phiên bản cũ của meta-agentkit) làm tăng latency và lãng phí token vào phần role-playing vô ích.
*   **Giải pháp**: Thiết kế hệ thống dưới dạng **Single Agent - Multi Skills** (Một agent thông minh tải các module kỹ năng theo nhu cầu). Chỉ dùng luồng Multi-Agent thực sự khi có công cụ gọi Agent chuyên biệt độc lập (như native Agent Tool của Claude Code / Gemini API).

### B. Siết chặt DoD Nhị phân
*   **Bài học**: Mọi dòng DoD có tính từ cảm tính ("sạch sẽ", "chuyên nghiệp") đều bị các agent lách luật khi chịu áp lực tiến độ.
*   **Giải pháp**: Dịch chuyển toàn bộ sang DoD kiểm tra được bằng kiểm tra nhị phân (Ví dụ: "Không có file rỗng", "Biểu đồ có đầy đủ nhãn trục", "Output JSON parse được").

### C. CSS Transform + GSAP Animation Conflict
*   **Bối cảnh**: Agent Kit dựng animation HTML/JS (HyperFrames, GSAP). Agent tự do viết CSS `transform: translate()` rồi dùng GSAP `.to()` animate `x`/`y` → layout bị phá vì GSAP overwrite CSS transform matrix.
*   **Giải pháp**: 
    1. **Hard rule**: Không dùng `xPercent`/`yPercent` trong CSS — đây là GSAP-only properties, browser silently ignore.
    2. **Nguyên tắc vàng**: Nếu GSAP animate `x`/`y` trên element, element đó KHÔNG được có CSS `transform`.
    3. **Center pattern**: Dùng `tl.set(element, {xPercent: -50, yPercent: -50}, 0)` ở time 0 thay vì CSS centering.
    4. **Wrapper pattern**: Khi cần vừa center vừa complex motion, dùng wrapper div với `style="position:absolute; top:50%; left:50%"` và target div bên trong với `transform: translate(-50%, -50%)`.
    5. **Lưu trữ**: Ghi nhớ rule này vào AGENTS.md — không phụ thuộc agent tự khám phá.
*   **Lợi ích**: Loại bỏ 100% lỗi layout invisible, tiết kiệm nhiều lần re-render.

### D. Fixed Scene Type System cho Pipeline Kit
*   **Bối cảnh**: Kit pipeline cần sinh script động (video scene, slide deck, etc.) nhưng không có ràng buộc scene type → agent sinh ra cấu trúc tùy tiện, khó CSS hóa.
*   **Giải pháp**: Định nghĩa 5 scene type cố định đủ dùng (hero_title, text_card, callout, stat_card, closing). Mỗi type có visual + animation pattern riêng. Agent chỉ chọn từ danh sách này.
*   **Lợi ích**: CSS + JS animation viết 1 lần cho mỗi type, tái sử dụng cho mọi output. Agent không phải thiết kế visual từ đầu.

### E. Pipeline Stage I/O Contract
*   **Bối cảnh**: Kit pipeline nhiều stage (4-6 stage). Agent dễ skip stage hoặc truyền sai kiểu dữ liệu giữa các stage.
*   **Giải pháp**: Định nghĩa rõ Input → Output contract cho mỗi stage dạng dataclass/JSON schema. Stage sau chỉ nhận đúng type từ stage trước.
*   **Ví dụ**: 
    ```
    Brief (dataclass) → Script (6 Scenes) → Scene JSON → Voice (WAV segments) → HTML → MP4
    ```
*   **Lợi ích**: Mỗi stage độc lập, dễ test, dễ swap implementation (vd: đổi Piper TTS sang OpenAI TTS).

### F. Local-First Tool Integration (Platform Independence)
*   **Bối cảnh**: Kit cần tích hợp nhiều CLI tool (FFmpeg, TTS, render engine) nhưng mỗi OS có cách cài đặt và đường dẫn khác nhau.
*   **Giải pháp**: 
    1. Preflight check command để kiểm tra môi trường trước khi chạy pipeline.
    2. Auto-add tool paths vào session PATH (vd: hardcode WinGet path cho FFmpeg trên Windows).
    3. Windows-specific workaround cho UTF-8 pipe bug (Piper TTS: dùng temp file thay vì stdin pipe).
*   **Lợi ích**: User chạy 1 lệnh duy nhất — không mất thời gian debug môi trường.


### [2026-07-30 09:35] Selective Progressive Disclosure Pattern
- **Type**: `pattern`
- **Distilled At**: 2026-07-30 09:35

Only YAML headers are loaded by default to save token budget; full SKILL.md body is loaded on demand.
