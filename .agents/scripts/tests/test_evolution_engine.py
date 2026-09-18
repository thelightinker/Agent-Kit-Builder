import unittest
import tempfile
import json
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import feedback_collector
import evolution_engine

class TestEvolutionEngine(unittest.TestCase):
    def test_claim_and_upgrade_gate_net_gain(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            engine_root = Path(tmpdir)
            inbox = engine_root / "evolution" / "inbox"
            proc = engine_root / "evolution" / "processing"
            batch_dir = inbox / "batch-test-20260824-001"
            batch_dir.mkdir(parents=True)
            
            manifest_data = {
                "schema_version": "1.0.0",
                "batch_id": "batch-test-20260824-001",
                "kit_id": "test-kit",
                "kit_version": "1.0.0",
                "statistics": {"total_trigger_score": 25.0, "total_feedback_count": 5},
                "clusters": [{"cluster_key": "test.cluster", "derived_frequency": 5, "max_impact": 4, "avg_confidence": 1.0, "generalizability": 2, "cluster_score": 15.0}]
            }
            (batch_dir / "manifest.json").write_text(json.dumps(manifest_data), encoding="utf-8")
            (batch_dir / "feedback.jsonl").write_text("{}", encoding="utf-8")
            
            # Claim batch
            claimed = evolution_engine.claim_batch(inbox, proc, "batch-test-20260824-001")
            self.assertIsNotNone(claimed)
            self.assertTrue(claimed.exists())
            self.assertFalse(batch_dir.exists())
            
            # Evaluate Net Gain
            gate_report = evolution_engine.evaluate_upgrade_gate(manifest_data)
            self.assertTrue(gate_report["passed"])
            self.assertGreater(gate_report["net_gain"], 0)

    def test_scan_evolution_radar_and_classification(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            
            # 1. Ready Kit (Primary marker .agents/manifest.json)
            ready_kit = workspace / "ready-kit"
            (ready_kit / ".agents" / "evolution" / "feedback").mkdir(parents=True)
            (ready_kit / ".agents" / "manifest.json").write_text("{}", encoding="utf-8")
            ready_fb = ready_kit / ".agents" / "evolution" / "feedback" / "feedback.jsonl"
            for i in range(6):
                feedback_collector.append_feedback(ready_fb, {
                    "category": "failure",
                    "problem": f"Crash #{i}",
                    "impact": 5 if i == 0 else 4,
                    "confidence": 1.0,
                    "generalizability": 2,
                    "context": {"agent": "worker", "skill": "core"}
                })
                
            # 2. Watch Kit (Primary marker)
            watch_kit = workspace / "watch-kit"
            (watch_kit / ".agents" / "evolution" / "feedback").mkdir(parents=True)
            (watch_kit / ".agents" / "manifest.json").write_text("{}", encoding="utf-8")
            watch_fb = watch_kit / ".agents" / "evolution" / "feedback" / "feedback.jsonl"
            for i in range(3):
                feedback_collector.append_feedback(watch_fb, {
                    "category": "friction",
                    "problem": f"Slow response #{i}",
                    "impact": 4,
                    "confidence": 0.8,
                    "generalizability": 3,
                    "context": {"agent": "worker", "skill": "formatter"}
                })
                
            # 3. Healthy Kit (Primary marker, 0 feedbacks)
            healthy_kit = workspace / "healthy-kit"
            (healthy_kit / ".agents").mkdir(parents=True)
            (healthy_kit / ".agents" / "manifest.json").write_text("{}", encoding="utf-8")
            
            # 4. Legacy Kit (Fallback marker .agents/VERSION)
            legacy_kit = workspace / "legacy-kit"
            (legacy_kit / ".agents").mkdir(parents=True)
            (legacy_kit / ".agents" / "VERSION").write_text("1.0.0", encoding="utf-8")
            
            # 5. Non-kit directory (Must be ignored)
            random_dir = workspace / "random-folder"
            random_dir.mkdir()
            
            # 6. Self Engine directory (Must be ignored)
            engine_dir = workspace / "Agent Kit Engine"
            (engine_dir / ".agents").mkdir(parents=True)
            (engine_dir / ".agents" / "manifest.json").write_text("{}", encoding="utf-8")
            
            radar = evolution_engine.scan_evolution_radar(workspace)
            radar_dict = {item["kit_id"]: item for item in radar}
            
            self.assertEqual(len(radar), 4)
            self.assertIn("ready-kit", radar_dict)
            self.assertIn("watch-kit", radar_dict)
            self.assertIn("healthy-kit", radar_dict)
            self.assertIn("legacy-kit", radar_dict)
            self.assertNotIn("random-folder", radar_dict)
            self.assertNotIn("Agent Kit Engine", radar_dict)
            
            self.assertEqual(radar_dict["ready-kit"]["status"], "🔴 READY")
            self.assertIn(radar_dict["watch-kit"]["status"], ["🟡 WATCH", "🔴 READY"])
            self.assertEqual(radar_dict["healthy-kit"]["status"], "🟢 HEALTHY")
            self.assertEqual(radar_dict["legacy-kit"]["status"], "🟢 HEALTHY")

    def test_radar_detects_outbox_batch_when_buffer_is_empty(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            
            # Kit with empty buffer but valid outbox batch
            kit = workspace / "outbox-kit"
            (kit / ".agents" / "evolution" / "feedback").mkdir(parents=True)
            (kit / ".agents" / "manifest.json").write_text("{}", encoding="utf-8")
            (kit / ".agents" / "evolution" / "outbox" / "batch-outbox-kit-20260824-001").mkdir(parents=True)
            
            manifest_data = {
                "schema_version": "1.0.0",
                "batch_id": "batch-outbox-kit-20260824-001",
                "kit_id": "outbox-kit",
                "statistics": {"total_trigger_score": 25.0, "total_feedback_count": 4},
                "clusters": [{"cluster_key": "c.k", "cluster_score": 25.0}]
            }
            (kit / ".agents" / "evolution" / "outbox" / "batch-outbox-kit-20260824-001" / "manifest.json").write_text(
                json.dumps(manifest_data), encoding="utf-8"
            )
            
            radar = evolution_engine.scan_evolution_radar(workspace)
            radar_dict = {item["kit_id"]: item for item in radar}
            
            self.assertIn("outbox-kit", radar_dict)
            self.assertEqual(radar_dict["outbox-kit"]["trigger_score"], 25.0)
            self.assertEqual(radar_dict["outbox-kit"]["status"], "🔴 READY")
            self.assertIn("outbox:", radar_dict["outbox-kit"]["source_desc"])

if __name__ == "__main__":
    unittest.main()
