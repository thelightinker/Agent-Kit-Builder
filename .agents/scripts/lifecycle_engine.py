#!/usr/bin/env python3
"""Lifecycle Engine for Agent Kit Creator.

Provides state management, authority matrix enforcement, evidence validation,
and quota/oscillation protection for the unified closed-loop lifecycle.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class LifecycleError(Exception):
    """Base error for lifecycle state violations."""
    pass


class UnauthorizedTransitionError(LifecycleError):
    """Raised when a workflow attempts a transition outside its authority."""
    pass


class MissingEvidenceError(LifecycleError):
    """Raised when a transition is attempted without required evidence artifacts."""
    pass


class MaxRepairCyclesExceededError(LifecycleError):
    """Raised when repair cycles exceed the configured maximum."""
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# Workflow -> Allowed Target States mapping
AUTHORITY_MATRIX: Dict[str, List[str]] = {
    "create-kit": ["DRAFT", "READY_FOR_VALIDATION"],
    "validate-kit": ["VALIDATED", "NEEDS_REFACTOR", "NEEDS_HUMAN_INTERVENTION"],
    "refactor-kit": ["READY_FOR_VALIDATION"],
    "remember-kit": ["EXEMPLAR_ARCHIVED"],
    "manual_admin": [
        "DRAFT",
        "READY_FOR_VALIDATION",
        "VALIDATED",
        "NEEDS_REFACTOR",
        "NEEDS_HUMAN_INTERVENTION",
        "EXEMPLAR_ARCHIVED",
    ],
}


class LifecycleEngine:
    """Manages lifecycle.json SSOT contracts and transitions."""

    LIFECYCLE_FILENAME = "lifecycle.json"

    def __init__(self, schema_path: Optional[Path] = None):
        self.schema_path = schema_path

    def get_lifecycle_path(self, kit_path: Path) -> Path:
        return kit_path / self.LIFECYCLE_FILENAME

    def init_lifecycle(
        self,
        kit_path: Path,
        kit_name: str,
        kit_version: str = "1.0.0",
        created_by: str = "create-kit",
    ) -> Dict[str, Any]:
        """Initializes a new lifecycle.json file in DRAFT state."""
        timestamp = now_iso()
        data: Dict[str, Any] = {
            "$schema": "schemas/lifecycle.schema.json",
            "schema_version": "1.0.0",
            "kit_name": kit_name,
            "kit_version": kit_version,
            "lifecycle_state": "DRAFT",
            "active_change_gate": None,
            "lineage": {
                "created_at": timestamp,
                "updated_at": timestamp,
                "created_by": created_by,
                "repair_cycle_count": 0,
                "max_repair_cycles": 3,
            },
            "verdicts": {
                "validation": {
                    "pass": False,
                    "score": 0,
                    "findings_file": None,
                    "last_validated_at": None,
                },
                "memory_promotion": {
                    "promoted": False,
                    "promoted_at": None,
                    "memory_ref": None,
                },
            },
            "handoff": {
                "contract_version": "1.0.0",
                "source_workflow": created_by,
                "target_workflow": "validate-kit",
                "payload_file": None,
                "evidence_refs": [],
                "notes": "Initial draft created.",
            },
        }
        self.save_lifecycle(kit_path, data)
        return data

    def load_lifecycle(self, kit_path: Path) -> Dict[str, Any]:
        """Loads and parses lifecycle.json. Synthesizes a legacy default if missing."""
        path = self.get_lifecycle_path(kit_path)
        if not path.is_file():
            # Synthesize legacy default for backward compatibility
            return self.init_lifecycle(
                kit_path,
                kit_name=kit_path.name,
                kit_version="1.0.0",
                created_by="manual_scaffold",
            )
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            raise LifecycleError(f"Corrupt lifecycle.json at {path}: {e}")

    def save_lifecycle(self, kit_path: Path, data: Dict[str, Any]) -> None:
        """Saves lifecycle.json formatted with 2-space indentation."""
        path = self.get_lifecycle_path(kit_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def transition_state(
        self,
        kit_path: Path,
        target_state: str,
        workflow_name: str,
        evidence_refs: List[str],
        payload_file: Optional[str] = None,
        notes: str = "",
        next_target_workflow: str = "validate-kit",
    ) -> Dict[str, Any]:
        """Executes an authority-checked, evidence-gated state transition."""
        data = self.load_lifecycle(kit_path)
        current_state = data.get("lifecycle_state", "DRAFT")

        # 1. Authority Matrix Check
        allowed_targets = AUTHORITY_MATRIX.get(workflow_name, [])
        if target_state not in allowed_targets:
            raise UnauthorizedTransitionError(
                f"Workflow '{workflow_name}' is unauthorized to transition to state '{target_state}'. "
                f"Allowed states for '{workflow_name}': {allowed_targets}"
            )

        # 2. Evidence Requirement Check (No evidence -> No transition)
        if not evidence_refs and target_state != "NEEDS_HUMAN_INTERVENTION":
            raise MissingEvidenceError(
                f"State transition to '{target_state}' requires at least one valid evidence artifact in evidence_refs."
            )

        # Check evidence files exist on disk if relative to kit_path
        for ref in evidence_refs:
            ref_path = kit_path / ref
            if not ref_path.exists():
                raise MissingEvidenceError(f"Evidence file '{ref}' declared in evidence_refs does not exist on disk at {ref_path}")

        # 3. Special handling for repair cycle quota (refactor-kit)
        if workflow_name == "refactor-kit" and target_state == "READY_FOR_VALIDATION":
            data["lineage"]["repair_cycle_count"] += 1

        # 4. Mutate State
        data["lifecycle_state"] = target_state
        data["lineage"]["updated_at"] = now_iso()
        data["handoff"] = {
            "contract_version": "1.0.0",
            "source_workflow": workflow_name,
            "target_workflow": next_target_workflow,
            "payload_file": payload_file or (evidence_refs[0] if evidence_refs else None),
            "evidence_refs": list(evidence_refs),
            "notes": notes or f"Transitioned from {current_state} to {target_state} by {workflow_name}",
        }

        self.save_lifecycle(kit_path, data)
        return data

    def record_validation_verdict(
        self,
        kit_path: Path,
        pass_status: bool,
        score: int,
        findings_file: Optional[str] = "audit_findings.json",
        notes: str = "",
    ) -> Dict[str, Any]:
        """Records validation outcome from /validate-kit and computes state mutation."""
        data = self.load_lifecycle(kit_path)
        timestamp = now_iso()

        data["verdicts"]["validation"] = {
            "pass": bool(pass_status),
            "score": int(score),
            "findings_file": findings_file,
            "last_validated_at": timestamp,
        }
        data["lineage"]["updated_at"] = timestamp

        evidence_list = [findings_file] if findings_file and (kit_path / findings_file).exists() else []

        if pass_status:
            target_state = "VALIDATED"
            next_workflow = "remember-kit" if score == 5 else "release_ready"
            notes = notes or f"Passed validation with score {score}/5."
        else:
            current_repair_count = data["lineage"].get("repair_cycle_count", 0)
            max_repairs = data["lineage"].get("max_repair_cycles", 3)
            if current_repair_count >= max_repairs:
                target_state = "NEEDS_HUMAN_INTERVENTION"
                next_workflow = "manual_escalation"
                notes = f"Failed validation. Max repair cycles ({max_repairs}) reached. Escalating to human."
            else:
                target_state = "NEEDS_REFACTOR"
                next_workflow = "refactor-kit"
                notes = notes or f"Failed validation (score {score}/5). Handing off to refactor."

        data["lifecycle_state"] = target_state
        data["handoff"] = {
            "contract_version": "1.0.0",
            "source_workflow": "validate-kit",
            "target_workflow": next_workflow,
            "payload_file": findings_file,
            "evidence_refs": evidence_list,
            "notes": notes,
        }

        self.save_lifecycle(kit_path, data)
        return data

    def open_change_gate(self, kit_path: Path, gate_name: str = "architecture_evolution") -> Dict[str, Any]:
        """Opens an active change gate."""
        data = self.load_lifecycle(kit_path)
        data["active_change_gate"] = gate_name
        data["lineage"]["updated_at"] = now_iso()
        self.save_lifecycle(kit_path, data)
        return data

    def close_change_gate(self, kit_path: Path) -> Dict[str, Any]:
        """Closes the active change gate."""
        data = self.load_lifecycle(kit_path)
        data["active_change_gate"] = None
        data["lineage"]["updated_at"] = now_iso()
        self.save_lifecycle(kit_path, data)
        return data

    def promote_to_memory(self, kit_path: Path, memory_ref: str) -> Dict[str, Any]:
        """Promotes an exemplar 5/5 validated kit into memory."""
        data = self.load_lifecycle(kit_path)
        state = data.get("lifecycle_state")
        verdict = data.get("verdicts", {}).get("validation", {})

        if state != "VALIDATED" or not verdict.get("pass") or verdict.get("score") != 5:
            raise UnauthorizedTransitionError(
                f"Cannot promote kit to memory: Kit must be in state 'VALIDATED' with pass=true and score=5. "
                f"Current state: '{state}', pass: {verdict.get('pass')}, score: {verdict.get('score')}"
            )

        timestamp = now_iso()
        data["verdicts"]["memory_promotion"] = {
            "promoted": True,
            "promoted_at": timestamp,
            "memory_ref": memory_ref,
        }
        data["lifecycle_state"] = "EXEMPLAR_ARCHIVED"
        data["lineage"]["updated_at"] = timestamp
        data["handoff"] = {
            "contract_version": "1.0.0",
            "source_workflow": "remember-kit",
            "target_workflow": "completed",
            "payload_file": memory_ref,
            "evidence_refs": [memory_ref],
            "notes": f"Promoted to memory as exemplar at {memory_ref}",
        }
        self.save_lifecycle(kit_path, data)
        return data
