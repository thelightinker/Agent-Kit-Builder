# Next-Gen Teaching Architecture Kit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete, production-ready Multi-Agent Suite Kit (`Resonant-Teaching-OS`) in `./output/teaching-architecture-kit/` featuring 4 specialist agents, 8 dedicated skills, 2 system rules, 4 workflows, and `manifest.json`.

**Architecture:** A modular Agent Suite Kit combining TNT 2.0, Made to Stick, Storyworthy, and Rosa's Resonance frameworks. The `teaching-orchestrator` agent manages input diagnostics and quality auditing, delegating content, narrative, and multi-format transpilation to specialist agents.

**Tech Stack:** Antigravity Agent Kit Standard (YAML Frontmatter, Markdown Instructions, JSON Manifest).

## Global Constraints

- Isolation: All output files MUST be created strictly under `./output/teaching-architecture-kit/`.
- Zero External References: The generated kit must contain full distilled domain logic and operate 100% independently of source files.
- Agent-to-Skill Mapping: 4 Agents, each owning exactly 2 dedicated skills (8 skills total).
- Frontmatter Standard: All `.md` files must use standard YAML frontmatter bounded by `---`.

---

### Task 1: Scaffolding Workspace & Manifest
**Files:**
- Create: `./output/teaching-architecture-kit/manifest.json`

- [ ] **Step 1: Create directory tree**
  Create directories:
  - `./output/teaching-architecture-kit/agent/`
  - `./output/teaching-architecture-kit/rules/`
  - `./output/teaching-architecture-kit/skills/`
  - `./output/teaching-architecture-kit/workflows/`

- [ ] **Step 2: Create `manifest.json`**
  Write complete manifest with schema version 2.0.0, referencing all 4 agents, 8 skills, 2 rules, and 4 workflows.

---

### Task 2: System Rules
**Files:**
- Create: `./output/teaching-architecture-kit/rules/core-teaching-principles.md`
- Create: `./output/teaching-architecture-kit/rules/slide-zero-textdump.md`

- [ ] **Step 1: Write `core-teaching-principles.md`**
  Define P0 rules for TNT 2.0, Made to Stick SUCCESs filters, Storyworthy 5s moments, and Hartmut Rosa resonance.
- [ ] **Step 2: Write `slide-zero-textdump.md`**
  Define strict constraints against bullet walls on slides, enforcing visual anchor + keyphrase density.

---

### Task 3: Agent 1 (`teaching-orchestrator`) & its 2 Skills
**Files:**
- Create: `./output/teaching-architecture-kit/agent/teaching-orchestrator.md`
- Create: `./output/teaching-architecture-kit/skills/diagnostic-gap-evaluator/SKILL.md`
- Create: `./output/teaching-architecture-kit/skills/quality-resonance-auditor/SKILL.md`

- [ ] **Step 1: Write `SKILL.md` for `diagnostic-gap-evaluator`**
  Define evaluation algorithm for Knowledge, Audience, Message, Experience, and Format.
- [ ] **Step 2: Write `SKILL.md` for `quality-resonance-auditor`**
  Define 3-layer audit protocol (Structural, 5-Star Rubric, Adversarial Stress Test).
- [ ] **Step 3: Write `teaching-orchestrator.md`**
  System prompt for Orchestrator Agent linking the 2 skills.

---

### Task 4: Agent 2 (`content-strategist`) & its 2 Skills
**Files:**
- Create: `./output/teaching-architecture-kit/agent/content-strategist.md`
- Create: `./output/teaching-architecture-kit/skills/tnt-mindset-framing/SKILL.md`
- Create: `./output/teaching-architecture-kit/skills/thesis-nail-extractor/SKILL.md`

- [ ] **Step 1: Write `SKILL.md` for `tnt-mindset-framing`**
  Define mindset reframing ($S_0 \to S_1$) and pattern interruption.
- [ ] **Step 2: Write `SKILL.md` for `thesis-nail-extractor`**
  Define core thesis nail extraction and Made to Stick SUCCESs validation.
- [ ] **Step 3: Write `content-strategist.md`**
  System prompt for Content Strategist Agent.

---

### Task 5: Agent 3 (`narrative-director`) & its 2 Skills
**Files:**
- Create: `./output/teaching-architecture-kit/agent/narrative-director.md`
- Create: `./output/teaching-architecture-kit/skills/storyworthy-hammer-crafting/SKILL.md`
- Create: `./output/teaching-architecture-kit/skills/resonant-experience-designer/SKILL.md`

- [ ] **Step 1: Write `SKILL.md` for `storyworthy-hammer-crafting`**
  Define 5-second moment story scripting, stakes, and visual metaphors.
- [ ] **Step 2: Write `SKILL.md` for `resonant-experience-designer`**
  Define Hartmut Rosa 4-phase resonance, energy pacing, and audience interaction loops.
- [ ] **Step 3: Write `narrative-director.md`**
  System prompt for Narrative Director Agent.

---

### Task 6: Agent 4 (`multi-format-transpiler`) & its 2 Skills
**Files:**
- Create: `./output/teaching-architecture-kit/agent/multi-format-transpiler.md`
- Create: `./output/teaching-architecture-kit/skills/visual-slide-transpiler/SKILL.md`
- Create: `./output/teaching-architecture-kit/skills/multi-deliverable-exporter/SKILL.md`

- [ ] **Step 1: Write `SKILL.md` for `visual-slide-transpiler`**
  Define visual slide transpilation rules, layout specs, and visual anchor extraction.
- [ ] **Step 2: Write `SKILL.md` for `multi-deliverable-exporter`**
  Define transpilation mapping across Keynotes, Workshops, Courses, and Handouts.
- [ ] **Step 3: Write `multi-format-transpiler.md`**
  System prompt for Multi-Format Transpiler Agent.

---

### Task 7: Workflows & Final Validation
**Files:**
- Create: `./output/teaching-architecture-kit/workflows/auto-teach.md`
- Create: `./output/teaching-architecture-kit/workflows/create-from-scratch.md`
- Create: `./output/teaching-architecture-kit/workflows/refactor-existing.md`
- Create: `./output/teaching-architecture-kit/workflows/transpile-format.md`

- [ ] **Step 1: Write the 4 Workflows**
  Write step-by-step instructions for auto-teach, create-from-scratch, refactor-existing, and transpile-format.
- [ ] **Step 2: Execute validation audit**
  Audit the generated kit in `./output/teaching-architecture-kit/` using `/validate-kit` rubrics to ensure 5-star quality.
