# Agent Kit Creator

Agent Kit Creator là bộ công cụ chuyên dụng để tư vấn, thiết kế, xây dựng, cải tiến và kiểm định chất lượng các **Agent Kit** cho các mô hình AI Agent (Gemini, Claude, Antigravity IDE, Cursor, v.v.).

## Quick start

1. Nắm 3 Core Rules:
   - `.agents/rules/core-guardrails.md`: Workspace isolation (`./output/<kit-name>/`), binary DoD, progressive disclosure.
   - `.agents/rules/dynamic-routing.md`: Mode classification (`FAST_TRACK`, `TARGETED_TRACK`, `DEEP_TRACK`, `REFACTOR_TRACK`, `AUDIT_TRACK`, `MEMORY_TRACK`, `COMPRESSION_TRACK`).

   - `.agents/rules/collaboration-protocol.md`: Grounding Gate, HUD Protocol, High-Automation Flow.
2. Định tuyến yêu cầu qua 4 Workflows:
   - `/create-kit`: Tạo Agent Kit mới từ đầu (Deep Track)
   - `/refactor-kit`: Cải tiến & nâng cấp Agent Kit sẵn có
   - `/validate-kit`: Kiểm định chất lượng 3 lớp & chấm điểm Rubric 5 sao
   - `/remember-kit`: Lưu đúc rút kinh nghiệm vào bộ nhớ dài hạn `MEMORY.md`
3. Kiểm định Agent Kit:

```bash
python .agents/scripts/generate_manifest.py
python .agents/scripts/dependency_graph.py
python .agents/scripts/validate_kit.py
```

## Core concepts

- **Orchestrator (1)**: `kit-architect` với 5 Dynamic Role Profiles (`@analyst`, `@compiler`, `@architect`, `@designer`, `@auditor`).
- **Focused Skills (8)**: `domain-profiling`, `prompt-compiling`, `skill-architecting`, `context-compression`, `kit-assembling`, `kit-verifying`, `kit-exporting`, `kit-evolving`.
- **Workflows (4)**: `/create-kit`, `/refactor-kit`, `/validate-kit`, `/remember-kit`.


- **Core Rules (3)**: `core-guardrails` (P0 invariants), `dynamic-routing` (mode selector), `collaboration-protocol` (grounding & HUD).
- **Workspace Isolation (BẤT BIẾN)**: Mọi kit đầu ra bắt buộc lưu tại `./output/<kit-name>/`.
- **Decision vs Execution**: Role `@auditor` quyết định phạm vi kiểm thử; Python scripts thực thi kiểm định tất định.

## Context Footprint (Read-set Footprint)

Số đo byte thô của các read-set theo mode từ `readsets.json` (chưa phải token):

| Mode | Context Footprint (Raw Bytes) | Ghi chú |
|:---|:---:|:---|
| `micro` | 128,876 B | Tối giản: 1 agent, không workflow phức tạp |
| `standard` | 140,962 B | `micro` + `outcome-lenses` + `workflow-template` |
| `mini_suite` | 156,439 B | `standard` + `orchestrator-template` + `prompt-compiling-suite` |
| `full_suite` | 163,988 B | `mini_suite` + `multi-agent-orchestration` |

## Documentation

- [Architecture and inventory](ARCHITECTURE.md)
- [Generated dependency graph](DEPENDENCY_GRAPH.md)
- [Runtime scripts](scripts/README.md)
- [AI Onboarding Guide](AI_ONBOARDING.md)
