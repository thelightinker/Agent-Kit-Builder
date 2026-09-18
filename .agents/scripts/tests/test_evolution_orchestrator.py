import json
import pytest
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import evolution_orchestrator
import evolution_ledger

@pytest.fixture
def mock_engine_and_kit(tmp_path):
    engine_dir = tmp_path / "engine"
    engine_dir.mkdir()
    
    # Schemas
    schemas_dir = engine_dir / ".agents" / "schemas"
    schemas_dir.mkdir(parents=True)
    real_schemas = Path(__file__).resolve().parents[2] / "schemas"
    for schema_file in real_schemas.glob("*.json"):
        (schemas_dir / schema_file.name).write_text(schema_file.read_text(encoding="utf-8"), encoding="utf-8")
        
    # Scripts in engine
    engine_scripts = engine_dir / ".agents" / "scripts"
    engine_scripts.mkdir(parents=True)
    for s in ["feedback_collector.py", "evolution_submitter.py", "validate_kit.py"]:
        real_s = SCRIPTS_DIR / s
        if real_s.exists():
            (engine_scripts / s).write_text(real_s.read_text(encoding="utf-8"), encoding="utf-8")
            
    # Output kit
    output_dir = engine_dir / "Output" / "mock-kit"
    kit_agents = output_dir / ".agents"
    kit_agents.mkdir(parents=True)
    (output_dir / "README.md").write_text("# Mock Kit v1.0", encoding="utf-8")
    (kit_agents / "VERSION").write_text("1.0.0", encoding="utf-8")
    
    agent_dir = kit_agents / "agent"
    agent_dir.mkdir()
    (agent_dir / "mock-orchestrator.md").write_text("""---
name: mock-orchestrator
description: Mock agent
---
# Mock Orchestrator
## 1. Vai trò & Quyền hạn (Role & Outcome)
Primary role
## 2. Quy trình Xử lý (Process)
Step 1
## 3. Ranh giới Phủ định (Hard Constraints)
No errors
## 4. Format Đầu Ra & Definition of Done (DoD)
- [ ] Done
""", encoding="utf-8")
    
    (kit_agents / "manifest.json").write_text(json.dumps({
        "schema_version": "2.0.0",
        "name": "mock-kit",
        "version": "1.0.0",
        "agents": {
            "mock-orchestrator": {"path": "agent/mock-orchestrator.md", "version": "1.0.0"}
        },
        "skills": {},
        "workflows": {}
    }), encoding="utf-8")
    
    # Create inbox batch
    inbox_dir = engine_dir / "evolution" / "inbox" / "batch-mock-kit-20260826T000000Z"
    inbox_dir.mkdir(parents=True)
    (inbox_dir / "manifest.json").write_text(json.dumps({
        "batch_id": inbox_dir.name,
        "kit_id": "mock-kit",
        "source_version": "1.0.0",
        "total_entries": 1
    }), encoding="utf-8")
    (inbox_dir / "feedback.jsonl").write_text(json.dumps({
        "feedback_id": "fb_mock_001",
        "category": "failure",
        "cluster_key": "formatting",
        "description": "Output was messy",
        "timestamp": "2026-08-26T00:00:00Z"
    }) + "\n", encoding="utf-8")
    
    return engine_dir, output_dir

def test_evolution_orchestrator_pipeline(mock_engine_and_kit, tmp_path):
    engine_dir, kit_dir = mock_engine_and_kit
    
    # Run orchestrator
    res = evolution_orchestrator.run_evolution_pipeline(
        kit_id="mock-kit",
        engine_root=engine_dir,
        kit_path=kit_dir,
        bump_type="minor",
        skip_human_gate=True
    )
    
    assert res["success"] is True
    assert res["old_version"] == "1.0.0"
    assert res["new_version"] == "1.1.0"
    assert res["snapshot_created"] is True
    assert len(res["feedbacks_resolved"]) == 1
    assert "fb_mock_001" in res["feedbacks_resolved"]
    
    # Check snapshot exists
    snapshot_dir = engine_dir / "evolution" / "snapshots" / "mock-kit"
    assert snapshot_dir.exists()
    snaps = list(snapshot_dir.glob("v1.0.0-*"))
    assert len(snaps) == 1
    
    # Check ledger state
    ledger = evolution_ledger.EvolutionLedger(engine_dir, "mock-kit")
    status = ledger.query_status()
    assert status["current_version"] == "1.1.0"
    assert status["by_status"]["RELEASED"] == 1
    assert len(ledger.evolution_runs) == 1
    
    # Check local mirror in kit
    mirror = kit_dir / ".agents" / "evolution" / "EVOLUTION_HISTORY.json"
    assert mirror.exists()
    m_data = json.loads(mirror.read_text(encoding="utf-8"))
    assert m_data["current_version"] == "1.1.0"
    assert m_data["resolved_feedbacks_count"] == 1
