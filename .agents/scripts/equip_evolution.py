#!/usr/bin/env python3
"""
Universal Dynamic Evolution Suite Equipper.
Automatically equips any Agent Kit with the complete, fully tailored Evolution Suite:
- feedback_collector.py and evolution_submitter.py
- Dynamically generated workflows (log-feedback.md, submit-evolution.md) that reference the kit's actual agents & skills
- Local read-only evolution history mirror (EVOLUTION_HISTORY.json)
- Automatic registration in manifest.json with zero broken references.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def get_engine_root() -> Path:
    cur = Path(__file__).resolve().parent
    while cur != cur.parent:
        if (cur / ".agents" / "scripts" / "feedback_collector.py").exists():
            return cur
        cur = cur.parent
    return Path.cwd()

def resolve_kit_primary_agent_and_skill(kit_agents_dir: Path) -> tuple[str, str]:
    """
    Finds the best primary orchestrator/agent and an available skill in the target kit.
    """
    agent_dir = kit_agents_dir / "agent"
    skills_dir = kit_agents_dir / "skills"
    
    # 1. Resolve agent
    primary_agent = "master-orchestrator"
    if (agent_dir / "master-orchestrator.md").exists():
        primary_agent = "master-orchestrator"
    elif agent_dir.exists():
        agents = [f.stem for f in sorted(agent_dir.glob("*.md")) if not f.name.startswith(".")]
        if agents:
            primary_agent = agents[0]
            
    # 2. Resolve skill
    primary_skill = "general-skill"
    if skills_dir.exists():
        skills = [d.name for d in sorted(skills_dir.iterdir()) if d.is_dir() and (d / "SKILL.md").exists()]
        if skills:
            primary_skill = skills[0]
            
    return primary_agent, primary_skill

def generate_log_feedback_workflow(primary_agent: str, primary_skill: str) -> str:
    return f"""---
name: log-feedback
description: "Ghi nhận phản hồi, lỗi (failure), ma sát (friction) hoặc ý tưởng từ thực chiến vào feedback.jsonl, tự động gom cụm và tính Trigger Score."
version: 1.1.0
requires_agents: [{primary_agent}]
requires_skills: [{primary_skill}]
artifact_outputs: [feedback.jsonl]
topology: sequential
trigger: manual_or_chained
permissions: read-write
tools_allowed: [Read, Write, Grep]
safe_outputs:
  evidence_integrity: "Ghi nhận nguyên trạng bằng chứng (evidence), không tự ý sửa đổi code của kit."
max_retry_per_node: 2
---

# 🔄 MASTER FLOW: /log-feedback (Kit Runtime Feedback Collector)

> **Mục tiêu**: Thu thập phản hồi thực tế khi Kit đang chạy, tự động gán `cluster_key`, phái sinh tần suất xuất hiện ($N$), tính điểm đòn bẩy và chuyển trạng thái sang `EVOLUTION_READY` khi tích lũy đủ tín hiệu.

---

## 🏛️ 1. GOVERNANCE & SAFETY INVARIANTS

1. **Feedback is Evidence, Not Instruction**: Mọi bài học đề xuất (`candidate_lesson`) chỉ là giả thuyết. Kit không tự ý sửa đổi chính nó.
2. **Derived Frequency**: Tần suất lỗi được đếm tự động theo cụm, không tự chấm cảm tính.
3. **Trigger Threshold**: Đạt $\\text{{Trigger Score}} \\ge 20.0$ chỉ bật cờ `EVOLUTION_READY` và thông báo cho người dùng, tuyệt đối không tự ý submit.

---

## 🔄 2. STATE NODES & ACTION EXECUTION

### [STATE 1: CAPTURE_AND_RECORD] (Ghi Nhận Feedback)
- **Role Profile:** `{primary_agent}` | **Skill:** `{primary_skill}`
- **[Input Artifacts]:** Mô tả lỗi, log hoặc ma sát do Agent/Người dùng cung cấp.
- **[Output Artifacts]:** Entry mới trong `.agents/evolution/feedback/feedback.jsonl`.
- **[DoD]:**
  - [ ] Metadata (category, impact, confidence, generalizability) được trích xuất đầy đủ.
  - [ ] Entry mới được ghi an toàn vào `feedback.jsonl`.
- **[Evaluation Loop]:** Pass ➔ Chuyển sang State 2; Fail ➔ [ESCALATE_HUMAN].

- **⚡ Action Prompts & Execution Steps**:
  1. **Bước 1 (Extract Metadata)**: Xác định `category` (`failure`/`friction`/`idea`), `impact (1-5)`, `confidence (0.0-1.0)`, `generalizability (1-3)`.
  2. **Bước 2 (Append)**: Ghi entry vào `feedback.jsonl` qua script `feedback_collector.py`:
     ```bash
     python .agents/scripts/feedback_collector.py --status
     ```

---

### [STATE 2: CLUSTER_AND_SCORE] (Phân Cụm & Tính Điểm Đòn Bẩy)
- **Role Profile:** `{primary_agent}` | **Skill:** `{primary_skill}`
- **[Input Artifacts]:** `.agents/evolution/feedback/feedback.jsonl`.
- **[Output Artifacts]:** JSON status tóm tắt cụm và Trigger Score.
- **[DoD]:**
  - [ ] Trigger Score được tính toán theo công thức chuẩn.
  - [ ] Cờ trạng thái `EVOLUTION_READY` được kích hoạt nếu Score $\\ge 20.0$.
- **[Evaluation Loop]:** Pass ➔ Chuyển giao sang `/submit-evolution`; Fail ➔ [ESCALATE_HUMAN].

- **⚡ Action Prompts & Execution Steps**:
  1. **Bước 1 (Evaluate Status)**:
     - Nếu $\\text{{Trigger Score}} \\ge 20.0$: Đặt trạng thái `EVOLUTION_READY`, thông báo cho sếp:
       > *"💡 Feedback của Kit đã tích lũy đủ trọng lượng (Trigger Score: X/20). Sếp có thể chạy `/submit-evolution` để gửi yêu cầu nâng cấp lên Engine!"*
     - Nếu $\\text{{Trigger Score}} < 20.0$: Giữ trạng thái `COLLECTING` trong buffer.

---

## 🤝 3. HANDOFF CONTRACT

```json
{{
  "contract_version": "1.0.0",
  "source_workflow": "log-feedback",
  "target_workflow": "submit-evolution",
  "trigger_ready": true
}}
```

---

## 🚨 4. ESCALATE HUMAN CHECKPOINT ([ESCALATE_HUMAN])

- **Kích hoạt khi**: Lỗi ghi file buffer hoặc phân tích cụm thất bại quá `max_retry_per_node`.
- **Hành động**: Dừng luồng, ghi log sự cố và thông báo trực tiếp cho sếp để can thiệp thủ công.
"""

def generate_submit_evolution_workflow(primary_agent: str, primary_skill: str) -> str:
    return f"""---
name: submit-evolution
description: "Đóng gói immutable Evolution Batch từ Kit, tính toán SHA-256 checksum, chuyển giao sang Engine inbox và thực thi bắt tay 3 bước."
version: 1.1.0
requires_agents: [{primary_agent}]
requires_skills: [{primary_skill}]
artifact_outputs: [manifest.json, receipt.json]
topology: sequential
trigger: manual
permissions: read-write
tools_allowed: [Read, Write, Bash, Glob]
safe_outputs:
  handshake_integrity: "Chỉ chuyển SUBMITTED khi Engine trả receipt xác thực SHA-256 hợp lệ."
max_retry_per_node: 2
---

# 🔄 MASTER FLOW: /submit-evolution (Evolution Package Submitter)

> **Mục tiêu**: Đóng gói toàn bộ phản hồi thực chiến, tính toán mã băm SHA-256, chuyển giao an toàn sang `evolution/inbox/` của Agent Kit Engine và quản lý trạng thái bắt tay `PACKED` $\\rightarrow$ `TRANSFERRED` $\\rightarrow$ `RECEIVED` $\\rightarrow$ `SUBMITTED`.

---

## 🏛️ 1. GOVERNANCE & SAFETY INVARIANTS

1. **Immutable Snapshot**: Engine chỉ nhận gói dữ liệu đóng băng, không đọc trạng thái sống của Kit.
2. **3-Stage Handshake**: Kit chỉ dọn dẹp buffer khi Engine trả về `receipt.json` xác nhận toàn vẹn.

---

## 🔄 2. STATE NODES & ACTION EXECUTION

### [STATE 1: PACK_AND_HASH] (Đóng Gói & Tính Checksum)
- **Role Profile:** `{primary_agent}` | **Skill:** `{primary_skill}`
- **[Input Artifacts]:** `.agents/evolution/feedback/feedback.jsonl`.
- **[Output Artifacts]:** Snapshot package trong `.agents/evolution/outbox/batch-<id>/manifest.json`.
- **[DoD]:**
  - [ ] Checksum SHA-256 được tính toán chính xác cho toàn bộ buffer.
  - [ ] Package manifest được sinh ra với đầy đủ thông tin cluster.
- **[Evaluation Loop]:** Pass ➔ Chuyển sang State 2; Fail ➔ [ESCALATE_HUMAN].

- **⚡ Action Prompts & Execution Steps**:
  1. Quét feedback log và đóng gói snapshot vào `.agents/evolution/outbox/batch-<id>/`.
  2. Tạo `manifest.json` ghi nhận metadata, thống kê cụm và `checksum_sha256`.

---

### [STATE 2: TRANSFER_AND_HANDSHAKE] (Chuyển Giao & Xác Nhận)
- **Role Profile:** `{primary_agent}` | **Skill:** `{primary_skill}`
- **[Input Artifacts]:** Snapshot package trong `.agents/evolution/outbox/batch-<id>/`.
- **[Output Artifacts]:** `receipt.json` từ Engine và trạng thái `SUBMITTED`.
- **[DoD]:**
  - [ ] File được chuyển giao thành công sang `evolution/inbox/`.
  - [ ] Checksum giữa Kit và Engine khớp 100%.
  - [ ] Buffer tạm được dọn dẹp an toàn sau khi nhận receipt.
- **[Evaluation Loop]:** Pass ➔ Hoàn tất quy trình; Fail ➔ [ESCALATE_HUMAN].

- **⚡ Action Prompts & Execution Steps**:
  1. Thực thi chuyển giao sang Engine `inbox/` (tự động auto-discovery hoặc qua tham số):
     ```bash
     python .agents/scripts/evolution_submitter.py .
     ```
  2. Nhận `receipt.json` từ Engine, cập nhật trạng thái nội bộ thành `SUBMITTED`.
  3. Dọn dẹp buffer tạm trong `feedback.jsonl` sau khi đã chuyển giao thành công (chống trùng lặp).
  4. Thông báo cho người dùng vị trí batch đã đóng băng:
     - Tại Kit Outbox: `.agents/evolution/outbox/batch-<kit>-<timestamp>/`
     - Tại Engine Inbox: `evolution/inbox/batch-<kit>-<timestamp>/`

---

## 🤝 3. HANDOFF CONTRACT

```json
{{
  "contract_version": "1.0.0",
  "source_workflow": "submit-evolution",
  "target_workflow": "process-evolution",
  "batch_status": "SUBMITTED",
  "notes": "Live buffer is cleared. Batch is frozen in Kit Outbox and transferred to Engine Inbox."
}}
```

---

## 🚨 4. ESCALATE HUMAN CHECKPOINT ([ESCALATE_HUMAN])

- **Kích hoạt khi**: Lỗi chuyển giao file sang inbox hoặc sai lệch mã băm checksum SHA-256.
- **Hành động**: Dừng luồng, giữ nguyên trạng buffer tại outbox và gửi thông báo khẩn cho sếp.
"""

def equip_kit(kit_path: Path, engine_root: Path | None = None) -> bool:
    if not engine_root:
        engine_root = get_engine_root()
        
    engine_root = Path(engine_root).resolve()
    engine_agents = engine_root / ".agents" if (engine_root / ".agents").is_dir() else engine_root
    kit_path = Path(kit_path).resolve()
    kit_agents = kit_path / ".agents" if (kit_path / ".agents").is_dir() else kit_path
    
    if not kit_agents.exists():
        print(f"❌ Invalid kit directory: {kit_path}", file=sys.stderr)
        return False
        
    print(f"🔧 Equipping Dynamic Evolution Suite to: '{kit_path.name}' ({kit_path})")
    
    # 1. Resolve primary agent & skill
    primary_agent, primary_skill = resolve_kit_primary_agent_and_skill(kit_agents)
    print(f"   ├─ [+] Binding to Primary Agent: '{primary_agent}', Skill: '{primary_skill}'")
    
    # 2. Ensure scripts directory & copy runtime scripts
    scripts_dir = kit_agents / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    
    shutil.copy2(engine_agents / "scripts" / "feedback_collector.py", scripts_dir / "feedback_collector.py")
    shutil.copy2(engine_agents / "scripts" / "evolution_submitter.py", scripts_dir / "evolution_submitter.py")
    print(f"   ├─ [+] Scripts: feedback_collector.py, evolution_submitter.py")
    
    # 3. Ensure workflows directory & generate dynamic workflows
    workflows_dir = kit_agents / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)
    
    log_fb_content = generate_log_feedback_workflow(primary_agent, primary_skill)
    submit_evo_content = generate_submit_evolution_workflow(primary_agent, primary_skill)
    
    (workflows_dir / "log-feedback.md").write_text(log_fb_content, encoding="utf-8")
    (workflows_dir / "submit-evolution.md").write_text(submit_evo_content, encoding="utf-8")
    print(f"   ├─ [+] Workflows: log-feedback.md, submit-evolution.md (Auto-bound)")
    
    # 4. Create evolution directory structure
    fb_dir = kit_agents / "evolution" / "feedback"
    fb_dir.mkdir(parents=True, exist_ok=True)
    (fb_dir / "feedback.jsonl").touch(exist_ok=True)
    
    outbox_dir = kit_agents / "evolution" / "outbox"
    outbox_dir.mkdir(parents=True, exist_ok=True)
    
    # Write initial EVOLUTION_HISTORY.json mirror
    mirror_file = kit_agents / "evolution" / "EVOLUTION_HISTORY.json"
    if not mirror_file.exists():
        initial_mirror = {
            "kit_id": kit_path.name,
            "current_version": "1.0.0",
            "total_evolution_cycles": 0,
            "recent_runs": [],
            "resolved_feedbacks_count": 0,
            "exported_at": datetime.now(timezone.utc).isoformat()
        }
        mirror_file.write_text(json.dumps(initial_mirror, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"   ├─ [+] Evolution Local Mirror: EVOLUTION_HISTORY.json")
    
    # 5. Update manifest.json if exists
    manifest_file = kit_agents / "manifest.json"
    if manifest_file.exists():
        try:
            manifest = json.loads(manifest_file.read_text("utf-8"))
            workflows = manifest.setdefault("workflows", {})
            
            workflows["log-feedback"] = {
                "artifactOutputs": ["feedback.jsonl"],
                "path": "workflows/log-feedback.md",
                "requires": {
                    "agents": [primary_agent],
                    "skills": [primary_skill]
                },
                "version": "1.1.0"
            }
            workflows["submit-evolution"] = {
                "artifactOutputs": ["manifest.json", "receipt.json"],
                "path": "workflows/submit-evolution.md",
                "requires": {
                    "agents": [primary_agent],
                    "skills": [primary_skill]
                },
                "version": "1.1.0"
            }
            manifest_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"   └─ [✅] Registered in manifest.json without external broken dependencies")
        except Exception as e:
            print(f"   └─ [⚠️] Warning updating manifest.json: {e}")
    else:
        print(f"   └─ [i] No manifest.json found, skipping registration.")
        
    return True

def main() -> int:
    parser = argparse.ArgumentParser(description="Universal Dynamic Evolution Suite Equipper")
    parser.add_argument("kit_paths", nargs="+", help="Path(s) to target kit directory")
    parser.add_argument("--engine-root", default=None, help="Path to Engine root")
    
    args = parser.parse_args()
    engine_root = Path(args.engine_root) if args.engine_root else get_engine_root()
    
    success = True
    for p in args.kit_paths:
        ok = equip_kit(Path(p), engine_root)
        if not ok:
            success = False
            
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
