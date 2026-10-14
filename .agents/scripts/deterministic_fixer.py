#!/usr/bin/env python3
"""Zero-token deterministic fixes for structural errors in AG Kit."""
from __future__ import annotations

import datetime
import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path

from component_registry import build_manifest, build_lock, canonical_json
from dependency_graph import render as render_dependency_graph


@dataclass
class FixReport:
    fixed: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)
    actions_taken: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def _log(report: FixReport, code: str, file: str, action: str, success: bool) -> None:
    entry = {"code": code, "file": file, "action": action, "success": success}
    report.actions_taken.append(entry)
    (report.fixed if success else report.failed).append(f"{code}:{file}")


def fix(root: Path, findings: list) -> dict:
    """Apply deterministic fixes for findings with fix_strategy='deterministic'."""
    report = FixReport()
    det = [f for f in findings if getattr(f, "fix_strategy", "") == "deterministic"]

    codes_present = {f.code for f in det}

    # --- Manifest / Lock / Dependency Graph: regenerate from source of truth ---
    registry_codes = {
        "manifest.stale",
        "manifest.lock_stale",
        "manifest.missing",
        "graph.stale",
        "graph.missing",
    }
    if codes_present & registry_codes:
        try:
            manifest = build_manifest(root)
            (root / "manifest.json").write_text(canonical_json(manifest), "utf-8")
            lock = build_lock(root, manifest)
            (root / "manifest.lock.json").write_text(canonical_json(lock), "utf-8")
            dep_text = render_dependency_graph(root)
            (root / "DEPENDENCY_GRAPH.md").write_text(dep_text, "utf-8")
            for code in sorted(codes_present & registry_codes):
                _log(report, code, "registry", "regenerated from frontmatter SOT", True)
        except Exception as exc:
            for code in sorted(codes_present & registry_codes):
                _log(report, code, "registry", f"regeneration failed: {exc}", False)

    # --- ARCHITECTURE.md count mismatch: rewrite the Statistics table ---
    arch_codes = {"architecture.count_mismatch", "architecture.count_missing"}
    if codes_present & arch_codes:
        arch_path = root / "ARCHITECTURE.md"
        if arch_path.is_file():
            try:
                text = arch_path.read_text("utf-8")
                actual = {
                    "Total Agents": len(list((root / "agent").glob("*.md"))),
                    "Total Skills": len(list((root / "skills").glob("*/SKILL.md"))),
                    "Total Workflows": len(list((root / "workflows").glob("*.md"))),
                    "Total Skill Scripts": len(list((root / "skills").glob("*/scripts/*.py"))),
                }
                for label, count in actual.items():
                    pattern = rf"(\*\*{re.escape(label)}\*\*\s*\|\s*)\d+"
                    text = re.sub(pattern, rf"\g<1>{count}", text)
                arch_path.write_text(text, "utf-8")
                for code in sorted(codes_present & arch_codes):
                    _log(report, code, "ARCHITECTURE.md", f"counts updated to {actual}", True)
            except Exception as exc:
                for code in sorted(codes_present & arch_codes):
                    _log(report, code, "ARCHITECTURE.md", f"fix failed: {exc}", False)

    # --- VERSION file: create with today's CalVer if missing ---
    if "version.missing" in codes_present:
        try:
            today = datetime.date.today()
            calver = f"{today.year}.{today.month}.{today.day}"
            (root / "VERSION").write_text(calver + "\n", "utf-8")
            _log(report, "version.missing", "VERSION", f"created with {calver}", True)
        except Exception as exc:
            _log(report, "version.missing", "VERSION", f"fix failed: {exc}", False)

    if "version.invalid_calver" in codes_present:
        try:
            today = datetime.date.today()
            calver = f"{today.year}.{today.month}.{today.day}"
            (root / "VERSION").write_text(calver + "\n", "utf-8")
            _log(report, "version.invalid_calver", "VERSION", f"overwritten with {calver}", True)
        except Exception as exc:
            _log(report, "version.invalid_calver", "VERSION", f"fix failed: {exc}", False)

    # --- Generated doc blocks: synchronize using render_docs ---
    doc_trigger_codes = {
        "docs.generated_stale",
        "architecture.count_mismatch",
        "architecture.count_missing",
        "version.missing",
        "version.invalid_calver",
    }
    if codes_present & doc_trigger_codes:
        try:
            import render_docs
            modified = render_docs.apply_generated_blocks(root, check=False)
            if "docs.generated_stale" in codes_present:
                _log(report, "docs.generated_stale", "ARCHITECTURE.md", f"generated blocks refreshed: {modified}", True)
        except Exception as exc:
            if "docs.generated_stale" in codes_present:
                _log(report, "docs.generated_stale", "ARCHITECTURE.md", f"fix failed: {exc}", False)

    return report.to_dict()
