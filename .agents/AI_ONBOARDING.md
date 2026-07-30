# Agent Kit Creator — AI System Onboarding & Leverage Upgrade Guide

> **Target Audience:** Any AI Model / Agent (Gemini, Claude, Antigravity IDE, Cursor, Custom GPTs).
> **Objective:** Single source of truth context guide to help any AI instantly understand the Agent Kit Creator architecture, enforce strict IDE contracts, and propose high-leverage 80/20 system upgrades.

---

## 🎯 1. System Core Purpose & Core Principles

Agent Kit Creator is an expert **Meta-Agent Suite** designed to build, refactor, audit, evaluate, and export production-ready AI Agent Kits for any LLM platform.

### Core Principles
1. **Progressive Disclosure**: Keep System Prompts lightweight (< 500 lines); offload heavy reference materials into `skills/` and `references/`.
2. **Binary Definition of Done (DoD)**: Every output criterion must pass 3 checks:
   - **Binary**: Pass/Fail with zero ambiguity.
   - **Measurable**: Directly verifiable from the output artifact.
   - **Concrete**: 0 subjective adjectives (e.g. replace "professional output" with "file exists and contains ≥ 500 words").
3. **Workspace Output Isolation**: Newly generated Agent Kits MUST be written to an isolated directory `./output/<kit-name>/`. NEVER write generated kit files directly into Creator's `.agents/` workspace.
4. **Provider-Agnostic**: Prompts and specs must run cleanly across LLM providers without vendor lock-in.

---

## 🏗️ 2. Detailed Component Architecture

```
.agents/
├── agent/            # 5 Specialist Agents
├── skills/           # 20 Specialized Skills
├── workflows/        # 4 Slash Command Workflows
├── rules/            # 6 System Rules
├── memory/           # Persistent Memory (MEMORY.md index + topic files)
├── templates/        # Component & Master Workflow Templates
├── evals/            # Automated Eval Suite JSONs
└── scripts/          # Python Tooling & Validation
```

### A. 5 Specialist Agents & Handoff Pipeline
- `master-compiler`: Orchestrates the creation pipeline, classifies user intent, assigns output `./output/<kit-name>/`.
- `domain-analyst`: Analyzes target domain, extracts core verbs, failure modes, and 80/20 leverage mechanisms.
- `kit-generator`: Compiles 4-section System Prompts with binary DoD and Hard Constraints.
- `skill-architect`: Scaffolds SKILL.md files, progressive disclosure levels, and reference docs.
- `quality-auditor`: Performs 3-layer audit (Structural, Semantic, Adversarial) & 5-star Rubric scoring.

### B. 20 Specialized Skills
- **Core Design**: `domain-analysis`, `prompt-engineering`, `skill-crafting`, `scaffolding-skills`, `kit-assembly`, `tiering-complexity`, `compiling-prompts`, `building-component-specs`, `guided-intaking`, `analyzing-domain-verbs`, `discovering-enhancements`, `optimizing-progressive-disclosure`.
- **Quality & Evolution**: `quality-assurance`, `auditing-quality-gates`, `adversarial-evaluating`, `kit-evolution`.
- **Testing, Export & Self-Extension**:
  - `eval-running`: Executes automated behavioral eval suites via `scripts/eval_runner.py`.
  - `exporting-kits`: Multi-platform export engine via `scripts/export_kit.py` (Cursor, Claude, Custom GPTs).
  - `kit-extending`: Meta-skill bundled with created kits to allow target kits to self-extend rules/workflows/skills.
  - `memory-system`: Cross-session persistent memory index management.

### C. 4 Workflows
- `/create-kit`: End-to-end creation of new Agent Kits.
- `/refactor-kit`: Upgrade and delta patch existing Agent Kits.
- `/validate-kit`: Structural, semantic, and behavioral quality audit.
- `/remember-kit`: Distill lessons learned into persistent memory.

### D. Python Tooling Suite (`.agents/scripts/`)
- `validate_kit.py`: Self-validation runner checking structural integrity, SHA-256 hashes, links, and SemVer.
- `generate_manifest.py`: Synchronizes `manifest.json` and `manifest.lock.json`.
- `dependency_graph.py`: Generates `DEPENDENCY_GRAPH.md` from manifest dependencies.
- `audit_kit.py`: 3-layer quality audit tool.
- `eval_runner.py`: Behavioral test suite assertion runner (`regex_match`, `contains_keywords`, `forbidden_keywords`, `min_sections`).
- `export_kit.py`: Multi-platform bundle compiler for Cursor (`.cursorrules`), Claude (`claude_instructions.txt`), OpenAI GPTs (`gpt_instructions.txt`).

---

## 📜 3. Antigravity IDE Contract Specifications

Any AI extending or creating components for this system MUST adhere to these strict contracts:

### Rule Contract (`.agents/rules/<name>.md`)
- YAML Frontmatter: `name`, `version`, `priority` (`P0` | `P1` | `P2`), `trigger`, `description`.
- `trigger` MUST be one of: `always_on`, `manual`, `model_decision`.

### Workflow Contract (`.agents/workflows/<name>.md`)
- YAML Frontmatter: `name`, `description`, `version`, `requires_agents`, `requires_skills`, `artifact_outputs`, `topology`, `trigger`, `permissions`, `tools_allowed`, `safe_outputs`, `max_retry_per_node`.
- Markdown Body: 5-Part Node Anatomy for every state (`[STATE]`, `[Input Artifacts]`, `[Output Artifacts]`, `[DoD]`, `[Evaluation Loop]` with `[ESCALATE_HUMAN]`).

### Skill Contract (`.agents/skills/<name>/SKILL.md`)
- YAML Frontmatter: `name`, `description` (pushy trigger format), `when_to_use`, `allowed-tools`, `version`.

---

## 💡 4. How Any AI Can Discover & Propose 80/20 Leverage Upgrades

When tasked with improving or extending Agent Kit Creator, follow this 3-step decision protocol:

```
Step 1: Identify Point of Failure
  └─ Ask: "Where do LLMs or users encounter friction, context rot, or syntax errors?"
     (e.g., format hallucination, missing test runners, workspace pollution, multi-platform incompatibility)

Step 2: Design 80/20 Technical Mechanism
  └─ Ask: "What 20% solution (script, meta-skill, hard constraint) resolves 80% of the issue?"
     (Prefer deterministic Python scripts + standardized YAML contracts over lengthy prompt text)

Step 3: Implement & Validate
  └─ 1. Write/update component files
  └─ 2. Update ARCHITECTURE.md counts if adding skills/agents
  └─ 3. Run: python .agents/scripts/generate_manifest.py
  └─ 4. Run: python .agents/scripts/dependency_graph.py
  └─ 5. Run: python .agents/scripts/validate_kit.py
  └─ 6. Run: python -m unittest discover -s .agents/scripts/tests
  └─ Verify: 0 errors, 0 warnings, 100% test pass rate.
```
