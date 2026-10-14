---
name: draft-outline
description: Workflow to produce validated book outline
version: 1.0.0
requires_agents: [golden-writer]
requires_skills: [outline-drafting]
artifact_outputs: [outline.md]
initial_state: draft_node
terminal_states: [draft_node]
global_invariants:
  - id: inv.golden.no_overwrite
    description: Cannot modify approved outline
    check: check_no_overwrite
nodes:
  draft_node:
    role: golden-writer
    skill: outline-drafting
    required_outcome: outcome.outline.drafted
---

# Workflow: Draft Outline

## 1. Overview
Produce a validated outline artifact. If unrecoverable failure occurs, escalate via `[ESCALATE_HUMAN]`.

## 2. Nodes
### Step 1: draft_node
- **Role**: golden-writer
- **Skill**: outline-drafting
- **Input Artifacts**: `inputs/brief.md`
- **Output Artifacts**: `outputs/outline.md`
- **[DoD]**: Outline hierarchy verified and complete.
- **Evaluation Loop**: Pass -> complete; Fail -> retry or `[ESCALATE_HUMAN]`.
