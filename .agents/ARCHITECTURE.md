# AG Kit Architecture — Agent Kit Creator

> Comprehensive AI Agent Kit Creation, Refactoring, & Validation Suite — 2026.8.24 (v2.1.0 Evolvable Architecture)

---

## 📋 Overview

Agent Kit Creator là hệ thống chuyên gia tinh gọn gồm:

- **1 Orchestrator Agent** (`kit-architect`) với 5 Dynamic Role Profiles (`@analyst`, `@compiler`, `@architect`, `@designer`, `@auditor`).
- **10 Focused Skills** - Bộ kỹ năng chuyên sâu phục vụ phân tích domain, biên dịch prompt, cấu trúc skill, nén context phiên dài, lắp ráp, kiểm định, xuất bản và tiến hóa kit.
- **8 Workflows** - Các quy trình slash command (`/create-kit`, `/refactor-kit`, `/validate-kit`, `/remember-kit`, `/architecture-evolution`, `/create-visual`, `/copy-kit`, `/evolve-kit`).
- **3 Core Rules** - Ràng buộc bất biến (`core-guardrails`), phân loại mode (`dynamic-routing`), và giao thức cộng tác & nạp quyền hạn (`collaboration-protocol`).

---

## 🔐 Managed Component Registry (2026.8.24)

Hệ thống quản lý phiên bản:
- Toolkit releases giữ **CalVer** trong `VERSION` (`YYYY.M.D`).
- Agent, skills, workflows, và rules sử dụng **SemVer** trong frontmatter.
- `manifest.json` ghi nhận đường dẫn, phiên bản, công cụ và phụ thuộc.
- `DEPENDENCY_GRAPH.md` được tự động sinh từ registry.

Đồng bộ registry bằng các lệnh:
```bash
python .agents/scripts/generate_manifest.py
python .agents/scripts/dependency_graph.py
python .agents/scripts/validate_kit.py
```

---

## 🏗️ Directory Structure

```plaintext
.agents/
├── README.md                # Quick start và hướng dẫn vận hành
├── ARCHITECTURE.md          # Kiến trúc hệ thống và danh mục cấu phần
├── CHANGELOG.md             # Lịch sử cập nhật
├── VERSION                  # Phiên bản CalVer
├── manifest.json            # Bộ đăng ký phiên bản cấu phần
├── DEPENDENCY_GRAPH.md      # Sơ đồ phụ thuộc Workflow → Agent → Skill
├── schemas/                 # JSON schema contracts
├── agent/                   # 1 Orchestrator Agent (kit-architect.md)
├── skills/                  # 10 Focused Skills
├── workflows/               # 8 Slash Command Workflows
├── rules/                   # 3 Core Rules
├── templates/               # Component, Contract & Workflow Templates
├── references/              # Deep Reference Docs & Domain Guides
├── memory/                  # Persistent Memory (MEMORY.md index & topic files)
└── scripts/                 # Validation, Eval & Export Scripts
```

---

## 🤖 Agents (1)

| Agent | Focus | Skills Used |
|---|---|---|
| `kit-architect` | Orchestrator duy nhất điều phối toàn bộ pipeline với 5 Role Profiles (`@analyst`, `@compiler`, `@architect`, `@designer`, `@auditor`) | architecture-mapping, context-compression, domain-profiling, prompt-compiling, skill-architecting, kit-assembling, kit-verifying, kit-exporting, kit-evolving, ui-ux-pro-max |

---

## 🧩 Skills (10)

Bộ kỹ năng chuyên môn phân cấp theo Progressive Disclosure.

| Skill | Description |
|---|---|
| `domain-profiling` | Phân tích Core Verbs, 80/20 leverage points, failure modes, tier classification |
| `prompt-compiling` | Biên dịch System Prompt 4 khối, Worker Briefing, binary DoD, negative constraints |
| `skill-architecting` | Thiết kế cấu trúc thư mục skill, conditional loading when_to_use, progressive disclosure |
| `context-compression` | Quản lý và nén ngữ cảnh 3 cấp độ (Micro-compact, Phase summary, Session checkpoint) |
| `kit-assembling` | Đóng gói Agent Kit vào `./output/<kit-name>/`, sinh antigravity.json, checklist, manifest.json |
| `kit-verifying` | Kiểm định 3 lớp, Verification by Execution, Worker Briefing checks & Rubric 5 sao |
| `kit-exporting` | Đóng gói Antigravity Plugin bundle, Cursor, Claude Desktop, OpenAI Custom GPTs |
| `kit-evolving` | Phân tích Gap Analysis, Delta Patch, Auto-Skillify heuristics, Anti-Overengineering |
| `architecture-mapping` | Khảo sát & Định vị Bản đồ Kiến trúc Sống (Living Architecture Mapping & Blast Radius) |
| `ui-ux-pro-max` | Trí tuệ thiết kế UI/UX toàn diện: DESIGN.md YAML tokens SSOT, 192 palettes, WCAG AA, HTML visual kits |

---

## 🔄 Workflows (8)

| Command | Description | Artifact Outputs |
|---|---|---|
| `/create-kit` | Quy trình tạo Agent Kit mới từ đầu (Deep Track) | `agent-kit-spec` |
| `/refactor-kit` | Cải tiến & Nâng cấp Agent Kit đã có sẵn (Refactor Track) | `refactored-kit-spec` |
| `/architecture-evolution` | Tiến hóa & nâng cấp kiến trúc an toàn dựa trên Living Map | `impact_assessment.md`, `change_proposal.md` |
| `/create-visual` | Sản xuất UI/UX Visual Kit, Interactive Preview, Dashboard, Landing Page và Design System | `design-system`, `visual-kit-html`, `visual-qa-report` |
| `/validate-kit` | Kiểm định Chất lượng Agent Kit (Audit 3 lớp & Rubric 5 sao) | `audit-report` |
| `/remember-kit` | Lưu bài học kinh nghiệm và ví dụ mẫu vào bộ nhớ dài hạn | `memory-entry` |
| `/copy-kit` | Sao chép (COPY) Agent Kit an toàn sang thư mục dự án đích | `copy_summary.md` |
| `/evolve-kit` | Quy trình tiến hóa tự động 1 lệnh duy nhất tại Engine: Ingest Inbox -> Ledger SSOT -> Freeze Snapshot -> Validate L1-L3 -> Tier 2 Human Gate -> Release SemVer -> Sync Test Workspace | `evolution_report.md`, `ledger.json` |

---

## 🛠️ Runtime Scripts

| Script | Purpose | Typical use |
|---|---|---|
| `scripts/validate_kit.py` | Tự kiểm định cấu trúc, audit 5 sao (`--audit`), auto-sync (`--sync`), quick check (`--quick`), và self-healing (`--converge`) | Sau khi chỉnh sửa `.agents/` |
| `scripts/lifecycle_engine.py` | Quản lý SSOT `lifecycle.json`, phân quyền Authority Matrix, kiểm soát hạn ngạch repair cycle và điều phối state transition | Trong toàn bộ workflows |
| `scripts/convergence_engine.py` | Vòng lặp tự sửa hội tụ (bounded self-healing loop max 3 iterations) | Trong `@auditor` profile / `--converge` flag |
| `scripts/deterministic_fixer.py` | Sửa lỗi cấu trúc tự động (zero token cost) | Gọi bởi `convergence_engine.py` |
| `scripts/generate_manifest.py` | Sinh bộ đăng ký `manifest.json` | Sau khi cập nhật metadata |
| `scripts/dependency_graph.py` | Sinh sơ đồ phụ thuộc `DEPENDENCY_GRAPH.md` | Sau khi thay đổi phụ thuộc |
| `scripts/eval_runner.py` | Kiểm thử hành vi và chấm điểm DoD tự động | Trong workflow `/validate-kit` / skill `kit-verifying` |
| `scripts/export_kit.py` | Xuất bản Agent Kit sang Antigravity Plugin, Cursor, Claude Desktop, OpenAI Custom GPTs | Trong skill `kit-exporting` |
| `scripts/copy_kit.py` | Sao chép (COPY) Agent Kit sang thư mục quản lý dự án AI Agent đích | Trong workflow `/copy-kit` / skill `kit-exporting` |
| `scripts/feedback_hub.py` | Append-only event stream JSONL, fold events, query unresolved và regression knowledge | Trong `validate_kit.py --audit` & `kit-assembling` |
| `scripts/evolution_engine.py` | Quản lý vòng đời batch tại Engine, thẩm định Net Gain và staging vNext | Trong workflow `/evolve-kit` |
| `scripts/evolution_ledger.py` | SSOT ledger cho evolution batches, trạng thái 6 pha | Trong workflow `/evolve-kit` |
| `scripts/evolution_orchestrator.py` | Điều phối toàn chu trình evolution 1-command | Trong workflow `/evolve-kit` |
| `scripts/atomic_promoter.py` | Thực thi nâng cấp nguyên tử 2 pha kèm đối soát SHA-256 Checksum | Trong workflow `/evolve-kit` |
| `scripts/snapshot_manager.py` | Đóng băng Full-Kit Snapshot kèm SHA-256 tree checksum | Trong workflow `/evolve-kit` |
| `scripts/equip_evolution.py` | Tự động trang bị trọn bộ Evolution Suite cho bất kỳ kit nào (1-shot / --all) | Trong `copy_kit.py` & `/refactor-kit` |
| `scripts/benchmark_behavior.py` | Đo lường Routing, JIT Context, DAG Parallelism và Convergence | Benchmark kiểm thử hành vi |
| `scripts/compile_execution_policy.py` | Sinh `execution_policy.json` (ACO Lite orchestration intent) | Trong kit-assembling compile pipeline |
| `scripts/component_registry.py` | Module xử lý SemVer và registry | Thư viện nội bộ |

---

## 📊 Statistics

| Metric | Value |
| --- | --- |
| **Total Agents** | 1 |
| **Total Skills** | 10 |
| **Total Workflows** | 8 |
| **Total Skill Scripts** | 5 |
| **Total Rules** | 3 |
| **Top-level Utilities** | 14 user-facing + 2 internal engine modules |
| **Coverage** | Domain analysis, prompt compilation, skill architecture, context compression, visual design intelligence, assembly, 3-layer verification, export, evolution, closed-loop convergence, unified lifecycle |
| **Token Efficiency** | Always-on rules <= 3KB (giảm >=75% context overhead) |

---

## 🔗 Quick Reference

| Nhu cầu | Agent / Role | Workflows / Skills |
|---|---|---|
| Tạo kit mới | `kit-architect` (`@analyst`, `@compiler`, `@architect`) | `/create-kit`, `domain-profiling`, `prompt-compiling`, `kit-assembling` |
| Tạo Visual Kit / UI / Dashboard | `kit-architect` (`@designer`) | `/create-visual`, `ui-ux-pro-max` |
| Nâng cấp kit | `kit-architect` (`@compiler`, `@architect`) | `/refactor-kit`, `kit-evolving` |
| Kiểm định chất lượng | `kit-architect` (`@auditor`) | `/validate-kit`, `kit-verifying` |
| Xuất bản nền tảng | `kit-architect` | `kit-exporting` (`export_kit.py`) |
| Lưu bài học / pattern | `kit-architect` | `/remember-kit`, `kit-evolving` |
