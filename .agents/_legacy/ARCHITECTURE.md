# AG Kit Architecture — Agent Kit Creator

> Comprehensive AI Agent Kit Creation, Refactoring, & Validation Suite — 2026.7.18

---

## 📋 Overview

Agent Kit Creator là hệ thống chuyên gia gồm:

- **5 Specialist Agents** - Bộ não điều phối, phân tích domain, sinh prompt, thiết kế skill và kiểm định chất lượng.
- **21 Specialized Skills** - Bộ kỹ năng chuyên sâu phục vụ quy trình thiết kế, tối ưu token và kiểm tra nhị phân.
- **4 Workflows** - Các quy trình slash command (`/create-kit`, `/refactor-kit`, `/validate-kit`, `/remember-kit`).

---

## 🔐 Managed Component Registry (2026.7.18)

Hệ thống sử dụng cơ chế quản lý phiên bản kép:

- Toolkit releases giữ **CalVer** trong `VERSION` (`YYYY.M.D`).
- Agents, skills, workflows, và rules sử dụng **SemVer** trong frontmatter.
- `manifest.json` ghi nhận đường dẫn, phiên bản, công cụ và phụ thuộc.
- `manifest.lock.json` ghi nhận mã băm SHA-256 xác thực tính toàn vẹn.
- `DEPENDENCY_GRAPH.md` được tự động sinh từ registry.

Đồng bộ registry bằng các lệnh:

```bash
python .agents/scripts/generate_manifest.py --check
python .agents/scripts/dependency_graph.py --check
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
├── manifest.lock.json       # Khóa toàn vẹn SHA-256
├── DEPENDENCY_GRAPH.md      # Sơ đồ phụ thuộc Workflow → Agent → Skill
├── schemas/                 # JSON schema contracts
├── agent/                   # 5 Specialist Agents
├── skills/                  # 21 Specialized Skills
├── workflows/               # 4 Slash Command Workflows
├── rules/                   # 6 System Rules
├── memory/                  # Persistent Memory (MEMORY.md index & topic files)
└── scripts/                 # Validation & Manifest Scripts
```

---

## 🤖 Agents (5)

Chuyên gia AI cho từng công đoạn tạo Agent Kit.

| Agent | Focus | Skills Used |
|---|---|---|
| `master-compiler` | Điều phối toàn bộ hệ thống Agent Kit Creator | guided-intaking, tiering-complexity, kit-assembly |
| `domain-analyst` | Phân tích domain, đòn bẩy 80/20 & failure modes | analyzing-domain-verbs, discovering-enhancements, domain-analysis |
| `kit-generator` | Sinh System Prompt 4 khối, DoD nhị phân & specs | compiling-prompts, building-component-specs, prompt-engineering |
| `skill-architect` | Thiết kế cấu trúc thư mục skill & SKILL.md | scaffolding-skills, skill-crafting, optimizing-progressive-disclosure |
| `quality-auditor` | Kiểm định chất lượng 3 lớp & chấm Rubric 5 sao | auditing-quality-gates, adversarial-evaluating, quality-assurance |

---

## 🧩 Skills (21)

Bộ kỹ năng chuyên môn phân cấp theo Progressive Disclosure.

| Skill | Description |
|---|---|
| `domain-analysis` | Phân tích lĩnh vực, xác định Core Verbs, 80/20 leverage points |
| `prompt-engineering` | Thiết kế System Prompt 4 phần chuẩn mực, binary DoD |
| `skill-crafting` | Viết nội dung SKILL.md, quy tắc phân cấp thông tin |
| `scaffolding-skills` | Dựng cấu trúc thư mục skill |
| `kit-assembly` | Lắp ráp các thành phần thành bộ Agent Kit hoàn chỉnh |
| `kit-evolution` | Phân tích sự lệch pha (Gap Analysis) & thực hiện Delta Patch |
| `quality-assurance` | Đánh giá 3 lớp (Structural, Semantic, Adversarial) & bảng điểm Rubric |
| `auditing-quality-gates` | Kiểm tra tiêu chuẩn Quality Gates cho Agent Kit |
| `adversarial-evaluating` | Chạy thử nghiệm kịch bản đối kháng để phát hiện lỗ hổng DoD |
| `tiering-complexity` | Phân loại độ phức tạp hệ thống (Micro, Standard, Professional, Suite Kit) |
| `compiling-prompts` | Đóng gói System Prompt với Hard Constraints & Negative Guidance |
| `building-component-specs` | Thiết kế thông số kỹ thuật chi tiết cho Memory, Workflows, Tools |
| `guided-intaking` | Phỏng vấn làm rõ ý tưởng người dùng bằng ngôn ngữ đời thường |
| `analyzing-domain-verbs` | Phân tích các động từ hành động đặc trưng theo từng lĩnh vực |
| `discovering-enhancements` | Khai phá cơ chế đòn bẩy riêng ngoài 6 Outcome Lenses |
| `optimizing-progressive-disclosure` | Tối ưu hóa ngân sách Token Budgeting & phân tầng ngữ cảnh |
| `memory-system` | Quản lý bộ nhớ dài hạn MEMORY.md (dùng cho `/remember-kit`) |
| `eval-running` | Kiểm thử đánh giá chất lượng hành vi tự động bằng script `eval_runner.py` |
| `exporting-kits` | Đóng gói và xuất bản Agent Kit sang Cursor, Claude Desktop, OpenAI Custom GPTs |
| `kit-extending` | Meta-skill tự mở rộng Rule, Workflow, và Skill chuẩn 100% Antigravity IDE |
| `output-checkpointing` | Chuyên biệt kiểm định, tính Blast Radius và kích hoạt Envelope cho sản phẩm Output |


---

## 🔄 Workflows (4)

Slash command procedures. Thực thi bằng `/command`.

| Command | Description | Artifact Outputs |
|---|---|---|
| `/create-kit` | Quy trình tạo Agent Kit mới từ đầu | `agent-kit-spec` |
| `/refactor-kit` | Cải tiến & Nâng cấp Agent Kit đã có sẵn | `refactored-kit-spec` |
| `/validate-kit` | Kiểm định Chất lượng Agent Kit (Audit 3 lớp & Rubric 5 sao) | `audit-report` |
| `/remember-kit` | Lưu bài học kinh nghiệm và ví dụ mẫu vào bộ nhớ dài hạn | `memory-entry` |

---

## 🛠️ Runtime Scripts

Agent Kit Creator bao gồm các công cụ thực thi kiểm định và đồng bộ registry:

| Script | Purpose | Typical use |
|---|---|---|
| `scripts/validate_kit.py` | Tự kiểm định cấu trúc, phiên bản, liên kết và quy tắc | Sau khi chỉnh sửa `.agents/` |
| `scripts/generate_manifest.py` | Sinh bộ đăng ký `manifest.json` và `manifest.lock.json` | Sau khi cập nhật metadata |
| `scripts/dependency_graph.py` | Sinh sơ đồ phụ thuộc `DEPENDENCY_GRAPH.md` | Sau khi thay đổi phụ thuộc |
| `scripts/audit_kit.py` | Kiểm định chất lượng Agent Kit 3 lớp | Trong workflow `/validate-kit` |
| `scripts/eval_runner.py` | Kiểm thử hành vi đối kháng và chấm điểm DoD tự động | Trong workflow `/validate-kit` / skill `eval-running` |
| `scripts/export_kit.py` | Xuất bản Agent Kit sang Cursor, Claude Desktop, OpenAI Custom GPTs | Trong skill `exporting-kits` |
| `scripts/distill_memory.py` | Tự động đúc rút bài học kinh nghiệm và pattern vào `MEMORY.md` | Trong workflow `/remember-kit` / skill `memory-system` |
| `scripts/component_registry.py` | Module xử lý SemVer, SHA-256 và registry | Thư viện nội bộ |

---

## 📊 Statistics

| Metric | Value |
| --- | --- |
| **Total Agents** | 5 |
| **Total Skills** | 21 |
| **Total Workflows** | 4 |

| **Top-level Utilities** | 6 user-facing + 1 internal module |
| **Total Skill Scripts** | 0 |
| **Coverage** | Kit design, domain analysis, prompt engineering, validation, audit, eval, export, self-extension |
| **Token Efficiency** | Phân cấp ngữ cảnh qua Progressive Disclosure |



---

## 🔗 Quick Reference

| Nhu cầu | Agent | Workflows / Skills |
|---|---|---|
| Tạo kit mới | `master-compiler`, `kit-generator` | `/create-kit`, `prompt-engineering`, `kit-assembly` |
| Nâng cấp kit | `quality-auditor`, `kit-generator` | `/refactor-kit`, `kit-evolution` |
| Kiểm định chất lượng | `quality-auditor` | `/validate-kit`, `quality-assurance`, `auditing-quality-gates` |
| Lưu bài học | `master-compiler` | `/remember-kit`, `memory-system` |
