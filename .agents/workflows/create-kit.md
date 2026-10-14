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
  write_output_dir: Ghi file vào thư mục đích chỉ định (<target-dir>, mặc định ./output/<kit-name>/)
max_retry_per_node: 2
---

# Workflow: /create-kit

Quy trình chuẩn mực để tạo một Agent Kit mới từ đầu, tích hợp **Targeted Grounding Gate (Dependency Mapping + Evidence Gate)** kết hợp Superpowers.

## 🛫 BƯỚC -1: PREFLIGHT CHECK
Chạy kiểm tra điều kiện tiên quyết trước khi bắt đầu tạo kit:
```bash
python .agents/scripts/preflight.py .agents
```
Nếu thiếu file hoặc template, hệ thống sẽ dừng và báo lỗi. Nếu thiếu các plugin ngoài (như `superpowers:*`), áp dụng phương án dự phòng đã quy định tại `.agents/DEPENDENCIES.md`.

---

## 🚦 BƯỚC 0: SCOPE CLARIFICATION & DESIGN SPEC

Trước khi tạo bất kỳ thư mục hoặc file nào trong thư mục đích (`<target-dir>`, mặc định `./output/<kit-name>/`):

0. **Context Readset theo Mode (JIT Loading):** Xác định mode (`micro`, `standard`, `mini_suite`, `full_suite`) rồi chỉ nạp các file trong `.agents/readsets.json[mode]`; không nạp file ngoài danh sách trừ khi một bước sau yêu cầu rõ.

1. **Brainstorming (Conditional):**
   - Nếu scope chưa rõ, requirements mâu thuẫn, hoặc có nhiều hướng kiến trúc hợp lý → invoke `superpowers:brainstorming` để khám phá trước khi commit (phương án dự phòng khi vắng mặt: hỏi trực tiếp sếp tối đa 3 câu về mục tiêu, tier, core verbs rồi chờ `APPROVED`).
   - Nếu requirements đã rõ ràng (user cung cấp đủ domain context, complexity tier, core verbs) → tiến thẳng vào Design Spec.
   - `FAST_TRACK` / `TARGETED_TRACK`: Bỏ qua Bước 0 hoàn toàn.
2. **Khóa Design Spec & Tri-Bucket Scope:** Thống nhất với User về: Mục tiêu cốt lõi, Complexity Tier, 5 Core Verbs, 80/20 Leverage, Danh sách Cấu phần tối thiểu.
   - **Tri-Bucket Intake (nếu kế thừa hoặc tham chiếu):** Phân loại toàn bộ năng lực cũ/tham chiếu vào 3 rổ: `Preserve` (giữ/nâng cấp), `Merge/Abstract` (gom vào component sẵn có), `Cut/Non-Goal` (cắt bỏ có chủ đích, ghi rõ vào mục `Non-Goals`).
3. **Approval Gate:** Nhận sự phê duyệt (`APPROVED`) từ User cho Design Spec trước khi tiến hành viết Plan.
   - 🚫 **HARD CONSTRAINT:** TUYỆT ĐỐI KHÔNG tự ý viết code, tạo file hay scaffold thư mục khi Design Spec chưa được User phê duyệt.
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
- **[Evaluation Loop]:** Pass ➔ Chuyển Bước 1.5 | Fail ➔ Bổ sung phân tích.

---

### Bước 1.5: Khớp Nối Kiến Trúc & Hợp Đồng Node (Topology & Node-Contract Reconciliation Gate)
*(Chỉ thực hiện cho Professional / Suite Kits có > 1 Agent. Micro / Standard Kit bỏ qua bước này.)*
- **Role Profile:** `@architect` | **Skill:** `skill-architecting`

- **[Input Artifacts]:** `domain_profile.md` + Topology & Workflow sơ bộ.
- **[Output Artifacts]:** Ma trận phân định hợp đồng Node-Role-Skill (ghi trong plan hoặc design spec).
- **[DoD - Reconciliation Assertions]:**
  - [ ] **Zero Orphan Nodes:** Mọi Node trong mọi Workflow đều có đúng 1 Role chịu trách nhiệm và đúng 1 Skill tương ứng.
  - [ ] **Zero Self-Audit:** Mọi Node thuộc tầng kiểm định/review bắt buộc do một Role độc lập với Role đã tạo tác đảm nhiệm ($\text{Auditor} \ne \text{Author}$). Cấm tuyệt đối một agent tự cấp quyền `PASS` cho chính mình.
  - [ ] **Zero Split-Lifecycle Skills:** Không có Skill nào ôm 2 giai đoạn phân kỳ ngăn cách bởi Human Gate (ví dụ: cấm 1 skill vừa lập card metadata trước Gate vừa viết prose sau Gate).
  - [ ] **Heuristic Ownership Alignment:** Mọi bảng quy tắc/heuristic/ngân sách thuộc về chính xác Role thực thi Node đó.
- **[Evaluation Loop]:** Pass ➔ Chuyển Bước 2 | Fail ➔ Điều chỉnh phân bổ Topology.

---

### Bước 2: Biên dịch System Prompt (Prompt Compiling)
- **Role Profile:** `@compiler` | **Skill:** `prompt-compiling`
- **[Mandatory Grounding Template]:** Đọc `.agents/templates/orchestrator-template.md` (nếu là Master Orchestrator) HOẶC `.agents/templates/agent-template.md` (nếu là Single/Specialist Agent).
- **[Input Artifacts]:** `domain_profile.md`, Ma trận phân bổ Hợp đồng Node.
- **[Output Artifacts]:** `kit_spec.json` + file thân agent `bodies/<name>.md` (render tự động, cấm viết tay frontmatter chuỗi).
- **[Evidence Gate DoD]:**
  - [ ] Có phần TÓM TẮT CHO NGƯỜI DÙNG ở đầu (0 thuật ngữ AI, 3-5 dòng).
  - [ ] Chứa đủ 4 khối chuẩn từ template: Vai trò, Quy trình, Hard Constraints dạng phủ định, Format đầu ra.
  - [ ] Binary DoD: 100% nhị phân, đo lường được, 0 tính từ cảm tính.
  - [ ] **Anti-Pseudo-Metric Mandate:** Tuyệt đối cấm đưa ra các chỉ số số học thập phân (như `sentence-CV < 0.3`, `hedge-ratio > 0.04`) trong prompt nếu không có script thực thi đi kèm để đo đạc khách quan. Tiêu chí định lượng phải có script; tiêu chí định tính phải viết dạng checklist/rubric cụ thể.
- **[Evaluation Loop]:** Pass ➔ Chuyển Bước 3 | Fail ➔ Tinh chỉnh prompt.

---

### Bước 3: Thiết kế Kỹ năng & Kiến trúc (Skill Architecting — DAG Parallel Safe)
*(Chỉ thực hiện cho Standard / Professional / Suite Kits)*
- **Role Profile:** `@architect` | **Skill:** `skill-architecting`
- **[Mandatory Skill Creator Gate (Zero-Bypass)]:** Trước khi tạo bất kỳ file skill nào trong `skills/`, BẮT BUỘC phải nạp / kích hoạt skill `skill-creator` (`.agents/skills/skill-creator/SKILL.md`). TUYỆT ĐỐI KHÔNG sinh `SKILL.md` từ trí nhớ khi chưa nạp `skill-creator`.
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
  - [ ] **Chu trình Cách Ly Tuần Tự (SEQ-001 đến SEQ-008):** Mỗi node workflow chỉ có đúng 1 active agent, có ranh giới `[CONTEXT_RESET]` khi chuyển vai trò, và cấm khai báo mảng `requires_agents` đa tác tử ở frontmatter của từng node.
  - [ ] Memory có đủ 4 required topics và index $\le 200$ dòng.
- **[Evaluation Loop]:** Pass ➔ Chuyển Bước 4.

---

### Bước 4: Lắp ráp, Biên dịch Hệ thống Quyết định & Đóng gói (Kit Assembling & Compiler Pipeline)
- **Skill:** `kit-assembling`
- **[Mandatory Grounding Template]:** Đọc `.agents/templates/manifest-template.json`.
- **[Input Artifacts]:** Toàn bộ components đã tạo.
- **[Output Artifacts]:** Thư mục kit đích hoàn chỉnh (`<target-dir>`, mặc định `./output/<kit-name>/`) kèm `manifest.json`, `manifest.lock.json`, `routing_index.json`, `invariant_rules.json`, `state_schema.json`, `task_classifier_index.json`, `evidence_schemas.json`, `DEPENDENCY_GRAPH.md`, và `lifecycle.json`.
- **[Compiler & Lifecycle Execution Pipeline]:**
  0. Chạy render frontmatter tất định cho agent: `python .agents/scripts/render_frontmatter.py <kit_spec.json> --bodies <bodies_dir> --out <target-dir>/agent` (thoát khác 0 thì dừng ngay).
  1. Chạy bộ 6 script Compiler: `compile_routing_index.py`, `compile_invariants.py`, `compile_state_schema.py`, `compile_task_classifier.py`, `compile_evidence_schemas.py`, `dry_run_simulation.py` trên `<target-dir>`.
  2. Khởi tạo `lifecycle.json` với `schema_version: "1.0.0"`, `kit_name: "<kit-name>"`, `lifecycle_state: "DRAFT"`.
  3. Sau khi các artifacts compiled và `manifest.json` được tạo hoàn tất, chuyển trạng thái sang `lifecycle_state: "READY_FOR_VALIDATION"`.
  4. Khởi tạo khối `handoff` chuyển giao quyền kiểm định sang `validate-kit`.

- **[DoD]:**
  - [ ] Toàn bộ file nằm trong thư mục đích (`<target-dir>`). CẤM ghi đè `.agents/` của Creator Engine.
  - [ ] Bộ 5 compiled decision artifacts (`routing_index.json`, `invariant_rules.json`, `state_schema.json`, `task_classifier_index.json`, `evidence_schemas.json`) được tạo và validate sạch.
  - [ ] Dry-run simulation PASS 100% (0 unreachable nodes, 0 deadlock states).
  - [ ] `manifest.json` và `manifest.lock.json` đồng bộ 100% danh mục files và SemVer `1.0.0`.
  - [ ] `lifecycle.json` tồn tại ở trạng thái `READY_FOR_VALIDATION`.
- **[Evaluation Loop]:** Pass ➔ Tự động chuyển tiếp (Handoff) sang `/validate-kit`.

---

### Bước 5: Chuyển Giao Kiểm định Chất lượng (Handoff to /validate-kit)
- **Role Profile:** `@auditor` | **Skill:** `kit-verifying`
- **[Input Artifacts]:** Thư mục kit đích (`<target-dir>`, mặc định `./output/<kit-name>/`) kèm `lifecycle.json`.
- **[Output Artifacts]:** `audit_findings.json`, `validation_report.md`.
- **[Execution]:** Kích hoạt trực tiếp `/validate-kit <target-dir>` để chạy kiểm tra 3 lớp (L1 Linter $\rightarrow$ L2 Kịch bản $\rightarrow$ L3 Adversarial) và xuất `audit_findings.json`.
- **[DoD]:**
  - [ ] `validate_kit.py <target-dir> --kit-output --findings-json <target-dir>/audit_findings.json` trả về `0 error(s)`.
  - [ ] **Executable Script Smoke Test:** 100% các script Python đi kèm kit (nếu có) phải vượt qua bài kiểm tra cú pháp AST và chạy thử `--help` trả về exit code `0` không có exception.
  - [ ] Điểm Rubric $\ge 4/5$ ⭐ $\rightarrow$ Cập nhật `lifecycle_state: "VALIDATED"`.
  - [ ] Nếu có lỗi $\rightarrow$ Tự động chuyển giao sang `/refactor-kit` (tối đa 3 vòng repair cycle).
- **[Evaluation Loop]:** Pass ➔ Hoàn tất quy trình | Fail ➔ Chuyển giao sang `/refactor-kit` (nếu vượt quá 3 vòng ➔ `[ESCALATE_HUMAN]`).
