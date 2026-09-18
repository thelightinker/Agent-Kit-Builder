---
name: prompt-compiling
description: >
  Biên dịch System Prompt cho 3 dạng Archetypes (Standalone Agent, Master Orchestrator,
  hoặc Domain Specialist Agent), thiết lập Binary Definition of Done (DoD),
  Hard Constraints dạng phủ định, Worker Briefing Protocol, Deterministic Computation Guard
  và Negative Completeness Matrix.
when_to_use: "Khi cần biên dịch, tối ưu hoặc chuẩn hóa System Prompt cho bất kỳ Agent nào."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.5.0
---

# Prompt Compiling

Kỹ năng biên dịch System Prompt chuyên nghiệp, biến yêu cầu nghiệp vụ thành chỉ dẫn tối ưu cho LLM với tỷ lệ đúng ngay lần đầu (Right-First-Time) cao nhất.

---

## 📚 REFERENCE KNOWLEDGE ACTIVATION (NẠP ON-DEMAND)

Khi cần tra cứu kỹ thuật biên dịch prompt nâng cao:
- **Lý thuyết Verification Abstraction**: Đọc [verification-abstraction.md](../../references/verification-abstraction.md).
- **Nguyên tắc Điều phối Suite & Specialist Authority**: Đọc [multi-agent-orchestration.md](../../references/multi-agent-orchestration.md).
- **3-Tier Autonomy Gate, Anti-Defaults & Reality Check**: Đọc [agent-design-patterns.md](../../references/agent-design-patterns.md).
- **Mẫu Scaffolding System Prompt**: Dùng [templates/agent-template.md](../../templates/agent-template.md) hoặc [templates/orchestrator-template.md](../../templates/orchestrator-template.md).

---

## 1. 3 PROMPT ARCHETYPES

Biên dịch prompt theo đúng vai trò kiến trúc:

### 🌟 Archetype A: Standalone Single Agent
Dành cho Micro / Standard Kit. 1 agent duy nhất nắm toàn bộ quy trình:
1. **Vai trò & Outcome**: 3-5 dòng tóm tắt đời thường + tiêu chí hoàn thành.
2. **Quy trình & Action Matrix**: Các bước tuần tự.
3. **Hard Constraints**: Ràng buộc phủ định.
4. **Output Format**: Khung mẫu đầu ra.

### 🌟 Archetype B: Master Orchestrator (Nhạc Trưởng Điều Phối)
Dành cho Suite Kit. Đóng vai trò nhạc trưởng điều phối với kỷ luật cao nhất:
1. **Socratic & Pre-flight Check**: Làm rõ 1-3 câu về Trade-offs/Edge-cases nếu rủi ro cao; nếu rõ thì phân rã task ngay.
2. **Decomposition & Concurrency Matrix**: Tách task lớn thành các sub-tasks độc lập (Parallel reads cho khảo sát $\rightarrow$ Coordinator synthesis $\rightarrow$ Sequential writes cho chỉnh sửa file).
3. **"Never Delegate Understanding" Hard Gate**: Cấm tuyệt đối việc ủy quyền mù quáng ("Dựa vào findings hãy fix đi"). Orchestrator bắt buộc phải tự phân tích root cause, chỉ định chính xác file path, line range và tiêu chí nghiệm thu trước khi giao việc.
4. **Worker Briefing Contract (Đủ 5 phần)**: Goal & Context, What was ruled out, Specific file scope, Negative boundaries, Verification evidence.
5. **Specialist Routing Table & Boundary Enforcement**: Ma trận chọn Specialist và khóa cứng quyền sở hữu file (File Ownership Matrix).
6. **Synthesis & Conflict Resolution**: Gom kết quả, xử lý mâu thuẫn theo thứ tự ưu tiên (User $\rightarrow$ Evidence/Tests $\rightarrow$ Architecture $\rightarrow$ Specialist) và xuất báo cáo bàn giao.

### 🌟 Archetype C: Domain Specialist Agent (Real Agent)
Dành cho các chuyên gia trong Suite Kit:
1. **Domain Authority**: Khẳng định quyền quyết định cao nhất trong domain được giao.
2. **Owned Skills Authority**: Danh sách các kỹ năng thuộc quyền chỉ huy và điều kiện kích hoạt.
3. **Strict Boundaries**: Danh mục những điều ĐƯỢC LÀM và KHÔNG ĐƯỢC LÀM (File ownership).
4. **Handoff Trigger**: Điều kiện khi nào cần dừng lại và chuyển tiếp yêu cầu về cho Orchestrator.

---

## 2. DETERMINISTIC ARITHMETIC GUARDRAIL (CHỐNG ẢO GIÁC SỐ HỌC)

Khi biên dịch Prompt cho các agent thuộc domain định lượng (Growth, Data, Finance, Logistics):
- Bắt buộc nhúng câu lệnh Hard Constraint P0:
  > *"TUYỆT ĐỐI KHÔNG tự tính nhẩm các phép tính $\ge 3$ biến số, tính phần trăm phễu, ROI, LTV:CAC hoặc tổng hợp bảng số liệu. BẮT BUỘC phải viết và chạy script Python hoặc sử dụng tool tính toán để lấy kết quả tất định."*

---

## 3. NEGATIVE COMPLETENESS MATRIX (KIỂM TRA OMISSION)

Khi biên dịch Prompt cho các agent thuộc domain Audit, Legal, Compliance, Security:
- Bắt buộc yêu cầu Specialist xuất cấu trúc báo cáo 2 chiều:
  ```markdown
  | Hạng Mục Bắt Buộc | Trạng Thái (Found / MISSING) | Mức Rủi Ro | Dòng Trích Dẫn / Bằng Chứng |
  |:---|:---:|:---:|:---|
  ```
- Nếu phát hiện hạng mục bắt buộc bị thiếu $\rightarrow$ Gắn cờ cảnh báo `[CRITICAL OMISSION]` thay vì bỏ qua trong im lặng.

---

## 4. TIÊU CHUẨN BINARY DEFINITION OF DONE (DoD)

Mọi tiêu chí trong DoD bắt buộc phải thỏa mãn 3 kiểm định:
1. **Tính nhị phân**: Chỉ có 2 trạng thái Đạt hoặc Không đạt.
2. **Tính đo lường được**: Có thể kiểm chứng trực tiếp trên output mà không cần phỏng đoán.
3. **Không sáo ngữ**: Cấm dùng tính từ cảm tính ("viết hay", "đầy đủ", "chuyên nghiệp"). Phải thay bằng số liệu hoặc sự kiện ("≥ 500 từ", "có trích dẫn nguồn", "đầy đủ 4 đề mục").

---

## 5. TIÊU CHUẨN HARD CONSTRAINTS

- Viết ở dạng **phủ định bắt buộc** ("KHÔNG BAO GIỜ...", "TUYỆT ĐỐI KHÔNG...").
- Ngăn chặn trực diện các Failure Modes đã dự đoán ở bước Domain Profiling.

---

## 6. TIÊU CHUẨN CAPABILITY DECLARATION & NEGATIVE SCOPE (COMPILER SSOT)

Khi biên dịch Prompt cho Specialist Agent hoặc Master Orchestrator, BẮT BUỘC biên dịch khối `capabilities:` và `negative_scope:` trong frontmatter theo chuẩn Compiler + Runtime Model:
1. **Namespacing (CANON 9)**: Format `domain.component.action`.
2. **Preconditions**: Phân tách rõ `structural` (binary state keys) và `semantic` (judge verdicts kèm `evaluator`).
3. **Evidence Contract**: Khai báo `evidence_schema` với các checks cụ thể (`file_exists`, `metric_threshold`).
4. **Explicit Negative Scope (CANON 6)**: Liệt kê rõ các tài nguyên và state transitions bị cấm can thiệp (`cannot_modify`, `cannot_trigger_state_transition`).
5. **Compiled Failure Policy (CANON 8)**: Khai báo rõ `on_structural_failure`, `on_semantic_rejection` và `checkpoint_resume_policy`.

---

## 7. ORCHESTRATION PROTOCOL COMPILATION (ACO Lite)

Khi biên dịch System Prompt cho **Archetype B (Master Orchestrator)**, BẮT BUỘC biên dịch thêm khối `## Orchestration Protocol` vào Orchestrator prompt theo mẫu trong `templates/orchestrator-template.md`:

1. **Complexity Ladder**: Copy bảng L0-L3 từ template. Tùy chỉnh ví dụ L0 theo domain cụ thể của kit.
2. **Context Handoff**: Giữ nguyên quy tắc artifact reference. Chỉ thay đổi đường dẫn artifact nếu kit dùng thư mục khác thay vì `shared_state/`.
3. **Recovery Cascade**: Giữ nguyên `repair → reroute → replan → STOP`. Tùy chỉnh `retry.max_attempts` trong `execution_policy.json` nếu domain yêu cầu (nhưng KHÔNG VƯỢT QUÁ 3).
4. **Orchestration Invariants**: Giữ nguyên — đây là hard constraints.

Khi biên dịch **Archetype A (Standalone)** hoặc **Archetype C (Specialist)**, KHÔNG chèn Orchestration Protocol section đầy đủ. Chỉ chèn `## Context Handoff Protocol` (xem `templates/agent-template.md`).

---

## 8. COMPILED ROUTING INJECTION (BẮT BUỘC — P0 INVARIANT)

Khi biên dịch System Prompt, BẮT BUỘC thực hiện 3 bước Routing Injection sau.
**Nếu bỏ qua, kit FAIL validation** (`routing_index.json` rỗng → `routing.empty_capabilities` error).

### 8.1 Populate Frontmatter `capabilities:` Block (MỌI Agent)

Dùng `skill_invocation_matrix` và `Capability Skeleton` từ Domain Profile để sinh `capabilities:` block trong YAML frontmatter của mỗi Agent:
- Mỗi scenario + skill → 1 capability entry với `id: domain.component.action` (CANON 9).
- `intent_patterns:` lấy từ `routing_table.intent_pattern` hoặc từ scenario text.
- `preconditions:`, `postconditions:`, `evidence_schema:` lấy từ Capability Skeleton (Domain Profile Section 5).
- `negative_scope:` lấy từ domain boundary analysis.

**Ví dụ populated frontmatter:**
```yaml
capabilities:
  - id: seo.onpage.audit
    intent_patterns:
      - "phân tích SEO"
      - "kiểm tra on-page"
    preconditions:
      structural:
        - key: url_provided
          value: true
    postconditions:
      - key: seo_report_generated
        value: true
    evidence_schema:
      structural:
        - check: file_exists
          path: "shared_state/seo_report.json"
    failure_policy:
      on_structural_failure: "retry(max=2) → escalate_human"
      on_semantic_rejection: "escalate_human"
    negative_scope:
      cannot_modify:
        - approved_content
```

### 8.2 Inject Routing Table vào Orchestrator Body (Archetype B)

Khi biên dịch Orchestrator prompt, BẮT BUỘC inject bảng `## 📡 ROUTING TABLE` **đã populated** vào body text. Lấy data trực tiếp từ `routing_table` trong Domain Profile Section 6.

Format bắt buộc (mỗi dòng là data thực, KHÔNG placeholder):
```markdown
## 📡 ROUTING TABLE (COMPILED — DO NOT MODIFY AT RUNTIME)

| User Intent Pattern | Target Agent | Required Skills | Execution Mode |
|:---|:---|:---|:---|
| "phân tích SEO" | `seo-specialist` | `seo-audit` | L1 Routed |
| "tạo chiến dịch toàn phễu" | **STAGED** | Step 1: `seo-specialist` → Step 2: `copy-specialist` | L2 Staged |
| Intent không khớp | **ESCALATE** | — | ⛔ Hỏi user |
```

**HARD RULE:** Routing table PHẢI có ≥1 dòng data thực + 1 dòng ESCALATE fallback. Bảng toàn placeholder = FAIL.

### 8.3 Inject Skill Invocation Matrix vào Agent Body (Archetype A & C)

Khi biên dịch Agent prompt (Standalone hoặc Specialist), BẮT BUỘC inject khối `## 🔧 SKILL INVOCATION MATRIX` **đã populated** vào body text. Lấy data từ `skill_invocation_matrix` trong Domain Profile Section 6.

Format bắt buộc:
```markdown
## 🔧 SKILL INVOCATION MATRIX (BẮT BUỘC)

| Khi gặp scenario... | Nạp Skill | Cách nạp | Tại sao |
|:---|:---|:---|:---|
| Cần phân tích SEO | `seo-audit` | Đọc `skills/seo-audit/SKILL.md` trước khi bắt đầu | Skill chứa checklist 42 tiêu chí |
| Task không khớp skill | ⛔ KHÔNG tự xử lý | Emit handoff về Orchestrator | Không vượt domain authority |

### 🔴 HARD RULE: Skill Loading Protocol
1. Khi Matrix chỉ định nạp Skill → ĐỌC FILE `SKILL.md` TRƯỚC (dùng tool Read).
2. KHÔNG BAO GIỜ xử lý bằng "kiến thức chung" nếu Skill tương ứng tồn tại.
3. Nếu Skill hướng dẫn nạp `references/*.md` → đọc tiếp.
```
