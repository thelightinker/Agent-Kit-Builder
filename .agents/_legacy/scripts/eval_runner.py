#!/usr/bin/env python3
"""
Agent Kit Automated Behavioral Eval Harness
Parses eval suite JSON test cases, runs assertions against generated Agent Kit files,
and outputs binary DoD score pass/fail reports.
"""

import sys
import os
import re
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def evaluate_assertion(content, assertion):
    atype = assertion.get("type")
    desc = assertion.get("description", atype)
    
    if atype == "regex_match":
        pattern = assertion.get("pattern", "")
        if re.search(pattern, content, re.MULTILINE):
            return True, f"PASS: Match regex '{pattern}' ({desc})"
        return False, f"FAIL: Did not match regex '{pattern}' ({desc})"
        
    elif atype == "contains_keywords":
        keywords = assertion.get("keywords", [])
        missing = [kw for kw in keywords if kw.lower() not in content.lower()]
        if not missing:
            return True, f"PASS: Contains all keywords {keywords} ({desc})"
        return False, f"FAIL: Missing keywords {missing} ({desc})"
        
    elif atype == "forbidden_keywords":
        keywords = assertion.get("keywords", [])
        found = [kw for kw in keywords if kw.lower() in content.lower()]
        if not found:
            return True, f"PASS: No forbidden keywords found ({desc})"
        return False, f"FAIL: Found forbidden keywords {found} ({desc})"
        
    elif atype == "min_sections":
        min_sec = assertion.get("count", 1)
        sections = re.findall(r"^#{1,6}\s+", content, re.MULTILINE)
        if len(sections) >= min_sec:
            return True, f"PASS: Found {len(sections)} sections (min required: {min_sec})"
        return False, f"FAIL: Found {len(sections)} sections (min required: {min_sec})"
        
    return False, f"FAIL: Unknown assertion type '{atype}'"

def run_eval_suite(eval_file_path, target_dir="."):
    print(f"[*] Executing Eval Suite: {eval_file_path}")
    print(f"[*] Target Directory: {target_dir}\n")
    
    try:
        with open(eval_file_path, "r", encoding="utf-8") as f:
            suite = json.load(f)
    except Exception as e:
        print(f"[-] Failed to load eval suite file: {e}")
        return {"passed": 0, "failed": 1, "score": 0.0, "error": str(e)}

    test_cases = suite.get("test_cases", [])
    results = []
    total_passed = 0
    total_failed = 0

    for tc in test_cases:
        tc_id = tc.get("id", "eval-unknown")
        tc_name = tc.get("name", "Unnamed Test Case")
        rel_path = tc.get("target_file", "")
        full_path = os.path.join(target_dir, rel_path)
        
        print(f"--- Running [{tc_id}] {tc_name} ---")
        if not os.path.exists(full_path):
            print(f"[-] Target file missing: {rel_path}")
            results.append({"id": tc_id, "name": tc_name, "status": "FAIL", "reason": f"File missing: {rel_path}"})
            total_failed += 1
            continue
            
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"[-] Cannot read file: {e}")
            results.append({"id": tc_id, "name": tc_name, "status": "FAIL", "reason": str(e)})
            total_failed += 1
            continue

        assertions = tc.get("assertions", [])
        tc_passed = True
        tc_logs = []

        for ass in assertions:
            ok, msg = evaluate_assertion(content, ass)
            tc_logs.append(msg)
            if not ok:
                tc_passed = False

        if tc_passed:
            print(f"[+] [{tc_id}] PASSED ({len(assertions)} assertions)")
            total_passed += 1
            results.append({"id": tc_id, "name": tc_name, "status": "PASS", "logs": tc_logs})
        else:
            print(f"[-] [{tc_id}] FAILED")
            for log in tc_logs:
                if "FAIL:" in log:
                    print(f"    - {log}")
            total_failed += 1
            results.append({"id": tc_id, "name": tc_name, "status": "FAIL", "logs": tc_logs})

    total = total_passed + total_failed
    score = (total_passed / total * 100.0) if total > 0 else 0.0

    print("\n--- EVALUATION SUMMARY ---")
    print(f"Total Test Cases: {total}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    print(f"Score: {score:.1f}%")

    report = {
        "kit_type": suite.get("kit_type", "unknown"),
        "total": total,
        "passed": total_passed,
        "failed": total_failed,
        "score_pct": score,
        "results": results
    }
    return report

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Agent Kit Eval Harness")
    parser.add_argument("--eval-file", "--suite", dest="eval_file", required=True, help="Path to eval suite JSON file")
    parser.add_argument("--target-dir", "--target-kit", dest="target_dir", default=".", help="Base directory of the target Agent Kit (e.g. ./output/<kit-name>)")
    parser.add_argument("--output-report", help="Optional path to save JSON eval report")
    
    args = parser.parse_args()
    report = run_eval_suite(args.eval_file, args.target_dir)
    
    if args.output_report:
        with open(args.output_report, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"[+] Report saved to {args.output_report}")
        
    sys.exit(0 if report["failed"] == 0 else 1)

if __name__ == "__main__":
    main()
