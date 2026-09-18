import json
import pytest
from pathlib import Path
import jsonschema

SCHEMAS_DIR = Path(__file__).resolve().parents[2] / "schemas"

def test_evolution_ledger_schema_valid():
    schema_path = SCHEMAS_DIR / "evolution-ledger.schema.json"
    assert schema_path.exists(), "evolution-ledger.schema.json must exist"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    
    valid_ledger = {
        "schema_version": "2.0.0",
        "kit_id": "test-agent-kit",
        "current_canonical_version": "1.1.0",
        "lineage": {
            "created_at": "2026-08-26T00:00:00Z",
            "last_evolved_at": "2026-08-26T01:00:00Z",
            "total_evolution_cycles": 1
        },
        "evolution_runs": [
            {
                "run_id": "evo_run_20260826_01",
                "from_version": "1.0.0",
                "to_version": "1.1.0",
                "triggered_by_batch": "batch-test-20260826T000000Z",
                "risk_tier": "TIER_1_STANDARD",
                "human_approval": {
                    "required": False,
                    "approved_by": None,
                    "approved_at": None
                },
                "snapshot_ref": "evolution/snapshots/test-agent-kit/v1.0.0-abcdef/",
                "feedbacks_addressed": ["fb_001"],
                "verification_evidence": {
                    "l1_linter_pass": True,
                    "linter_command": "python .agents/scripts/validate_kit.py .agents",
                    "linter_score": 5,
                    "error_count": 0,
                    "log_snippet": "0 error(s) - [PASS]"
                }
            }
        ],
        "feedback_items": [
            {
                "feedback_id": "fb_001",
                "batch_id": "batch-test-20260826T000000Z",
                "source_version": "1.0.0",
                "cluster_key": "prompt_format_error",
                "category": "failure",
                "status": "RELEASED",
                "received_at": "2026-08-26T00:00:00Z",
                "diagnosed_root_cause": "Missing negative constraints",
                "resolved_in_run_id": "evo_run_20260826_01",
                "resolved_in_version": "1.1.0",
                "impacted_files": ["agent/writer.md"]
            }
        ]
    }
    
    jsonschema.validate(instance=valid_ledger, schema=schema)

def test_evolution_ledger_schema_rejects_invalid_status():
    schema_path = SCHEMAS_DIR / "evolution-ledger.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    
    invalid_ledger = {
        "schema_version": "2.0.0",
        "kit_id": "test-agent-kit",
        "current_canonical_version": "1.0.0",
        "lineage": {
            "created_at": "2026-08-26T00:00:00Z",
            "last_evolved_at": "2026-08-26T00:00:00Z",
            "total_evolution_cycles": 0
        },
        "evolution_runs": [],
        "feedback_items": [
            {
                "feedback_id": "fb_001",
                "batch_id": "batch-01",
                "source_version": "1.0.0",
                "cluster_key": "test",
                "category": "failure",
                "status": "INVALID_STATUS_NAME",
                "received_at": "2026-08-26T00:00:00Z"
            }
        ]
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_ledger, schema=schema)

def test_snapshot_manifest_schema_valid():
    schema_path = SCHEMAS_DIR / "snapshot-manifest.schema.json"
    assert schema_path.exists(), "snapshot-manifest.schema.json must exist"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    
    valid_manifest = {
        "schema_version": "1.0.0",
        "kit_name": "test-agent-kit",
        "version": "1.0.0",
        "created_at": "2026-08-26T00:00:00Z",
        "root_hash": "a1b2c3d4e5f67890",
        "total_files": 12,
        "total_bytes": 45000,
        "tree_checksum": {
            "manifest.json": "hash1",
            ".agents/agent/main.md": "hash2"
        }
    }
    jsonschema.validate(instance=valid_manifest, schema=schema)
