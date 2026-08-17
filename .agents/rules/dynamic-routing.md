---
name: dynamic-routing
version: 2.0.0
priority: P1
trigger: always_on
description: "Phân loại Mode (Fast/Deep/Refactor/Audit) và Capability Bundle."
---
# Dynamic Routing

Phân loại yêu cầu thành mode + capability bundle.

## Mode Classifier
| Signal | Mode | Capability Bundle | Workflow |
|:---|:---|:---|:---|
| Prompt 1-shot, Micro | `FAST_TRACK` | `prompt-compiling` | — |
| Multi-component, domain mới | `DEEP_TRACK` | `domain-profiling` → `prompt-compiling` → `skill-architecting` → `kit-assembling` → `kit-verifying` | `/create-kit` |
| Sửa/nâng cấp kit có sẵn | `REFACTOR_TRACK` | `kit-evolving` → `kit-verifying` | `/refactor-kit` |
| Audit/chấm điểm kit | `AUDIT_TRACK` | `kit-verifying` | `/validate-kit` |
| Lưu bài học/pattern | `MEMORY_TRACK` | `kit-evolving` | `/remember-kit` |

### Quy tắc
1. **Tech Level**: User low-tech → delegate `superpowers:brainstorming`. Tech user → xử lý trực tiếp.
2. **Tiering**: Đơn lẻ → Micro/FAST_TRACK. Nhiều component → Standard+/DEEP_TRACK.
3. **Bundle**: Chỉ nạp skill trong bundle chỉ định.

## Plugin Delegation
| Tình huống | Delegate tới |
|:---|:---|
| Clarify/brainstorm yêu cầu mơ hồ | `superpowers:brainstorming` |
| Tạo/sửa rules, workflows, skills của workspace | `agy-customizations` |
| Tối giản hóa / audit over-engineering | `ponytail` |
| Export kit sang Cursor/Claude/OpenAI | `kit-exporting` |
