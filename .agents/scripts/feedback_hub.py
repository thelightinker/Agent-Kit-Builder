#!/usr/bin/env python3
"""
Feedback Hub - Event-Sourced Feedback & Learning Engine.
Append-only event stream for Kit Feedback and Builder Feedback.
JSONL is the Single Source of Truth (SSOT).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DEFAULT_HUB_DIR = Path.home() / "Downloads" / "Shared Workspace" / "Feedback"

class FileLock:
    """Cross-platform advisory file lock using atomic lockfile creation."""
    def __init__(self, lock_path: Path, timeout: float = 3.0, poll_interval: float = 0.05):
        self.lock_path = Path(lock_path)
        self.timeout = timeout
        self.poll_interval = poll_interval
        self._is_locked = False

    def acquire(self) -> None:
        import time
        deadline = time.time() + self.timeout
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        while time.time() < deadline:
            try:
                fd = os.open(str(self.lock_path), os.O_CREAT | os.O_EXCL | os.O_RDWR)
                with os.fdopen(fd, "w") as f:
                    f.write(str(os.getpid()))
                self._is_locked = True
                return
            except FileExistsError:
                # Check for stale lock (> 10s old)
                try:
                    mtime = self.lock_path.stat().st_mtime
                    if time.time() - mtime > 10.0:
                        self.lock_path.unlink(missing_ok=True)
                        continue
                except OSError:
                    pass
                time.sleep(self.poll_interval)
        raise TimeoutError(f"Could not acquire file lock for {self.lock_path} within {self.timeout}s")

    def release(self) -> None:
        if self._is_locked:
            try:
                self.lock_path.unlink(missing_ok=True)
            except OSError:
                pass
            self._is_locked = False

    def __enter__(self) -> "FileLock":
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()

def get_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def generate_event_id() -> str:
    now = datetime.now(timezone.utc)
    ts = now.strftime("%Y%m%d-%H%M%S")
    micro = now.microsecond // 1000
    return f"evt-{ts}-{micro:03d}"

def append_event(jsonl_path: Path, event_data: Dict[str, Any]) -> Dict[str, Any]:
    """Append an immutable event to the specified JSONL stream protected by FileLock."""
    jsonl_path = Path(jsonl_path)
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    
    entry = dict(event_data)
    if "event_id" not in entry:
        entry["event_id"] = generate_event_id()
    if "timestamp" not in entry:
        entry["timestamp"] = get_now_iso()
    if "id" not in entry:
        entry["id"] = f"fb-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"

    # Invariant 2: Không evidence -> không được verified
    if entry.get("status") == "verified":
        ver = entry.get("verification")
        evidence = ""
        if isinstance(ver, dict):
            evidence = str(ver.get("evidence", "")).strip()
        if not evidence:
            raise ValueError("Không evidence -> không được verified. (Bắt buộc cung cấp verification.evidence để đóng ticket)")

    # Invariant 3: Không lock -> không được concurrent-write feedback
    lock_file = jsonl_path.with_suffix(jsonl_path.suffix + ".lock")
    with FileLock(lock_file):
        with open(jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())
    return entry

def load_and_fold_events(jsonl_path: Path) -> Dict[str, Dict[str, Any]]:
    """
    Fold immutable events by feedback ID into current snapshot states with full history.
    """
    jsonl_path = Path(jsonl_path)
    if not jsonl_path.is_file():
        return {}

    folded: Dict[str, Dict[str, Any]] = {}
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                evt = json.loads(line)
            except json.JSONDecodeError:
                continue

            fb_id = evt.get("id")
            if not fb_id:
                continue

            if fb_id not in folded:
                folded[fb_id] = dict(evt)
                folded[fb_id]["history"] = [dict(evt)]
                if evt.get("failed_attempt"):
                    folded[fb_id]["failed_attempts"] = [dict(evt["failed_attempt"])]
            else:
                current = folded[fb_id]
                history = current.get("history", [])
                history.append(dict(evt))
                
                # If new status is failed or retry:
                if evt.get("status") in ("failed", "retry"):
                    # clear previous active resolution to avoid false positive "fixed"
                    current["resolution"] = None
                    if evt.get("failed_attempt"):
                        failed_attempts = current.get("failed_attempts", [])
                        failed_attempts.append(dict(evt["failed_attempt"]))
                        current["failed_attempts"] = failed_attempts
                
                # Merge new attributes over current state
                current.update(evt)
                current["history"] = history

    return folded

def query_unresolved(jsonl_path: Path, agent_kit: Optional[str] = None) -> List[Dict[str, Any]]:
    """Return all feedback snapshots whose latest status is not 'verified'."""
    folded = load_and_fold_events(jsonl_path)
    results = []
    for item in folded.values():
        if item.get("status") != "verified":
            if agent_kit is None or item.get("agent_kit") == agent_kit:
                results.append(item)
    return sorted(results, key=lambda x: str(x.get("timestamp", "")), reverse=True)

def query_regression_knowledge(jsonl_path: Path, agent_kit: Optional[str] = None) -> List[Dict[str, Any]]:
    """Return all feedback snapshots whose latest status is 'verified'."""
    folded = load_and_fold_events(jsonl_path)
    results = []
    for item in folded.values():
        if item.get("status") == "verified":
            if agent_kit is None or item.get("agent_kit") == agent_kit:
                results.append(item)
    return sorted(results, key=lambda x: str(x.get("timestamp", "")), reverse=True)

def audit_kit_feedback(jsonl_path: Path, agent_kit: str) -> Dict[str, Any]:
    """Provide a complete feedback audit for a specific Agent Kit."""
    unresolved = query_unresolved(jsonl_path, agent_kit=agent_kit)
    knowledge = query_regression_knowledge(jsonl_path, agent_kit=agent_kit)
    return {
        "kit_name": agent_kit,
        "unresolved": unresolved,
        "regression_knowledge": knowledge
    }

def render_feedback_board(hub_dir: Path) -> str:
    """
    Render a Markdown summary dashboard (FEEDBACK_BOARD.md) from the JSONL SSOT.
    This view is completely disposable and re-generated from JSONL.
    """
    hub_dir = Path(hub_dir)
    kit_file = hub_dir / "kit_feedback.jsonl"
    bld_file = hub_dir / "builder_feedback.jsonl"

    kit_folded = load_and_fold_events(kit_file)
    bld_folded = load_and_fold_events(bld_file)

    lines: List[str] = []
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines.append("# 📋 Feedback & Learning Dashboard (Generated View)\n")
    lines.append("> ⚠️ **Đây là bảng hiển thị tự động được sinh từ JSONL.**")
    lines.append("> Nguồn sự thật duy nhất (SSOT) nằm tại `kit_feedback.jsonl` và `builder_feedback.jsonl`.")
    lines.append(f"> Cập nhật tự động lúc: `{now_str}`\n")

    # Section 1: Kit Feedback Active & Unverified
    lines.append("## 🚨 Kit Feedback: Cần Xử Lý (Active & Unverified)\n")
    unverified_kits = [f for f in kit_folded.values() if f.get("status") != "verified"]
    if not unverified_kits:
        lines.append("_Không có phản hồi nào đang tồn đọng. Toàn bộ Kit Feedback đã được verified!_\n")
    else:
        lines.append("| ID | Kit | Nguồn | Nội Dung | Trạng Thái | Fix Ref | Hành Động Tiếp Theo |")
        lines.append("|:---|:---|:---|:---|:---|:---|:---|")
        for item in sorted(unverified_kits, key=lambda x: str(x.get("timestamp", "")), reverse=True):
            f_id = f"`{item.get('id', '')}`"
            kit = f"`{item.get('agent_kit', 'global')}`"
            src = "👤 user" if item.get("source") == "user" else "🤖 system"
            content = item.get("content", "").replace("\n", " ")[:60]
            status = f"`{item.get('status', 'new')}`"
            res = item.get("resolution", {})
            fix_ref = f"{res.get('commit', '')} ({res.get('version', '')})".strip() if res else "—"
            
            if item.get("status") == "fixed":
                action = "Chờ Test/User nghiệm thu (`verified`)"
            elif item.get("status") in ("failed", "retry"):
                action = "Mở lại điều tra (`investigating`)"
            elif item.get("status") == "investigating":
                action = "Đang vá lỗi"
            else:
                action = "Tiếp nhận & Phân tích"
                
            lines.append(f"| {f_id} | {kit} | {src} | {content} | {status} | {fix_ref} | {action} |")
        lines.append("")

    # Section 2: Regression Knowledge
    lines.append("## 🛡️ Regression Knowledge: Đã Giải Quyết Triệt Để (Verified)\n")
    verified_kits = [f for f in kit_folded.values() if f.get("status") == "verified"]
    if not verified_kits:
        lines.append("_Chưa có bài học verified nào._\n")
    else:
        lines.append("| ID | Kit | Nội Dung | Đã Sửa Ở | Verified Bởi | Bài Học Phòng Ngừa |")
        lines.append("|:---|:---|:---|:---|:---|:---|")
        for item in sorted(verified_kits, key=lambda x: str(x.get("timestamp", "")), reverse=True):
            f_id = f"`{item.get('id', '')}`"
            kit = f"`{item.get('agent_kit', 'global')}`"
            content = item.get("content", "").replace("\n", " ")[:50]
            res = item.get("resolution", {})
            fix_ref = f"{res.get('commit', '')} {res.get('version', '')}".strip() or "—"
            ver = item.get("verification", {})
            verifier = ver.get("verified_by", "user")
            rule = ver.get("regression_rule", "—")
            lines.append(f"| {f_id} | {kit} | {content} | {fix_ref} | {verifier} | {rule} |")
        lines.append("")

    # Section 3: Builder Feedback
    lines.append("## 🏛️ Builder Feedback (Chỉ Đạo Chiến Lược)\n")
    if not bld_folded:
        lines.append("_Chưa có yêu cầu chiến lược nào cho Builder._\n")
    else:
        lines.append("| ID | Nội Dung | Trạng Thái | Bằng Chứng / Áp Dụng |")
        lines.append("|:---|:---|:---|:---|")
        for item in sorted(bld_folded.values(), key=lambda x: str(x.get("timestamp", "")), reverse=True):
            f_id = f"`{item.get('id', '')}`"
            content = item.get("content", "").replace("\n", " ")[:70]
            status = f"`{item.get('status', 'new')}`"
            res = item.get("resolution", {})
            evidence = res.get("evidence", "") or res.get("commit", "—")
            lines.append(f"| {f_id} | {content} | {status} | {evidence} |")
        lines.append("")

    content = "\n".join(lines)
    board_path = hub_dir / "FEEDBACK_BOARD.md"
    board_path.parent.mkdir(parents=True, exist_ok=True)
    with open(board_path, "w", encoding="utf-8") as f:
        f.write(content)
    return content

def main() -> int:
    parser = argparse.ArgumentParser(description="Unified Feedback & Learning Hub Engine")
    parser.add_argument("--hub-dir", default=str(DEFAULT_HUB_DIR), help="Feedback Hub directory")
    parser.add_argument("--add", action="store_true", help="Add new feedback event")
    parser.add_argument("--status-change", action="store_true", help="Transition status of an existing feedback")
    parser.add_argument("--id", help="Feedback ID")
    parser.add_argument("--kit", help="Target Agent Kit name")
    parser.add_argument("--content", help="Feedback content description")
    parser.add_argument("--status", default="new", help="Feedback status (new, investigating, fixed, verified, failed, retry)")
    parser.add_argument("--source", choices=["user", "system"], default="user", help="Source type")
    parser.add_argument("--target", choices=["agent_kit", "builder"], default="agent_kit", help="Target entity")
    parser.add_argument("--commit", help="Commit hash that fixed the issue")
    parser.add_argument("--version", help="Kit version that fixed the issue")
    parser.add_argument("--evidence", help="Verification evidence")
    parser.add_argument("--regression-rule", help="Preventative lesson rule")
    parser.add_argument("--audit", help="Audit feedback for a specific kit")
    parser.add_argument("--render", action="store_true", help="Render FEEDBACK_BOARD.md")

    args = parser.parse_args()
    hub_dir = Path(args.hub_dir).resolve()
    kit_file = hub_dir / "kit_feedback.jsonl"
    bld_file = hub_dir / "builder_feedback.jsonl"

    if args.audit:
        kit_name = args.audit
        audit = audit_kit_feedback(kit_file, kit_name)
        print(f"\n🔍 [FEEDBACK_AUDIT] Kit: '{kit_name}'")
        unresolved = audit["unresolved"]
        knowledge = audit["regression_knowledge"]
        print(f"   ├─ Chưa giải quyết / Chưa verified: {len(unresolved)}")
        for u in unresolved:
            print(f"   │  • [{u.get('status').upper()}] {u.get('id')}: {u.get('content')}")
        print(f"   └─ Bài học phòng ngừa (Verified): {len(knowledge)}")
        for k in knowledge:
            rule = k.get("verification", {}).get("regression_rule", "")
            print(f"      • {k.get('id')}: {rule or k.get('content')}")
        print()
        return 0

    if args.add:
        target_file = bld_file if args.target == "builder" else kit_file
        evt = {
            "source": args.source,
            "target": args.target,
            "content": args.content or "",
            "status": args.status or "new"
        }
        if args.id:
            evt["id"] = args.id
        if args.kit:
            evt["agent_kit"] = args.kit
        result = append_event(target_file, evt)
        print(f"✅ Feedback logged: {result.get('id')} [{result.get('status')}]")
        render_feedback_board(hub_dir)
        return 0

    if args.status_change:
        if not args.id:
            print("❌ --id is required for --status-change", file=sys.stderr)
            return 1
        target_file = bld_file if args.target == "builder" else kit_file
        evt: Dict[str, Any] = {
            "id": args.id,
            "status": args.status
        }
        if args.commit or args.version:
            evt["resolution"] = {
                "commit": args.commit or "",
                "version": args.version or ""
            }
        if args.evidence or args.regression_rule:
            evt["verification"] = {
                "verified_by": "user" if args.source == "user" else "auto_test",
                "evidence": args.evidence or "",
                "regression_rule": args.regression_rule or ""
            }
        result = append_event(target_file, evt)
        print(f"✅ Status updated: {result.get('id')} -> {result.get('status')}")
        render_feedback_board(hub_dir)
        return 0

    if args.render:
        render_feedback_board(hub_dir)
        print(f"✅ Board rendered at: {hub_dir / 'FEEDBACK_BOARD.md'}")
        return 0

    # Default: summary
    kit_unres = len(query_unresolved(kit_file))
    bld_unres = len(query_unresolved(bld_file))
    print(f"📋 Feedback Hub at [{hub_dir}]:")
    print(f"   ├─ Kit Feedback Chưa Giải Quyết: {kit_unres}")
    print(f"   └─ Builder Feedback Chưa Giải Quyết: {bld_unres}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
