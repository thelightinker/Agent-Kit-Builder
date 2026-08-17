# Component Contracts & Technical Specifications

> Đặc tả kỹ thuật, cấu trúc YAML Frontmatter và chuẩn thiết kế Tool / ACI cho toàn bộ các thành phần trong Agent Kit.

---

## 1. AGENT CONTRACT (`agent/<name>.md`)

Mọi System Prompt của Agent bắt buộc tuân thủ cấu trúc 4 khối cốt lõi:

```yaml
---
name: kebab-case-name
description: "Vai trò và năng lực của agent."
tools: Read, Grep, Glob, Edit, Write, Bash
model: inherit
skills: [skill-a, skill-b]
version: 1.0.0
---
# [TÊN AGENT]

## TÓM TẮT CHO NGƯỜI DÙNG
[3-5 dòng ngôn ngữ đời thường: Làm gì / Dùng khi nào / Giới hạn. 0 biệt ngữ AI.]

---

# SYSTEM PROMPT: [TÊN AGENT]
## 1. VAI TRÒ & DEFINITION OF DONE (DoD)
## 2. QUY TRÌNH XỬ LÝ & MA TRẬN HÀNH ĐỘNG
## 3. HARD CONSTRAINTS (RÀNG BUỘC PHỦ ĐỊNH)
## 4. FORMAT ĐẦU RA (OUTPUT TEMPLATE)
```

---

## 2. SKILL CONTRACT (`skills/<name>/SKILL.md`)

```yaml
---
name: kebab-case-name
description: >
  Mô tả năng lực và bối cảnh trigger. Viết pushy và cụ thể.
when_to_use: "Điều kiện khi nào cần nạp skill này."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---
# [Tên Skill]

## 1. QUY TRÌNH HƯỚNG DẪN (IMPERATIVE)
## 2. EXAMPLES MINH HỌA
## 3. CHECKLIST KIỂM THỬ
```

*Progressive Disclosure:* `SKILL.md` giữ dưới 500 dòng. Chi tiết tra cứu dài > 300 dòng bắt buộc tách sang `references/`.

---

## 3. WORKFLOW CONTRACT (`workflows/<name>.md`)

```yaml
---
name: kebab-case-name
description: "Mô tả mục đích của workflow."
version: 1.0.0
requires_agents: kit-architect
requires_skills: [skill-a, skill-b]
artifact_outputs: [output-name]
---
# Workflow: [Tên Workflow]

## Các bước thực hiện (State Machine Nodes)
### Bước 1: [Tên State]
- [Input Artifacts]: ...
- [Output Artifacts]: ...
- [DoD]: Tiêu chí nhị phân
- [Evaluation Loop]: Pass ➔ Bước 2 | Fail ➔ Revise | Quá Max Retry ➔ ESCALATE_HUMAN
```

---

## 4. MEMORY CONTRACT (`memory/`)

- `MEMORY.md`: File chỉ mục chính, giới hạn nghiêm ngặt **$\le 200$ dòng**.
- Các topic files (`project-conventions.md`, `user-preferences.md`, `tech-decisions.md`, `feedback-history.md`, `kit-patterns.md`).
- `golden-examples/`: Chứa các mẫu Agent Kit hoàn chỉnh đạt 5/5 ⭐.

---

## 5. THIẾT KẾ TOOL & ACI (AGENT-COMPUTER INTERFACE)

- **Namespacing**: Đặt tên tool theo tiền tố phân cấp rõ ràng (ví dụ: `git_commit`, `db_query_logs`).
- **Consolidated Tools**: Gộp các thao tác hay đi liền nhau thành 1 tool cấp cao thay vì phân mảnh thành nhiều tool nhỏ gây nhầm lẫn cho LLM.
- **Tối giản Output**: Tool chỉ trả về phần dữ liệu liên quan kèm ngữ cảnh cần thiết, tránh trả toàn bộ raw log khổng lồ gây context rot.
- **Phân quyền An toàn**: Phân định rõ công cụ chỉ đọc (read-only) và công cụ có khả năng thay đổi trạng thái (state-modifying/destructive).
