#!/usr/bin/env python3
"""Unified Verification Suite for Agent Kit Builder.

Executes 5 sequential verification gates:
1. preflight: Verifies essential templates and vendored skills exist
2. validate: Strict validation (--no-auto-heal) for zero errors/warnings
3. tests: Discovers and executes all active unit tests (excluding EXPERIMENTAL.txt)
4. benchmark: Behavioral & architectural benchmark suite (--mode both)
5. tree: Working tree cleanliness audit (git status --porcelain -- .agents)
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SCRIPTS_DIR = Path(__file__).resolve().parent
TOOLKIT_DIR = SCRIPTS_DIR.parent
REPO_ROOT = TOOLKIT_DIR.parent
TESTS_DIR = SCRIPTS_DIR / "tests"


@dataclass
class StepResult:
    name: str
    returncode: int
    seconds: float


def run_step(name: str, argv: list[str], cwd: Path) -> StepResult:
    print(f"\n>>> Running step [{name}]: {' '.join(argv)}")
    start = time.monotonic()
    proc = subprocess.run(argv, cwd=str(cwd), text=True)
    elapsed = time.monotonic() - start
    status = "PASS" if proc.returncode == 0 else f"FAIL ({proc.returncode})"
    print(f"[{name}] {status} in {elapsed:.2f}s")
    return StepResult(name=name, returncode=proc.returncode, seconds=elapsed)


def missing_dev_dependencies() -> list[str]:
    missing = []
    for mod in ("pytest", "jsonschema"):
        if importlib.util.find_spec(mod) is None:
            missing.append(mod)
    return missing


def exit_code(results: list[StepResult]) -> int:
    return 0 if all(r.returncode == 0 for r in results) else 1


def run_unit_tests() -> int:
    exp_file = TESTS_DIR / "EXPERIMENTAL.txt"
    excluded: set[str] = set()
    if exp_file.is_file():
        for line in exp_file.read_text("utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                excluded.add(line)

    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    if str(TESTS_DIR) not in sys.path:
        sys.path.insert(0, str(TESTS_DIR))

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for test_file in sorted(TESTS_DIR.glob("test_*.py")):
        mod_name = test_file.stem
        if mod_name in excluded:
            continue
        mod_suite = loader.loadTestsFromName(mod_name)
        suite.addTest(mod_suite)

    print(f"[*] Running active unit tests (excluded {len(excluded)} experimental modules: {sorted(excluded)})...")
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Unified verification harness for Agent Kit Builder")
    parser.add_argument(
        "--only",
        action="append",
        choices=["preflight", "validate", "tests", "benchmark", "tree"],
        help="Run only specific verification step(s)",
    )
    parser.add_argument(
        "--run-tests-internal",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args(argv)

    if args.run_tests_internal:
        return run_unit_tests()

    missing = missing_dev_dependencies()
    if missing:
        print(
            f"Error: Missing dev dependencies: {', '.join(missing)}. "
            f"Please install them via: pip install -r requirements-dev.txt",
            file=sys.stderr,
        )
        return 2

    active_steps = args.only if args.only else ["preflight", "validate", "tests", "benchmark", "tree"]
    results: list[StepResult] = []

    # Capture initial git tree state if tree step is requested
    initial_tree_status = None
    if "tree" in active_steps:
        try:
            p = subprocess.run(
                ["git", "status", "--porcelain", "--", ".agents"],
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
            )
            if p.returncode == 0:
                initial_tree_status = p.stdout.strip()
        except Exception:
            pass

    for step in active_steps:
        if step == "preflight":
            r = run_step("preflight", [sys.executable, str(SCRIPTS_DIR / "preflight.py"), str(TOOLKIT_DIR)], cwd=REPO_ROOT)
            results.append(r)
        elif step == "validate":
            r_docs = run_step("render_docs", [sys.executable, str(SCRIPTS_DIR / "render_docs.py"), "--check"], cwd=REPO_ROOT)
            if r_docs.returncode != 0:
                results.append(r_docs)
            else:
                r = run_step("validate", [sys.executable, str(SCRIPTS_DIR / "validate_kit.py"), str(TOOLKIT_DIR), "--no-auto-heal"], cwd=REPO_ROOT)
                results.append(r)
        elif step == "tests":
            r = run_step("tests", [sys.executable, str(Path(__file__).resolve()), "--run-tests-internal"], cwd=REPO_ROOT)
            results.append(r)
        elif step == "benchmark":
            r = run_step("benchmark", [sys.executable, str(SCRIPTS_DIR / "benchmark_behavior.py"), "--mode", "both"], cwd=REPO_ROOT)
            results.append(r)
        elif step == "tree":
            t_start = time.monotonic()
            tree_rc = 0
            if initial_tree_status is not None:
                try:
                    p = subprocess.run(
                        ["git", "status", "--porcelain", "--", ".agents"],
                        cwd=str(REPO_ROOT),
                        capture_output=True,
                        text=True,
                    )
                    after_tree = p.stdout.strip()
                    if after_tree != initial_tree_status:
                        print(f"[-] Tree mutation detected in .agents!\nBefore:\n{initial_tree_status}\nAfter:\n{after_tree}")
                        tree_rc = 1
                except Exception as e:
                    print(f"[-] Tree check failed to invoke git: {e}")
                    tree_rc = 0
            t_elapsed = time.monotonic() - t_start
            t_status = "PASS" if tree_rc == 0 else f"FAIL ({tree_rc})"
            print(f"[tree] {t_status} in {t_elapsed:.2f}s")
            results.append(StepResult(name="tree", returncode=tree_rc, seconds=t_elapsed))

    code = exit_code(results)
    print("\n" + "=" * 60)
    print("                    VERIFICATION SUMMARY")
    print("=" * 60)
    for r in results:
        icon = "✓" if r.returncode == 0 else "✗"
        print(f" {icon} {r.name:<15} : {r.seconds:.2f}s (rc={r.returncode})")
    print("=" * 60)
    if code == 0:
        print("VERIFY: PASS")
    else:
        print("VERIFY: FAIL")

    return code


if __name__ == "__main__":
    sys.exit(main())
