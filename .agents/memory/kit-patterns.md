# Kit Design Patterns — Các khuôn mẫu thiết kế Agent Kit xuất sắc

Tổng hợp các khuôn mẫu thiết kế và kỹ thuật tối ưu hóa được đúc rút từ thực tiễn phát triển các Agent Kit sản xuất (production-grade), tiêu biểu là hệ thống demo kit.

---

## 1. Mẫu Thiết kế Kỹ thuật (Technical Design Patterns)

### A. Modular Skill Loading Protocol (Conditional Loading)
<!-- tags: skill, loading, token-saving, conditional, when_to_use, progressive-disclosure -->
*   **Bối cảnh**: Hệ thống Agent Kit có hàng chục kỹ năng khác nhau nhưng mỗi task của user chỉ cần dùng 1-2 kỹ năng.
*   **Giải pháp**: Thiết lập frontmatter `when_to_use` trong mỗi SKILL.md. Agent chỉ đọc/nạp kỹ năng khi context khớp với mô tả trigger của kỹ năng đó.
*   **Lợi ích**: Giảm 50-80% hao phí token, duy trì độ tập trung (attention budget) của mô hình.

### B. Core Protocol (Read → Understand → Apply)
<!-- tags: grounding, rule, P0, announce, self-check, discipline -->
*   **Bối cảnh**: Agent thường bỏ qua các chỉ dẫn quan trọng của skill/rules và thực thi trực tiếp (nhảy cóc).
*   **Giải pháp**: Thiết lập Rule bắt buộc (P0 - priority cao nhất). Yêu cầu agent phải:
    1.  Công bố (announce) kỹ năng/agent đang áp dụng trước khi trả lời.
    2.  Tự vấn 3 câu hỏi trước khi thực thi: Mục tiêu là gì? Nguyên lý cốt lõi nào cần áp dụng? Cách này khác biệt gì so với output chung chung?
*   **Ví dụ thông báo bắt buộc**: `🤖 Applying knowledge of @[agent-name]...` hoặc `📚 Using skill: @[skill-name]...`.

### C. Agent Boundary Enforcement
<!-- tags: multi-agent, suite, boundary, scope, ownership, delegation -->
*   **Bối cảnh**: Trong hệ đa agent, các agent chuyên biệt thường lấn sân nhiệm vụ của nhau hoặc đùn đẩy trách nhiệm.
*   **Giải pháp**: Định nghĩa rõ phạm vi (scope) và danh sách các agent bị cấm (banned agents) trong từng ngữ cảnh. Ví dụ: Trong Agent Kit Viết sách, chỉ cho phép `book-researcher` đảm nhận khâu tra cứu, cấm `book-editor` tự ý sửa outline khi chưa có sự đồng ý.

---

## 2. Quy chuẩn Hợp đồng I/O & Manifest

### A. manifest.json & manifest.lock.json
<!-- tags: manifest, versioning, ssot, registry, dependency -->
*   Professional Kit cần có file manifest làm nguồn thông tin duy nhất (source of truth) đăng ký phiên bản, đường dẫn và các dependency của từng agent/skill/rule.
*   Hỗ trợ quản lý cập nhật đồng bộ thông qua các script tự động.

### B. Schema Validation
<!-- tags: schema, json, validation, contract, integrity -->
*   Định nghĩa sẵn các JSON contract schema (ví dụ: `manifest.schema.json`, `memory.schema.json`) để kiểm tra tính toàn vẹn cấu trúc thông qua script validation.

---

## 3. Các Bài học Tối ưu hóa (Optimization Levers)

### A. Tránh Giả lập Multi-Agent trong cùng 1 Context
<!-- tags: multi-agent, single-agent, latency, token, architecture -->
*   **Bài học**: Việc cố tạo ra 5 "agent giả lập" chuyển tiếp việc cho nhau trong cùng 1 luồng trò chuyện đơn (như phiên bản cũ của meta-agentkit) làm tăng latency và lãng phí token vào phần role-playing vô ích.
*   **Giải pháp**: Thiết kế hệ thống dưới dạng **Single Agent - Multi Skills** (Một agent thông minh tải các module kỹ năng theo nhu cầu). Chỉ dùng luồng Multi-Agent thực sự khi có công cụ gọi Agent chuyên biệt độc lập (như native Agent Tool của Claude Code / Gemini API).

### B. Siết chặt DoD Nhị phân
<!-- tags: dod, binary, verification, quality, compliance -->
*   **Bài học**: Mọi dòng DoD có tính từ cảm tính ("sạch sẽ", "chuyên nghiệp") đều bị các agent lách luật khi chịu áp lực tiến độ.
*   **Giải pháp**: Dịch chuyển toàn bộ sang DoD kiểm tra được bằng kiểm tra nhị phân (Ví dụ: "Không có file rỗng", "Biểu đồ có đầy đủ nhãn trục", "Output JSON parse được").

### C. CSS Transform + GSAP Animation Conflict
<!-- tags: css, gsap, animation, html, visual, hyperframes -->
*   **Bối cảnh**: Agent Kit dựng animation HTML/JS (HyperFrames, GSAP). Agent tự do viết CSS `transform: translate()` rồi dùng GSAP `.to()` animate `x`/`y` → layout bị phá vì GSAP overwrite CSS transform matrix.
*   **Giải pháp**: 
    1. **Hard rule**: Không dùng `xPercent`/`yPercent` trong CSS — đây là GSAP-only properties, browser silently ignore.
    2. **Nguyên tắc vàng**: Nếu GSAP animate `x`/`y` trên element, element đó KHÔNG được có CSS `transform`.
    3. **Center pattern**: Dùng `tl.set(element, {xPercent: -50, yPercent: -50}, 0)` ở time 0 thay vì CSS centering.
    4. **Wrapper pattern**: Khi cần vừa center vừa complex motion, dùng wrapper div với `style="position:absolute; top:50%; left:50%"` và target div bên trong với `transform: translate(-50%, -50%)`.
    5. **Lưu trữ**: Ghi nhớ rule này vào AGENTS.md — không phụ thuộc agent tự khám phá.
*   **Lợi ích**: Loại bỏ 100% lỗi layout invisible, tiết kiệm nhiều lần re-render.

### D. Fixed Scene Type System cho Pipeline Kit
<!-- tags: pipeline, scene, video, css, component-library -->
*   **Bối cảnh**: Kit pipeline cần sinh script động (video scene, slide deck, etc.) nhưng không có ràng buộc scene type → agent sinh ra cấu trúc tùy tiện, khó CSS hóa.
*   **Giải pháp**: Định nghĩa 5 scene type cố định đủ dùng (hero_title, text_card, callout, stat_card, closing). Mỗi type có visual + animation pattern riêng. Agent chỉ chọn từ danh sách này.
*   **Lợi ích**: CSS + JS animation viết 1 lần cho mỗi type, tái sử dụng cho mọi output. Agent không phải thiết kế visual từ đầu.

### E. Pipeline Stage I/O Contract
<!-- tags: pipeline, io-contract, stage, dataclass, typing -->
*   **Bối cảnh**: Kit pipeline nhiều stage (4-6 stage). Agent dễ skip stage hoặc truyền sai kiểu dữ liệu giữa các stage.
*   **Giải pháp**: Định nghĩa rõ Input → Output contract cho mỗi stage dạng dataclass/JSON schema. Stage sau chỉ nhận đúng type từ stage trước.
*   **Ví dụ**: 
    ```
    Brief (dataclass) → Script (6 Scenes) → Scene JSON → Voice (WAV segments) → HTML → MP4
    ```
*   **Lợi ích**: Mỗi stage độc lập, dễ test, dễ swap implementation (vd: đổi Piper TTS sang OpenAI TTS).

### F. Local-First Tool Integration (Platform Independence)
<!-- tags: cli, platform, ffmpeg, tts, preflight, windows -->
*   **Bối cảnh**: Kit cần tích hợp nhiều CLI tool (FFmpeg, TTS, render engine) nhưng mỗi OS có cách cài đặt và đường dẫn khác nhau.
*   **Giải pháp**: 
    1. Preflight check command để kiểm tra môi trường trước khi chạy pipeline.
    2. Auto-add tool paths vào session PATH (vd: hardcode WinGet path cho FFmpeg trên Windows).
    3. Windows-specific workaround cho UTF-8 pipe bug (Piper TTS: dùng temp file thay vì stdin pipe).
*   **Lợi ích**: User chạy 1 lệnh duy nhất — không mất thời gian debug môi trường.


### G. Canonical File Architecture & Registry-First Retrieval
<!-- tags: file-registry, path, naming, reuse, organization -->
*   **Bối cảnh**: Agent tạo file phân tán, trùng lặp, tự phát minh tên thư mục trong lúc chạy workflow và khó tìm lại tài sản cũ.
*   **Giải pháp**: 
    1. Thiết lập hệ thống thư mục đánh số theo chặng (`00_control/`, `01_discovery/`, `02_genesis/`, `03_architecture/`, `04_blueprints/`, `05_chapters/`, `06_book_audit/`, `07_publish/`).
    2. Quản lý canonical path templates qua `file_registry.json`.
    3. Tra cứu qua `path_resolver.py` (Registry First, Scoped Fallback Search).
    4. Áp dụng bất biến `REUSE BEFORE CREATE`.
*   **Lợi ích**: 100% tài sản có đúng 1 vị trí chính thức, zero orphan files, dễ dàng duyệt file trên IDE.

### H. Parametric SVG Subsystem vs Markdown Slop
<!-- tags: svg, diagram, visual, rendering, print -->
*   **Bối cảnh**: LLM thường tự ý vẽ sơ đồ bằng code block (Mermaid, ASCII art, text boxes thô) xen giữa bản thảo văn chương gây vỡ bố cục in ấn.
*   **Giải pháp**: 
    1. Cấm Writer tự vẽ trực quan trong prose manuscript.
    2. Visual subsystem: `visual-architect` sinh Spec JSON ngắn gọn $\rightarrow$ Gọi script Python `render_diagram.py` kết xuất SVG vector $\rightarrow$ Kiểm định 5 tiêu chuẩn qua `qa_diagram.py` (Zero Overflow, Contrast $\ge 4.5:1$, Valid XML).
*   **Lợi ích**: Sơ đồ sắc nét, chuẩn in ấn xuất bản, tiết kiệm hàng nghìn token mô tả geometry SVG trong context.

### I. 3-Tier Architectural Decoupling & Blueprint Barrier
<!-- tags: architecture, decoupling, barrier, phase-gate, blueprint -->
*   **Bối cảnh**: Agent có xu hướng "nhảy cóc" vừa lập đề cương vừa tiện tay viết luôn bản thảo chương, dẫn đến hiệu ứng domino đập đi viết lại khi thay đổi móng toàn sách.
*   **Giải pháp**: 
    1. Tách hẳn thành 3 tầng độc lập: Kiến trúc (`/book-architecture`) $\rightarrow$ Khung móng toàn sách (`/book-blueprint`) $\rightarrow$ Sản xuất bản thảo (`/chapter-production`).
    2. Bất biến `ZERO PROSE DRAFTING` trong `book-blueprint.md`.
    3. Bất biến `BLUEPRINT-FIRST BARRIER`: Chặn drafting cho đến khi toàn bộ móng qua `[CP_ALL_BLUEPRINTS_GATE]`.
*   **Lợi ích**: Bảo vệ tính toàn vẹn tư tưởng toàn thư, chống vỡ mạch logic giữa các chương.

### J. "Teach Before You Police" Formatting & Quality Architecture
<!-- tags: formatting, quality, linter, writing, teach -->
*   **Bối cảnh**: Đẩy toàn bộ luật cấm đoán formatting vào prompt hoặc linter biến hệ thống thành "máy chém văn phong" làm nghẽn mạch sáng tạo.
*   **Giải pháp**: 
    1. Dạy kỹ thuật viết và layout chuẩn xuất bản (Headings `#`/`##`, Whitespace `\n\n`, Bolding trên Key Concepts, List chỉ cho công cụ 24h) ngay từ đầu trong Writing Skill.
    2. Phân định rạch ròi: `clutter_checker.py` chỉ bắt lỗi cơ học khách quan (gạch `---`, code block rác, cú pháp lỗi); `developmental-editor` đánh giá phong cách trong ngữ cảnh (AI-slop, nhịp thở câu chữ, cognitive drag).
*   **Lợi ích**: Bản thảo sinh ra đã là Format-Conforming Draft, giảm 95% công sức biên tập hậu kỳ.

### K. Autonomous Natural Language Intent & State Routing
<!-- tags: routing, intent, natural-language, state-machine, slash-command -->
*   **Bối cảnh**: Hệ thống Agent Suite chỉ chạy khi người dùng gõ đúng slash command `/command`, không biết tự xử lý khi người dùng trò chuyện tự nhiên.
*   **Giải pháp**: Xây dựng `state_router.py` phân giải prompt tự nhiên $\rightarrow$ Xác định Intent $\rightarrow$ Đọc `00_control/book_state.json` $\rightarrow$ Kiểm tra rào chắn Barrier $\rightarrow$ Kích hoạt đúng Workflow $\rightarrow$ Nạp đúng Specialist Agent và JIT Grounding Bundle (1-2 skills tối giản).
*   **Lợi ích**: Người dùng trò chuyện tự nhiên mà hệ thống vẫn vận hành chính xác 100% như một cỗ máy tự động thông minh.

---

### [2026-07-30 09:35] Selective Progressive Disclosure Pattern
<!-- tags: progressive-disclosure, token-saving, yaml, header, lazy-loading -->
- **Type**: `pattern`
- **Distilled At**: 2026-07-30 09:35

Only YAML headers are loaded by default to save token budget; full SKILL.md body is loaded on demand.

---

### L. Evolutionary Refactoring Pattern
<!-- tags: refactor, evolution, orchestration, progressive-disclosure, ergonomic --> (Bảo Tồn Domain Nền + Nâng Cấp 4 Lớp Hạ Tầng)
*   **Bối cảnh**: Khi một Agent Kit lớn (như Writing Book Agent V2) đã hoạt động tốt ở các năng lực nghiệp vụ (domain skills, role models, dự án sandbox) nhưng gặp ma sát về điều phối monolithic, nhồi nhét context, linter tự tiện sửa văn phong hoặc ma sát phê duyệt nghi lễ.
*   **Giải pháp (Công thức SSOT)**:
    $$\text{V}_{\text{Next}} = \text{V}_{\text{Base}}\text{ (Core Domain)} + \text{Refactor Orchestration} + \text{Progressive Disclosure} + \text{Preventive Quality} + \text{Ergonomic HITL}$$
    1. **Giữ nguyên 100% Core Domain**: Không rewrite các kỹ năng và dữ liệu đã chứng minh hiệu quả.
    2. **Xé nhỏ Workflow (Goldilocks)**: Chuyển pipeline nguyên khối thành các workflow độc lập, hỗ trợ chạy lẻ từng khâu.
    3. **Progressive Disclosure Scoped Context**: Whitelist 1:1 theo từng artifact, chặn rò rỉ context.
    4. **Preventive Quality & Voice-Safe Mechanical Repair**: Shift-left ngăn lỗi sớm, auto-repair chỉ sửa lỗi cơ học tất định, cấm làm biến dạng giọng văn tác giả.
    5. **Ergonomic Human-in-the-Loop**: Tự động hóa việc cơ học, thay thế cổng nghi lễ bằng chính sách linh hoạt (`chapter_approval_policy`), chỉ dừng lại ở các quyết định chiến lược.
*   **Lợi ích**: Bảo vệ 100% tài sản tri thức cũ, loại bỏ rủi ro regression, tăng gấp đôi tính linh hoạt và cắt giảm 70% ma sát cho người dùng.

