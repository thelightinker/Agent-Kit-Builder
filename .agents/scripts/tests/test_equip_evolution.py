import json
import pytest
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import equip_evolution

@pytest.fixture
def sample_single_agent_kit(tmp_path):
    kit_dir = tmp_path / "solo-writer"
    agents_dir = kit_dir / ".agents"
    agents_dir.mkdir(parents=True)
    
    (agents_dir / "VERSION").write_text("1.0.0", encoding="utf-8")
    
    agent_dir = agents_dir / "agent"
    agent_dir.mkdir()
    (agent_dir / "solo-agent.md").write_text("""---
name: solo-agent
description: A solo writer agent
---
# Solo Agent
## 1. Vai trò & Quyền hạn (Role & Outcome)
Trách nhiệm chính
## 2. Quy trình Xử lý (Process)
Bước 1, Bước 2
## 3. Ranh giới Phủ định (Hard Constraints)
Cấm làm bậy
## 4. Format Đầu Ra & Definition of Done (DoD)
- [ ] Xong
""", encoding="utf-8")

    skills_dir = agents_dir / "skills" / "writing-skill"
    skills_dir.mkdir(parents=True)
    (skills_dir / "SKILL.md").write_text("""---
name: writing-skill
description: Useful writing skill
---
# Writing Skill
### Examples
Input: a
Output: b
""", encoding="utf-8")

    (agents_dir / "manifest.json").write_text(json.dumps({
        "schema_version": "2.0.0",
        "name": "solo-writer",
        "version": "1.0.0",
        "agents": {
            "solo-agent": {"path": "agent/solo-agent.md", "version": "1.0.0"}
        },
        "skills": {
            "writing-skill": {"path": "skills/writing-skill/SKILL.md", "version": "1.0.0"}
        },
        "workflows": {}
    }), encoding="utf-8")
    
    return kit_dir

def test_equip_kit_resolves_dynamic_agent_and_skill(sample_single_agent_kit, tmp_path):
    engine_root = Path(__file__).resolve().parents[2]
    
    ok = equip_evolution.equip_kit(sample_single_agent_kit, engine_root=engine_root)
    assert ok is True
    
    agents_dir = sample_single_agent_kit / ".agents"
    log_fb_wf = (agents_dir / "workflows" / "log-feedback.md").read_text(encoding="utf-8")
    submit_evo_wf = (agents_dir / "workflows" / "submit-evolution.md").read_text(encoding="utf-8")
    
    # Must NOT contain hardcoded kit-architect or kit-evolving
    assert "kit-architect" not in log_fb_wf
    assert "kit-evolving" not in log_fb_wf
    assert "solo-agent" in log_fb_wf
    assert "writing-skill" in log_fb_wf
    
    assert "kit-architect" not in submit_evo_wf
    assert "kit-exporting" not in submit_evo_wf
    assert "solo-agent" in submit_evo_wf
    assert "writing-skill" in submit_evo_wf
    
    # Check directory structure
    assert (agents_dir / "evolution" / "feedback").exists()
    assert (agents_dir / "evolution" / "outbox").exists()
    assert (agents_dir / "evolution" / "EVOLUTION_HISTORY.json").exists()
    
    # Check manifest
    manifest = json.loads((agents_dir / "manifest.json").read_text(encoding="utf-8"))
    assert "log-feedback" in manifest["workflows"]
    assert "submit-evolution" in manifest["workflows"]
    assert manifest["workflows"]["log-feedback"]["requires"]["agents"] == ["solo-agent"]
    assert manifest["workflows"]["log-feedback"]["requires"]["skills"] == ["writing-skill"]
