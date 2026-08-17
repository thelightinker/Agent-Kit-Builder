---
name: sample_state_machine_workflow
description: "Mẫu workflow tham khảo chuẩn State Machine áp dụng AGENT WORKFLOW MASTER FRAMEWORK."
version: 1.2.0
requires_agents: [orchestrator, architect, writer]
requires_skills: [book-architect, book-writer]
artifact_outputs: [BOOK_DNA.json, drafts/chapter_01.md]
topology: orchestrator-workers
trigger: manual
permissions: read-only
tools_allowed: [read_file, write_file]
safe_outputs:
  create_dna: "BOOK_DNA.json"
  write_draft: "drafts/chapter_*.md"
max_retry_per_node: 2
---

# Workflow Mẫu: Từ Ý Tưởng Đến Bản Thảo Chương 1

> **Mục tiêu**: Hướng dẫn Agent tạo Concept và viết bản thảo Chương 1 theo quy trình State Machine khép kín.

---

## 🔄 State Machine & Node Execution

### [STATE: CP-1_MARKET_POSITIONING]
- **Input Artifacts**: `author_profile.md`
- **Output Artifacts**: `positioning_options`
- **Definition of Done (DoD)**:
  - [ ] Tìm kiếm ít nhất 3 sách đối thủ trên thị trường.
  - [ ] Liệt kê 3 điểm yếu lớn nhất của đối thủ từ đánh giá 2-3 sao.
  - [ ] Xuất 3 Option góc tiếp cận độc đáo (Thực chiến, Phản trực giác, Liên ngành).
- **Evaluation Loop & Transition**:
  - Evaluate ➔ Pass ➔ Transition sang `[STATE: CP-2_CONCEPT_FORMULATION]`
  - Fail ➔ Revise (Tối đa 2 lần) ➔ Vượt ngưỡng ➔ `[ESCALATE_HUMAN]`

---

### [STATE: CP-2_CONCEPT_FORMULATION]
- **Input Artifacts**: `selected_option`
- **Output Artifacts**: `BOOK_DNA.json`
- **Definition of Done (DoD)**:
  - [ ] Đúc kết câu định vị S.I.G.I 1 câu duy nhất.
  - [ ] Ghi nhận toàn bộ thông số vào tệp `BOOK_DNA.json`.
- **Evaluation Loop & Transition**:
  - Evaluate ➔ Pass ➔ Transition sang `[STATE: CP-3_DRAFTING]`

---

### [STATE: NODE_FINALIZE]
- **Input Artifacts**: `BOOK_DNA.json`, `drafts/chapter_01.md`
- **Output Artifacts**: Deliverable hoàn chỉnh
- **Definition of Done (DoD)**:
  - [ ] Không có mâu thuẫn giữa BOOK_DNA và nội dung chương 1.
  - [ ] File nháp nằm đúng vị trí trong thư mục safe_outputs.
- **Evaluation Loop**: Evaluate ➔ Pass ➔ Done ➔ `[*]`.

---

## 🚨 [ESCALATE_HUMAN]

- **Kích hoạt khi**: Node fail DoD vượt quá 2 lần.
- **Output**: Bản thảo hiện tại + Log lý do fail + `needs_human_review: true`.
- **Constraint**: KHÔNG tự động publish khi ở trạng thái này.
