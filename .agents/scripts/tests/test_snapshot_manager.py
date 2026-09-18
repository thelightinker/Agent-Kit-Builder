import json
import pytest
from pathlib import Path
import shutil
import sys

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import snapshot_manager

@pytest.fixture
def mock_kit(tmp_path):
    kit_dir = tmp_path / "sample-kit"
    kit_dir.mkdir(parents=True)
    (kit_dir / "README.md").write_text("# Sample Kit\nVersion 1.0", encoding="utf-8")
    (kit_dir / "config.json").write_text('{"name": "sample-kit"}', encoding="utf-8")
    
    agents_dir = kit_dir / ".agents"
    agents_dir.mkdir()
    (agents_dir / "VERSION").write_text("1.0.0", encoding="utf-8")
    
    agent_dir = agents_dir / "agent"
    agent_dir.mkdir()
    (agent_dir / "main.md").write_text("Agent Main Prompt", encoding="utf-8")
    
    return kit_dir

def test_compute_tree_hash(mock_kit):
    tree_data = snapshot_manager.compute_tree_hash(mock_kit)
    assert "root_hash" in tree_data
    assert "tree_checksum" in tree_data
    assert "total_files" in tree_data
    assert tree_data["total_files"] == 4
    assert "README.md" in tree_data["tree_checksum"]
    assert ".agents/VERSION" in tree_data["tree_checksum"] or ".agents\\VERSION" in tree_data["tree_checksum"] or any("VERSION" in k for k in tree_data["tree_checksum"])

def test_create_snapshot_and_manifest(mock_kit, tmp_path):
    engine_root = tmp_path / "engine"
    engine_root.mkdir()
    
    snap_path = snapshot_manager.create_snapshot(mock_kit, engine_root, version="1.0.0")
    assert snap_path.exists()
    assert (snap_path / "snapshot_manifest.json").exists()
    assert (snap_path / "README.md").exists()
    assert (snap_path / ".agents" / "VERSION").exists()
    
    manifest = json.loads((snap_path / "snapshot_manifest.json").read_text("utf-8"))
    assert manifest["version"] == "1.0.0"
    assert manifest["kit_name"] == "sample-kit"
    assert manifest["total_files"] == 4

def test_diff_snapshots(mock_kit, tmp_path):
    engine_root = tmp_path / "engine"
    engine_root.mkdir()
    
    snap1 = snapshot_manager.create_snapshot(mock_kit, engine_root, version="1.0.0")
    
    # Modify kit for v2
    (mock_kit / "README.md").write_text("# Sample Kit v2", encoding="utf-8")
    (mock_kit / "new_file.txt").write_text("hello", encoding="utf-8")
    
    snap2 = snapshot_manager.create_snapshot(mock_kit, engine_root, version="1.1.0")
    
    diff = snapshot_manager.diff_snapshots(snap1, snap2)
    assert "new_file.txt" in diff["added"]
    assert any("README.md" in f for f in diff["modified"])
    assert len(diff["removed"]) == 0

def test_rollback_to_snapshot(mock_kit, tmp_path):
    engine_root = tmp_path / "engine"
    engine_root.mkdir()
    
    snap1 = snapshot_manager.create_snapshot(mock_kit, engine_root, version="1.0.0")
    
    # Mess up the kit
    (mock_kit / "README.md").write_text("CORRUPTED CONTENT", encoding="utf-8")
    (mock_kit / "unwanted.tmp").write_text("junk", encoding="utf-8")
    
    ok = snapshot_manager.rollback_to_snapshot(mock_kit, snap1)
    assert ok is True
    assert (mock_kit / "README.md").read_text("utf-8") == "# Sample Kit\nVersion 1.0"
    assert not (mock_kit / "unwanted.tmp").exists()
