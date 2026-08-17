import os
import random
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from checkpoints.guard_engine import compute_scoped_hash, create_snapshot, verify_staleness, rollback_snapshot
from checkpoints.impact_engine import classify_blast_radius, generate_impact_summary
from checkpoints.trust_engine import record_decision, check_compounding_batch

def render_envelope(risk_tier: str, reason_code: str, summary: str, core_delta: str, confirm_code: str | None = None) -> str:
    """Renders human-readable markdown envelope for Low-Tech UX."""
    if risk_tier == "T3":
        return f"""
====================================================================
⛔ CRITICAL CHECKPOINT REVIEW [Tier: 🔴 T3 - HIGH RISK / IRREVERSIBLE]
--------------------------------------------------------------------
Lý do: {reason_code}

📝 Tóm tắt tác động:
{summary}

🔍 Core Delta:
{core_delta}

--------------------------------------------------------------------
🔒 XÁC NHẬN AN TOÀN (Chống bấm nhầm):
Để thực thi thao tác này, vui lòng nhập chính xác chuỗi sau:

   {confirm_code}

(Hoặc nhập "cancel" để Từ chối & Rollback an toàn)
====================================================================
"""
    else:
        return f"""
====================================================================
🚨 CHECKPOINT REVIEW [Tier: 🟡 T2 - Moderate Risk]
--------------------------------------------------------------------
Lý do: {reason_code}

📝 Tóm tắt tác động:
{summary}

🔍 Core Delta:
{core_delta}

--------------------------------------------------------------------
👉 LỰA CHỌN CỦA BẠN (Gõ 1, 2 hoặc 3):
[1] Approve (Đồng ý & Tiếp tục)
[2] Revise  (Yêu cầu chỉnh sửa)
[3] Reject  (Hủy bỏ & Rollback)
====================================================================
"""

def evaluate_checkpoint(
    node_id: str,
    target_files: list[str],
    operation: str,
    history_file: str,
    interactive: bool = False,
    mock_input: str | None = None
) -> dict:
    """Evaluates checkpoint logic deterministically. Returns evaluation status dictionary."""
    primary_path = target_files[0] if target_files else "unknown"
    radius, reason_code, risk_tier = classify_blast_radius(primary_path, operation)

    # T0 Auto-pass
    if risk_tier == "T0":
        return {"status": "APPROVED", "risk_tier": "T0", "reason_code": reason_code}

    # T1 Auto-proceed log
    if risk_tier == "T1":
        tier_adjusted = check_compounding_batch(len(target_files), node_id)
        if tier_adjusted == "T1":
            return {"status": "APPROVED", "risk_tier": "T1", "reason_code": reason_code}
        risk_tier = "T2"

    # T2 & T3 Sync Interrupts
    initial_hash = compute_scoped_hash(target_files)
    snap_dir = os.path.join(os.path.dirname(primary_path), f".snap_{node_id}")
    create_snapshot(target_files, snap_dir)

    summary = generate_impact_summary(target_files, [operation], reason_code)
    delta = f"+ Operation {operation} on {primary_path}"

    confirm_code = f"CONFIRM {random.randint(1000, 9999)}" if risk_tier == "T3" else None
    envelope_text = render_envelope(risk_tier, reason_code, summary, delta, confirm_code)

    if interactive:
        print(envelope_text)
        user_choice = input("Nhập lựa chọn của bạn: ").strip()
    else:
        user_choice = mock_input or "1"

    # Verify staleness before applying decision
    if not verify_staleness(target_files, initial_hash):
        rollback_snapshot(snap_dir, target_files)
        return {"status": "INVALIDATED", "reason": "State drifted while pending review"}

    if risk_tier == "T3":
        if user_choice.strip() == confirm_code:
            record_decision(history_file, reason_code, "approve")
            return {"status": "APPROVED", "risk_tier": "T3", "reason_code": reason_code}
        else:
            rollback_snapshot(snap_dir, target_files)
            record_decision(history_file, reason_code, "reject")
            return {"status": "REJECTED", "risk_tier": "T3", "reason_code": reason_code}

    # T2 Evaluation
    if user_choice == "1":
        record_decision(history_file, reason_code, "approve")
        return {"status": "APPROVED", "risk_tier": "T2", "reason_code": reason_code}
    elif user_choice == "2":
        record_decision(history_file, reason_code, "revise")
        return {"status": "REVISE_REQUESTED", "risk_tier": "T2", "reason_code": reason_code}
    else:
        rollback_snapshot(snap_dir, target_files)
        record_decision(history_file, reason_code, "reject")
        return {"status": "REJECTED", "risk_tier": "T2", "reason_code": reason_code}
