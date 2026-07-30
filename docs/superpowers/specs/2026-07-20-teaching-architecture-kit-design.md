# Design Specification: Next-Gen Teaching Architecture Kit (Resonant-Teaching-OS)

**Date:** 2026-07-20  
**Target Location:** `./output/teaching-architecture-kit/`  
**Kit Type:** Multi-Agent Suite Kit (Professional Grade)  

---

## 1. Executive Summary & Core Philosophy

The **Teaching Architecture Kit thế hệ mới** (`Resonant-Teaching-OS`) is a standalone operating system for converting raw knowledge, ideas, audience problems, or existing drafts into high-resonance educational and communicative experiences (Keynotes, Workshops, Online Courses, Lectures, Visual Slides, and Workbook Handouts).

Rather than relying on linear 7-step checklists or static templates, `Resonant-Teaching-OS` integrates four foundational frameworks:
1. **TNT 2.0 Core (FuSuSu Extended)**: Mindset Interrupt ($S_0 \to S_1$), Need Anchoring, Single Thesis Nail, and 4-Layer Illustration Hammers.
2. **Made to Stick (Heath Brothers)**: SUCCESs filter (Simple, Unexpected, Concrete, Credible, Emotional, Story) for content durability.
3. **Storyworthy (Matthew Dicks)**: The 5-Second Moment of transformation, stakes escalation, and location-anchored sensory details.
4. **Resonance Experience Design (Hartmut Rosa)**: The 4-phase relational space (*Afreado* $\to$ *Anverwandlung* $\to$ *Transformation* $\to$ *Unverfügbarkeit*).

---

## 2. Multi-Agent Suite Architecture

The kit is composed of **4 Specialist Agents**, each equipped with exactly **2 dedicated skills** (8 skills total):

```
+-------------------------------------------------------------------------------+
|                         teaching-orchestrator                                 |
|  Skills: [diagnostic-gap-evaluator, quality-resonance-auditor]                |
+------------------------+------------------------------------+-----------------+
                         |                                    |
                         v                                    v
+----------------------------------+        +-----------------------------------+
|        content-strategist        |        |         narrative-director        |
| Skills: [tnt-mindset-framing,    |        | Skills: [storyworthy-hammer-craft,|
|          thesis-nail-extractor]  |        |  resonant-experience-designer]    |
+----------------------------------+        +-----------------------------------+
                         |                                    |
                         +-----------------+------------------+
                                           |
                                           v
                        +-------------------------------------+
                        |        multi-format-transpiler      |
                        | Skills: [visual-slide-transpiler,   |
                        |          multi-deliverable-exporter]|
                        +-------------------------------------+
```

### Agent Roles & Skills Summary:

1. **`teaching-orchestrator.md`** (Chief Teaching Architect)
   - *Role*: Master Diagnostic, Gap Analysis, Strategy Router & Quality Controller.
   - *Skill 1*: `diagnostic-gap-evaluator` (Evaluates 5 state variables: Knowledge, Audience, Message, Experience, Format; routes dynamic workflows for partial/mixed inputs).
   - *Skill 2*: `quality-resonance-auditor` (Executes 3-layer audit: Structural, 5-Star Semantic Rubric, Adversarial Stress Testing).

2. **`content-strategist.md`** (Mindset & Core Message Strategist)
   - *Role*: Content extraction, mindset reframing, and Core Thesis Nail forging.
   - *Skill 1*: `tnt-mindset-framing` (Reframes audience assumptions from $S_0$ to $S_1$, bridges pain points).
   - *Skill 2*: `thesis-nail-extractor` (Extracts single sharp thesis, validates through SUCCESs filters).

3. **`narrative-director.md`** (Story & Experience Director)
   - *Role*: Illustration hammer forging, emotional resonance, and interactive dynamics.
   - *Skill 1*: `storyworthy-hammer-crafting` (Crafts 5-second transformational stories, stakes, and vivid metaphors).
   - *Skill 2*: `resonant-experience-designer` (Engineers 4-phase Hartmut Rosa resonance loops, pacing, and interaction spikes).

4. **`multi-format-transpiler.md`** (Visual & Format Transpiler)
   - *Role*: Transpiling content primitives into specific output artifacts.
   - *Skill 1*: `visual-slide-transpiler` (Applies absolute *Zero Text-Dump* rule, extracts visual anchors and minimal keyphrases for slides).
   - *Skill 2*: `multi-deliverable-exporter` (Transpiles primitives across Keynote Talk, Workshop Curriculum, Course Syllabus, and Handout Workbook).

---

## 3. The 6 Dynamic Entry Points & Auto-Diagnosis

The system handles inputs at any state through **Entry Point 6 (Adaptive Diagnostic Router)**:
1. `From Knowledge / Idea`: Raw topics/frameworks $\to$ System asks targeted questions to map audience and message.
2. `From Audience / Problem / Goal`: Pain points $\to$ System works backwards from $S_1$ target state.
3. `From Existing Content`: Drafts/outlines $\to$ System refactors and elevates to 5-star quality.
4. `From Existing Presentation`: Old slides $\to$ System audits, strips text dumps, and re-architects narrative.
5. `From Format Conversion`: Finished output $\to$ Transpiles across Talk $\leftrightarrow$ Workshop $\leftrightarrow$ Course $\leftrightarrow$ Handout.
6. `From Partial / Mixed Inputs` (**Primary Entry**): User inputs any raw combination $\to$ Diagnostic Engine evaluates state vector ($K, A, M, E, F$) and auto-routes the exact execution pipeline.

---

## 4. Multi-Format Transpilation & Primitives

All content is parsed into 4 Content Primitives:
- **`P_thesis`**: Sharp Core Thesis statement.
- **`P_visual`**: Visual/Sensory Anchor (diagrams, metaphors, iconography).
- **`P_narrative`**: Story script, verbal cues, 5-second moment.
- **`P_interactive`**: Action prompts, exercise templates, reflection questions.

Output mappings:
- **Slide Deck**: `P_visual` + Minimal `P_thesis` (Max 7 words per slide, zero bullet walls).
- **Keynote / Talk**: `P_narrative` + `P_thesis` + `P_visual` cue.
- **Workshop**: `P_interactive` (60%) + `P_thesis` (20%) + `P_narrative` (20%).
- **Course System**: Hierarchical `P_thesis` map + `P_narrative` + `P_interactive` quizzes.
- **Handout**: `P_visual` diagrams + `P_thesis` summary + `P_interactive` fillable fields.

---

## 5. Directory Structure in `./output/teaching-architecture-kit/`

```
./output/teaching-architecture-kit/
├── manifest.json
├── agent/
│   ├── teaching-orchestrator.md
│   ├── content-strategist.md
│   ├── narrative-director.md
│   └── multi-format-transpiler.md
├── rules/
│   ├── core-teaching-principles.md
│   └── slide-zero-textdump.md
├── skills/
│   ├── diagnostic-gap-evaluator/
│   │   └── SKILL.md
│   ├── quality-resonance-auditor/
│   │   └── SKILL.md
│   ├── tnt-mindset-framing/
│   │   └── SKILL.md
│   ├── thesis-nail-extractor/
│   │   └── SKILL.md
│   ├── storyworthy-hammer-crafting/
│   │   └── SKILL.md
│   ├── resonant-experience-designer/
│   │   └── SKILL.md
│   ├── visual-slide-transpiler/
│   │   └── SKILL.md
│   └── multi-deliverable-exporter/
│       └── SKILL.md
└── workflows/
    ├── auto-teach.md
    ├── create-from-scratch.md
    ├── refactor-existing.md
    └── transpile-format.md
```

---

## 6. Definition of Done (DoD)

The Agent Kit will be considered 100% complete and production-ready when:
1. All 4 Agent files exist in `./output/teaching-architecture-kit/agent/` with valid YAML frontmatter and binary DoD.
2. All 8 Skill files exist in `./output/teaching-architecture-kit/skills/<skill-name>/SKILL.md` with complete instructions, YAML frontmatter, allowed tools, and non-empty guidelines.
3. All 2 Rules and 4 Workflows exist in their respective directories.
4. `manifest.json` correctly references all agents, skills, workflows, and version 2.0.0 metadata.
5. A full validation audit using `workflows/validate-kit.md` yields a score of at least **4.5 / 5 Stars**.
