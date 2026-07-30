# Domain: Software Development

**Core Verbs**: design, implement, test, review, debug, deploy, document, refactor

---

## Outcome Patterns

| Vai trò | Core Competency |
|:--------|:----------------|
| Architect | System design, technology selection, pattern decisions |
| Developer | Implementation, code generation, feature building |
| Reviewer | Code quality, security, best practices enforcement |
| DevOps | Build, deploy, infrastructure, CI/CD |

---

## Typical Lenses

| Lens | Lý do áp dụng | Mức độ |
|:-----|:--------------|:-------|
| A — Token Efficiency | Codebase lớn → context window limited | Nên có |
| B — Adaptive Flexibility | Nhiều ngôn ngữ, framework, complexity levels | Nên có |
| C — Reliable Performance | Code sai = bug = downtime | Bắt buộc |
| D — Lean Context | Chỉ load file/module liên quan, không toàn bộ repo | Nên có |
| F — Safety & Escalation | Không tự deploy, không modify production | Bắt buộc |

---

## Quality Signals

- Code correctness: build passes, tests pass
- Convention compliance: follows project style, patterns
- Security: no known vulnerabilities introduced
- Documentation: changes documented appropriately

---

## Common Failure Modes

| Failure | Đòn bẩy khắc phục |
|:--------|:------------------|
| Hallucinated APIs | Hard constraint: verify API exists before using |
| Breaking existing code | Self-check: run tests before claiming done |
| Over-engineering | Scope guard: implement only what was asked |
| Ignoring existing patterns | Context load: read existing code patterns first |

---

## Domain-Specific Leverage (Dynamic Enhancement)

**Existing Pattern Adherence** là đòn bẩy đặc trưng cho domain này.
Cơ chế: trước khi implement, đọc existing codebase patterns:
- Naming conventions in use
- Architecture patterns (MVC, hexagonal, etc.)
- Test patterns (unit, integration style)
- Error handling conventions
→ Follow existing patterns > introduce new ones, trừ khi user explicitly yêu cầu.
