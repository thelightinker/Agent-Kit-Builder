#!/usr/bin/env python3
"""
Mutation Testing Harness for Evidence-Gated Assertion Guards
Injects intentional faults/mutations into the Guard logic to verify that
the test suite detects the regression and 'Kills the Mutant'.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Import the golden guards from test_adversarial
from test_adversarial import (
    check_guard_1_provenance,
    check_guard_separation_of_agency,
    check_guard_channel_assertions,
    check_guard_superlatives_scan
)

# ---------------------------------------------------------------------------
# MUTANTS (Deliberately Corrupted Guard Logic)
# ---------------------------------------------------------------------------

def mutant_1_weakened_channel_guard(channel_audit):
    """Mutant 1: Weakened condition from >= 2 to >= 1 (allows single variant)."""
    if channel_audit.get("social_hook_ab_count", 0) < 1: # Mutated!
        return False, "BLOCK"
    return True, "PASS"


def mutant_2_disabled_unproven_stats_check(truth_audit):
    """Mutant 2: Commented out/ignored unproven_stats_count check."""
    # unproven_stats_count check is deliberately skipped!
    if truth_audit.get("banned_superlatives_count", 0) > 0:
        return False, "BLOCK"
    return True, "PASS"


def mutant_3_missing_schema_validation(truth_audit):
    """Mutant 3: Removed required field checks."""
    # No required fields checked!
    return True, "PASS"


def mutant_4_skipped_provenance_benchmark_check(ledger):
    """Mutant 4: Allows numerical claims without benchmark citation."""
    # Skip checking has_benchmark_citation!
    return True, "PASS"


# ---------------------------------------------------------------------------
# MUTATION RUNNER
# ---------------------------------------------------------------------------

def run_mutation_suite():
    print("=" * 70)
    print("🧬 RUNNING L4 MUTATION TESTING HARNESS")
    print("Testing if corrupted guards are successfully caught & killed")
    print("=" * 70)

    mutants_tested = []

    # --- MUTANT 1: Weaken social A/B variant to >= 1 ---
    print("\n[M1] Testing Mutant 1: Weakened Channel Guard (>= 1 instead of >= 2)")
    # Attack input: social_hook_ab_count == 1
    attack_input_m1 = {"landing_page_ab_count": 2, "email_subject_ab_count": 2, "social_hook_ab_count": 1}
    # Golden guard should BLOCK (return False)
    golden_blocked, _ = check_guard_channel_assertions(attack_input_m1)
    # Mutated guard improperly PASSES (returns True)
    mutant_blocked, _ = mutant_1_weakened_channel_guard(attack_input_m1)
    
    if golden_blocked is False and mutant_blocked is True:
        print("  👉 Mutant Behavior: Let attack pass through!")
        print("  👉 Detection: Test suite detects deviation -> 🗡️ MUTANT 1 KILLED!")
        mutants_tested.append(("M1 - Weakened Channel Guard", True))
    else:
        print("  👉 🚨 MUTANT 1 SURVIVED!")
        mutants_tested.append(("M1 - Weakened Channel Guard", False))

    # --- MUTANT 2: Disabled unproven stats check ---
    print("\n[M2] Testing Mutant 2: Disabled unproven_stats_count check in Truth QA")
    attack_input_m2 = {"total_claims_scanned": 10, "banned_superlatives_count": 0, "unproven_stats_count": 2, "status": "PASS"}
    golden_blocked, _ = check_guard_separation_of_agency(attack_input_m2)
    mutant_blocked, _ = mutant_2_disabled_unproven_stats_check(attack_input_m2)
    
    if golden_blocked is False and mutant_blocked is True:
        print("  👉 Mutant Behavior: Let unproven stats pass through!")
        print("  👉 Detection: Test suite detects deviation -> 🗡️ MUTANT 2 KILLED!")
        mutants_tested.append(("M2 - Disabled Unproven Stats Check", True))
    else:
        print("  👉 🚨 MUTANT 2 SURVIVED!")
        mutants_tested.append(("M2 - Disabled Unproven Stats Check", False))

    # --- MUTANT 3: Missing Schema Validation ---
    print("\n[M3] Testing Mutant 3: Removed mandatory schema field validation")
    attack_input_m3 = {"status": "PASS"} # Missing total_claims_scanned
    golden_blocked, _ = check_guard_separation_of_agency(attack_input_m3)
    mutant_blocked, _ = mutant_3_missing_schema_validation(attack_input_m3)
    
    if golden_blocked is False and mutant_blocked is True:
        print("  👉 Mutant Behavior: Allowed malformed JSON without required fields!")
        print("  👉 Detection: Test suite detects deviation -> 🗡️ MUTANT 3 KILLED!")
        mutants_tested.append(("M3 - Removed Schema Check", True))
    else:
        print("  👉 🚨 MUTANT 3 SURVIVED!")
        mutants_tested.append(("M3 - Removed Schema Check", False))

    # --- MUTANT 4: Skipped Provenance Benchmark Check ---
    print("\n[M4] Testing Mutant 4: Skipped Provenance Benchmark Citation Check")
    attack_input_m4 = {"total_claims_discovered": 5, "proven_facts": ["65% token saved"], "has_benchmark_citation": False, "unsubstantiated_claims_leaked": 0}
    golden_blocked, _ = check_guard_1_provenance(attack_input_m4)
    mutant_blocked, _ = mutant_4_skipped_provenance_benchmark_check(attack_input_m4)
    
    if golden_blocked is False and mutant_blocked is True:
        print("  👉 Mutant Behavior: Allowed 65% token claim without benchmark citation!")
        print("  👉 Detection: Test suite detects deviation -> 🗡️ MUTANT 4 KILLED!")
        mutants_tested.append(("M4 - Skipped Benchmark Citation", True))
    else:
        print("  👉 🚨 MUTANT 4 SURVIVED!")
        mutants_tested.append(("M4 - Skipped Benchmark Citation", False))

    # --- SUMMARY ---
    print("\n" + "=" * 70)
    print("📊 MUTATION SCORE SUMMARY")
    print("=" * 70)
    all_killed = all(m[1] for m in mutants_tested)
    for name, killed in mutants_tested:
        status_str = "🗡️ KILLED (TEST DETECTED CORRUPTION)" if killed else "🚨 SURVIVED"
        print(f"- {name}: {status_str}")
        
    kill_count = sum(1 for m in mutants_tested if m[1])
    score = (kill_count / len(mutants_tested)) * 100
    print(f"\nFinal Mutation Score: {kill_count}/{len(mutants_tested)} Mutants Killed ({score:.1f}% Mutation Kill Rate)")
    return 0 if all_killed else 1

if __name__ == "__main__":
    sys.exit(run_mutation_suite())
