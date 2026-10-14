# Dynamic Role Profiles Reference

Khi xử lý các giai đoạn chuyên sâu, chuyển đổi ngữ cảnh tư duy theo 5 profiles (On-Demand):

### 🔍 `@analyst` (Domain & Risk Analysis Profile)

*Kích hoạt khi: Cần bóc tách domain, tìm core verbs, failure modes, mô hình hóa rủi ro và đòn bẩy 80/20.*

- Đọc `references/verification-abstraction.md` & `references/workflow-topologies.md`.
- Xác định 5-10 **Core Verbs** (Precision vs Creativity, Knowledge, Failure Severity).
- Mô hình hóa **4 Chiều Rủi Ro (Risk Profiling)**: Omission Risk, Arithmetic Risk, Mutation Risk, Visual Risk $\rightarrow$ Ánh xạ sang 5 Verification Archetypes.
- Phân tích **3 câu hỏi đòn bẩy**: Outcome quan trọng nhất? Điểm thất vọng phổ biến? Đòn bẩy $ROI \ge 1.25$?

### ✍️ `@compiler` (Prompt Engineering Profile)

*Kích hoạt khi: Biên dịch System Prompt và đặc tả tiêu chí hoàn thành.*

- **Targeted Template**: Đọc `templates/agent-template.md` (Specialist) hoặc `templates/orchestrator-template.md` (Master Orchestrator).
- Thiết lập khung System Prompt 4 khối: Vai trò & Outcome, Quy trình & Ma trận, Hard Constraints, Format đầu ra.
- Chuẩn hóa **Worker Briefing Protocol**: Bắt buộc nhúng quy tắc 5 phần và "Never Delegate Understanding".
- Nhúng **Deterministic Arithmetic Guardrail** cho domain định lượng (ép gọi script tính toán).
- Nhúng **Negative Completeness Matrix** cho domain audit/legal/compliance (đối chiếu danh mục bắt buộc).
- Chuẩn hóa **Binary Definition of Done (DoD)**: 100% nhị phân, đo lường được, 0 tính từ mơ hồ.

### 📐 `@architect` (Skill & System Architecture Profile)

*Kích hoạt khi: Cần thiết kế cấu trúc thư mục skill, workflow, memory schema, platform contract.*

- **Mandatory Precondition Gate for Skills**: Khi tạo hoặc sửa bất kỳ Skill nào (`skills/<name>/SKILL.md`), BẮT BUỘC phải nạp / kích hoạt skill `skill-creator` (`.agents/skills/skill-creator/SKILL.md`) TRƯỚC TIÊN cùng với `templates/skill-template.md`.
- **Targeted Templates**: 
  - Workflow $\rightarrow$ `templates/workflow-template.md` (5-Part Node Anatomy + Transactional Mutation nếu có đột biến).
  - Skill $\rightarrow$ `templates/skill-template.md` (kết hợp `skill-creator` và `when_to_use`).
  - Memory $\rightarrow$ `templates/memory-template.md`.
  - Checklist $\rightarrow$ `templates/domain-checklist-template.py`.
- Áp dụng **Progressive Disclosure**: Metadata (~100 từ) → Body (< 500 dòng) → References (on-demand).

### 🎨 `@designer` (Visual & UX/UI Design Profile)

*Kích hoạt khi: Cần thiết kế, xây dựng giao diện, visual kits, interactive previews, design systems, dashboards, landing pages, slides.*

- **Targeted Intelligence**: Kích hoạt `ui-ux-pro-max` để truy vấn design system & quy tắc UX chuyên sâu.
- **DESIGN.md Hard Gate**: Sinh file `DESIGN.md` chứa YAML Design Tokens làm SSOT trước khi code UI.
- **Visual Output Delivery**: Sinh file HTML self-contained, SVG icons, micro-interactions, dark/light mode toggle.
- **Visual QA**: Rà soát Pre-Delivery Checklist và tuân thủ Purple Ban.

### 🛡️ `@auditor` (Quality & Verification Profile)

*Kích hoạt khi: Đánh giá chất lượng kit đầu ra.*

- **L0 Self-Healing**: Kích hoạt Convergence Engine (`validate_kit.py --converge`) tự sửa lỗi deterministic.
- **L1 Structural Check & Anchor Gate**: Kích hoạt `validate_kit.py` kiểm tra toàn vẹn cấu trúc, frontmatter, và **Structural Anchors** bắt buộc (Anthropic Skill Creator examples & triggers, Workflow 5-Part Node Anatomy, Agent core blocks & Worker Briefing, Memory topics).
- **L2 Verification Abstraction & Scenario Test**: Xác thực `scripts/checklist.py` khớp với Risk Profile của domain; chạy `eval_runner.py --regression` bảo đảm không suy thoái 5 domain chuẩn.
- **L3 Adversarial Stress Test**: Thử phá prompt bằng edge cases, kiểm tra kẽ hở DoD.
