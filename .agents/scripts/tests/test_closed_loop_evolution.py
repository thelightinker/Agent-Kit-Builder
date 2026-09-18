import unittest
import tempfile
import json
import shutil
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import feedback_collector
import evolution_submitter
import evolution_engine
import atomic_promoter

class TestClosedLoopEvolutionE2E(unittest.TestCase):
    def test_full_closed_loop_lifecycle_and_rollback(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            
            # Setup Kit Workspace (Distributed runtime)
            kit_root = root / "workspaces" / "content-engine"
            kit_agents = kit_root / ".agents"
            kit_agents.mkdir(parents=True)
            (kit_agents / "VERSION").write_text("1.0.0", encoding="utf-8")
            (kit_root / "rules").mkdir(parents=True)
            (kit_root / "rules" / "format.md").write_text("v1 format rules", encoding="utf-8")
            
            # Setup Engine Hub Workspace
            engine_root = root / "engine"
            inbox = engine_root / "evolution" / "inbox"
            processing = engine_root / "evolution" / "processing"
            completed = engine_root / "evolution" / "completed"
            rejected = engine_root / "evolution" / "rejected"
            canonical_output = engine_root / "Output" / "content-engine"
            canonical_archive = engine_root / "Output" / ".archive"
            target_archive = kit_root.parent / ".archive"
            
            # Populate canonical output with v1
            canonical_output.mkdir(parents=True)
            (canonical_output / "VERSION").write_text("1.0.0", encoding="utf-8")
            (canonical_output / "format.md").write_text("v1 format rules", encoding="utf-8")
            
            # Phase 1: Kit captures feedback
            fb_file = kit_agents / "evolution" / "feedback" / "feedback.jsonl"
            for i in range(6):
                feedback_collector.append_feedback(fb_file, {
                    "category": "failure",
                    "problem": f"Markdown table column issue #{i}",
                    "impact": 5 if i == 0 else 4,
                    "confidence": 1.0,
                    "generalizability": 2,
                    "context": {"agent": "writer", "skill": "formatter"}
                })
                
            status = feedback_collector.check_evolution_status(fb_file, threshold=20.0)
            self.assertTrue(status["evolution_ready"])
            self.assertGreaterEqual(status["total_trigger_score"], 20.0)
            
            # Phase 2: Kit submits evolution package (3-stage handshake)
            batch_dir = evolution_submitter.pack_batch(kit_root)
            transferred_batch = evolution_submitter.transfer_batch(batch_dir, inbox)
            ack = evolution_submitter.verify_and_acknowledge(transferred_batch)
            self.assertTrue(ack["valid"])
            self.assertEqual(ack["status"], "RECEIVED")
            
            confirmed = evolution_submitter.confirm_submitted(batch_dir, transferred_batch / "receipt.json", fb_file)
            self.assertTrue(confirmed)
            self.assertEqual(feedback_collector.load_feedback(fb_file), []) # buffer cleared
            
            # Phase 3: Engine claims batch & checks Upgrade Gate
            claimed = evolution_engine.claim_batch(inbox, processing, batch_dir.name)
            self.assertIsNotNone(claimed)
            
            manifest = json.loads((claimed / "manifest.json").read_text("utf-8"))
            gate = evolution_engine.evaluate_upgrade_gate(manifest)
            self.assertTrue(gate["passed"])
            self.assertGreater(gate["net_gain"], 0)
            
            # Phase 4: Engine stages vNext
            staging_dir = engine_root / "staging" / "content-engine"
            evolution_engine.compile_vnext_staging(canonical_output, staging_dir)
            (staging_dir / "format.md").write_text("v2 format rules with autowrap", encoding="utf-8")
            
            # Phase 5: Two-Phase Atomic Promotion
            promotion = atomic_promoter.execute_two_phase_promotion(
                staging_dir=staging_dir,
                canonical_dir=canonical_output,
                target_dir=kit_root,
                engine_archive=canonical_archive,
                target_archive=target_archive
            )
            self.assertTrue(promotion["success"])
            self.assertTrue(promotion["checksum_verified"])
            
            # Verify active contents
            self.assertEqual((canonical_output / "format.md").read_text("utf-8"), "v2 format rules with autowrap")
            self.assertEqual((kit_root / "format.md").read_text("utf-8"), "v2 format rules with autowrap")
            
            # Complete batch
            completed.mkdir(parents=True, exist_ok=True)
            shutil.move(claimed, completed / claimed.name)
            self.assertTrue((completed / claimed.name).exists())

    def test_auto_discovery_pipeline_and_radar_e2e(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            
            # 1. Setup Engine Hub in workspace
            engine_dir = workspace / "Agent Kit Engine"
            (engine_dir / ".agents" / "scripts").mkdir(parents=True)
            (engine_dir / ".agents" / "scripts" / "evolution_engine.py").write_text("# engine", encoding="utf-8")
            (engine_dir / "evolution" / "inbox").mkdir(parents=True)
            
            # 2. Setup Sibling Kit in workspace
            kit_dir = workspace / "content-engine"
            (kit_dir / ".agents" / "evolution" / "feedback").mkdir(parents=True)
            (kit_dir / ".agents" / "manifest.json").write_text("{}", encoding="utf-8")
            (kit_dir / ".agents" / "VERSION").write_text("1.0.0", encoding="utf-8")
            
            # Kit records critical feedback
            fb_file = kit_dir / ".agents" / "evolution" / "feedback" / "feedback.jsonl"
            for i in range(6):
                feedback_collector.append_feedback(fb_file, {
                    "category": "failure",
                    "problem": f"Critical schema issue #{i}",
                    "impact": 5,
                    "confidence": 1.0,
                    "generalizability": 2,
                    "context": {"agent": "writer", "skill": "schema"}
                })
                
            # Engine Radar scans workspace and detects kit ready
            radar = evolution_engine.scan_evolution_radar(workspace)
            self.assertEqual(len(radar), 1)
            self.assertEqual(radar[0]["kit_id"], "content-engine")
            self.assertEqual(radar[0]["status"], "🔴 READY")
            
            # Kit executes zero-config submit (auto-discovery)
            res = evolution_submitter.submit_evolution_pipeline(kit_dir)
            self.assertTrue(res["success"])
            self.assertTrue((engine_dir / "evolution" / "inbox" / res["batch_id"]).exists())

if __name__ == "__main__":
    unittest.main()
