import json
import pytest
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import evolution_ledger

@pytest.fixture
def temp_engine(tmp_path):
    engine_dir = tmp_path / "engine"
    engine_dir.mkdir()
    
    # Setup schemas dir
    schemas_dir = engine_dir / ".agents" / "schemas"
    schemas_dir.mkdir(parents=True)
    real_schemas = Path(__file__).resolve().parents[2] / "schemas"
    for schema_file in real_schemas.glob("*.json"):
        (schemas_dir / schema_file.name).write_text(schema_file.read_text(encoding="utf-8"), encoding="utf-8")
        
    return engine_dir

def test_ledger_initialization_and_save(temp_engine):
    ledger = evolution_ledger.EvolutionLedger(engine_root=temp_engine, kit_id="writing-book-agent-v2")
    assert ledger.kit_id == "writing-book-agent-v2"
    assert ledger.current_version == "1.0.0"
    assert len(ledger.feedback_items) == 0
    assert len(ledger.evolution_runs) == 0
    
    ledger.save()
    ledger_file = temp_engine / "evolution" / "state" / "kits" / "writing-book-agent-v2-ledger.json"
    assert ledger_file.exists()

def test_ingest_batch(temp_engine, tmp_path):
    ledger = evolution_ledger.EvolutionLedger(engine_root=temp_engine, kit_id="writing-book-agent-v2")
    
    # Create mock batch
    batch_dir = tmp_path / "batch-writing-book-agent-v2-20260826T000000Z"
    batch_dir.mkdir()
    
    fb_lines = [
        json.dumps({
            "feedback_id": "fb_01",
            "category": "failure",
            "cluster_key": "formatting",
            "description": "Too many parentheses in chapter 1",
            "timestamp": "2026-08-26T00:00:00Z"
        }),
        json.dumps({
            "feedback_id": "fb_02",
            "category": "friction",
            "cluster_key": "visuals",
            "description": "Visual diagram missing SVG",
            "timestamp": "2026-08-26T00:00:00Z"
        })
    ]
    (batch_dir / "feedback.jsonl").write_text("\n".join(fb_lines), encoding="utf-8")
    (batch_dir / "manifest.json").write_text(json.dumps({
        "batch_id": batch_dir.name,
        "kit_id": "writing-book-agent-v2",
        "source_version": "1.0.0",
        "total_entries": 2
    }), encoding="utf-8")
    
    ids = ledger.ingest_batch(batch_dir)
    assert len(ids) == 2
    assert "fb_01" in ids
    assert "fb_02" in ids
    
    item1 = ledger.get_feedback("fb_01")
    assert item1["status"] == "RECEIVED"
    assert item1["cluster_key"] == "formatting"

def test_full_6_stage_lifecycle(temp_engine):
    ledger = evolution_ledger.EvolutionLedger(engine_root=temp_engine, kit_id="test-kit")
    
    # 1. Add direct feedback entry
    fb_id = ledger.add_feedback_entry(
        feedback_id="fb_100",
        batch_id="batch_manual",
        source_version="1.0.0",
        category="failure",
        cluster_key="rule_violation",
        diagnosed_root_cause=""
    )
    assert ledger.get_feedback("fb_100")["status"] == "RECEIVED"
    
    # 2. Triage
    assert ledger.triage_item("fb_100") is True
    assert ledger.get_feedback("fb_100")["status"] == "TRIAGED"
    
    # 3. Diagnose
    assert ledger.diagnose_item(
        "fb_100",
        root_cause="Rule was not strictly enforced in prompt",
        planned_files=["agent/writer.md"]
    ) is True
    assert ledger.get_feedback("fb_100")["status"] == "DIAGNOSED"
    
    # 4. Patch
    assert ledger.patch_item(
        "fb_100",
        run_id="run_01",
        impacted_files=["agent/writer.md"]
    ) is True
    assert ledger.get_feedback("fb_100")["status"] == "PATCHED"
    
    # 5. Verify
    evidence = {
        "l1_linter_pass": True,
        "linter_command": "python validate_kit.py",
        "linter_score": 5,
        "error_count": 0,
        "log_snippet": "0 errors"
    }
    assert ledger.verify_item("fb_100", evidence) is True
    assert ledger.get_feedback("fb_100")["status"] == "VERIFIED"
    
    # 6. Release Run
    assert ledger.release_run(
        run_id="run_01",
        from_version="1.0.0",
        to_version="1.1.0",
        triggered_by_batch="batch_manual",
        risk_tier="TIER_1_STANDARD",
        snapshot_ref="evolution/snapshots/test-kit/v1.0.0-hash/",
        feedbacks_addressed=["fb_100"],
        verification_evidence=evidence
    ) is True
    
    assert ledger.get_feedback("fb_100")["status"] == "RELEASED"
    assert ledger.get_feedback("fb_100")["resolved_in_version"] == "1.1.0"
    assert ledger.current_version == "1.1.0"
    
    # Check status summary
    status = ledger.query_status()
    assert status["total_feedbacks"] == 1
    assert status["by_status"]["RELEASED"] == 1
