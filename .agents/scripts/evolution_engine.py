#!/usr/bin/env python3
"""
Central Evolution Engine & Net System Gain Upgrade Gate.
Manages the batch lifecycle (inbox -> processing -> completed/rejected),
evaluates Net System Gain according to UPGRADE_PRINCIPLES.md,
compiles vNext staging artifacts, and provides Evolution Radar telemetry.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import feedback_collector

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def is_valid_kit_directory(path: Path) -> bool:
    if not path.is_dir() or path.name.startswith('.'):
        return False
    # Exclude engine itself
    if path.name == 'Agent Kit Engine' or (path / '.agents' / 'scripts' / 'evolution_engine.py').exists():
        return False
    # Primary Marker
    if (path / '.agents' / 'manifest.json').exists():
        return True
    # Fallback Marker
    if (path / '.agents' / 'VERSION').exists() or (path / 'VERSION').exists():
        return True
    return False

def get_engine_root() -> Path:
    cur = Path(__file__).resolve().parents[2]
    return cur

def scan_evolution_radar(kits_root: Path | None = None) -> list[dict[str, Any]]:
    engine_root = get_engine_root()
    is_custom_root = bool(kits_root)
    if not kits_root:
        kits_root = engine_root.parent
        
    kits_root = Path(kits_root).resolve()
    if not kits_root.is_dir():
        return []
        
    radar_results = []
    # Check direct kits in kits_root and also in kits_root / 'Output' (if running default inside Engine workspace)
    search_dirs = [kits_root]
    if not is_custom_root and (engine_root / "Output").is_dir() and kits_root != (engine_root / "Output"):
        search_dirs.append(engine_root / "Output")
        
    seen_kits = set()
    for s_dir in search_dirs:
        for item in sorted(s_dir.iterdir()):
            if is_valid_kit_directory(item) and item.name not in seen_kits:
                seen_kits.add(item.name)
                wf_data = feedback_collector.locate_kit_feedback_sources(item, engine_root)
                agg = wf_data["aggregate"]
                
                score = agg["effective_trigger_score"]
                is_ready = agg["evolution_ready"]
                has_pending = agg["has_pending_inbox"] or agg["has_processing"] or agg["has_outbox_unprocessed"]
                
                if is_ready:
                    tier = '🔴 READY'
                elif has_pending:
                    tier = '📦 BATCH_PENDING'
                elif score >= 10.0:
                    tier = '🟡 WATCH'
                else:
                    tier = '🟢 HEALTHY'
                    
                # Determine primary source description
                if agg["has_pending_inbox"]:
                    b_id = wf_data["inbox_batches"][0]["batch_id"]
                    source_desc = f"inbox:{b_id}"
                elif agg["has_outbox_unprocessed"]:
                    b_id = wf_data["outbox_batches"][-1]["batch_id"]
                    source_desc = f"outbox:{b_id}"
                elif agg["has_active_feedback"]:
                    source_desc = "active_buffer"
                else:
                    source_desc = "none"
                    
                radar_results.append({
                    'kit_id': item.name,
                    'path': str(item.resolve()),
                    'trigger_score': score,
                    'feedback_count': agg["effective_feedback_count"],
                    'clusters_count': len(agg["clusters"]),
                    'status': tier,
                    'evolution_ready': is_ready,
                    'source_desc': source_desc,
                    'waterfall': wf_data,
                    'clusters': agg["clusters"]
                })
            
    radar_results.sort(key=lambda x: x['trigger_score'], reverse=True)
    return radar_results

def print_radar_report(kits_root: Path | None = None) -> None:
    results = scan_evolution_radar(kits_root)
    workspace_path = str(Path(kits_root).resolve()) if kits_root else str(get_engine_root().parent)
    
    print('=' * 85)
    print('📡 AGENT KIT EVOLUTION RADAR (Unified 4-Tier Waterfall)')
    print('=' * 85)
    print(f'Workspace: {workspace_path}')
    print('-' * 85)
    print(f'{"Kit Name":<26} {"Score":>7} {"Feedback":>9} {"Clusters":>9}   {"Status":<16} {"Source":<16}')
    print('─' * 85)
    
    ready_count = 0
    pending_count = 0
    for r in results:
        if 'READY' in r['status']:
            ready_count += 1
        if 'PENDING' in r['status']:
            pending_count += 1
        print(f'{r["kit_id"]:<26} {r["trigger_score"]:>7.1f} {r["feedback_count"]:>9} {r["clusters_count"]:>9}   {r["status"]:<16} {r["source_desc"]:<16}')
        
    print('=' * 85)
    print('💡 Actionable Insights:')
    if ready_count > 0 or pending_count > 0:
        print(f'   [!] {ready_count + pending_count} kit(s) ready or pending evolution. Run: /process-evolution <kit-name>')
    else:
        print('   [+] All active kits are within healthy operational boundaries.')
    print('=' * 85)

def list_inbox_batches(inbox_dir: Path) -> list[dict[str, Any]]:
    if not inbox_dir.is_dir():
        return []
    batches = []
    for item in sorted(inbox_dir.iterdir()):
        if item.is_dir() and item.name.startswith('batch-'):
            manifest_file = item / 'manifest.json'
            if manifest_file.exists():
                try:
                    data = json.loads(manifest_file.read_text('utf-8'))
                    batches.append(data)
                except json.JSONDecodeError:
                    pass
    return batches

def claim_batch(inbox_dir: Path, processing_dir: Path, batch_id: str) -> Path | None:
    src = inbox_dir / batch_id
    if not src.is_dir():
        return None
    processing_dir.mkdir(parents=True, exist_ok=True)
    dst = processing_dir / batch_id
    shutil.move(src, dst)
    return dst

def evaluate_upgrade_gate(batch_manifest: dict[str, Any]) -> dict[str, Any]:
    stats = batch_manifest.get('statistics', {})
    clusters = batch_manifest.get('clusters', [])
    trigger_score = stats.get('total_trigger_score', 0.0)
    
    # Gross Value = Sum of cluster scores + impact weights
    gross_value = trigger_score
    
    # Total Cost = complexity + risk baseline
    total_cost = 5.0
    
    net_gain = gross_value - total_cost
    passed = net_gain > 0 and len(clusters) > 0
    
    return {
        'passed': passed,
        'gross_value': round(gross_value, 2),
        'total_cost': round(total_cost, 2),
        'net_gain': round(net_gain, 2),
        'cluster_count': len(clusters),
        'reason': 'Positive Net System Gain' if passed else 'Insufficient Net Gain / No evidence'
    }

def compile_vnext_staging(canonical_kit_dir: Path, staging_dir: Path) -> Path:
    staging_dir.parent.mkdir(parents=True, exist_ok=True)
    if staging_dir.exists():
        shutil.rmtree(staging_dir)
    shutil.copytree(canonical_kit_dir, staging_dir)
    
    # Bump VERSION in staging
    v_file = staging_dir / '.agents' / 'VERSION' if (staging_dir / '.agents' / 'VERSION').exists() else staging_dir / 'VERSION'
    if v_file.exists():
        cur_v = v_file.read_text('utf-8').strip()
        parts = cur_v.split('.')
        if len(parts) == 3 and parts[-1].isdigit():
            parts[-1] = str(int(parts[-1]) + 1)
            new_v = '.'.join(parts)
        else:
            new_v = cur_v + '-vNext'
        v_file.write_text(new_v, encoding='utf-8')
    return staging_dir

def process_kit_evolution(kit_name: str, engine_root: Path | None = None, auto_compile: bool = False) -> dict[str, Any]:
    engine_root = engine_root or get_engine_root()
    inbox_dir = engine_root / "evolution" / "inbox"
    proc_dir = engine_root / "evolution" / "processing"
    
    # Locate kit
    kit_candidate = engine_root.parent / kit_name
    if not kit_candidate.is_dir():
        kit_candidate = engine_root / "Output" / kit_name
    
    wf = feedback_collector.locate_kit_feedback_sources(kit_candidate if kit_candidate.is_dir() else Path(kit_name), engine_root)
    
    # Check for pending inbox batch
    target_manifest = None
    target_batch_dir = None
    
    if wf["inbox_batches"]:
        target_batch_dir = Path(wf["inbox_batches"][0]["path"])
        target_manifest = wf["inbox_batches"][0]["manifest"]
    elif wf["processing_batches"]:
        target_batch_dir = Path(wf["processing_batches"][0]["path"])
        target_manifest = wf["processing_batches"][0]["manifest"]
    elif wf["outbox_batches"]:
        target_batch_dir = Path(wf["outbox_batches"][-1]["path"])
        target_manifest = wf["outbox_batches"][-1]["manifest"]
    elif wf["active_buffer"]["exists"] and wf["active_buffer"]["count"] > 0:
        return {
            "success": False,
            "error": f"Kit '{kit_name}' has unsubmitted active feedback ({wf['active_buffer']['count']} items). Run '/submit-evolution' first."
        }
    else:
        return {
            "success": False,
            "error": f"No feedback or evolution batch found for kit '{kit_name}' across all 4 Waterfall tiers."
        }
        
    gate_eval = evaluate_upgrade_gate(target_manifest)
    
    result = {
        "success": True,
        "kit_name": kit_name,
        "batch_id": target_manifest.get("batch_id"),
        "source_batch_dir": str(target_batch_dir),
        "gate_evaluation": gate_eval,
        "clusters": target_manifest.get("clusters", [])
    }
    
    if auto_compile and gate_eval["passed"] and kit_candidate.is_dir():
        staging_dir = engine_root / "Output" / f"{kit_name}_vNext"
        compile_vnext_staging(kit_candidate, staging_dir)
        result["staging_dir"] = str(staging_dir)
        
    return result

def main():
    parser = argparse.ArgumentParser(description='Agent Kit Central Evolution Engine')
    parser.add_argument('kit_name', nargs='?', help='Kit name to process')
    parser.add_argument('--inbox', default='evolution/inbox', help='Path to inbox directory')
    parser.add_argument('--processing', default='evolution/processing', help='Path to processing directory')
    parser.add_argument('--list', action='store_true', help='List pending batches in inbox')
    parser.add_argument('--radar', action='store_true', help='Scan all active workspace kits and print telemetry radar')
    parser.add_argument('--inspect', help='Inspect complete Waterfall sources for a specific kit')
    parser.add_argument('--compile', action='store_true', help='Automatically compile staging vNext if gate passes')
    parser.add_argument('--workspace', default=None, help='Workspace directory for --radar (default: parent of Engine)')
    
    args = parser.parse_args()
    engine_root = get_engine_root()
    
    if args.radar:
        print_radar_report(args.workspace)
        return
        
    if args.inspect:
        target = Path(args.inspect)
        if not target.is_dir():
            target = engine_root.parent / args.inspect
        if not target.is_dir():
            target = engine_root / "Output" / args.inspect
        res = feedback_collector.locate_kit_feedback_sources(target, engine_root)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return
        
    inbox_p = (engine_root / args.inbox).resolve()
    
    if args.list:
        batches = list_inbox_batches(inbox_p)
        print(json.dumps(batches, indent=2, ensure_ascii=False))
        return
        
    if args.kit_name:
        res = process_kit_evolution(args.kit_name, engine_root, auto_compile=args.compile)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return
        
    parser.print_help()

if __name__ == '__main__':
    main()
