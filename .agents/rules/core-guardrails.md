---
name: core-guardrails
priority: P0
trigger: always_on
version: 2.7.0
description: "Core guardrails: workspace isolation, targeted grounding, sequential execution, verification feasibility."
---

# Core Guardrails

## 1. Không Gian & Thẩm Quyền (BẤT BIẾN)
- **Workspace Isolation:** Ghi kit theo thư mục chỉ định (mặc định `./output/`). CẤM ghi vào `.agents/` của Creator.
- **Orchestration Mandate:** Mọi hoạt động do `@kit-architect` điều phối qua 5 Profiles: `@analyst`, `@compiler`, `@architect`, `@designer`, `@auditor`.
- **Risk Tiers:** Tier 0 (Read/Inspect = zero gate) | Tier 1 (Scaffold/Gen = Evidence Gate) | Tier 2 (Sửa `.agents/` = Human Gate `gateStatus: approved_golden`).
- **Upgrade SSOT & Net System Gain:** Tuân thủ `UPGRADE_PRINCIPLES.md`. Chỉ nâng cấp khi $\text{Net Gain} = \text{Value} - \text{Complexity} > 0$. Cấm copy pattern riêng lẻ.

## 2. 5 Điều Răn Kiến Trúc P0 (BẤT BIẾN)
1. **Topology & Node-Contract Reconciliation:** Mọi Node có đúng 1 Role, 1 Skill. Node Audit bắt buộc $\text{Auditor} \ne \text{Author}$ (Zero Self-Audit). Cấm Split-Lifecycle God-Skills. Heuristic thuộc về đúng Role.
2. **Verification Feasibility (Cấm Pseudo-Metrics):** Cấm đưa số thập phân (`hedge-ratio > 0.04`, `sentence-CV < 0.3`) vào prompt nếu không có script đo đạc. Định lượng = script; Định tính = checklist rubric cụ thể. Binary DoD: 100% nhị phân, 0 tính từ cảm tính.
3. **Sequential Context Isolation (SEQ-001 đến SEQ-008):** Duy nhất 1 Active Agent/turn. Cấm multi-agent bundling. Precondition đạt `DONE`/`PASS` mới chuyển vai. Bắt buộc `[CONTEXT_RESET]` khi đổi vai. Bàn giao 100% qua file đĩa. Cấm sinh văn xuôi/logic song song. `Shared Skill != Shared Context`.
4. **Legacy Intake & Tri-Bucket Scope:** Phân loại 100% tham chiếu vào 3 rổ: `Preserve` (giữ), `Merge/Abstract` (gộp), `Cut/Non-Goal` (cắt). Bắt buộc có mục `## Non-Goals & Intentional Scope Boundaries` trong README/ARCHITECTURE.
5. **Executable Script Smoke Test:** 100% script Python đi kèm kit phải pass AST parse và chạy thử CLI `--help` qua subprocess trả về exit code 0. Zero third-party dependency leak nếu tuyên bố stdlib.

## 3. Grounding & Rào Chắn Cấu Trúc (1:1 Mapping)
- **Targeted Grounding (1:1):** Workflow $\rightarrow$ `workflow-template.md` | Orchestrator $\rightarrow$ `orchestrator-template.md` | Specialist $\rightarrow$ `agent-template.md` | Skill $\rightarrow$ `skill-creator` + `skill-template.md` | Rule $\rightarrow$ `rule-template.md` | Memory $\rightarrow$ `memory-template.md` | Manifest $\rightarrow$ `manifest-template.json` | UI $\rightarrow$ `ui-ux-pro-max` + `design-spec-template.md`. Anti-spam: không đọc lại nếu đã có trong context.
- **Skill Generation Gate:** Bắt buộc nạp `skill-creator` trước khi tạo/sửa `SKILL.md`. Description pushy có `when_to_use`, anatomy 3 tầng, hướng dẫn lối mệnh lệnh (Imperative + "Why" + I/O examples). Guideline: giữ body tinh gọn, đẩy tra cứu sâu sang `references/`.
- **Worker Briefing Contract:** Không ủy quyền mù quáng ("Never Delegate Understanding"). Đủ 5 phần: Goal & Context, Ruled Out, File Scope, Negative Boundaries, Verification Evidence.
- **Visual & UX Gate:** Bắt buộc sinh `DESIGN.md` token SSOT trước khi code UI. Contrast $\ge 4.5:1$, touch $\ge 44\text{px}$, SVG icons (cấm emoji), Purple Ban (cấm gradient tím).
- **Central Feedback Hub:** Append-only event stream vào `Feedback/kit_feedback.jsonl`. Trạng thái `fixed` chỉ đóng khi đã `verified`.
- **Output:** Khớp ngôn ngữ user. Code/comments: English. Tóm tắt 3-5 dòng đời thường đầu output. Link file dạng `file:///...`.