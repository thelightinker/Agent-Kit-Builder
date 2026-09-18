---
name: create-kit
description: "Quy trình tạo Agent Kit mới từ đầu theo chuẩn Evolvable Architecture (Create Kit)."
version: 2.5.0
requires_agents: kit-architect
requires_skills: [domain-profiling, prompt-compiling, skill-architecting, kit-assembling, kit-verifying]
artifact_outputs: [domain_profile, system_prompt, skill_manifest, validation_report]
topology: orchestrator-workers
trigger: manual
permissions: read-write
tools_allowed: [Read, Write, Edit, Glob, Grep, Bash]
safe_outputs:
  write_output_dir: Chỉ ghi file vào ./output/<kit-name>/
max_retry_per_node: 2
---

# Workflow: /create-kit

Quy trình chuẩn mực để tạo một Agent Kit mới từ đầu, tích hợp **Targeted Grounding Gate (Dependency Mapping + Evidence Gate)** kết hợp Superpowers.

---

## 🚦 BƯỚC 0: SUPERPOWERS PROCESS & SKILL GATE (BẮT BUỘC)

Trước khi tạo bất kỳ thư mục hoặc file nào trong `./output/<kit-name>/`:

1. **Invoke Brainstorming:** BẮT BUỘC invoke `superpowers:brainstorming`.
2. **Khóa Design Spec:** Thống nhất với User về: Mục tiêu cốt lõi, Complexity Tier, 5 Core Verbs, 80/20 Leverage và Danh sách Cấu phần tối thiểu.
3. **Approval Gate:** Nhận sự phê duyệt (`APPROVED`) từ User cho Design Spec trước khi tiến hành viết Plan.
   - 🚫 **HARD CONSTRAINT:** TUYỆT ĐỐI KHÔNG tự ý viết code, tạo file hay scaffold thư mục khi Design Spec chưa được User phê duyệt.
   - ⚠️ **Quy tắc Bypass:** Cho phép bỏ qua Bước 0 khi yêu cầu là `FAST_TRACK` (Micro Kit 1-shot) hoặc `TARGETED_TRACK` (tạo/sửa 1 component đơn lẻ đã có domain context rõ ràng). Không tự ý bypass khi tạo Standard/Pro/Suite Kit.
4. **Planning & Execution:** Sau khi Design Spec được duyệt ➔ Invoke `superpowers:writing-plans` để lập kế hoạch ➔ Thực thi qua `superpowers:executing-plans`.

---

## 🔄 STATE MACHINE NODES (With Targeted Grounding Gate & DAG Parallelism)

### Bước 1: Phân tích Nghiệp vụ (Domain Profiling)
- **Role Profile:** `@analyst` | **Skill:** `domain-profiling`
- **[Targeted References]:** `.agents/references/outcome-lenses.md` + `.agents/references/workflow-topologies.md` (chỉ nạp khi cân nhắc Spectrum).
- **[Input Artifacts]:** Yêu cầu của User + Design Spec đã duyệt.
- **[Output Artifacts]:** `domain_profile.md` (Core Verbs, ROI leverage $\ge 1.25$, Predicted Failure Modes).
- **[DoD]:** 
  - [ ] Liệt kê đủ 5-10 Core Verbs kèm 4 tiêu chí đánh giá.
  - [ ] Có ít nhất 1 đòn bẩy 80/20 đạt tỷ lệ ROI $\ge 1.25$.
  - [ ] Dự đoán $\ge 3$ Failure Modes đặc trưng domain.
- **[Evaluation Loop]:** Pass ➔ Chuyển Bước 2 | Fail ➔ Bổ sung phân tích.

---

### Bước 2: Biên dịch System Prompt (Prompt Compiling)
- **Role Profile:** `@compiler` | **Skill:** `prompt-compiling`
- **[Mandatory Grounding Template]:** Đọc `.agents/templates/orchestrator-template.md` (nếu là Master Orchestrator) HOẶC `.agents/templates/agent-template.md` (nếu là Single/Specialist Agent).
- **[Input Artifacts]:** `domain_profile.md`
- **[Output Artifacts]:** System Prompt của Agent (`agent/<name>.md` hoặc `<name>.md`).
- **[Evidence Gate DoD]:**
  - [ ] Có phần TÓM TẮT CHO NGƯỜI DÙNG ở đầu (0 thuật ngữ AI, 3-5 dòng).
  - [ ] Chứa đủ 4 khối chuẩn từ template: Vai trò, Quy trình, Hard Constraints dạng phủ định, Format đầu ra.
  - [ ] Binary DoD: 100% nhị phân, đo lường được, 0 tính từ cảm tính.
- **[Evaluation Loop]:** Pass ➔ Chuyển Bước 3 | Fail ➔ Tinh chỉnh prompt.

---

### Bước 3: Thiết kế Kỹ năng & Kiến trúc (Skill Architecting — DAG Parallel Safe)
*(Chỉ thực hiện cho Standard / Professional / Suite Kits)*
- **Role Profile:** `@architect` | **Skill:** `skill-architecting`
- **[Mandatory Skill Creator Gate (Zero-Bypass)]:** Trước khi tạo bất kỳ file skill nào trong `skills/`, BẮT BUỘC phải nạp / kích hoạt skill `skill-creator` (`C:\Users\nhdcb\.gemini\config\plugins\anthropic-skills\skills\skill-creator\SKILL.md`). TUYỆT ĐỐI KHÔNG sinh `SKILL.md` từ trí nhớ khi chưa nạp `skill-creator`.
- **[DAG Parallel Execution Matrix]:**
  - **Phase 1 (Parallel-Safe)**: Sinh song song các Skills (`skills/<name>/SKILL.md`), Rules (`rules/<name>.md`), và Memory Topics (`memory/<topic>.md`) độc lập vì Read/Write sets không xung đột.
  - **Phase 2 (Sequential / Dependency-Grounded)**: Sinh Workflows (`workflows/*.md`) sau khi đã có danh sách Skills hoàn chỉnh.
- **[Mandatory Grounding Templates (1:1 per component)]:**
  - Tạo Skill $\rightarrow$ Nạp `skill-creator` + Đọc `.agents/templates/skill-template.md`
  - Tạo Workflow $\rightarrow$ Đọc `.agents/templates/workflow-template.md` (5-Part Node Anatomy)
  - Tạo Rule $\rightarrow$ Đọc `.agents/templates/rule-template.md`
  - Tạo Memory $\rightarrow$ Đọc `.agents/templates/memory-template.md`
- **[Input Artifacts]:** `domain_profile.md`, System Prompt.
- **[Output Artifacts]:** `skills/<skill-name>/SKILL.md`, `workflows/*.md`, `rules/*.md`, `memory/MEMORY.md`.
- **[Evidence Gate DoD]:**
  - [ ] Đã nạp và tuân thủ 100% quy chuẩn của `skill-creator` (Pushy Trigger Description chống under-triggering, 3-tier progressive disclosure, why-driven imperative instructions, concrete examples, chiều dài $\le 500$ dòng).
  - [ ] Mọi Workflow đều chứa đủ 5-Part Node Anatomy (`[STATE]`, Input, Output, DoD, Evaluation Loop) và `[ESCALATE_HUMAN]`.
  - [ ] Memory có đủ 4 required topics và index $\le 200$ dòng.
- **[Evaluation Loop]:** Pass ➔ Chuyển Bước 4.

---

### Bước 4: Lắp ráp, Biên dịch Hệ thống Quyết định & Đóng gói (Kit Assembling & Compiler Pipeline)
- **Skill:** `kit-assembling`
- **[Mandatory Grounding Template]:** Đọc `.agents/templates/manifest-template.json`.
- **[Input Artifacts]:** Toàn bộ components đã tạo.
- **[Output Artifacts]:** `./output/<kit-name>/` hoàn chỉnh kèm `manifest.json`, `manifest.lock.json`, `routing_index.json`, `invariant_rules.json`, `state_schema.json`, `task_classifier_index.json`, `evidence_schemas.json`, `DEPENDENCY_GRAPH.md`, `lifecycle.json`, và phân hệ Dynamic Evolution Suite.
- **[Compiler & Lifecycle Execution Pipeline]:**
  1. Chạy bộ 6 script Compiler: `compile_routing_index.py`, `compile_invariants.py`, `compile_state_schema.py`, `compile_task_classifier.py`, `compile_evidence_schemas.py`, `dry_run_simulation.py`.
  2. Tự động chạy `python .agents/scripts/equip_evolution.py ./output/<kit-name>/`.
  3. Khởi tạo `lifecycle.json` với `schema_version: "1.0.0"`, `kit_name: "<kit-name>"`, `lifecycle_state: "DRAFT"`.
  4. Sau khi các artifacts compiled và `manifest.json` được tạo hoàn tất, chuyển trạng thái sang `lifecycle_state: "READY_FOR_VALIDATION"`.
  5. Khởi tạo khối `handoff` chuyển giao quyền kiểm định sang `validate-kit`.
- **[DoD]:**
  - [ ] Toàn bộ file nằm trong `./output/<kit-name>/`.
  - [ ] Bộ 5 compiled decision artifacts (`routing_index.json`, `invariant_rules.json`, `state_schema.json`, `task_classifier_index.json`, `evidence_schemas.json`) được tạo và validate sạch.
  - [ ] Dry-run simulation PASS 100% (0 unreachable nodes, 0 deadlock states).
  - [ ] `manifest.json` và `manifest.lock.json` đồng bộ 100% danh mục files và SemVer `1.0.0`.
  - [ ] `lifecycle.json` tồn tại ở trạng thái `READY_FOR_VALIDATION`.
- **[Evaluation Loop]:** Pass ➔ Tự động chuyển tiếp (Handoff) sang `/validate-kit`.

---

### Bước 5: Chuyển Giao Kiểm định Chất lượng (Handoff to /validate-kit)
- **Role Profile:** `@auditor` | **Skill:** `kit-verifying`
- **[Input Artifacts]:** `./output/<kit-name>/` kèm `lifecycle.json`.
- **[Output Artifacts]:** `audit_findings.json`, `validation_report.md`.
- **[Execution]:** Kích hoạt trực tiếp `/validate-kit` để chạy kiểm tra 3 lớp (L1 Linter $\rightarrow$ L2 Kịch bản $\rightarrow$ L3 Adversarial) và xuất `audit_findings.json`.
- **[DoD]:**
  - [ ] `validate_kit.py --findings-json ./output/<kit-name>/audit_findings.json` trả về `0 error(s)`.
  - [ ] Điểm Rubric $\ge 4/5$ ⭐ $\rightarrow$ Cập nhật `lifecycle_state: "VALIDATED"`.
  - [ ] Nếu có lỗi $\rightarrow$ Tự động chuyển giao sang `/refactor-kit` (tối đa 3 vòng repair cycle).
- **[Evaluation Loop]:** Pass ➔ Hoàn tất quy trình | Fail ➔ Chuyển giao sang `/refactor-kit` (nếu vượt quá 3 vòng ➔ `[ESCALATE_HUMAN]`).
