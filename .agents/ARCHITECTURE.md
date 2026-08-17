# AG Kit Architecture — Agent Kit Creator

> Comprehensive AI Agent Kit Creation, Refactoring, & Validation Suite — 2026.8.17 (v2.0.0 Evolvable Architecture)

---

## 📋 Overview

Agent Kit Creator là hệ thống chuyên gia tinh gọn gồm:

- **1 Orchestrator Agent** (`kit-architect`) với 4 Dynamic Role Profiles (`@analyst`, `@compiler`, `@architect`, `@auditor`).
- **7 Focused Skills** - Bộ kỹ năng chuyên sâu phục vụ phân tích domain, biên dịch prompt, cấu trúc skill, lắp ráp, kiểm định, xuất bản và tiến hóa kit.
- **4 Workflows** - Các quy trình slash command (`/create-kit`, `/refactor-kit`, `/validate-kit`, `/remember-kit`).
- **2 Lean Rules** - Ràng buộc bất biến (`core-guardrails`) và phân loại mode (`dynamic-routing`).

---

## 🔐 Managed Component Registry (2026.8.17)

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
├── skills/                  # 7 Focused Skills
├── workflows/               # 4 Slash Command Workflows
├── rules/                   # 2 Lean Rules
├── templates/               # Component & Workflow Templates
├── references/              # Deep Reference Docs & Domain Guides
├── memory/                  # Persistent Memory (MEMORY.md index & topic files)
└── scripts/                 # Validation, Eval & Export Scripts
```

---

## 🤖 Agents (1)

| Agent | Focus | Skills Used |
|---|---|---|
| `kit-architect` | Orchestrator duy nhất điều phối toàn bộ pipeline với 4 Role Profiles (`@analyst`, `@compiler`, `@architect`, `@auditor`) | domain-profiling, prompt-compiling, skill-architecting, kit-assembling, kit-verifying, kit-exporting, kit-evolving |

---

## 🧩 Skills (7)

Bộ kỹ năng chuyên môn phân cấp theo Progressive Disclosure.

| Skill | Description |
|---|---|
| `domain-profiling` | Phân tích Core Verbs, 80/20 leverage points, failure modes, tier classification |
| `prompt-compiling` | Biên dịch System Prompt 4 khối, binary DoD, negative constraints, multi-target transpiling |
| `skill-architecting` | Thiết kế cấu trúc thư mục skill, SKILL.md progressive disclosure, YAML frontmatter contracts |
| `kit-assembling` | Đóng gói Agent Kit vào thư mục cách ly `./output/<kit-name>/`, sinh manifest.json |
| `kit-verifying` | Kiểm định 3 lớp (L1 Linting, L2 Adaptive Scenarios, L3 Adversarial Tests) & Rubric 5 sao |
| `kit-exporting` | Đóng gói và xuất bản Agent Kit sang Cursor, Claude Desktop, OpenAI Custom GPTs |
| `kit-evolving` | Phân tích Gap Analysis, thực hiện Delta Patch, quản lý memory/ và golden examples |

---

## 🔄 Workflows (4)

| Command | Description | Artifact Outputs |
|---|---|---|
| `/create-kit` | Quy trình tạo Agent Kit mới từ đầu (Deep Track) | `agent-kit-spec` |
| `/refactor-kit` | Cải tiến & Nâng cấp Agent Kit đã có sẵn (Refactor Track) | `refactored-kit-spec` |
| `/validate-kit` | Kiểm định Chất lượng Agent Kit (Audit 3 lớp & Rubric 5 sao) | `audit-report` |
| `/remember-kit` | Lưu bài học kinh nghiệm và ví dụ mẫu vào bộ nhớ dài hạn | `memory-entry` |

---

## 🛠️ Runtime Scripts

| Script | Purpose | Typical use |
|---|---|---|
| `scripts/validate_kit.py` | Tự kiểm định cấu trúc, phiên bản, liên kết và quy tắc | Sau khi chỉnh sửa `.agents/` |
| `scripts/generate_manifest.py` | Sinh bộ đăng ký `manifest.json` | Sau khi cập nhật metadata |
| `scripts/dependency_graph.py` | Sinh sơ đồ phụ thuộc `DEPENDENCY_GRAPH.md` | Sau khi thay đổi phụ thuộc |
| `scripts/eval_runner.py` | Kiểm thử hành vi và chấm điểm DoD tự động | Trong workflow `/validate-kit` / skill `kit-verifying` |
| `scripts/export_kit.py` | Xuất bản Agent Kit sang Cursor, Claude Desktop, OpenAI Custom GPTs | Trong skill `kit-exporting` |
| `scripts/audit_kit.py` | Kiểm định chất lượng Agent Kit 3 lớp | Trong workflow `/validate-kit` |
| `scripts/component_registry.py` | Module xử lý SemVer và registry | Thư viện nội bộ |

---

## 📊 Statistics

| Metric | Value |
| --- | --- |
| **Total Agents** | 1 |
| **Total Skills** | 7 |
| **Total Workflows** | 4 |
| **Total Skill Scripts** | 0 |
| **Total Rules** | 2 |
| **Top-level Utilities** | 5 user-facing + 1 internal module |
| **Coverage** | Domain analysis, prompt compilation, skill architecture, assembly, 3-layer verification, export, evolution |
| **Token Efficiency** | Always-on rules <= 3KB (giảm >=75% context overhead) |

---

## 🔗 Quick Reference

| Nhu cầu | Agent / Role | Workflows / Skills |
|---|---|---|
| Tạo kit mới | `kit-architect` (`@analyst`, `@compiler`, `@architect`) | `/create-kit`, `domain-profiling`, `prompt-compiling`, `kit-assembling` |
| Nâng cấp kit | `kit-architect` (`@compiler`, `@architect`) | `/refactor-kit`, `kit-evolving` |
| Kiểm định chất lượng | `kit-architect` (`@auditor`) | `/validate-kit`, `kit-verifying` |
| Xuất bản nền tảng | `kit-architect` | `kit-exporting` (`export_kit.py`) |
| Lưu bài học / pattern | `kit-architect` | `/remember-kit`, `kit-evolving` |
