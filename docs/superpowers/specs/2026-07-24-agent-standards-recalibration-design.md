# Design Spec: Recalibration of Agent Writing Standards

> **Goal:** Recalibrate the Agent Writing Standards in Agent Kit Creator to eliminate "Prompt Ceremony" and "Autonomy Paralysis", balancing autonomy, safety, domain-appropriate thinking, and context leverage.

---

## 4 Core Philosophies

1. **Ask when uncertainty materially changes the outcome.**
2. **Challenge defaults, not stability.**
3. **Fix causes, not symptoms.**
4. **Spend context where it creates leverage.**

---

## Key Recalibrations

### 1. 3-Tier Autonomy Gate (Replacing Blind Clarification Gates)
When user prompts lack specifications:
- **Tier A (Low Risk / Reversible / Minor Scope)**: Act immediately with zero questions (e.g., "Change button color to Dawn").
- **Tier B (Medium Risk / Reasonable Defaults Exist)**: Proceed autonomously + explicitly document assumptions in output.
- **Tier C (High Risk / Irreversible / High Impact)**: Dừng lại hỏi người dùng (`Stop & Ask`) ONLY when uncertainty materially changes the outcome.

### 2. Domain-Aware Anti-Default Thinking (Replacing Blind Anti-Safe-Harbor)
- **UI/UX & Creative Domains**: Challenge cliché layouts (e.g., standard bento grids, AI-purple) to foster unique aesthetic identities.
- **Backend, Security, Infrastructure Domains**: Prioritize **Boring & Stable Technology**. Never pick a new stack just because it's new. Select the optimal `Outcome / Complexity / Risk` ratio.

### 3. Heuristic Token ROI
- Treat $ROI \ge 1.25$ as a heuristic mental rule for context leverage (Micro = lean prompt, Standard/Professional = modular context leverage), NOT as a literal LLM math calculation.

---

## Affected Component Specifications

1. **`.agents/references/agent-design-patterns.md`**:
   - Refactor Pattern 2 (`Deep Mental Analysis`) to include Domain-Aware Anti-Default rules.
   - Refactor Pattern 3 (`Clarification Gate`) to the `3-Tier Autonomy Gate`.
   - Update Token ROI definitions to Heuristic Context Leverage.

2. **`.agents/templates/agent-template.md`**:
   - Update template placeholders to reflect the `3-Tier Autonomy Gate` and Domain-Aware thinking.

3. **`.agents/skills/compiling-prompts/SKILL.md` & `.agents/skills/prompt-engineering/SKILL.md`**:
   - Update compilation guidelines to enforce autonomy balance and prevent prompt bloat.

4. **`.agents/agent/kit-generator.md`**:
   - Update generation rules so generated agents select the right autonomy and domain patterns.
