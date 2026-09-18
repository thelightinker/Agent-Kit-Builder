#!/usr/bin/env python3
"""Bounded Convergence Engine for AgentKit self-healing loop.

Pipeline: Validate → Diagnose → Deterministic Fix → (LLM Patch Queue) → Re-validate → Report
Invariants:
  - Max 3 iterations (configurable)
  - Oscillation detection halts immediately
  - Deterministic fixes always run before LLM
  - Tier 2 mutations are never auto-applied
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path

from validate_kit import validate, Finding
from deterministic_fixer import fix as deterministic_fix


@dataclass
class ConvergenceReport:
    converged: bool = False
    iterations: int = 0
    first_pass_errors: int = 0
    auto_fixed_count: int = 0
    llm_patched_count: int = 0
    escalated_count: int = 0
    oscillation_detected: bool = False
    iteration_log: list[dict] = field(default_factory=list)
    final_findings: list[dict] = field(default_factory=list)
    llm_repair_queue: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def _detect_oscillation(error_history: list[set[str]]) -> bool:
    """Detect if the same error code set repeats across iterations."""
    if len(error_history) < 2:
        return False
    latest = error_history[-1]
    for previous in error_history[:-1]:
        if latest == previous and len(latest) > 0:
            return True
    return False


def _classify_findings(findings: list[Finding]) -> dict[str, list[Finding]]:
    """Group findings by fix_strategy."""
    groups: dict[str, list[Finding]] = {
        "deterministic": [],
        "llm_patch": [],
        "escalate_human": [],
    }
    for f in findings:
        strategy = getattr(f, "fix_strategy", "escalate_human")
        groups.setdefault(strategy, []).append(f)
    return groups


def converge(root: Path, max_iterations: int = 3) -> dict:
    """Run bounded convergence loop.

    Returns a JSON-serializable ConvergenceReport dict.
    """
    report = ConvergenceReport()
    error_history: list[set[str]] = []

    # Initial validation pass
    findings = validate(root, auto_heal=False)
    errors = [f for f in findings if f.severity == "error"]
    report.first_pass_errors = len(errors)

    if not errors:
        report.converged = True
        return report.to_dict()

    for iteration in range(max_iterations):
        report.iterations = iteration + 1
        classified = _classify_findings(errors)

        iter_log = {
            "iteration": iteration + 1,
            "errors_in": len(errors),
            "deterministic": len(classified["deterministic"]),
            "llm_patch": len(classified["llm_patch"]),
            "escalate_human": len(classified["escalate_human"]),
        }

        # Phase 1: Deterministic fixes (zero tokens)
        if classified["deterministic"]:
            fix_report = deterministic_fix(root, classified["deterministic"])
            report.auto_fixed_count += len(fix_report["fixed"])
            iter_log["det_fixed"] = fix_report["fixed"]
            iter_log["det_failed"] = fix_report["failed"]

        # Phase 2: LLM patch queue — produce structured repair instructions with JIT context
        llm_queue = []
        for f in classified["llm_patch"]:
            file_path = root / f.file
            file_content = ""
            if file_path.is_file():
                try:
                    file_content = file_path.read_text("utf-8", errors="replace")
                    lines = file_content.splitlines()
                    if len(lines) > 200:
                        file_content = "\n".join(lines[:200]) + f"\n... ({len(lines) - 200} more lines truncated)"
                except Exception:
                    pass
            llm_queue.append({
                "code": f.code,
                "file": f.file,
                "line": f.line,
                "message": f.message,
                "evidence": f.evidence,
                "file_content_jit": file_content,
            })
        report.llm_repair_queue = llm_queue
        iter_log["llm_queue_size"] = len(llm_queue)

        # Phase 3: Escalate (not auto-fixable)
        report.escalated_count = len(classified["escalate_human"])
        iter_log["escalated"] = [f.code for f in classified["escalate_human"]]

        report.iteration_log.append(iter_log)

        # Re-validate after deterministic fixes
        findings = validate(root, auto_heal=False)
        errors = [f for f in findings if f.severity == "error"]
        error_codes = {f.code for f in errors}
        error_history.append(error_codes)

        # Check convergence
        if not errors:
            report.converged = True
            break

        # Check oscillation
        if _detect_oscillation(error_history):
            report.oscillation_detected = True
            break

        # If only escalate_human errors remain, stop — can't auto-fix
        retryable = [f for f in errors if f.retryable]
        if not retryable:
            break

    report.final_findings = [f.__dict__ for f in findings]
    return report.to_dict()
