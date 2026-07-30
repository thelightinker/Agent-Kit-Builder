# Dynamic Checkpoint System v1.1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a risk-tiered, token-efficient, orchestrator-controlled checkpoint system (v1.1 Spec) for Agent Kit Creator with Scoped Dual-Hash Staleness Guard, 2D Blast Radius Classifier, Risk-Prioritized Diff Truncation, T3 Confirmation Code, and Trust Calibration.

**Architecture:** 3 modular Python engines (`GuardEngine`, `ImpactEngine`, `TrustEngine`) in `.agents/scripts/checkpoints/` orchestrated by `checkpoint_gate.py` and validated by extending `validate_kit.py`. 

**Tech Stack:** Python 3.10+, `hashlib`, `pytest`, `git`, standard JSON libraries.

## Global Constraints

- **Language**: Python 3.10+ (Standard library + pytest).
- **Execution Mode**: CLI Synchronous, Zero external network dependencies.
- **DoD**: Binary pass/fail test cases via pytest. No vague assertions.
- **Orchestration Rule**: Nodes must NEVER self-judge escalation (`decided_by: orchestrator` strictly required).

---

### Task 1: Scoped GuardEngine (`.agents/scripts/checkpoints/guard_engine.py`)

**Files:**
- Create: `.agents/scripts/checkpoints/__init__.py`
- Create: `.agents/scripts/checkpoints/guard_engine.py`
- Create: `.agents/scripts/tests/test_guard_engine.py`

**Interfaces:**
- Consumes: None (Standard Python library `hashlib`, `shutil`, `os`, `pathlib`)
- Produces: `compute_scoped_hash`, `create_snapshot`, `verify_staleness`, `rollback_snapshot`

- [ ] **Step 1: Write the failing test for GuardEngine**

Create `.agents/scripts/tests/test_guard_engine.py`:
```python
import os
import shutil
import tempfile
import pytest
from .checkpoints.guard_engine import (
    compute_scoped_hash,
    create_snapshot,
    verify_staleness,
    rollback_snapshot
)

def test_guard_engine_hash_and_rollback():
    with tempfile.TemporaryDirectory() as tmp_dir:
        file1 = os.path.join(tmp_dir, "test1.txt")
        with open(file1, "w", encoding="utf-8") as f:
            f.write("initial content")

        # 1. Compute scoped hash
        hash_val = compute_scoped_hash([file1])
        assert isinstance(hash_val, str) and len(hash_val) == 64

        # 2. Create snapshot
        snap_dir = os.path.join(tmp_dir, "snapshot")
        create_snapshot([file1], snap_dir)
        assert os.path.exists(os.path.join(snap_dir, "test1.txt"))

        # 3. Verify no staleness initially
        assert verify_staleness([file1], hash_val) is True

        # 4. Mutate file (simulate drift)
        with open(file1, "w", encoding="utf-8") as f:
            f.write("tampered content")

        # 5. Verify staleness detected
        assert verify_staleness([file1], hash_val) is False

        # 6. Rollback snapshot
        rollback_snapshot(snap_dir, [file1])
        with open(file1, "r", encoding="utf-8") as f:
            assert f.read() == "initial content"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest .agents/scripts/tests/test_guard_engine.py -v`
Expected: FAIL with "ModuleNotFoundError" or "ImportError"

- [ ] **Step 3: Implement GuardEngine**

Create `.agents/scripts/checkpoints/__init__.py`:
```python
# Checkpoints package initialization
```

Create `.agents/scripts/checkpoints/guard_engine.py`:
```python
import hashlib
import os
import shutil
from pathlib import Path

def compute_scoped_hash(target_files: list[str]) -> str:
    """Computes a SHA-256 hash strictly over the specified target files."""
    hasher = hashlib.sha256()
    for file_path in sorted(target_files):
        if os.path.exists(file_path):
            hasher.update(file_path.encode('utf-8'))
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
        else:
            hasher.update(f"MISSING:{file_path}".encode('utf-8'))
    return hasher.hexdigest()

def create_snapshot(target_files: list[str], snapshot_dir: str) -> None:
    """Creates a backup snapshot of specified target files into snapshot_dir."""
    if os.path.exists(snapshot_dir):
        shutil.rmtree(snapshot_dir)
    os.makedirs(snapshot_dir, exist_ok=True)
    
    for file_path in target_files:
        if os.path.exists(file_path):
            rel_name = os.path.basename(file_path)
            dest_path = os.path.join(snapshot_dir, rel_name)
            shutil.copy2(file_path, dest_path)

def verify_staleness(target_files: list[str], expected_hash: str) -> bool:
    """Returns True if current hash matches expected_hash (no drift). Returns False if drifted."""
    current_hash = compute_scoped_hash(target_files)
    return current_hash == expected_hash

def rollback_snapshot(snapshot_dir: str, target_files: list[str]) -> None:
    """Restores target_files from snapshot_dir."""
    for file_path in target_files:
        rel_name = os.path.basename(file_path)
        dest_path = os.path.join(snapshot_dir, rel_name)
        if os.path.exists(dest_path):
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            shutil.copy2(dest_path, file_path)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest .agents/scripts/tests/test_guard_engine.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add .agents/scripts/checkpoints/ .agents/scripts/tests/test_guard_engine.py
git commit -m "feat(checkpoints): implement GuardEngine with scoped SHA-256 state hash and rollback"
```

---

### Task 2: 2D ImpactEngine (`.agents/scripts/checkpoints/impact_engine.py`)

**Files:**
- Create: `.agents/scripts/checkpoints/impact_engine.py`
- Create: `.agents/scripts/tests/test_impact_engine.py`

**Interfaces:**
- Consumes: None (Standard Python string processing)
- Produces: `classify_blast_radius`, `prioritize_and_truncate_diff`, `generate_impact_summary`

- [ ] **Step 1: Write failing test for ImpactEngine**

Create `.agents/scripts/tests/test_impact_engine.py`:
```python
import pytest
from .checkpoints.impact_engine import (
    classify_blast_radius,
    prioritize_and_truncate_diff,
    generate_impact_summary
)

def test_2d_blast_radius_matrix():
    # 1. Modify HIGH path -> T3
    radius, reason, tier = classify_blast_radius(".agents/rules/universal-rules.md", "modify")
    assert radius == "HIGH" and reason == "POLICY_BOUNDARY" and tier == "T3"

    # 2. Delete on MEDIUM path -> T3 (Auto +1 Tier)
    radius, reason, tier = classify_blast_radius("output/my-kit/manifest.json", "delete")
    assert radius == "HIGH" and reason == "IRREVERSIBLE_ACTION" and tier == "T3"

    # 3. Create on MEDIUM path -> T2
    radius, reason, tier = classify_blast_radius("output/my-kit/SKILL.md", "create")
    assert radius == "MEDIUM" and reason == "EXTERNAL_WRITE" and tier == "T2"

    # 4. Create on LOW path -> T1
    radius, reason, tier = classify_blast_radius("output/draft/tmp.txt", "create")
    assert radius == "LOW" and reason == "INTERNAL_DRAFT" and tier == "T1"

def test_risk_prioritized_diff_truncation():
    raw_diff = (
        "+ normal line 1\n"
        "+ normal line 2\n"
        "- deletion line in core .agents/rules/\n"
        "+ normal line 3\n"
    )
    truncated = prioritize_and_truncate_diff(raw_diff, max_lines=2)
    # Deletion line MUST be prioritized first
    assert "- deletion line in core" in truncated
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest .agents/scripts/tests/test_impact_engine.py -v`
Expected: FAIL with "ImportError"

- [ ] **Step 3: Implement ImpactEngine**

Create `.agents/scripts/checkpoints/impact_engine.py`:
```python
def classify_blast_radius(path: str, operation: str) -> tuple[str, str, str]:
    """
    Classifies risk based on 2D Matrix (Path Sensitivity x Operation).
    Returns (blast_radius, reason_code, risk_tier).
    """
    op = operation.lower()
    path_clean = path.replace("\\", "/")

    # Path Sensitivity Check
    is_high_path = any(keyword in path_clean for keyword in [".agents/rules/", "ARCHITECTURE.md", "manifest.json"])
    is_medium_path = path_clean.startswith("output/") or path_clean.startswith("./output/")

    if op == "delete":
        # Delete operation always escalates to T3
        return "HIGH", "IRREVERSIBLE_ACTION", "T3"

    if is_high_path:
        if op in ("modify", "delete"):
            return "HIGH", "POLICY_BOUNDARY", "T3"
        return "MEDIUM", "EXTERNAL_WRITE", "T2"

    if is_medium_path:
        if op == "modify":
            return "MEDIUM", "EXTERNAL_WRITE", "T2"
        return "LOW", "INTERNAL_DRAFT", "T1"

    # Default fallback
    return "LOW", "INTERNAL_DRAFT", "T1"

def prioritize_and_truncate_diff(raw_diff: str, max_lines: int = 15) -> str:
    """
    Prioritizes deletions (-) and core rule modifications before addition/context lines.
    Truncates to max_lines.
    """
    lines = [line.strip() for line in raw_diff.splitlines() if line.strip()]

    p1_deletions = [l for l in lines if l.startswith("-")]
    p2_additions = [l for l in lines if l.startswith("+")]
    p3_context = [l for l in lines if not l.startswith("+") and not l.startswith("-")]

    ordered = p1_deletions + p2_additions + p3_context
    truncated_lines = ordered[:max_lines]

    return "\n".join(truncated_lines)

def generate_impact_summary(target_files: list[str], operations: list[str], reason_code: str) -> str:
    """Generates plain language Vietnamese impact summary for Low-Tech UX."""
    files_str = ", ".join([f"`{f}`" for f in target_files[:3]])
    if len(target_files) > 3:
        files_str += f" (và {len(target_files) - 3} file khác)"

    if reason_code == "IRREVERSIBLE_ACTION":
        return f"- Thao tác XÓA dữ liệu trên {files_str}. Thao tác này không thể hoàn tác tự động."
    elif reason_code == "POLICY_BOUNDARY":
        return f"- Sửa đổi trực tiếp file quy tắc Core hệ thống trên {files_str}."
    elif reason_code == "EXTERNAL_WRITE":
        return f"- Tạo mới/sửa đổi file cấu hình và tài nguyên tại {files_str}."
    else:
        return f"- Thay đổi bản nháp nội bộ tại {files_str}."
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest .agents/scripts/tests/test_impact_engine.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add .agents/scripts/checkpoints/impact_engine.py .agents/scripts/tests/test_impact_engine.py
git commit -m "feat(checkpoints): implement 2D ImpactEngine with risk-prioritized diff truncation"
```

---

### Task 3: TrustEngine & Decision History (`.agents/scripts/checkpoints/trust_engine.py`)

**Files:**
- Create: `.agents/scripts/checkpoints/trust_engine.py`
- Create: `.agents/scripts/tests/test_trust_engine.py`

**Interfaces:**
- Consumes: None (Standard `json`, `os`)
- Produces: `record_decision`, `check_trust_proposal`, `check_compounding_batch`

- [ ] **Step 1: Write failing test for TrustEngine**

Create `.agents/scripts/tests/test_trust_engine.py`:
```python
import json
import os
import tempfile
import pytest
from .checkpoints.trust_engine import (
    record_decision,
    check_trust_proposal,
    check_compounding_batch
)

def test_trust_engine_history_and_batching():
    with tempfile.TemporaryDirectory() as tmp_dir:
        history_file = os.path.join(tmp_dir, "decision_history.json")

        # 1. Record 20 approve decisions
        for _ in range(20):
            record_decision(history_file, "EXTERNAL_WRITE", "approve")

        # 2. Verify trust proposal triggered (>95% approve)
        assert check_trust_proposal(history_file, "EXTERNAL_WRITE") is True

        # 3. Verify batching rule (>= 3 files in phase -> escalate to T2)
        assert check_compounding_batch(t1_file_count=2, phase_name="skill-crafting") == "T1"
        assert check_compounding_batch(t1_file_count=3, phase_name="skill-crafting") == "T2"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest .agents/scripts/tests/test_trust_engine.py -v`
Expected: FAIL with "ImportError"

- [ ] **Step 3: Implement TrustEngine**

Create `.agents/scripts/checkpoints/trust_engine.py`:
```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest .agents/scripts/tests/test_trust_engine.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add .agents/scripts/checkpoints/trust_engine.py .agents/scripts/tests/test_trust_engine.py
git commit -m "feat(checkpoints): implement TrustEngine with decision logging and proposal checker"
```

---

### Task 4: Orchestrator Gate Script & Envelope Renderer (`.agents/scripts/checkpoint_gate.py`)

**Files:**
- Create: `.agents/scripts/checkpoint_gate.py`
- Create: `.agents/scripts/tests/test_checkpoint_gate.py`

**Interfaces:**
- Consumes: `guard_engine`, `impact_engine`, `trust_engine`
- Produces: `render_envelope`, `evaluate_checkpoint`

- [ ] **Step 1: Write failing test for Checkpoint Gate**

Create `.agents/scripts/tests/test_checkpoint_gate.py`:
```python
import tempfile
import os
import pytest
from .checkpoint_gate import render_envelope, evaluate_checkpoint

def test_checkpoint_gate_t3_confirm_code():
    envelope_t3 = render_envelope(
        risk_tier="T3",
        reason_code="IRREVERSIBLE_ACTION",
        summary="Delete core rule",
        core_delta="- legacy rule",
        confirm_code="CONFIRM 8492"
    )
    assert "CONFIRM 8492" in envelope_t3
    assert "CRITICAL CHECKPOINT REVIEW" in envelope_t3

def test_evaluate_checkpoint_t2_approve():
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_file = os.path.join(tmp_dir, "manifest.json")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write('{"key": "val"}')

        history_file = os.path.join(tmp_dir, "history.json")

        res = evaluate_checkpoint(
            node_id="test-node",
            target_files=[test_file],
            operation="modify",
            history_file=history_file,
            interactive=False,
            mock_input="1"
        )
        assert res["status"] == "APPROVED"
        assert res["risk_tier"] == "T2"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest .agents/scripts/tests/test_checkpoint_gate.py -v`
Expected: FAIL with "ImportError"

- [ ] **Step 3: Implement Checkpoint Gate**

Create `.agents/scripts/checkpoint_gate.py`:
```python
import os
import random
import sys
from .checkpoints.guard_engine import compute_scoped_hash, create_snapshot, verify_staleness, rollback_snapshot
from .checkpoints.impact_engine import classify_blast_radius, prioritize_and_truncate_diff, generate_impact_summary
from .checkpoints.trust_engine import record_decision, check_trust_proposal, check_compounding_batch

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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest .agents/scripts/tests/test_checkpoint_gate.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add .agents/scripts/checkpoint_gate.py .agents/scripts/tests/test_checkpoint_gate.py
git commit -m "feat(checkpoints): implement Orchestrator Checkpoint Gate with T3 confirmation code"
```

---

### Task 5: Workflow Contract Validator Integration (`.agents/scripts/validate_kit.py`)

**Files:**
- Modify: `.agents/scripts/validate_kit.py`
- Modify: `.agents/scripts/tests/test_toolkit.py`

**Interfaces:**
- Consumes: `validate_kit.py`
- Produces: Enhanced workflow validation enforcing `decided_by: orchestrator`

- [ ] **Step 1: Write failing test for Workflow Validator extension**

Add test to `.agents/scripts/tests/test_toolkit.py`:
```python
def test_validate_workflow_contract_decided_by():
    from .validate_kit import validate_workflow_node_decided_by
    
    invalid_node = {"name": "test", "decided_by": "model"}
    valid_node = {"name": "test", "decided_by": "orchestrator"}

    assert validate_workflow_node_decided_by(invalid_node) is False
    assert validate_workflow_node_decided_by(valid_node) is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest .agents/scripts/tests/test_toolkit.py::test_validate_workflow_contract_decided_by -v`
Expected: FAIL with "ImportError"

- [ ] **Step 3: Update `validate_kit.py`**

Add `validate_workflow_node_decided_by` function into `.agents/scripts/validate_kit.py`:
```python
def validate_workflow_node_decided_by(node_data: dict) -> bool:
    """Enforces that no workflow checkpoint node allows decided_by: model."""
    decided_by = node_data.get("decided_by")
    if not decided_by or decided_by.lower() == "model":
        return False
    return decided_by.lower() == "orchestrator"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest .agents/scripts/tests/test_toolkit.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add .agents/scripts/validate_kit.py .agents/scripts/tests/test_toolkit.py
git commit -m "feat(validation): extend validate_kit.py to reject decided_by model in workflow contracts"
```
