import json
import os

def record_decision(history_file: str, reason_code: str, decision: str) -> None:
    """Records a decision entry (approve/revise/reject) into decision_history.json."""
    os.makedirs(os.path.dirname(os.path.abspath(history_file)), exist_ok=True)
    history = {}
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = {}

    if reason_code not in history:
        history[reason_code] = []

    history[reason_code].append(decision.lower())

    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def check_trust_proposal(history_file: str, reason_code: str, threshold: float = 0.95, min_samples: int = 20) -> bool:
    """Returns True if reason_code has >= min_samples and >= threshold approve rate."""
    if not os.path.exists(history_file):
        return False

    try:
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    except Exception:
        return False

    decisions = history.get(reason_code, [])
    if len(decisions) < min_samples:
        return False

    approves = sum(1 for d in decisions if d == "approve")
    return (approves / len(decisions)) >= threshold

def check_compounding_batch(t1_file_count: int, phase_name: str) -> str:
    """Escalates T1 batch to T2 if 3 or more files are impacted in a single phase."""
    if t1_file_count >= 3:
        return "T2"
    return "T1"
