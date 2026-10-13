---
name: create-visual
description: Quy trình sản xuất UI/UX Visual Kit, Interactive Preview, Dashboard, Landing Page và Design System chuẩn chất lượng cao từ UI/UX Pro Max.
version: 1.0.0
requires_agents: [kit-architect]
requires_skills: [ui-ux-pro-max, kit-verifying]
artifact_outputs: [design-system, visual-kit-html, visual-qa-report]
topology: chaining
trigger: manual
permissions: read-write
tools_allowed: [Read, Write, Edit, Glob, Grep, Bash]
safe_outputs:
  create_visual_artifacts: "Mọi file visual mới ghi vào ./output/<kit-name>/visuals/ hoặc thư mục dự án chỉ định"
max_retry_per_node: 2
recovery:
  idempotent: true
  resume_from_last_valid_state: true
  prevent_duplicate_artifacts: true
  prevent_infinite_handoff: true
---

# 🔄 MASTER FLOW: /create-visual (UI/UX Visual Kit Creation)

> **Mục tiêu**: Chuyển hóa yêu cầu giao diện thô từ người dùng thành thành phẩm Visual Kit / HTML Preview hoàn chỉnh, có chủ đích thiết kế (intentional design), phân cấp thị giác rõ ràng, bảng màu và typography đồng bộ, đạt chuẩn accessibility WCAG 2.1 AA và triệt tiêu toàn bộ AI aesthetic anti-patterns.

---

## 🏛️ 1. GOVERNANCE LAYER (HÀNG RÀO PHÁP LÝ & AN TOÀN)

1. **No Design Grounding $\rightarrow$ No HTML Generation**: Tuyệt đối không sinh mã HTML/CSS tự do từ trí nhớ. Mọi quyết định màu sắc, font chữ, bố cục và hiệu ứng BẮT BUỘC phải grounding qua công cụ tìm kiếm `ui-ux-pro-max/scripts/search.py`.
2. **Zero AI Cliche Policy**: Cấm triệt để việc dùng emoji làm icon, cấm dùng màu tím/hồng default (AI gradient), cấm tương phản yếu (gray-on-gray) và cấm các nút bấm thiếu tương tác (hover/active/focus).
3. **Focused State Design**: 4 State Nodes nghiệp vụ và 1 Deliverable Human Gate để đảm bảo tốc độ và sự liền mạch trong luồng suy luận.
4. **Self-Contained & Instant Preview**: Visual output mặc định là Single-File HTML hoặc cấu trúc module rõ ràng, sẵn sàng mở trực tiếp trên trình duyệt mà không yêu cầu build step phức tạp.

---

## 🏗️ 2. ORCHESTRATION LAYER (ĐIỀU HƯỚNG TRẠNG THÁI)

### 2.1. Shared State Schema
```json
{
  "workflow_state": {
    "session_id": "string",
    "current_state": "DESIGN_REASONING | DESIGN_SYSTEM_SPEC | VISUAL_IMPLEMENTATION | VISUAL_QA_AND_DELIVERY",
    "design_tokens": {
      "style": "string",
      "palette": "object",
      "typography": "object",
      "effects": "array",
      "anti_patterns": "array"
    },
    "artifacts": {
      "design_system_file": "string",
      "html_file": "string",
      "qa_report_file": "string"
    },
    "status": "pending | in_progress | needs_human_review | completed"
  }
}
```

### 2.2. Evidence-Gated Transition Matrix
| Current State | Target State | Required Evidence / Artifact | Transition Assertion Guard | Allowed Epistemic Status | Remediation Path (On Fail) | Max Retries |
|:---|:---|:---|:---|:---|:---|:---|
| `INIT` | `DESIGN_REASONING` | `user_prompt` | `prompt.length > 5` | `[CONFIRMED]` | Clarify requirements with user | 1 |
| `DESIGN_REASONING` | `DESIGN_SYSTEM_SPEC` | `search_results.json` / Design Tokens | `tokens.has_palette && tokens.has_typography` | `[CONFIRMED]` | Re-run search with adjusted keywords | 2 |
| `DESIGN_SYSTEM_SPEC` | `VISUAL_IMPLEMENTATION`| `design-system/MASTER.md` or Tokens block | `tokens.contrast_verified == true` | `[CONFIRMED]` | Adjust color contrast for WCAG AA | 2 |
| `VISUAL_IMPLEMENTATION`| `[GATE: DESIGN_APPROVAL]`| `index.html` / Visual file | `html.has_viewport && html.no_emojis_as_icons` | `[CONFIRMED]` | Fix HTML structure / inject SVGs | 2 |
| `[GATE: DESIGN_APPROVAL]`| `COMPLETED` | `user_approval` | `verdict == "APPROVE"` | `[CONFIRMED]` | Refine via user feedback | — |

---

## 🔄 3. INTELLIGENCE LAYER & NODE EXECUTION

### [STATE: DESIGN_REASONING]
- **Responsible Agent / Role**: `kit-architect` (`@designer`) | Skill: `ui-ux-pro-max`
- **Input**: Yêu cầu người dùng (Product type, target audience, style keywords).
- **Output Artifacts**: Trích xuất Design System Tokens từ `search.py`.

- **⚡ Action Prompts & Execution Steps**:
  1. **Bóc tách Domain & Product Context**: Xác định sản phẩm thuộc nhóm nào (SaaS Dashboard, Fintech, E-Commerce, Developer Tool, Landing Page, Healthcare...).
  2. **Chạy Trí tuệ Thiết kế UI/UX Pro Max**:
     ```bash
     python .agents/skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system -p "<Project Name>"
     ```
  3. **Tra cứu Bổ trợ (nếu cần)**:
     - Animation presets: `python .agents/skills/ui-ux-pro-max/scripts/search.py "<query>" --domain gsap`
     - Stack-specific patterns: `python .agents/skills/ui-ux-pro-max/scripts/search.py "<query>" --stack html-tailwind`
  4. **Tóm tắt Lựa chọn**: Trình bày ngắn gọn 1 Style chủ đạo, 1 Font pairing chính thức, 1 Bảng màu tương phản cao và 3 điều cần tránh (Anti-patterns).

- **Definition of Done (DoD)**:
  - [ ] Đã chạy `search.py` và nhận kết quả Design System thực tế.
  - [ ] Xác định rõ Primary, Secondary, Accent, Background, Card, Foreground và Google Fonts pairing.
  - [ ] Liệt kê ít nhất 2 anti-patterns cần chủ động phòng tránh.

---

### [STATE: DESIGN_SYSTEM_SPEC]
- **Responsible Agent / Role**: `kit-architect` (`@designer`) | Skill: `ui-ux-pro-max`
- **Input**: Design System Tokens từ State trước.
- **Output Artifacts**: `design-system/MASTER.md` hoặc khối CSS Custom Properties `:root`.

- **⚡ Action Prompts & Execution Steps**:
  1. **Khởi tạo Master Design System**:
     - Định nghĩa biến CSS / Tailwind config đầy đủ:
       - Colors: `--color-primary`, `--color-secondary`, `--color-accent`, `--color-background`, `--color-card`, `--color-foreground`, `--color-border`, `--color-muted`.
       - Typography: Display font (Google Fonts URL), Body font, Base size (16px), Line-height scale (1.2, 1.4, 1.6).
       - Spatial Grid: 4px/8px scale (`--space-1: 4px`, `--space-2: 8px`, `--space-4: 16px`, `--space-6: 24px`, `--space-8: 32px`).
       - Elevation & Radius: Box shadows, border-radius tokens (`--radius-sm: 6px`, `--radius-md: 10px`, `--radius-lg: 16px`).
  2. **Kiểm tra Độ tương phản (Contrast Gate)**:
     - Đảm bảo text trên background đạt tỉ lệ tương phản $\ge 4.5:1$ (WCAG AA).
     - Đảm bảo UI controls/borders đạt $\ge 3:1$.

- **Definition of Done (DoD)**:
  - [ ] Bộ token hoàn chỉnh không chứa giá trị placeholder `TBD`.
  - [ ] Đạt chuẩn tương phản màu sắc theo khuyến nghị của `ui-ux-pro-max`.

---

### [STATE: VISUAL_IMPLEMENTATION]
- **Responsible Agent / Role**: `kit-architect` (`@designer`) | Skill: `ui-ux-pro-max`
- **Input**: `design-system/MASTER.md` + Cấu trúc trang yêu cầu.
- **Output Artifacts**: File HTML trực quan (ví dụ: `<target-dir>/visuals/index.html` hoặc `preview.html` tại thư mục chỉ định, mặc định `./output/<kit-name>/visuals/`).

- **⚡ Action Prompts & Execution Steps**:
  1. **Cấu trúc HTML Semantic**:
     - Khai báo đầy đủ `<meta name="viewport" content="width=device-width, initial-scale=1.0">`.
     - Import Google Fonts hợp lệ ở `<head>`.
     - Tích hợp Tailwind CSS CDN hoặc Vanilla CSS tokens `:root`.
  2. **Xây dựng Bố cục & Phân cấp Trực quan (Visual Hierarchy)**:
     - Hero / Top Header / Navigation với logo và CTA rõ ràng.
     - Section nội dung sử dụng Bento Grid, Flexbox hoặc CSS Grid linh hoạt.
     - Cards, Data Tables, Stats Widgets với khoảng cách thở (whitespace) cân đối.
  3. **Tích hợp Tương tác & Micro-interactions**:
     - Tất cả phần tử click được (`button`, `a`) đều có `cursor: pointer` và hiệu ứng hover/active (150-250ms ease).
     - Focus ring rõ nét cho bàn phím (`focus:ring-2 focus:ring-offset-2`).
     - Dark/Light mode toggle (nếu là dashboard/app UI).
  4. **Iconography chuẩn SVG**:
     - Sử dụng inline SVG (Heroicons / Lucide), tuyệt đối không dùng emoji thay thế icon.

- **Definition of Done (DoD)**:
  - [ ] File HTML self-contained, mở được ngay trên trình duyệt mà không bị lỗi layout.
  - [ ] 100% icon là vector SVG, 0 emoji dùng làm icon.
  - [ ] Responsive mượt mà trên các kích thước 375px (Mobile), 768px (Tablet), 1024px (Desktop), 1440px (Wide).

---

### [STATE: VISUAL_QA_AND_DELIVERY]
- **Responsible Agent / Role**: `kit-architect` (`@auditor` / `@designer`) | Skill: `ui-ux-pro-max`, `kit-verifying`
- **Input**: File HTML đã tạo.
- **Output Artifacts**: `visual_qa_report.json`, Bàn giao file kèm Tóm tắt Trực quan cho người dùng.
- **Lifecycle & Evidence Integration**:
  - Ghi nhận `visual_qa_report.json` vào `verdicts.visual_qa` trong `lifecycle.json`.
  - Chuyển `lifecycle_state: "READY_FOR_VALIDATION"`, thiết lập `handoff.target_workflow: "validate-kit"` và `evidence_refs: ["visual_qa_report.json", "index.html"]`.

- **⚡ Action Prompts & Execution Steps**:
  1. **Đối chiếu Pre-Delivery Checklist & Xuất Bằng Chứng `visual_qa_report.json`**:
     - [ ] Không có emoji làm icon.
     - [ ] Mọi element clickable đều có pointer cursor và hover state.
     - [ ] Text contrast $\ge 4.5:1$ (WCAG AA).
     - [ ] Viewport meta và responsive layout hợp lệ.
     - [ ] Không có hiện tượng vỡ layout hoặc thanh cuộn ngang ngoài ý muốn (horizontal overflow).
  2. **Bàn giao Thành phẩm**:
     - Cung cấp đường dẫn file dạng `file:///...`.
     - Hướng dẫn mở và kiểm tra trực quan trong trình duyệt.

- **Definition of Done (DoD)**:
  - [ ] `visual_qa_report.json` được tạo đầy đủ với 100% tiêu chí Pass.
  - [ ] `lifecycle.json` được cập nhật trạng thái `READY_FOR_VALIDATION`.
  - [ ] Bàn giao link file chính xác cho người dùng.

---

## 🛑 4. FIRST-CLASS HUMAN GATES

| Gate ID | Vị Trí Kích Hoạt | Đầu Vào Thẩm Định | Quyền Quyết Định | Hành Động Khi APPROVE | Hành Động Khi REVISE / REJECT |
|:---|:---|:---|:---|:---|:---|
| `[GATE: DESIGN_APPROVAL]` | Sau `VISUAL_QA_AND_DELIVERY` | File HTML Visual Kit + Tóm tắt Token | Người dùng / Sếp (`[ESCALATE_HUMAN]`) | Hoàn tất & chuyển sang bước tích hợp tiếp theo | Tinh chỉnh style/palette/layout theo yêu cầu cụ thể |
