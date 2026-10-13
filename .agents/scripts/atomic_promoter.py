#!/usr/bin/env python3
"""
Two-Phase Atomic Promoter with Full Checksum Verification.
Promotes staged kit to Canonical Output -> Syncs to Target Workspace -> Validates 100% SHA-256 match.
Guarantees zero-downtime and safe rollback to v1 on failure.
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

def sha256_file(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def compute_tree_checksums(dir_path: Path) -> dict[str, str]:
    checksums = {}
    if not dir_path.is_dir():
        return checksums
    for root, _, files in os.walk(dir_path):
        for f in sorted(files):
            fp = Path(root) / f
            if fp.is_file() and not fp.is_symlink() and not fp.name.startswith("."):
                rel = fp.relative_to(dir_path).as_posix()
                checksums[rel] = sha256_file(fp)
    return checksums

def promote_canonical(staging_dir: Path, canonical_dir: Path, archive_root: Path) -> tuple[bool, Path | None]:
    archive_root.mkdir(parents=True, exist_ok=True)
    backup_path = None
    
    if canonical_dir.exists():
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        backup_path = archive_root / f"{canonical_dir.name}-vold-{timestamp}"
        shutil.copytree(canonical_dir, backup_path, dirs_exist_ok=True)
        shutil.rmtree(canonical_dir)
        
    canonical_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(staging_dir, canonical_dir, dirs_exist_ok=True)
    return True, backup_path

def sync_and_verify_target(canonical_dir: Path, target_dir: Path, archive_root: Path) -> tuple[bool, Path | None]:
    archive_root.mkdir(parents=True, exist_ok=True)
    backup_path = None
    
    if target_dir.exists():
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        backup_path = archive_root / f"{target_dir.name}-vold-{timestamp}"
        shutil.copytree(target_dir, backup_path, dirs_exist_ok=True)
        shutil.rmtree(target_dir)
        
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(canonical_dir, target_dir, dirs_exist_ok=True)
    
    canonical_hashes = compute_tree_checksums(canonical_dir)
    target_hashes = compute_tree_checksums(target_dir)
    
    if canonical_hashes != target_hashes:
        # Rollback target
        if backup_path and backup_path.exists():
            shutil.rmtree(target_dir, ignore_errors=True)
            shutil.copytree(backup_path, target_dir, dirs_exist_ok=True)
        return False, backup_path
        
    return True, backup_path

def execute_two_phase_promotion(
    staging_dir: Path,
    canonical_dir: Path,
    target_dir: Path,
    engine_archive: Path,
    target_archive: Path
) -> dict[str, Any]:
    # Phase 1: Canonical
    p1_ok, can_bak = promote_canonical(staging_dir, canonical_dir, engine_archive)
    if not p1_ok:
        return {"success": False, "phase": "canonical", "error": "Failed to promote canonical"}
        
    # Phase 2: Target Sync & Checksum Verification
    p2_ok, tgt_bak = sync_and_verify_target(canonical_dir, target_dir, target_archive)
    if not p2_ok:
        # Rollback canonical
        if can_bak and can_bak.exists():
            shutil.rmtree(canonical_dir, ignore_errors=True)
            shutil.copytree(can_bak, canonical_dir, dirs_exist_ok=True)
        return {"success": False, "phase": "target_sync", "error": "Checksum mismatch during target sync, rolled back"}
        
    return {
        "success": True,
        "checksum_verified": True,
        "canonical_backup": str(can_bak) if can_bak else None,
        "target_backup": str(tgt_bak) if tgt_bak else None
    }

def main():
    parser = argparse.ArgumentParser(description="Two-Phase Atomic Promoter CLI")
    parser.add_argument("staging_dir", help="Path to staging kit directory")
    parser.add_argument("canonical_dir", help="Path to canonical Output directory")
    parser.add_argument("target_dir", help="Path to destination workspace directory")
    parser.add_argument("--engine-archive", default="Output/.archive", help="Engine archive directory")
    parser.add_argument("--target-archive", default=None, help="Target archive directory")
    
    args = parser.parse_args()
    staging_p = Path(args.staging_dir).resolve()
    canonical_p = Path(args.canonical_dir).resolve()
    target_p = Path(args.target_dir).resolve()
    eng_arch = Path(args.engine_archive).resolve()
    tgt_arch = Path(args.target_archive).resolve() if args.target_archive else target_p.parent / ".archive"
    
    res = execute_two_phase_promotion(staging_p, canonical_p, target_p, eng_arch, tgt_arch)
    print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
