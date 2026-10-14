# Agent Kit Creator — AI System Onboarding & Leverage Upgrade Guide

> **Target Audience:** Any AI Model / Agent (Gemini, Claude, Antigravity IDE, Cursor, Custom GPTs).
> **Objective:** Single source of truth context guide to help any AI instantly understand the Agent Kit Creator Evolvable Architecture, enforce strict contracts, and propose high-leverage 80/20 system upgrades.

---

## 🎯 1. System Core Purpose & Core Principles

Agent Kit Creator is an expert **Meta-Agent Suite** designed to build, refactor, audit, evaluate, and export production-ready AI Agent Kits for any LLM platform.

### Core Principles
1. **Progressive Disclosure**: Keep System Prompts lightweight (< 500 lines); offload heavy reference materials into `skills/` and `references/`.
2. **Binary Definition of Done (DoD)**: Every output criterion must pass 3 checks:
   - **Binary**: Pass/Fail with zero ambiguity.
   - **Measurable**: Directly verifiable from the output artifact.
   - **Concrete**: 0 subjective adjectives (e.g. replace "professional output" with "file exists and contains ≥ 500 words").
3. **Workspace Output Isolation (BẤT BIẾN)**: Newly generated Agent Kits MUST be written to an isolated directory `<target-dir>` specified by the user (confirm before scaffolding). NEVER write generated kit files directly into Creator's `.agents/` workspace.
4. **Provider-Agnostic**: Prompts and specs must run cleanly across LLM providers without vendor lock-in.

---

## 🏗️ 2. Detailed Component Architecture (v2.0.0 Evolvable Architecture)

```
.agents/
├── agent/            # 1 Orchestrator Agent (kit-architect.md)
├── skills/           # 7 Focused Skills
├── workflows/        # 4 Slash Command Workflows
├── rules/            # 2 Lean Rules (core-guardrails.md, dynamic-routing.md)
├── memory/           # Persistent Memory (MEMORY.md index + topic files)
├── templates/        # Component & Master Workflow Templates
├── references/       # Deep Reference Docs & Domain Guides
├── evals/            # Automated Eval Suite JSONs
└── scripts/          # Python Tooling & Validation
```

### A. 1 Orchestrator Agent & Dynamic Role Profiles
- `kit-architect`: Single orchestrator with 4 lazy-loaded role profiles:
  - `@analyst`: Domain analysis, core verbs, failure modes, 80/20 leverage.
  - `@compiler`: Prompt engineering, 4-section system prompt, binary DoD, negative constraints.
  - `@architect`: Skill folder structure, progressive disclosure, YAML frontmatter contracts.
  - `@auditor`: Quality gates decision, 3-layer audit specification.

### B. 7 Focused Skills
- `domain-profiling`: Domain verbs, enhancement discovery, failure mode prediction, tier classification.
- `prompt-compiling`: System prompt 4 blocks, binary DoD, negative constraints, multi-target transpiling.
- `skill-architecting`: SKILL.md creation, progressive disclosure, frontmatter contracts.
- `kit-assembling`: Packaged assembly into `<target-dir>`, manifest.json generation.
- `kit-verifying`: 3-layer audit (L1 Linting, L2 Adaptive Scenarios, L3 Adversarial Tests).
- `kit-exporting`: Multi-platform export (Cursor `.cursorrules`, Claude `claude_instructions.txt`, Custom GPTs `gpt_instructions.txt`).
- `kit-evolving`: Gap analysis, delta patching, memory management.

### C. 4 Workflows
- `/create-kit`: End-to-end creation of new Agent Kits (Deep Track).
- `/refactor-kit`: Upgrade and delta patch existing Agent Kits.
- `/validate-kit`: Structural, semantic, and behavioral quality audit.
- `/remember-kit`: Distill lessons learned into persistent memory.

### D. Python Tooling Suite (`.agents/scripts/`)
- `validate_kit.py`: Self-validation runner checking structural integrity, links, and SemVer.
- `generate_manifest.py`: Synchronizes `manifest.json`.
- `dependency_graph.py`: Generates `DEPENDENCY_GRAPH.md` from manifest dependencies.
- `audit_kit.py`: 3-layer quality audit tool.
- `eval_runner.py`: Behavioral test suite assertion runner (`regex_match`, `contains_keywords`, `forbidden_keywords`, `min_sections`).
- `export_kit.py`: Multi-platform bundle compiler for Cursor, Claude, OpenAI GPTs.

---

## 📜 3. Antigravity IDE Contract Specifications

### Rule Contract (`.agents/rules/<name>.md`)
- YAML Frontmatter: `name`, `version`, `priority` (`P0` | `P1` | `P2`), `trigger`, `description`.
- `trigger` MUST be one of: `always_on`, `manual`, `model_decision`.

### Workflow Contract (`.agents/workflows/<name>.md`)
- YAML Frontmatter: `name`, `description`, `version`, `requires_agents`, `requires_skills`, `artifact_outputs`.

### Skill Contract (`.agents/skills/<name>/SKILL.md`)
- YAML Frontmatter: `name`, `description` (pushy trigger format), `when_to_use`, `allowed-tools`, `version`.

---

## 💡 4. How Any AI Can Discover & Propose 80/20 Leverage Upgrades

```
Step 1: Identify Point of Failure
  └─ Ask: "Where do LLMs or users encounter friction, context rot, or syntax errors?"

Step 2: Design 80/20 Technical Mechanism
  └─ Ask: "What 20% solution (script, focused skill, hard constraint) resolves 80% of the issue?"

Step 3: Implement & Validate
  └─ 1. Write/update component files
  └─ 2. Update ARCHITECTURE.md counts if adding skills/agents
  └─ 3. Run: python .agents/scripts/generate_manifest.py
  └─ 4. Run: python .agents/scripts/dependency_graph.py
  └─ 5. Run: python .agents/scripts/validate_kit.py
  └─ 6. Run: python -m unittest discover -s .agents/scripts/tests
  └─ Verify: 0 errors, 0 warnings, 100% test pass rate.
```
