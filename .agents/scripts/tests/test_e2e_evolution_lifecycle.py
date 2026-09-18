import json
import pytest
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import equip_evolution
import evolution_submitter
import evolution_ledger
import snapshot_manager
import evolution_orchestrator

def test_full_end_to_end_evolution_lifecycle(tmp_path):
    # 1. Setup Engine environment
    engine_dir = tmp_path / "engine"
    engine_dir.mkdir()
    
    schemas_dir = engine_dir / ".agents" / "schemas"
    schemas_dir.mkdir(parents=True)
    real_schemas = Path(__file__).resolve().parents[2] / "schemas"
    for schema_file in real_schemas.glob("*.json"):
        (schemas_dir / schema_file.name).write_text(schema_file.read_text(encoding="utf-8"), encoding="utf-8")
        
    engine_scripts = engine_dir / ".agents" / "scripts"
    engine_scripts.mkdir(parents=True)
    for s in ["feedback_collector.py", "evolution_submitter.py", "validate_kit.py", "evolution_ledger.py", "snapshot_manager.py", "evolution_orchestrator.py"]:
        real_s = SCRIPTS_DIR / s
        if real_s.exists():
            (engine_scripts / s).write_text(real_s.read_text(encoding="utf-8"), encoding="utf-8")

    # 2. Create sample kit
    kit_dir = engine_dir / "Output" / "content-genius"
    kit_agents = kit_dir / ".agents"
    kit_agents.mkdir(parents=True)
    (kit_dir / "README.md").write_text("# Content Genius Kit v1.0", encoding="utf-8")
    (kit_agents / "VERSION").write_text("1.0.0", encoding="utf-8")
    
    agent_dir = kit_agents / "agent"
    agent_dir.mkdir()
    (agent_dir / "chief-editor.md").write_text("""---
name: chief-editor
description: The main editor
---
# Chief Editor
## 1. Vai trò & Quyền hạn (Role & Outcome)
Lead editor
## 2. Quy trình Xử lý (Process)
Step 1
## 3. Ranh giới Phủ định (Hard Constraints)
No spam
## 4. Format Đầu Ra & Definition of Done (DoD)
- [ ] Done
""", encoding="utf-8")

    skills_dir = kit_agents / "skills" / "hook-writing"
    skills_dir.mkdir(parents=True)
    (skills_dir / "SKILL.md").write_text("""---
name: hook-writing
description: Hook writing skill
---
# Hook Writing
### Examples
Input: draft
Output: hooked
""", encoding="utf-8")

    (kit_agents / "manifest.json").write_text(json.dumps({
        "schema_version": "2.0.0",
        "name": "content-genius",
        "version": "1.0.0",
        "agents": {
            "chief-editor": {"path": "agent/chief-editor.md", "version": "1.0.0"}
        },
        "skills": {
            "hook-writing": {"path": "skills/hook-writing/SKILL.md", "version": "1.0.0"}
        },
        "workflows": {}
    }), encoding="utf-8")

    # 3. Equip Kit Dynamically
    assert equip_evolution.equip_kit(kit_dir, engine_root=engine_dir) is True
    
    # 4. Simulate test runtime in external workspace
    test_ws = tmp_path / "AI Agent Kits" / "content-genius"
    test_ws.mkdir(parents=True)
    evolution_orchestrator.sync_to_test_workspace(kit_dir, test_ws)
    assert (test_ws / ".agents" / "workflows" / "log-feedback.md").exists()
    
    # 5. Log feedback in test workspace
    test_fb_file = test_ws / ".agents" / "evolution" / "feedback" / "feedback.jsonl"
    fb_entry = {
        "feedback_id": "fb_cg_001",
        "category": "failure",
        "cluster_key": "hook_length",
        "description": "Hooks are too verbose for mobile readers",
        "timestamp": "2026-08-26T00:00:00Z"
    }
    test_fb_file.write_text(json.dumps(fb_entry) + "\n", encoding="utf-8")
    
    # 6. Submit batch from test workspace to engine
    engine_inbox = engine_dir / "evolution" / "inbox"
    pack_res = evolution_submitter.submit_evolution_pipeline(test_ws, engine_inbox=engine_inbox)
    assert pack_res.get("success") is True
    
    # Verify batch reached Engine Inbox
    batches = list(engine_inbox.glob("batch-content-genius-*"))
    assert len(batches) == 1
    
    # 7. Run Single-Command Evolution Orchestrator at Engine
    evo_res = evolution_orchestrator.run_evolution_pipeline(
        kit_id="content-genius",
        engine_root=engine_dir,
        kit_path=kit_dir,
        bump_type="minor",
        skip_human_gate=True,
        target_workspace=test_ws
    )
    
    assert evo_res["success"] is True
    assert evo_res["old_version"] == "1.0.0"
    assert evo_res["new_version"] == "1.1.0"
    
    # 8. Verify Snapshot
    snapshot_dir = engine_dir / "evolution" / "snapshots" / "content-genius"
    assert snapshot_dir.exists()
    snaps = list(snapshot_dir.glob("v1.0.0-*"))
    assert len(snaps) == 1
    assert (snaps[0] / "snapshot_manifest.json").exists()
    
    # 9. Verify Engine SSOT Ledger
    ledger = evolution_ledger.EvolutionLedger(engine_dir, "content-genius")
    status = ledger.query_status()
    assert status["current_version"] == "1.1.0"
    assert status["by_status"]["RELEASED"] == 1
    
    fb_item = ledger.get_feedback("fb_cg_001")
    assert fb_item is not None
    assert fb_item["status"] == "RELEASED"
    assert fb_item["resolved_in_version"] == "1.1.0"
    
    # 10. Verify Test Workspace updated to v1.1.0 cleanly
    ws_version = (test_ws / ".agents" / "VERSION").read_text("utf-8").strip()
    assert ws_version == "1.1.0"
    
    ws_mirror = json.loads((test_ws / ".agents" / "evolution" / "EVOLUTION_HISTORY.json").read_text("utf-8"))
    assert ws_mirror["current_version"] == "1.1.0"
    assert ws_mirror["resolved_feedbacks_count"] == 1
