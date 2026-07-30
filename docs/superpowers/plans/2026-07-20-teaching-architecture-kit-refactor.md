# Implementation Plan: Deep References & Intuitive Agent Refactoring

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extract deep reference knowledge from source materials into 4 functional `references/` sub-files, rename agents to highly intuitive English names, and remove external book title references across the kit in `./output/teaching-architecture-kit/`.

**Architecture:** Pure functional naming. Deep principles from source files are fully internalized into standalone domain reference guides without referencing book authors or titles.

**Tech Stack:** Antigravity Agent Kit Standard (YAML Frontmatter, Markdown Instructions, References).

## Global Constraints

- Isolation: All changes MUST strictly occur inside `./output/teaching-architecture-kit/`.
- Intuitive English Agent Names:
  - `teaching-orchestrator.md` $\to$ `master-director.md`
  - `content-strategist.md` $\to$ `message-architect.md`
  - `narrative-director.md` $\to$ `story-director.md`
  - `multi-format-transpiler.md` $\to$ `format-transpiler.md`
- Functional Reference Naming (No Book Titles):
  - `transformational-storytelling.md`
  - `high-stickiness-messaging.md`
  - `relational-resonance-framework.md`
  - `mindset-interrupt-patterns.md`

---

### Task 1: Refactor Agent Names & Manifest
**Files:**
- Rename/Re-create:
  - `./output/teaching-architecture-kit/agent/master-director.md`
  - `./output/teaching-architecture-kit/agent/message-architect.md`
  - `./output/teaching-architecture-kit/agent/story-director.md`
  - `./output/teaching-architecture-kit/agent/format-transpiler.md`
- Delete old agent files in `./output/teaching-architecture-kit/agent/`
- Modify: `./output/teaching-architecture-kit/manifest.json`

- [ ] **Step 1: Create 4 intuitively named Agent files**
  Write system prompts for `master-director.md`, `message-architect.md`, `story-director.md`, and `format-transpiler.md` without book title references.
- [ ] **Step 2: Clean old agent files**
- [ ] **Step 3: Update `manifest.json`** to reflect new agent paths and updated descriptions.

---

### Task 2: Create Deep Reference Knowledge Files
**Files:**
- Create: `./output/teaching-architecture-kit/skills/storyworthy-hammer-crafting/references/transformational-storytelling.md`
- Create: `./output/teaching-architecture-kit/skills/thesis-nail-extractor/references/high-stickiness-messaging.md`
- Create: `./output/teaching-architecture-kit/skills/resonant-experience-designer/references/relational-resonance-framework.md`
- Create: `./output/teaching-architecture-kit/skills/tnt-mindset-framing/references/mindset-interrupt-patterns.md`

- [ ] **Step 1: Write `transformational-storytelling.md`**
  Extract deep storytelling principles: 5-second moment, Homework for Life, Dinner Table Test, stakes escalation, opposite beginnings.
- [ ] **Step 2: Write `high-stickiness-messaging.md`**
  Extract deep messaging principles: Curiosity gap, schema violation, concrete sensory anchors, core thesis minimalism.
- [ ] **Step 3: Write `relational-resonance-framework.md`**
  Extract deep resonance principles: 4-phase relational space, energy pacing, time domination removal, uncoerced transformation.
- [ ] **Step 4: Write `mindset-interrupt-patterns.md`**
  Extract deep mindset framing patterns: S0 to S1 transition, pattern interrupt techniques, pain avoidance vs reward pursuit.

---

### Task 3: Clean Rules, Workflows, & Skills of Book References
**Files:**
- Modify: `./output/teaching-architecture-kit/rules/core-teaching-principles.md`
- Modify: All 8 `SKILL.md` files
- Modify: All 4 `workflows/*.md` files

- [ ] **Step 1: Update `core-teaching-principles.md`** to remove any book title references and use pure functional principle terms.
- [ ] **Step 2: Update SKILL.md files and Workflows** to link to the new `references/` files and use the new agent names (`master-director`, `message-architect`, `story-director`, `format-transpiler`).

---

### Task 4: Final Validation Audit
- [ ] **Step 1: Validate directory structure & manifest**
- [ ] **Step 2: Verify zero external book references remain in the kit**
