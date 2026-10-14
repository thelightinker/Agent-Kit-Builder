---
name: dynamic-routing
version: 2.5.0
priority: P1
trigger: always_on
description: "Phân loại Mode (Fast/Targeted/Deep/Refactor/Audit/Compression) và Capability Bundle dưới sự điều phối của Kit Architect."
---
# Dynamic Routing

Phân loại yêu cầu thành mode + capability bundle. Mọi quy trình xây dựng, tiến hóa và kiểm định Agent Kit đều do **Kit Architect (`@kit-architect`)** thống nhất điều phối.

## Mode Classifier
| Signal | Mode | Orchestrator & Role Profile Bundle | Workflow |
|:---|:---|:---|:---|
| Prompt 1-shot, Micro | `FAST_TRACK` | `@kit-architect` (`@compiler` + `prompt-compiling`) | — |
| Tạo/sửa 1 component đơn lẻ (Skill/Workflow/Rule/Memory) | `TARGETED_TRACK` | `@kit-architect` (1:1 Targeted Grounding: `@compiler` hoặc `@architect` + `skill-creator` nếu là Skill) | — |
| Multi-component, domain mới | `DEEP_TRACK` | `@kit-architect` (`@analyst` → `@compiler` → `@architect` kèm `skill-creator` → `kit-assembling` → `@auditor`) | `/create-kit` |
| Sửa/nâng cấp kit có sẵn | `REFACTOR_TRACK` | `@kit-architect` (`@architect` / `@compiler` kèm `skill-creator` nếu sửa skill → `@auditor`) | `/refactor-kit` |
| Audit/chấm điểm kit | `AUDIT_TRACK` | `@kit-architect` (`@auditor` + `kit-verifying`) | `/validate-kit` |
| Lưu bài học/pattern | `MEMORY_TRACK` | `@kit-architect` (`kit-evolving`) | `/remember-kit` |
| Tạo visual kit, HTML preview, dashboard, landing page, slide, UI/UX | `VISUAL_TRACK` | `@kit-architect` (`@designer` qua `ui-ux-pro-max` → `@auditor`) | `/create-visual` |
| Phiên dài 20+ turns, context bão hòa, log tool dài | `COMPRESSION_TRACK` | `context-compression` (Micro-compact, Phase summary, Session checkpoint) | — |


### Quy tắc Điều phối Bất biến
1. **Kit Architect Orchestrator Mandate**: Tuyệt đối không để Specialist Agent hoạt động độc lập không có chỉ đạo từ `@kit-architect`. Mọi thao tác tạo/sửa đều phải thuộc về 1 trong 5 Role Profiles (`@analyst`, `@compiler`, `@architect`, `@designer`, `@auditor`).
2. **Tech Level**: User low-tech → delegate `superpowers:brainstorming`. Tech user → xử lý trực tiếp.
3. **Tiering**: Đơn lẻ → Micro/FAST_TRACK hoặc TARGETED_TRACK. Nhiều component → Standard+/DEEP_TRACK.
4. **Bundle**: Chỉ nạp skill trong bundle chỉ định.

## Plugin & Skill Delegation
| Tình huống | Delegate tới |
|:---|:---|
| Clarify/brainstorm yêu cầu mơ hồ | `superpowers:brainstorming` |
| Tạo mới hoặc sửa đổi Skill bất kỳ | `skill-creator` (BẮT BUỘC nạp trước khi sinh file `SKILL.md`) |
| Thiết kế UI/UX, Design System, HTML Visual Kit, Dashboard, Slides | `ui-ux-pro-max` (`.agents/skills/ui-ux-pro-max/scripts/search.py`) |
| Nén context phiên dài / tóm tắt chặng | `context-compression` |
| Tạo/sửa rules, workflows, skills của workspace | `agy-customizations` |
| Tối giản hóa / audit over-engineering | `ponytail` |
| Export kit sang Antigravity Plugin / Cursor / Claude / OpenAI | `kit-exporting` |
