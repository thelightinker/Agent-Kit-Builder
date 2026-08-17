# AGENT WORKFLOW MASTER FRAMEWORK

> Tổng hợp nguyên tắc thiết kế agent workflow từ 10 nguồn hàng đầu hiện tại (Anthropic, GitHub Next/Microsoft Research, LangChain, HumanLayer, OpenAI, Cognition, Google) — dùng làm single source of truth để Agent Kit Creator tạo và tự-đánh giá bất kỳ workflow nào, từ pipeline tuyến tính đơn giản tới hệ multi-agent phức tạp.

Cập nhật: 2026-07-11 · Phạm vi: framework kiến trúc và nguyên tắc quyết định.

---

## PHẦN 0 — NGUYÊN TẮC NỀN TẢNG

### 0.1 Workflow vs Agent — ranh giới định nghĩa

Anthropic phân định 2 khái niệm hay bị dùng lẫn:

| | Workflow | Agent |
|---|---|---|
| Control flow | Code path định trước, LLM + tool được orchestrate theo path đó | LLM tự định hướng process, tự quyết bước tiếp theo |
| Định nghĩa rút gọn | Predefined code paths | "LLMs autonomously using tools in a loop" |
| Tính đoán trước | Cao — luôn biết bước kế tiếp | Thấp — model quyết định lúc runtime |

Một hệ thống có thể chứa cả hai — chọn ở cấp NODE, không phải cấp toàn hệ thống.

### 0.2 Complexity Ladder — leo thang khi có bằng chứng, không leo trước

```
Đơn LLM call (+ retrieval, in-context example)
  → đủ cho phần lớn use case. Nếu đủ, DỪNG Ở ĐÂY.
Workflow tĩnh (chaining / routing / parallelization)
  → task well-defined, path đoán trước được ở compile-time.
Orchestrator-Workers
  → task có complexity KHÔNG đoán trước được ở compile-time.
Autonomous Agent Loop
  → task mở, cần model-driven decision-making, có ground-truth feedback mỗi bước.
```

### 0.3 Checklist: có nên build Agent không
- [ ] **Task Complexity**: nếu vẽ được toàn bộ decision tree tường minh → build workflow tường minh, tối ưu từng node.
- [ ] **Value Justification**: exploration của agent tốn token — giá trị task phải bù được chi phí đó.
- [ ] **Error Cost đã có kế hoạch xử lý**: guardrail + human checkpoint phải nghiêm ngặt hơn tương ứng với rủi ro.

---

## PHẦN 1 — CÂY QUYẾT ĐỊNH TOPOLOGY

### 1.1 6 khối kiến trúc nền
- **Augmented LLM**: LLM + retrieval + tool + memory.
- **Prompt Chaining**: Chuỗi bước tuần tự, output bước N là input bước N+1.
- **Routing**: Phân loại input, chuyển tới prompt/path chuyên biệt.
- **Parallelization**: Sectioning (chia sub-task độc lập song song) / Voting (chạy nhiều lần lấy đồng thuận).
- **Orchestrator-Workers**: Orchestrator phân rã task động lúc runtime.
- **Evaluator-Optimizer**: 1 LLM sinh, 1 LLM khác đánh giá lặp lại.
- **Autonomous Agent**: Vòng lặp tự trị với ground-truth feedback.

### 1.2 Cảnh báo Đa-agent (Cognition vs Anthropic)
- Sub-task PHỤ THUỘC quyết định lẫn nhau (style, kiến trúc, thiết kế chung) → Dùng 1 agent tuyến tính, context đầy đủ. KHÔNG chia đa-agent song song.
- Sub-task ĐỘC LẬP thật sự (breadth-first search, tra cứu độc lập) → Cân nhắc Orchestrator-Workers song song với 1 lead agent giữ quyền quyết định cuối.

---

## PHẦN 2 — STATE MACHINE & DEFINITION OF DONE

### 2.1 Node Anatomy — 5 thành phần bắt buộc
```
[STATE: <tên>]
[Input Artifacts]   — khoá dữ liệu node được đọc (Artifacts Isolation).
[Output Artifacts]  — khoá dữ liệu node ghi vào.
[DoD]               — checklist nhị phân, đo được, không cảm tính.
[Evaluation Loop]   — Evaluate → Fail→Revise / Pass→Done → transition kế tiếp.
```

### 2.2 Quy tắc viết DoD (3 Kiểm định)
1. **Nhị phân**: pass/fail rõ ràng.
2. **Đo được từ Output Artifact**: không hỏi context ngoài.
3. **Không dùng tính từ sáo ngữ**: "chuyên nghiệp/đầy đủ/tối ưu" phải quy ra con số hoặc có/không tồn tại.

---

## PHẦN 3 — CONTEXT ENGINEERING & ACI DESIGN

- **Attention budget**: Context là tài nguyên hữu hạn. Nhồi thêm context "cho chắc ăn" làm giảm performance.
- **Just-in-time retrieval**: Load full content lúc thật sự cần dùng thay vì pre-load toàn bộ.
- **Namespacing & Consolidate Tool**: Nhóm tool theo prefix service + resource. Gộp các operation hay đi cùng nhau thành 1 tool cấp cao hơn.

---

## PHẦN 4 — LONG-RUNNING WORKFLOW (ĐA PHIÊN)

- **2 Vai trò Tách biệt**: Initializer Agent (dựng feature list & init script ở phiên đầu) vs Coding/Execution Agent (đọc feature list, chọn 1 feature `passes:false` để làm ở các phiên sau).
- **Feature List JSON**: Ràng buộc `passes:boolean` ở cấp file.
- **Nghi thức Đầu phiên**: `pwd` ➔ Read progress & git log ➔ Read feature list ➔ Run `init.sh`.

---

## PHẦN 5 — GUARDRAILS & SAFE OUTPUTS

- **Risk Tiering**: Low/Medium/High dựa trên quyền read-only hay write, tính đảo ngược và tài chính.
- **Read-only default + Safe Outputs**: Mặc định read-only. Mọi hành động ghi phải qua danh sách `safe_outputs` khai báo trước trong Frontmatter YAML.

---

## PHẦN 6 — PRE-PUBLISH AUDIT CHECKLIST (11 BƯỚC)

- [ ] Đã chạy Complexity Ladder — xác nhận KHÔNG có giải pháp đơn giản hơn?
- [ ] Nếu có ≥ 2 agent song song: sub-tasks độc lập thật sự (breadth-first)?
- [ ] Mọi node đều đủ 5 thành phần (STATE / Input Artifacts / Output Artifacts / DoD / Evaluation Loop)?
- [ ] DoD qua 3 kiểm định (nhị phân, đo được, 0 tính từ sáo ngữ)?
- [ ] Áp dụng Just-in-Time retrieval và Tool Consolidation?
- [ ] Có nghi thức đầu phiên cho Long-running Workflows?
- [ ] Safe Outputs khai báo tường minh trong Frontmatter YAML?
