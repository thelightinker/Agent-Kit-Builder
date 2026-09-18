# Golden Example: Writing Book Agent V2 (Full Non-Fiction Suite)

- **Kit Name**: `writing-book-agent-v2`
- **Kit Type**: Full Suite (Master Orchestrator + 6 Specialist Agents + 17 Skills + 6 Workflows + Visual SVG Engine)
- **Quality Score**: 5/5 ⭐ (EXEMPLARY - Production Ready)
- **Domain**: Sáng tác sách Non-Fiction Bestseller 10/10

---

## 🏛️ 1. Cấu Trúc Tổng Thể

```text
writing-book-agent-v2/
├── .agents/
│   ├── agent/
│   │   ├── master-orchestrator.md    (Runtime State Router & Sentinel)
│   │   ├── thesis-architect.md       (Big Idea, 3-Level TOC & Book Spine)
│   │   ├── transformation-writer.md  (6-Stage Hypnotic Prose Crafting)
│   │   ├── visual-architect.md       (Diagram Spec, SVG Engine, Visual QA)
│   │   ├── developmental-editor.md   (7 Quality Tests & Structural Surgery)
│   │   ├── intellectual-red-team.md  (Falsification, Steelmanning, Kill Power)
│   │   └── investigative-researcher.md (Story Bank & Deep Evidence)
│   ├── workflows/
│   │   ├── book-discovery.md         (/book-discovery: Author Assets & Stories)
│   │   ├── book-genesis.md           (/book-genesis: Cover Promise, Title & Arc)
│   │   ├── book-architecture.md      (/book-architecture: 3-Level TOC Spine)
│   │   ├── book-blueprint.md         (/book-blueprint: Macro Blueprint & Cross-QA)
│   │   ├── chapter-production.md     (/chapter-production: Drafting, SVG & 4-Pass QA)
│   │   └── book-audit-publish.md     (/book-audit-publish: 10/10 Audit & Typeset)
│   ├── schemas/
│   │   ├── file_registry.json        (Canonical path templates SSOT)
│   │   └── diagram_spec.schema.json  (JSON schema for 6 SVG Archetypes)
│   ├── scripts/
│   │   ├── render_diagram.py         (Parametric SVG rendering engine)
│   │   ├── qa_diagram.py             (5-point SVG visual validator)
│   │   ├── path_resolver.py          (Registry-First path resolver with fallback search)
│   │   └── state_router.py           (Autonomous Natural Language Intent & State Router)
│   ├── rules/
│   │   ├── constitutional-core.md    (11 Invariants: Blueprint-First, Canonical Home, Reuse)
│   │   └── collaboration-protocol.md (Grounding Bundles, Truthful Status HUD)
│   └── manifest.json
└── books/<book-slug>/
    ├── 00_control/       (book_state.json, decisions.json, active_manifest.json)
    ├── 01_discovery/     (author_assets.json, story_bank.json)
    ├── 02_genesis/       (cover_promise.md, book_positioning.md, title_decision.md, book_arc.md)
    ├── 03_architecture/  (toc_level_1.md, toc_level_2.md, full_3_level_toc.md)
    ├── 04_blueprints/    (cross_chapter_blueprint_audit.md, chapters/ch_XX/blueprint.md)
    ├── 05_chapters/      (ch_XX/draft.md, ch_XX/visuals/, ch_XX/audit/)
    ├── 06_book_audit/    (compilation_report.json, structural_audit.md, final_verdict.md)
    └── 07_publish/       (manuscript.md, release_manifest.json)
```

---

## 💎 2. Các Đột Phá Kiến Trúc Tiêu Biểu

1. **Phân Tầng 3 Nấc Tinh Khiết (Architecture $\rightarrow$ Blueprint $\rightarrow$ Production)**:
   - Tách riêng `book-blueprint.md` (Bất biến `ZERO PROSE DRAFTING`) khỏi `chapter-production.md`.
   - Khóa chặt `BLUEPRINT-FIRST BARRIER`: Cấm tuyệt đối draft khi toàn bộ móng sách chưa qua `[CP_ALL_BLUEPRINTS_GATE]`.
2. **Visual SVG Subsystem vs Markdown Slop**:
   - Loại bỏ hoàn toàn sơ đồ bằng ASCII art, code block hoặc Mermaid trong bản thảo.
   - Sử dụng mô hình `Diagram Spec JSON → render_diagram.py → qa_diagram.py` xuất 100% SVG vector chuẩn in ấn.
3. **Triết Lý "Teach Before You Police"**:
   - `prose-cadence-mastery` hướng dẫn viết đúng và format chuẩn xuất bản ngay từ nét bút đầu tiên.
   - `clutter_checker.py` chỉ quét lỗi cơ học máy tính khách quan; `developmental-editor` đánh giá ngữ cảnh nghệ thuật.
4. **Canonical File Architecture & Retrieval Layer**:
   - Cấu trúc 8 thư mục đánh số `00_` $\rightarrow$ `07_` khớp 1:1 với các Workflow.
   - Phân giải đường dẫn qua `file_registry.json` + `path_resolver.py` theo quy tắc `REUSE BEFORE CREATE`.
5. **Autonomous Natural Language Intent & State Router**:
   - `state_router.py` phân giải prompt tự nhiên của người dùng, đọc `book_state.json`, kích hoạt đúng workflow và nạp JIT Grounding Bundle tối giản.
