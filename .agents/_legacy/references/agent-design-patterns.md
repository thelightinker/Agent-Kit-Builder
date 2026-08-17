# Advanced Agent Prompt Patterns (Recalibrated)

> Reference guide detailing architectural prompt patterns for high-performing Agent Kit agents. Designed to maximize autonomy, prevent "Prompt Ceremony", and enforce domain-appropriate reasoning.

---

## 🏛️ The 4 Core Principles

```text
1. Ask when uncertainty materially changes the outcome.
2. Challenge defaults, not stability.
3. Fix causes, not symptoms.
4. Spend context where it creates leverage.
```

---

## 1. 📑 Quick Navigation Index (TOC Pattern)

### Overview
For complex **Standard** and **Professional** agents (prompts > 500 lines or covering multiple sub-domains), include a clickable Markdown index at the top of the prompt to enable rapid context routing.

### Template Snippet
```markdown
## 📑 Quick Navigation

### Strategic Execution
- [Core Philosophy & Mindset](#core-philosophy--mindset)
- [3-Tier Autonomy Gate](#-3-tier-autonomy-gate-mandatory)
- [Domain-Aware Mental Analysis](#-domain-aware-mental-analysis)

### Workflow & Decision Matrices
- [Execution Pipeline](#execution-pipeline)
- [Decision Matrix & Strategy](#decision-matrix--strategy)
- [Quality Control & Verification](#quality-control--verification)

### Guardrails
- [Hard Constraints & Anti-Defaults](#hard-constraints--anti-defaults)
- [Reality Check (Spirit Over Checklist)](#reality-check-anti-self-deception)
```

---

## 2. 🛑 3-Tier Autonomy Gate (Replacing Blind Clarification Gates)

### Overview
Prevents agent "autonomy paralysis" and avoids annoying the user with trivial questions. Calibrates when the agent must act immediately, when to act with documented assumptions, and when to Stop & Ask.

### Rule: Ask ONLY when uncertainty materially changes the outcome.

### 3-Tier Execution Matrix:
| Risk Tier | Task Characteristics | Agent Action | Example |
|:---|:---|:---|:---|
| **Tier A** (Low Risk / Reversible) | Minor UI tweaks, typo fixes, local refactors, explicit commands | **ACT IMMEDIATELY.** 0 questions. | *"Change button color to Dawn"* ➔ Execute immediately. |
| **Tier B** (Medium Risk / Defaults Exist) | Standard feature implementation where sensible defaults exist | **ACT AUTONOMOUSLY.** Proceed with sensible defaults + list assumptions in response. | *"Build REST API for User Profile"* ➔ Implement with standard schema + document assumptions. |
| **Tier C** (High Risk / Irreversible) | Structural architecture changes, high-cost external actions, destructive data ops | **STOP & ASK.** Ask clarifying questions ONLY if uncertainty materially alters outcome/risk. | *"Migrate database from Postgres to Mongo"* ➔ Ask to clarify data migration boundaries. |

---

## 3. 🧠 Domain-Aware Anti-Default Thinking (Replacing Blind Anti-Safe-Harbor)

### Overview
Prevents agents from defaulting to lazy clichés while avoiding "forced radicalism" where stability and boring technology are paramount.

### Core Mandate: Challenge defaults, not stability.

```text
❌ DO NOT pick a popular solution just because it is popular.
❌ DO NOT pick a new/radical solution just because it is new.

✅ Evaluate options based on: Outcome / Complexity / Risk ratio for the project.
```

### Domain-Specific Strategy:
- **UI/UX & Creative Domains**: Disrupt cliché layouts (Bento grids, AI-purple, standard SaaS splits) to foster distinct visual identities.
- **Backend, Security, & Infrastructure**: Prioritize **Boring & Stable Technology**. Choose proven, maintainable, and battle-tested patterns over shiny new frameworks.

---

## 4. 📐 Visual Reasoning & Strategy Matrices

### Overview
Uses ASCII flowcharts to map multi-phase workflows visually, combined with strategy lookup tables mapping symptoms to root-cause investigation techniques.

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: REPRODUCE & ISOLATE                               │
│  • Verify exact steps, error logs, and reproduction rate    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2: ROOT CAUSE ANALYSIS (5 WHYS)                      │
│  • Trace data flow upstream to identify underlying failure  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 3: FIX & VERIFY                                       │
│  • Fix root cause, run regression tests, verify zero side-fx│
└───────────────────────────┬─────────────────────────────────┘
```

---

## 5. 🛡️ Reality Check & Heuristic Context Leverage

### Reality Check (Spirit Over Checklist)
**Before marking any task complete, perform this reality audit:**
1. **Empirical Evidence First**: Did you execute verification commands (tests, builds, lints) and see actual passing logs? Editing a file is NOT completing a task.
2. **Fix Causes, Not Symptoms**: Did you resolve the root cause or just wrap a `try/catch` or mock fallback around the symptom?
3. **Zero Placeholder**: Are there any remaining `[TODO]`, `[TBD]`, or dummy blocks? Resolve them now.

### Heuristic Context Leverage ($ROI \ge 1.25$)
- View $ROI \ge 1.25$ as a **Heuristic Mental Rule** for context budget: spend token context where it creates high leverage (e.g. modular skills for complex tasks), while keeping Micro agents lean (< 300 words system prompt).
