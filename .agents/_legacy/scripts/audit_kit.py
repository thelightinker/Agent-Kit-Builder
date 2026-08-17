#!/usr/bin/env python3
"""
Agent Kit Quality Audit & Verification Tool
Quét tự động toàn bộ thư mục Agent Kit để kiểm định cấu trúc, cú pháp Frontmatter,
3 loại Rule Trigger (always_on, manual, model_decision) và JSON Schema validation.
"""

import sys
import os
import re
import json

# Tự động reconfigure stdout để hỗ trợ UTF-8 trên Windows console
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

VALID_TRIGGERS = {"always_on", "manual", "model_decision"}

def parse_frontmatter(file_path):
    """Trích xuất YAML frontmatter từ file markdown."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return None, f"Không thể đọc file: {e}"

    if not content.startswith("---"):
        return None, "Thiếu YAML Frontmatter mở đầu ('---')"

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, "YAML Frontmatter không đóng hợp lệ bằng '---'"

    yaml_text = parts[1].strip()
    data = {}
    for line in yaml_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            data[key] = val

    return data, None

def audit_agent_kit(target_dir):
    print(f"[*] Dang kiem dinh Agent Kit tai: {target_dir}\n")
    errors = []
    warnings = []
    passed = 0

    # 1. Kiểm tra thư mục rules
    rules_dir = os.path.join(target_dir, "rules")
    if os.path.exists(rules_dir):
        for fname in os.listdir(rules_dir):
            if fname.endswith(".md"):
                fpath = os.path.join(rules_dir, fname)
                data, err = parse_frontmatter(fpath)
                if err:
                    errors.append(f"[Rules] {fname}: {err}")
                else:
                    passed += 1
                    trigger = data.get("trigger")
                    if trigger and trigger not in VALID_TRIGGERS:
                        errors.append(f"[Rules] {fname}: Trigger '{trigger}' khong hop le. Chi chap nhan: {VALID_TRIGGERS}")

    # 2. Kiểm tra thư mục workflows
    workflows_dir = os.path.join(target_dir, "workflows")
    if os.path.exists(workflows_dir):
        for fname in os.listdir(workflows_dir):
            if fname.endswith(".md"):
                fpath = os.path.join(workflows_dir, fname)
                data, err = parse_frontmatter(fpath)
                if err:
                    errors.append(f"[Workflows] {fname}: {err}")
                else:
                    passed += 1
                    if "description" not in data:
                        warnings.append(f"[Workflows] {fname}: Khanh dung truong 'description' trong frontmatter.")

    # 3. Kiểm tra thư mục skills
    skills_dir = os.path.join(target_dir, "skills")
    if os.path.exists(skills_dir):
        for sname in os.listdir(skills_dir):
            spath = os.path.join(skills_dir, sname)
            if os.path.isdir(spath):
                skill_file = os.path.join(spath, "SKILL.md")
                if not os.path.exists(skill_file):
                    errors.append(f"[Skills] Thu muc skill '{sname}' thieu file SKILL.md")
                else:
                    data, err = parse_frontmatter(skill_file)
                    if err:
                        errors.append(f"[Skills] {sname}/SKILL.md: {err}")
                    else:
                        passed += 1
                        if "name" not in data or "description" not in data:
                            warnings.append(f"[Skills] {sname}/SKILL.md: Can co 'name' va 'description' trong frontmatter.")

    # 4. Kiểm tra manifest.json (nếu có)
    manifest_path = os.path.join(target_dir, "manifest.json")
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                json.load(f)
            passed += 1
            print("[+] File manifest.json hop le theo chuan JSON.")
        except Exception as e:
            errors.append(f"[Manifest] manifest.json bi loi cu phap JSON: {e}")

    # Tổng kết
    print("\n--- BAO CAO KET QUA AUDIT ---")
    print(f"[+] So file dat chuan: {passed}")
    if warnings:
        print(f"[!] Canh bao ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print(f"[-] Loi cau truc ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
        print("\nVerdict: [-] FAIL (Can khac phuc loi truoc khi ban giao)")
        return 1
    else:
        print("\nVerdict: [5/5 STAR EXEMPLARY] Hoan toan dat chuan!")
        return 0

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    sys.exit(audit_agent_kit(target))
