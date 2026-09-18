#!/usr/bin/env python3
"""
Agent Kit Safe Copier (copy_kit.py).
Safely copies Agent Kits from Output/ to the destination AI Agent project workspace
without moving, deleting, or altering source files.
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import List, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DEFAULT_DEST_PATH = Path(r"C:\Users\nhdcb\OneDrive\Desktop\AI Project\AI Agent Kits")

def get_engine_root() -> Path:
    cur = Path(__file__).resolve().parent
    while cur != cur.parent:
        if (cur / ".agents" / "scripts" / "equip_evolution.py").exists():
            return cur
        cur = cur.parent
    return Path.cwd()

def get_kit_stats(kit_path: Path) -> Tuple[int, int]:
    """Return (file_count, total_bytes)."""
    file_count = 0
    total_bytes = 0
    for root, _, files in os.walk(kit_path):
        for f in files:
            fp = Path(root) / f
            file_count += 1
            try:
                total_bytes += fp.stat().st_size
            except OSError:
                pass
    return file_count, total_bytes

def format_size(bytes_val: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} TB"

def list_kits(output_dir: Path, dest_dir: Path) -> None:
    if not output_dir.is_dir():
        print(f"❌ Output directory not found: {output_dir}")
        return
    
    print(f"📦 Available Agent Kits in [{output_dir}]:\n")
    kits = sorted([d for d in output_dir.iterdir() if d.is_dir() and not d.name.startswith(".")])
    if not kits:
        print("  (No kits found in Output/)")
        return
        
    for k in kits:
        files, size = get_kit_stats(k)
        dest_k = dest_dir / k.name
        dest_status = "✅ Copied" if dest_k.exists() else "⏳ Not Copied"
        print(f"  • {k.name:<30} | {files:>4} files | {format_size(size):>9} | Destination: {dest_status}")
    print()

def copy_single_kit(kit_src: Path, dest_dir: Path, dry_run: bool = False) -> bool:
    kit_name = kit_src.name
    dest_path = dest_dir / kit_name
    
    files, size = get_kit_stats(kit_src)
    print(f"🚀 {'[DRY RUN] ' if dry_run else ''}Copying Kit: '{kit_name}'")
    print(f"   ├─ Source: {kit_src}")
    print(f"   ├─ Target: {dest_path}")
    print(f"   ├─ Payload: {files} files ({format_size(size)})")
    
    if dry_run:
        print(f"   └─ [DRY RUN] Would copy {files} files successfully.\n")
        return True

    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(kit_src, dest_path, dirs_exist_ok=True)
        
        # Verify copy
        copied_files, copied_size = get_kit_stats(dest_path)
        print(f"   └─ [✅] Copied successfully: {copied_files} files ({format_size(copied_size)})\n")
        return True
    except Exception as e:
        print(f"   └─ [❌] Failed to copy '{kit_name}': {e}\n", file=sys.stderr)
        return False

def main() -> int:
    parser = argparse.ArgumentParser(description="Agent Kit Safe Copier")
    parser.add_argument("kits", nargs="*", help="Kit name(s) in Output/ or custom kit path(s)")
    parser.add_argument("--all", action="store_true", help="Copy ALL kits from Output/")
    parser.add_argument("--list", action="store_true", help="List available kits and copy status")
    parser.add_argument("--dest", default=str(DEFAULT_DEST_PATH), help=f"Destination directory (default: {DEFAULT_DEST_PATH})")
    parser.add_argument("--output-dir", default=None, help="Source Output directory (default: ./Output)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate copy without writing files")
    
    args = parser.parse_args()
    engine_root = get_engine_root()
    output_dir = Path(args.output_dir).resolve() if args.output_dir else engine_root / "Output"
    dest_dir = Path(args.dest).resolve()
    
    if args.list:
        list_kits(output_dir, dest_dir)
        return 0
        
    targets: List[Path] = []
    if args.all:
        if not output_dir.is_dir():
            print(f"❌ Output directory not found: {output_dir}", file=sys.stderr)
            return 1
        targets = sorted([d for d in output_dir.iterdir() if d.is_dir() and not d.name.startswith(".")])
    elif args.kits:
        for k in args.kits:
            p = Path(k)
            if not p.is_dir():
                p = output_dir / k
            if p.is_dir():
                targets.append(p)
            else:
                print(f"❌ Kit not found: '{k}' (searched in {output_dir})", file=sys.stderr)
                return 1
    else:
        parser.print_help()
        return 0

    if not targets:
        print("⚠️ No kits to copy.")
        return 0

    print(f"\n========================================================")
    print(f"📦 AGENT KIT SAFE COPY PIPELINE")
    print(f"📁 Destination: {dest_dir}")
    print(f"🎯 Total Kits to Copy: {len(targets)}")
    print(f"========================================================\n")
    
    success_count = 0
    for kit_path in targets:
        if copy_single_kit(kit_path, dest_dir, dry_run=args.dry_run):
            success_count += 1
            
    print(f"✨ Summary: {success_count}/{len(targets)} kits copied successfully.")
    return 0 if success_count == len(targets) else 1

if __name__ == "__main__":
    sys.exit(main())
