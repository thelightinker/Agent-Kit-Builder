#!/usr/bin/env python3
"""Deterministic Upgrade Gate Evaluator for Agent Kit Creator.

Strict Invariant: Evidence → Hard Gates → Net System Gain → Decision.
Evaluates upgrade proposals deterministically without LLM self-grading shortcuts.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")



@dataclass
class UpgradeEvaluationResult:
    proposal_id: str
    decision: str  # KEEP, ADAPT, REJECT, DEFER
    gross_value: float
    total_cost: float
    net_gain: float
    hard_gate_passed: bool
    violations: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    trade_offs_identified: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_proposal(proposal: dict[str, Any]) -> UpgradeEvaluationResult:
    """Evaluate an upgrade proposal deterministically."""
    proposal_id = proposal.get("proposal_id", "UNKNOWN")
    provenance = proposal.get("extraction_provenance", {})
    evidence = proposal.get("evidence", {})
    val_deltas = proposal.get("value_deltas", {})
    cost_deltas = proposal.get("cost_deltas", {})

    violations: list[str] = []
    reasons: list[str] = []
    trade_offs: list[str] = []

    # -------------------------------------------------------------
    # 1. EVIDENCE CHECK & EXTRACTION PROVENANCE (BEFORE -> WHY -> GENERALIZE)
    # -------------------------------------------------------------
    benchmarks = evidence.get("benchmarks", [])
    automated_tests = evidence.get("automated_tests", [])
    measurable_metrics = evidence.get("measurable_metrics", [])

    if len(benchmarks) == 0 and len(automated_tests) == 0 and len(measurable_metrics) == 0:
        violations.append("MISSING_EVIDENCE")
        reasons.append("Chưa cung cấp bất kỳ bằng chứng định lượng (Benchmark / Automated Test / Measurable Metric).")

    # Provenance fields check
    for field_name in ["what_works", "why_it_works", "generalizable_principle", "adapted_architecture_plan"]:
        val = str(provenance.get(field_name, "")).strip()
        if len(val) < 10:
            violations.append("BLIND_COPY_VIOLATION")
            reasons.append(f"Trường trích xuất nguyên lý '{field_name}' chưa đạt chuẩn (quá ngắn hoặc bỏ trống).")
            break

    # -------------------------------------------------------------
    # 2. HARD GATES (ANTI-BLOAT & ANTI-FATIGUE TRAPS)
    # -------------------------------------------------------------
    power = float(val_deltas.get("power", 0.0))
    flexibility = float(val_deltas.get("flexibility", 0.0))
    automation = float(val_deltas.get("automation", 0.0))
    optimization = float(val_deltas.get("optimization", 0.0))
    collaboration = float(val_deltas.get("collaboration", 0.0))

    token_delta = float(cost_deltas.get("token_delta_percent", 0.0))
    latency_delta = float(cost_deltas.get("latency_delta_percent", 0.0))
    complexity_delta = float(cost_deltas.get("structural_complexity_delta", 0.0))
    human_friction = float(cost_deltas.get("human_attention_friction", 0.0))
    regression_risk = float(cost_deltas.get("regression_risk", 0.0))

    # Hard Gate 1: Approval Fatigue Trap (Adding manual approvals without net automation)
    if human_friction > 0.5 and automation <= 0.0:
        violations.append("APPROVAL_FATIGUE_TRAP")
        reasons.append(f"Gia tăng can thiệp thủ công (human_friction={human_friction}) nhưng không tăng tự động hóa (automation={automation}).")
    elif human_friction >= 1.5:
        violations.append("APPROVAL_FATIGUE_TRAP")
        reasons.append(f"Mức độ phiền toái con người vượt ngưỡng an toàn (human_friction={human_friction} >= 1.5).")

    # Hard Gate 2: Performance Blowout
    if latency_delta > 100.0 or token_delta > 150.0:
        violations.append("PERFORMANCE_BLOWOUT")
        reasons.append(f"Độ trễ hoặc token tăng vọt ngoài tầm kiểm soát (+{latency_delta}% latency, +{token_delta}% tokens).")

    # Hard Gate 3: Doraemon Bloat Trap
    if complexity_delta > 1.0 and (automation + power) < 1.0:
        violations.append("DORAEMON_BLOAT_TRAP")
        reasons.append(f"Tăng độ phức tạp mã nguồn (+{complexity_delta}) mà không mang lại giá trị tương xứng (Power+Automation={power+automation:.2f} < 1.0).")

    # Hard Gate 4: Unsafe Regression Risk
    if regression_risk > 0.6 and len(automated_tests) < 2:
        violations.append("UNSAFE_REGRESSION_RISK")
        reasons.append(f"Rủi ro thoái lui cao ({regression_risk}) nhưng thiếu test tự động phòng thủ (cần >= 2 tests).")

    # Hard Gate 5: Goodhart LOC Gaming (Claiming massive complexity reduction while risk is high & 0 tests)
    if complexity_delta < -0.5 and regression_risk > 0.3 and len(automated_tests) == 0:
        violations.append("GOODHART_LOC_GAMING_TRAP")
        reasons.append("Goodhart Attack: Cắt giảm LOC giả tạo nhưng đẩy rủi ro hệ thống tăng cao mà không có test bảo vệ.")

    # -------------------------------------------------------------
    # 3. WEIGHTED NET SYSTEM GAIN CALCULATION
    # -------------------------------------------------------------
    # Gross Value weights sum to 1.0:
    gross_value = (
        0.25 * power +
        0.20 * flexibility +
        0.25 * automation +
        0.15 * optimization +
        0.15 * collaboration
    )

    # Cost weights:
    token_cost = 0.20 * (max(0.0, token_delta) / 100.0)
    latency_cost = 0.20 * (max(0.0, latency_delta) / 100.0)
    complexity_cost = 0.25 * max(0.0, complexity_delta)
    human_cost = 0.25 * max(0.0, human_friction)
    regression_cost = 0.10 * max(0.0, regression_risk)

    total_cost = token_cost + latency_cost + complexity_cost + human_cost + regression_cost
    net_gain = gross_value - total_cost

    # Identify trade-offs
    for name, val in [("Power", power), ("Flexibility", flexibility), ("Automation", automation), ("Optimization", optimization), ("Collaboration", collaboration)]:
        if val < 0.0:
            trade_offs.append(f"Hy sinh {name} (Delta={val:.2f})")

    # -------------------------------------------------------------
    # 4. DECISION ENGINE
    # -------------------------------------------------------------
    hard_gate_passed = len(violations) == 0

    if not hard_gate_passed:
        decision = "REJECT"
    elif net_gain >= 0.35 and all(v >= -0.5 for v in [power, flexibility, automation, optimization, collaboration]):
        decision = "KEEP"
        reasons.append(f"Net System Gain vượt trội (+{net_gain:.2f} > 0.35), 100% Hard Gates đạt chuẩn.")
    elif net_gain > 0.10:
        decision = "ADAPT"
        reasons.append(f"Net Gain dương (+{net_gain:.2f}) với Trade-off hợp lệ hoặc cần tinh chỉnh kiến trúc để giảm chi phí biên.")
    elif 0.0 <= net_gain <= 0.10:
        decision = "DEFER"
        reasons.append(f"Net Gain còn biên độ thấp (+{net_gain:.2f} <= 0.10), đề xuất hoãn để thu thập thêm bằng chứng thực tế.")
    else:
        decision = "REJECT"
        reasons.append(f"Net System Gain âm ({net_gain:.2f} <= 0.0) - Chi phí và rủi ro vượt quá giá trị gia tăng.")

    return UpgradeEvaluationResult(
        proposal_id=proposal_id,
        decision=decision,
        gross_value=round(gross_value, 4),
        total_cost=round(total_cost, 4),
        net_gain=round(net_gain, 4),
        hard_gate_passed=hard_gate_passed,
        violations=violations,
        reasons=reasons,
        trade_offs_identified=trade_offs
    )


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python upgrade_gate_evaluator.py <upgrade_proposal.json>")
        return 1

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"[ERROR] File not found: {path}")
        return 1

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[ERROR] Failed to parse JSON: {e}")
        return 1

    result = evaluate_proposal(data)
    print("=" * 60)
    print(f"UPGRADE GATE EVALUATION REPORT: {result.proposal_id}")
    print("=" * 60)
    print(f"Decision:         [{result.decision}]")
    print(f"Hard Gates:       {'PASS' if result.hard_gate_passed else 'FAIL'}")
    print(f"Gross Value:      +{result.gross_value:.4f}")
    print(f"Total Cost:       -{result.total_cost:.4f}")
    print(f"Net System Gain:  {result.net_gain:+.4f}")

    if result.violations:
        print("\nHard Gate Violations:")
        for v in result.violations:
            print(f"  ❌ {v}")

    if result.trade_offs_identified:
        print("\nTrade-offs Acknowledged:")
        for t in result.trade_offs_identified:
            print(f"  ⚖️  {t}")

    print("\nSummary & Rationale:")
    for r in result.reasons:
        print(f"  - {r}")
    print("=" * 60)

    # Return 0 for KEEP/ADAPT, 1 for REJECT/DEFER
    return 0 if result.decision in ("KEEP", "ADAPT") else 1


if __name__ == "__main__":
    sys.exit(main())
