---
name: universal-rules
version: 1.0.0
priority: P0
trigger: always_on
description: "Rule universal-rules for Agent Kit Creator."
---

# Universal Rules (TIER 0) - AG Kit

> Always-active rules that apply to every request, regardless of domain.

---

## 🌐 Language Handling

When user's prompt is NOT in English:

1. **Internally translate** for better comprehension
2. **Respond in user's language** - match their communication
3. **Code comments/variables** remain in English

---

## 🧹 Clean Output Standard

- **Output**: Concise, direct, no over-engineering. Self-documenting.
- **Validation**: Binary Definition of Done (Pass / Fail).

---
