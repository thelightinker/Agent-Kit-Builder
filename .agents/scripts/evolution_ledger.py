#!/usr/bin/env python3
"""
Evolution Ledger Authority (SSOT) for Agent Kit Engine.
Maintains canonical 6-stage lifecycle for feedback items (RECEIVED -> TRIAGED -> DIAGNOSED -> PATCHED -> VERIFIED -> RELEASED),
links resolution evidence, manages evolution run records, and exports local read-only mirrors for kits.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

VALID_STATUSES = {
    "RECEIVED",
    "TRIAGED",
    "REJECTED",
    "DIAGNOSED",
    "PATCHED",
    "VERIFIED",
    "RELEASED"
}

VALID_RISK_TIERS = {
    "TIER_0_LOW",
    "TIER_1_STANDARD",
    "TIER_2_ARCHITECTURAL"
}

def get_engine_root() -> Path:
    cur = Path(__file__).resolve().parent
    while cur != cur.parent:
        if (cur / ".agents" / "scripts" / "evolution_ledger.py").exists():
            return cur
        cur = cur.parent
    return Path.cwd()

class EvolutionLedger:
    def __init__(self, engine_root: Path | None = None, kit_id: str = "default"):
        self.engine_root = Path(engine_root).resolve() if engine_root else get_engine_root()
        self.kit_id = kit_id
        self.ledger_dir = self.engine_root / "evolution" / "state" / "kits"
        self.ledger_dir.mkdir(parents=True, exist_ok=True)
        self.ledger_file = self.ledger_dir / f"{self.kit_id}-ledger.json"
        
        self.schema_version = "2.0.0"
        self.current_version = "1.0.0"
        self.lineage = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_evolved_at": datetime.now(timezone.utc).isoformat(),
            "total_evolution_cycles": 0
        }
        self.evolution_runs: list[dict[str, Any]] = []
        self.feedback_items: list[dict[str, Any]] = []
        
        if self.ledger_file.exists():
            self.load()

    def load(self) -> None:
        try:
            data = json.loads(self.ledger_file.read_text("utf-8"))
            self.schema_version = data.get("schema_version", "2.0.0")
            self.kit_id = data.get("kit_id", self.kit_id)
            self.current_version = data.get("current_canonical_version", "1.0.0")
            self.lineage = data.get("lineage", self.lineage)
            self.evolution_runs = data.get("evolution_runs", [])
            self.feedback_items = data.get("feedback_items", [])
        except Exception as e:
            print(f"⚠️ Warning loading ledger for {self.kit_id}: {e}", file=sys.stderr)

    def save(self) -> None:
        data = {
            "schema_version": self.schema_version,
            "kit_id": self.kit_id,
            "current_canonical_version": self.current_version,
            "lineage": self.lineage,
            "evolution_runs": self.evolution_runs,
            "feedback_items": self.feedback_items
        }
        self.ledger_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def get_feedback(self, feedback_id: str) -> dict[str, Any] | None:
        for item in self.feedback_items:
            if item.get("feedback_id") == feedback_id:
                return item
        return None

    def add_feedback_entry(
        self,
        feedback_id: str,
        batch_id: str,
        source_version: str,
        category: str = "failure",
        cluster_key: str = "general",
        diagnosed_root_cause: str = ""
    ) -> str:
        existing = self.get_feedback(feedback_id)
        if existing:
            return feedback_id
            
        entry: dict[str, Any] = {
            "feedback_id": feedback_id,
            "batch_id": batch_id,
            "source_version": source_version,
            "cluster_key": cluster_key,
            "category": category if category in ["failure", "friction", "idea"] else "failure",
            "status": "RECEIVED",
            "received_at": datetime.now(timezone.utc).isoformat(),
            "diagnosed_root_cause": diagnosed_root_cause,
            "resolved_in_run_id": "",
            "resolved_in_version": "",
            "impacted_files": []
        }
        self.feedback_items.append(entry)
        self.save()
        return feedback_id

    def ingest_batch(self, batch_dir: Path) -> list[str]:
        batch_dir = Path(batch_dir).resolve()
        fb_file = batch_dir / "feedback.jsonl"
        manifest_file = batch_dir / "manifest.json"
        
        batch_id = batch_dir.name
        source_version = self.current_version
        
        if manifest_file.exists():
            try:
                m_data = json.loads(manifest_file.read_text("utf-8"))
                batch_id = m_data.get("batch_id", batch_id)
                source_version = m_data.get("source_version", source_version)
            except Exception:
                pass
                
        ingested_ids: list[str] = []
        if not fb_file.exists():
            return ingested_ids
            
        lines = fb_file.read_text("utf-8").splitlines()
        for idx, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                fb_id = entry.get("feedback_id") or f"fb_{batch_id}_{idx+1:03d}"
                cat = entry.get("category", "failure")
                cluster = entry.get("cluster_key", "general")
                
                self.add_feedback_entry(
                    feedback_id=fb_id,
                    batch_id=batch_id,
                    source_version=source_version,
                    category=cat,
                    cluster_key=cluster
                )
                ingested_ids.append(fb_id)
            except Exception as e:
                print(f"⚠️ Warning parsing feedback line {idx}: {e}", file=sys.stderr)
                
        self.save()
        return ingested_ids

    def triage_item(self, feedback_id: str, cluster_key: str | None = None, category: str | None = None) -> bool:
        item = self.get_feedback(feedback_id)
        if not item:
            return False
        if cluster_key:
            item["cluster_key"] = cluster_key
        if category and category in ["failure", "friction", "idea"]:
            item["category"] = category
        item["status"] = "TRIAGED"
        self.save()
        return True

    def reject_item(self, feedback_id: str, reason: str) -> bool:
        item = self.get_feedback(feedback_id)
        if not item:
            return False
        item["status"] = "REJECTED"
        item["diagnosed_root_cause"] = f"REJECTED: {reason}"
        self.save()
        return True

    def diagnose_item(self, feedback_id: str, root_cause: str, planned_files: list[str]) -> bool:
        item = self.get_feedback(feedback_id)
        if not item:
            return False
        item["status"] = "DIAGNOSED"
        item["diagnosed_root_cause"] = root_cause
        item["impacted_files"] = planned_files
        self.save()
        return True

    def patch_item(self, feedback_id: str, run_id: str, impacted_files: list[str]) -> bool:
        item = self.get_feedback(feedback_id)
        if not item:
            return False
        item["status"] = "PATCHED"
        item["resolved_in_run_id"] = run_id
        item["impacted_files"] = list(set(item.get("impacted_files", []) + impacted_files))
        self.save()
        return True

    def verify_item(self, feedback_id: str, evidence: dict[str, Any]) -> bool:
        item = self.get_feedback(feedback_id)
        if not item:
            return False
        item["status"] = "VERIFIED"
        self.save()
        return True

    def release_run(
        self,
        run_id: str,
        from_version: str,
        to_version: str,
        triggered_by_batch: str,
        risk_tier: str,
        snapshot_ref: str,
        feedbacks_addressed: list[str],
        verification_evidence: dict[str, Any],
        human_approval: dict[str, Any] | None = None
    ) -> bool:
        if risk_tier not in VALID_RISK_TIERS:
            risk_tier = "TIER_1_STANDARD"
            
        ha = human_approval or {
            "required": False,
            "approved_by": None,
            "approved_at": None
        }
        
        run_record = {
            "run_id": run_id,
            "from_version": from_version,
            "to_version": to_version,
            "triggered_by_batch": triggered_by_batch,
            "risk_tier": risk_tier,
            "human_approval": ha,
            "snapshot_ref": snapshot_ref,
            "feedbacks_addressed": feedbacks_addressed,
            "verification_evidence": verification_evidence
        }
        
        self.evolution_runs.append(run_record)
        self.current_version = to_version
        self.lineage["last_evolved_at"] = datetime.now(timezone.utc).isoformat()
        self.lineage["total_evolution_cycles"] = len(self.evolution_runs)
        
        for fb_id in feedbacks_addressed:
            item = self.get_feedback(fb_id)
            if item:
                item["status"] = "RELEASED"
                item["resolved_in_version"] = to_version
                item["resolved_in_run_id"] = run_id
                
        self.save()
        return True

    def export_local_mirror(self, dest_file: Path) -> None:
        """
        Exports a read-only historical summary for the kit runtime.
        """
        dest_file = Path(dest_file).resolve()
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        
        mirror_data = {
            "kit_id": self.kit_id,
            "current_version": self.current_version,
            "total_evolution_cycles": len(self.evolution_runs),
            "recent_runs": self.evolution_runs[-5:],
            "resolved_feedbacks_count": len([f for f in self.feedback_items if f["status"] == "RELEASED"]),
            "exported_at": datetime.now(timezone.utc).isoformat()
        }
        dest_file.write_text(json.dumps(mirror_data, indent=2, ensure_ascii=False), encoding="utf-8")

    def query_status(self) -> dict[str, Any]:
        counts: dict[str, int] = {st: 0 for st in VALID_STATUSES}
        for item in self.feedback_items:
            st = item.get("status", "RECEIVED")
            counts[st] = counts.get(st, 0) + 1
            
        return {
            "kit_id": self.kit_id,
            "current_version": self.current_version,
            "total_feedbacks": len(self.feedback_items),
            "total_evolution_runs": len(self.evolution_runs),
            "by_status": counts,
            "pending_count": counts["RECEIVED"] + counts["TRIAGED"] + counts["DIAGNOSED"] + counts["PATCHED"]
        }

def main() -> int:
    parser = argparse.ArgumentParser(description="Evolution Ledger SSOT Manager")
    parser.add_argument("kit_id", help="Target kit name")
    parser.add_argument("--status", action="store_true", help="Print ledger summary status")
    parser.add_argument("--ingest-batch", help="Path to batch directory to ingest")
    parser.add_argument("--engine-root", default=None, help="Path to Engine root")
    
    args = parser.parse_args()
    engine_root = Path(args.engine_root) if args.engine_root else get_engine_root()
    ledger = EvolutionLedger(engine_root, args.kit_id)
    
    if args.ingest_batch:
        ids = ledger.ingest_batch(Path(args.ingest_batch))
        print(f"✅ Ingested {len(ids)} feedback items into ledger for '{args.kit_id}': {ids}")
        
    if args.status or not args.ingest_batch:
        stat = ledger.query_status()
        print(json.dumps(stat, indent=2, ensure_ascii=False))
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
