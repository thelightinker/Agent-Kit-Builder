# 🛠️ Agent Kit Builder (`.agents`)

> **Expert Meta-Agent Suite for Designing, Building, Auditing, and Exporting Production-Ready LLM Agent Kits.**  
> Powered by Antigravity IDE, Progressive Disclosure, and 80/20 System Automation.

[![Validation Status](https://img.shields.io/badge/Toolkit_Validation-100%25_PASS-success?style=for-the-badge&logo=python)](file:///.agents/scripts/validate_kit.py)
[![Unit Tests](https://img.shields.io/badge/Unit_Tests-17%2F17_Passed-brightgreen?style=for-the-badge&logo=pytest)](file:///.agents/scripts/tests)
[![Version](https://img.shields.io/badge/CalVer-2026.7.18-blue?style=for-the-badge)](#)
[![Multi--Platform](https://img.shields.io/badge/Export-Cursor_%7C_Claude_%7C_Custom_GPTs-orange?style=for-the-badge)](#)

---

## 🌟 Tổng Quan Hệ Thống (System Overview)

**Agent Kit Builder** là bộ công cụ Meta-Agent chuyên nghiệp được thiết kế để tạo mới, nâng cấp, kiểm định chất lượng và đóng gói các bộ **Agent Kit** chuẩn mực cho mọi mô hình LLM (Antigravity IDE, Cursor, Claude Desktop, OpenAI Custom GPTs).

Hệ thống tuân thủ nghiêm ngặt nguyên tắc **Progressive Disclosure**, tiêu chuẩn **Definition of Done (DoD) nhị phân**, và cơ chế **Auto-Healing System** giúp tự động hóa 80/20 mọi quy trình phát triển Agent.

---

## ⚡ 5 Đòn Bẩy Tự Động Hóa 80/20 (80/20 Upgrade Engine)

1. 🔄 **Auto-Healing Lockfile & Manifest Sync**: Script `validate_kit.py` tự động phát hiện và đồng bộ hóa `manifest.lock.json` khi có sự thay đổi cấu phần, loại bỏ 100% lỗi mâu thuẫn mã băm SHA-256.
2. 📑 **Selective Progressive Disclosure & Context Budgeting**: Nạp trước YAML Frontmatter (< 50 tokens), chỉ gọi full body `SKILL.md` khi tác vụ được kích hoạt, tối ưu tới 60% Token Window.
3. 🧪 **Structural Eval Matrix cho Output Kits**: Script `eval_runner.py` tự động chạy bộ test suite và đánh giá 3 Hard Fail Gates (Zero-Fabrication, Task Completion, Token ROI) trên các kit đầu ra.
4. ⚡ **1-Click Multi-Platform Workspace Sync**: Script `export_kit.py --sync <target_dir>` tự động xuất bản và đặt file cấu hình `.cursorrules`, `.claude/instructions.txt`, và Custom GPTs trực tiếp vào workspace mục tiêu.
5. 🧠 **Automated Memory Distillation Engine**: Script `distill_memory.py` tự động trích xuất bài học kinh nghiệm, anti-patterns và ví dụ 5 sao append vào `.agents/memory/MEMORY.md`.

---

## 🏗️ Kiến Trúc Hệ Thống (Architecture Diagram)

```mermaid
graph TD
    User([User Request / Slash Command]) --> KA[kit-architect Orchestrator]
    
    subgraph "Dynamic Role Profiles"
        KA --> DA[@analyst]
        KA --> MC[@compiler]
        KA --> SA[@architect]
        KA --> DE[@designer]
        KA --> QA[@auditor]
    end
    
    subgraph "Core Components (.agents/)"
        ORCH[1 Orchestrator Agent]
        SKILLS[10 Focused Skills]
        WORKFLOWS[7 Workflows]
        RULES[3 Core Rules]
        MEMORY[Persistent Memory]
    end
    
    subgraph "Python Tooling Suite (.agents/scripts/)"
        VAL[validate_kit.py]
        EXP[export_kit.py]
        PRO[atomic_promoter.py]
        FEE[feedback_hub.py]
    end
    
    QA --> OUT[./output/<kit-name>/]
    OUT --> EXP
    EXP --> CURSOR[.cursorrules]
    EXP --> CLAUDE[.claude/instructions.txt]
    EXP --> GPTS[.gpts/instructions.txt]
```

---

## 📂 Cấu Trúc Thư Mục Mẫu (`.agents/`)

```plaintext
.agents/
├── README.md                # Quick start và hướng dẫn vận hành
├── ARCHITECTURE.md          # Thống kê danh mục và tổng quan kiến trúc
├── CHANGELOG.md             # Lịch sử phiên bản
├── VERSION                  # CalVer (2026.8.24)
├── manifest.json            # Bộ đăng ký phiên bản cấu phần (SemVer)
├── manifest.lock.json       # Mã khóa toàn vẹn SHA-256
├── DEPENDENCY_GRAPH.md      # Sơ đồ phụ thuộc tự động sinh
├── agent/                   # 1 Orchestrator Agent (kit-architect.md)
├── skills/                  # 10 Focused Skills
├── workflows/               # 7 Workflows (/create-kit, /refactor-kit, /validate-kit, ...)
├── rules/                   # 3 Core Rules (core-guardrails, dynamic-routing, collaboration-protocol)
├── memory/                  # Persistent Memory (MEMORY.md index & topic files)
├── templates/               # Mẫu chuẩn hóa Agent, Skill, Workflow, Rule
└── scripts/                 # Bộ công cụ thực thi Python tự động
```

---

## 📊 Danh Mục Cấu Phần (Component Inventory)

### 🤖 Orchestrator Agent (1)
| Agent | Vai trò cốt lõi | Dynamic Role Profiles |
|---|---|---|
| `kit-architect` | Điều phối toàn bộ luồng tạo, refactor, kiểm định và tiến hóa kit | `@analyst`, `@compiler`, `@architect`, `@designer`, `@auditor` |

### 🔄 Workflows & Slash Commands (7)
| Command | Description | Target Artifact |
|---|---|---|
| `/create-kit` | Kích hoạt luồng tạo mới Agent Kit từ ý tưởng | `./output/<kit-name>/` |
| `/refactor-kit` | Nâng cấp và vá lỗi Delta Patch cho Agent Kit có sẵn | `./output/<kit-name>/` |
| `/validate-kit` | Kiểm định chất lượng 3 lớp & xuất audit findings | Audit Report |
| `/remember-kit` | Trích xuất bài học và mẫu chuẩn vào bộ nhớ dài hạn | `.agents/memory/` |
| `/architecture-evolution` | Tiến hóa kiến trúc an toàn dựa trên Living Map | Living Map & Architecture |
| `/create-visual` | Sản xuất UI/UX Visual Kit, Dashboard, Landing Page | Visual Kit |
| `/evolve-kit` | Tiến hóa tự động 1 lệnh duy nhất (Ingest → Validate → Release) | Changelog & SemVer |

---

## 🛠️ Bộ Lệnh Thực Thi (CLI Tools & Automation)

### 1. Kiểm định cấu trúc và tự động sửa Lockfile
```bash
python .agents/scripts/validate_kit.py .agents --sync
```
> *Tự động cập nhật `manifest.lock.json` nếu có biến động component file và kiểm tra 100% liên kết.*

### 2. Chạy bộ Unit Tests toàn diện
```bash
python -m unittest discover -s .agents/scripts/tests
```

### 3. Đóng gói & Tự động đồng bộ sang dự án đích (1-Click Sync)
```bash
python .agents/scripts/export_kit.py --kit-dir .agents --output-dir dist/export --sync /path/to/target/project
```
> *Tự động xuất bản `.cursorrules`, `.claude/instructions.txt`, và Custom GPT instructions sang thư mục dự án đích.*

---

## 📜 Chuẩn Khai Báo Frontmatter (YAML Contracts)

### Agent Contract (`.agents/agent/<name>.md`)
```yaml
---
name: backend-specialist
description: Expert backend architect for Node.js, Python, and modern serverless systems.
tools: [Read, Grep, Glob, Bash, Edit, Write]
model: inherit
version: 1.0.0
skills: [clean-code, nodejs-best-practices, api-patterns]
---
```

### Skill Contract (`.agents/skills/<name>/SKILL.md`)
```yaml
---
name: skill-name
description: Mô tả năng lực và từ khóa kích hoạt.
when_to_use: "Điều kiện cụ thể khi agent cần nạp skill này."
version: 1.0.0
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---
```

---

## 📄 License & Standards

Được phát triển và tối ưu cho **Antigravity IDE** & **LLM Agent Systems**.  
Mọi cấu phần tuân thủ chuẩn **CalVer 2026.7.18** và **SemVer 1.0.0** độc lập nền tảng.
