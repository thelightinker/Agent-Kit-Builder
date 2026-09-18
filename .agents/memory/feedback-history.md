---
type: feedback
created: 2026-07-18
updated: 2026-09-06
---

# Feedback History

### [2026-09-06] Hardcoded absolute paths in skill references
- **Source**: Builder self-audit
- **Severity**: Critical
- **Description**: 16 internal reference links in 4 skill files used absolute paths from old workspace location (`OneDrive/Desktop/...`). Grounding Gate failed silently when agent tried to read references.
- **Resolution**: Converted all internal refs to relative `.agents/` paths.
- **Prevention rule**: All internal references MUST use relative paths. Never hardcode user-specific absolute paths.

### [2026-09-06] ARCHITECTURE.md drift — ghost workflows and phantom scripts
- **Source**: Builder self-audit
- **Severity**: Serious
- **Description**: ARCHITECTURE.md listed 3 workflows (`/log-feedback`, `/submit-evolution`, `/process-evolution`) and 2 scripts (`feedback_collector.py`, `evolution_submitter.py`) that did not exist on filesystem. Counts were inconsistent (11 vs 8 vs 6).
- **Resolution**: Removed ghost entries, corrected script names, synced all counts.
- **Prevention rule**: After adding/removing any component, run `validate_kit.py` which checks Architecture counts.

### [2026-09-06] domain-profiling/SKILL.md — duplicated section outside code block
- **Source**: Builder self-audit
- **Severity**: Serious
- **Description**: Lines 121-128 contained a duplicated `## 3. Right Altitude Test` section that rendered as real headings instead of template content, breaking Report Format and heading hierarchy.
- **Resolution**: Removed 9 trailing lines after the closing code block.
- **Prevention rule**: After editing any SKILL.md, verify heading count matches expected structure.
