#!/usr/bin/env python3
"""
Snapshot Manager for Agent Kit Engine.
Captures full-kit root snapshots with SHA-256 tree hashing, generates snapshot_manifest.json,
computes deterministic diffs between versions, and performs safe atomic rollbacks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

IGNORED_NAMES = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".DS_Store",
    "Thumbs.db",
    "snapshot_manifest.json"
}

def sha256_file(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def compute_tree_hash(kit_path: Path) -> dict[str, Any]:
    """
    Computes SHA-256 for every file in kit_path and aggregate root hash.
    """
    kit_path = Path(kit_path).resolve()
    tree_checksum: dict[str, str] = {}
    total_bytes = 0
    
    if not kit_path.is_dir():
        return {
            "root_hash": "",
            "total_files": 0,
            "total_bytes": 0,
            "tree_checksum": {}
        }
        
    for root, dirs, files in os.walk(kit_path):
        # Exclude ignored dirs in-place
        dirs[:] = [d for d in dirs if d not in IGNORED_NAMES]
        for f in sorted(files):
            if f in IGNORED_NAMES or f.endswith(".pyc") or f.endswith(".tmp"):
                continue
            fp = Path(root) / f
            rel = fp.relative_to(kit_path).as_posix()
            f_hash = sha256_file(fp)
            tree_checksum[rel] = f_hash
            try:
                total_bytes += fp.stat().st_size
            except OSError:
                pass
                
    # Aggregate root hash from sorted path:hash pairs
    h = hashlib.sha256()
    for rel_path in sorted(tree_checksum.keys()):
        h.update(f"{rel_path}:{tree_checksum[rel_path]}\n".encode("utf-8"))
        
    return {
        "root_hash": h.hexdigest(),
        "total_files": len(tree_checksum),
        "total_bytes": total_bytes,
        "tree_checksum": tree_checksum
    }

def create_snapshot(kit_path: Path, engine_root: Path, version: str) -> Path:
    """
    Snapshots entire kit root directory to engine's evolution/snapshots/<kit_name>/v<version>-<short_hash>/
    """
    kit_path = Path(kit_path).resolve()
    engine_root = Path(engine_root).resolve()
    kit_name = kit_path.name
    
    tree_data = compute_tree_hash(kit_path)
    root_hash = tree_data["root_hash"]
    short_hash = root_hash[:8] if root_hash else "00000000"
    
    snapshot_dir = engine_root / "evolution" / "snapshots" / kit_name / f"v{version}-{short_hash}"
    if snapshot_dir.exists():
        shutil.rmtree(snapshot_dir)
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy all kit files
    shutil.copytree(
        kit_path,
        snapshot_dir,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "*.tmp")
    )
    
    # Create snapshot_manifest.json
    manifest_data = {
        "schema_version": "1.0.0",
        "kit_name": kit_name,
        "version": version,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "root_hash": root_hash,
        "total_files": tree_data["total_files"],
        "total_bytes": tree_data["total_bytes"],
        "tree_checksum": tree_data["tree_checksum"]
    }
    
    manifest_file = snapshot_dir / "snapshot_manifest.json"
    manifest_file.write_text(json.dumps(manifest_data, indent=2, ensure_ascii=False), encoding="utf-8")
    
    return snapshot_dir

def diff_snapshots(snap_a: Path, snap_b: Path) -> dict[str, Any]:
    """
    Compares two snapshot directories using their snapshot_manifest.json or tree hashes.
    """
    snap_a = Path(snap_a).resolve()
    snap_b = Path(snap_b).resolve()
    
    manifest_a = snap_a / "snapshot_manifest.json"
    manifest_b = snap_b / "snapshot_manifest.json"
    
    tree_a = json.loads(manifest_a.read_text("utf-8"))["tree_checksum"] if manifest_a.exists() else compute_tree_hash(snap_a)["tree_checksum"]
    tree_b = json.loads(manifest_b.read_text("utf-8"))["tree_checksum"] if manifest_b.exists() else compute_tree_hash(snap_b)["tree_checksum"]
    
    added = sorted([f for f in tree_b if f not in tree_a])
    removed = sorted([f for f in tree_a if f not in tree_b])
    modified = sorted([f for f in tree_a if f in tree_b and tree_a[f] != tree_b[f]])
    
    return {
        "added": added,
        "removed": removed,
        "modified": modified,
        "is_identical": len(added) == 0 and len(removed) == 0 and len(modified) == 0
    }

def rollback_to_snapshot(kit_path: Path, snapshot_path: Path) -> bool:
    """
    Restores kit_path completely from snapshot_path.
    """
    kit_path = Path(kit_path).resolve()
    snapshot_path = Path(snapshot_path).resolve()
    
    if not snapshot_path.is_dir():
        print(f"❌ Snapshot path does not exist: {snapshot_path}", file=sys.stderr)
        return False
        
    # Backup current state into a temp folder in case rollback fails
    temp_backup = kit_path.parent / f".temp_backup_{kit_path.name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    if kit_path.exists():
        shutil.copytree(kit_path, temp_backup, dirs_exist_ok=True)
        shutil.rmtree(kit_path)
        
    try:
        shutil.copytree(
            snapshot_path,
            kit_path,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("snapshot_manifest.json")
        )
        if temp_backup.exists():
            shutil.rmtree(temp_backup, ignore_errors=True)
        return True
    except Exception as e:
        print(f"❌ Rollback failed: {e}. Restoring previous state.", file=sys.stderr)
        if temp_backup.exists():
            if kit_path.exists():
                shutil.rmtree(kit_path, ignore_errors=True)
            shutil.copytree(temp_backup, kit_path, dirs_exist_ok=True)
            shutil.rmtree(temp_backup, ignore_errors=True)
        return False

def main() -> int:
    parser = argparse.ArgumentParser(description="Snapshot Manager for Agent Kits")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # create
    create_p = subparsers.add_parser("create", help="Create a snapshot of a kit")
    create_p.add_argument("kit_path", help="Path to kit directory")
    create_p.add_argument("version", help="Version tag (e.g. 1.0.0)")
    create_p.add_argument("--engine-root", default=".", help="Path to Engine root")
    
    # diff
    diff_p = subparsers.add_parser("diff", help="Diff two snapshot directories")
    diff_p.add_argument("snap_a", help="Path to snapshot A")
    diff_p.add_argument("snap_b", help="Path to snapshot B")
    
    # rollback
    rb_p = subparsers.add_parser("rollback", help="Rollback kit to snapshot")
    rb_p.add_argument("kit_path", help="Path to target kit")
    rb_p.add_argument("snapshot_path", help="Path to source snapshot")
    
    args = parser.parse_args()
    
    if args.command == "create":
        snap_dir = create_snapshot(Path(args.kit_path), Path(args.engine_root), args.version)
        print(f"✅ Snapshot created at: {snap_dir}")
        return 0
    elif args.command == "diff":
        res = diff_snapshots(Path(args.snap_a), Path(args.snap_b))
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0
    elif args.command == "rollback":
        ok = rollback_to_snapshot(Path(args.kit_path), Path(args.snapshot_path))
        if ok:
            print(f"✅ Successfully rolled back {args.kit_path} to {args.snapshot_path}")
            return 0
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
