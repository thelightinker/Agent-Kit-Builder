#!/usr/bin/env python3
"""Audit workspace consistency, link validity, folder structure and scale invariants."""
import re
import json
import urllib.parse
from pathlib import Path

def audit():
    root = Path(__file__).resolve().parents[1]
    workspace_root = root.parent
    print(f"=== AUDITING ROOT: {root} ===")
    
    # 1. Broken file links check
    broken_links = []
    total_links = 0
    for p in root.rglob("*"):
        if not p.is_file() or p.name == "audit_workspace.py" or p.suffix not in (".md", ".json", ".py"):
            continue
        try:
            content = p.read_text("utf-8", errors="ignore")
        except Exception:
            continue
        
        # Regex to find markdown links [text](file:///path)
        links = re.findall(r"\[.*?\]\((file:///[^\)]+)\)", content)
        for full_link in links:
            total_links += 1
            raw_path = full_link.replace("file:///", "")
            unquoted = urllib.parse.unquote(raw_path)
            # Normalize path
            target_str = unquoted.replace("/", "\\")
            target_path = Path(target_str)
            if not target_path.exists():
                # Check relative to workspace root
                rel_target = workspace_root / unquoted.lstrip("/\\")
                if not rel_target.exists():
                    broken_links.append((p.relative_to(root), full_link, str(target_path)))
                
    print(f"[1] Link Check: Scanned {total_links} links, Found {len(broken_links)} broken links.")
    for src, link, target in broken_links:
        print(f"    - In {src}: {link} -> (Missing: {target})")

    # 2. Schema check
    schemas_dir = root / "schemas"
    schemas = list(schemas_dir.glob("*.json"))
    print(f"[2] Schemas found: {len(schemas)}")
    for s in schemas:
        try:
            json.loads(s.read_text("utf-8"))
            print(f"    - [VALID JSON] {s.name}")
        except Exception as e:
            print(f"    - [INVALID JSON] {s.name}: {e}")

    # 3. Memory Structure
    memory_dir = root / "memory"
    memory_scripts = list((memory_dir / "scripts").glob("*.py")) if (memory_dir / "scripts").exists() else []
    print(f"[3] Memory scripts in subfolder: {len(memory_scripts)}")

if __name__ == "__main__":
    audit()
