# Recalibrate Agent Writing Standards Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Recalibrate the Agent Writing Standards across `c:\Users\nhdcb\OneDrive\Desktop\Agent Kit\Agent Kit Creator\.agents` to enforce the 4 core principles: Ask when uncertainty materially changes outcome, Challenge defaults not stability, Fix causes not symptoms, and Spend context where it creates leverage.

**Architecture:** Update reference patterns, templates, compiler skills, and generator agents to replace rigid clarification gates with a 3-Tier Autonomy Gate and replace blind Anti-Safe-Harbor rules with Domain-Aware Anti-Default Thinking.

**Tech Stack:** Markdown, Python validation scripts.

---

## Global Constraints

- Preserve 100% Antigravity IDE contract compatibility.
- Ensure `python .agents/scripts/validate_kit.py .agents` passes with 0 errors.

---

## Proposed Changes

### Reference Architecture

#### [MODIFY] [agent-design-patterns.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/agent-design-patterns.md)
- Replace Pattern 2 (`Deep Mental Analysis`) with **Domain-Aware Anti-Default Thinking**:
  - UI/UX & Creative: Disrupt cliché layouts.
  - Backend/Infra/Security: **Boring & Stable Tech First** (optimize `Outcome / Complexity / Risk`).
- Replace Pattern 3 (`Clarification Gate`) with **3-Tier Autonomy Gate**:
  - Tier A (Low Risk/Reversible): Act immediately, 0 questions.
  - Tier B (Medium Risk/Defaults Exist): Act autonomously + list Assumptions.
  - Tier C (High Risk/Irreversible): Stop & Ask only when uncertainty materially alters outcome.
- Update Pattern 5 & Token ROI definitions to **Heuristic Context Leverage**.

---

### Core Templates & Skills

#### [MODIFY] [agent-template.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/templates/agent-template.md)
- Replace rigid clarification placeholders with the `3-Tier Autonomy Gate` matrix and Domain-Aware Mental Analysis blocks.

#### [MODIFY] [compiling-prompts/SKILL.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/skills/compiling-prompts/SKILL.md)
- Update compilation rules to prevent prompt ceremony and guide 3-Tier Autonomy Gate integration.

#### [MODIFY] [prompt-engineering/SKILL.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/skills/prompt-engineering/SKILL.md)
- Update prompt architecture section to reflect 3-Tier Autonomy and Domain-Aware rules.

---

### Generator Agent & Manifest

#### [MODIFY] [kit-generator.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/agent/kit-generator.md)
- Update Component Generation System Prompt to inject 3-Tier Autonomy Gate and Domain-Aware thinking into generated agents.

#### [MODIFY] Manifest & Lockfile
- Run `python .agents/scripts/generate_manifest.py .agents` to update `manifest.json` and `manifest.lock.json`.

---

## Verification Plan

### Automated Tests
- Run `python .agents/scripts/validate_kit.py .agents` to verify zero validation errors.

### Manual Verification
- Review updated files for exact wording of the 4 core principles and zero prompt ceremony bloat.
