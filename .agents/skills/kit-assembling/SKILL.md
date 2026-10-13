---
name: kit-assembling
description: "Lắp ráp các cấu phần thành Agent Kit hoàn chỉnh trong thư mục cách ly ./output/<kit-name>/, sinh manifest.json chuẩn SSOT (khai báo topology, delegatesTo, ownedSkills, memoryScope), sinh hooks an toàn runtime (PreToolUse), sinh hợp đồng antigravity.json 6 pha, sinh bộ Domain-Adaptive Checklist thực thi và đóng gói theo chuẩn Kit Type."
when_to_use: "Khi hoàn tất các cấu phần và cần lắp ráp thành thư mục Agent Kit hoàn chỉnh."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.6.0
---

# Kit Assembling

Kỹ năng tổng hợp, tổ chức thư mục và đóng gói Agent Kit hoàn chỉnh, tuân thủ nghiêm ngặt ranh giới cách ly không gian làm việc, chuẩn hóa `manifest.json` làm Single Source of Truth (SSOT), và tích hợp Domain-Adaptive Checklist & Runtime Contracts bảo vệ hệ thống.

---

## 1. WORKSPACE ISOLATION (BẤT BIẾN)

- Mọi file của Agent Kit mới **BẮT BỘC** được tạo tại:
  `./output/<kit-name>/` (ví dụ: `./output/marketing-growth-suite/`)
- **TUYỆT ĐỐI KHÔNG** ghi đè hoặc tạo trực tiếp vào `.agents/` của Agent Kit Creator.

---

## 2. CẤU TRÚC ĐÓNG GÓI THEO TOPOLOGY

### A. Single Agent Kit (Micro / Standard)
```
output/<kit-name>/
├── agent/
│   └── [kit-name].md         # System prompt chính
├── skills/
│   └── [skill-name]/SKILL.md # Skills trực thuộc
├── workflows/
├── hooks/
│   ├── hooks.json
│   └── validate-tool-call.mjs # PreToolUse safety gate
├── antigravity.json           # Antigravity 6-Phase Contract
├── execution_policy.json      # ACO Lite Orchestration Intent
└── manifest.json
```

### B. Multi-Agent Suite Kit (Mini-Suite / Full Suite)
```
output/<suite-name>/
├── agent/
│   ├── [orchestrator-name].md # Master Orchestrator (với Worker Briefing & Anti-Delegation)
│   ├── [specialist-a].md      # Real Specialist Agent A
│   └── [specialist-b].md      # Real Specialist Agent B
├── skills/                    # Domain skills mapped to Specialists
│   ├── [skill-a1]/SKILL.md
│   └── context-compression/   # Chống thoái hóa context phiên dài
├── workflows/
├── memory/
│   ├── MEMORY.md
│   ├── shared/
│   └── domains/
├── hooks/
│   ├── hooks.json
│   ├── validate-tool-call.mjs # Boundary & Safety enforcement
│   └── antigravity-doctor.mjs # Health diagnostics
├── scripts/
│   ├── checklist.py           # Domain-Adaptive Checklist Runner (từ domain-checklist-template.py)
│   └── validation_runner.py   # Shared execution runner
├── DESIGN.md                  # YAML Design Tokens SSOT (nếu có UI)
├── antigravity.json           # Antigravity 6-Phase Contract
├── execution_policy.json      # ACO Lite Orchestration Intent
└── manifest.json              # Khai báo SSOT phân cấp
```

---

## 3. DOMAIN-ADAPTIVE CHECKLIST GENERATION

Khi sinh `scripts/checklist.py` (sử dụng `templates/domain-checklist-template.py` làm gốc), kit-assembling tự động cấu hình các lớp kiểm định tương ứng với Risk Profile:
- **Content / Copywriting**: Tích hợp kiểm tra Readability, độ dài từ, và phát hiện từ cấm AI (banned words).
- **Growth / Finance / Data**: Tích hợp gọi script Python tính toán tất định (Deterministic Computation Guard).
- **Legal / Compliance / Audit**: Tích hợp Negative Completeness Matrix (kiểm tra điều khoản bắt buộc bị thiếu).
- **UI / UX / Frontend**: Tích hợp `DESIGN.md` token syntax check và Web/Headless render validation.
- **DevOps / Engineering**: Tích hợp Linter, Unit tests, Healthcheck và Transactional Rollback trigger.

---

## 4. RUNTIME SAFETY & PLATFORM CONTRACT GENERATION

Mọi kit sinh ra được tự động tích hợp:
1. **OS Destruction Protection**: Chặn đứng `rm -rf /`, `mkfs`, `format` ở tầng PreToolUse (`hooks/validate-tool-call.mjs`).
2. **Antigravity 6-Phase Contract (`antigravity.json`)**: Khai báo đầy đủ các pha discovery, mcp, hooks, orchestration, plugin, validation.
3. **Specialist Boundary Enforcement (Dành cho Suite)**: Chặn đứng hành vi ghi đè file ngoài domain sở hữu của từng Specialist.
4. **Central Feedback & Learning Connectivity**: Mọi Kit sinh ra được cấu hình kết nối trực tiếp với Central Feedback Hub tại `Downloads/Shared Workspace/Feedback/kit_feedback.jsonl` qua `feedback_hub.py` để ghi nhận lỗi runtime (`source: "system"`) và phản hồi người dùng (`source: "user"`), loại bỏ hoàn toàn các thư mục evolution cục bộ cồng kềnh.
5. **Universal Filesystem & Workspace Contract**:
   - Khối lệnh `### 🔒 FILESYSTEM & WORKSPACE CONTRACT (BẤT BIẾN)` bắt buộc xuất hiện trong System Prompt của các Agent.
   - Nhốt toàn bộ intermediate files, chunks, debug logs, cache vào `.workspace/` để giữ `outputs/` sạch sẽ hoàn toàn.
   - Khai báo cấu trúc `artifact_contracts` với `workspace_dir: ".workspace"` trong `manifest.json`.
   - Chèn card README 4 dòng chuẩn từ `templates/readme-card-template.md` lên đầu tài liệu của Kit.

---

## 5. SINH MANIFEST.JSON CHUẨN SSOT

Khai báo đầy đủ trường `topology`, `role`, `delegatesTo`, `ownedSkills`, `memoryScope`:

```json
{
  "name": "kit-name",
  "kitVersion": "1.0.0",
  "topology": {
    "type": "hierarchical-multi-agent",
    "orchestrator": "master-orchestrator",
    "spectrumPosition": "full-suite",
    "rightAltitudeRationale": "Decoupled domains with independent skill clusters."
  },
  "agents": {
    "master-orchestrator": {
      "role": "master-orchestrator",
      "tools": ["Read", "Grep", "Glob", "Agent"],
      "delegatesTo": ["specialist-a", "specialist-b"]
    },
    "specialist-a": {
      "role": "domain-specialist",
      "domain": "domain-a",
      "tools": ["Read", "Grep", "Glob", "Edit", "Write"],
      "ownedSkills": ["skill-a1", "skill-a2"],
      "memoryScope": ["shared", "domains/domain-a"]
    }
  },
  "skills": { ... },
  "workflows": { ... }
}
```

---

## 6. COMPILE DECISION SYSTEM & INTEGRITY LOCK PIPELINE

Sau khi sinh toàn bộ cấu phần trong `./output/<kit-name>/`, kit-assembling **BẮT BUỘC** thực thi pipeline biên dịch hệ thống ra quyết định và khóa toàn vẹn:
1. `python .agents/scripts/compile_routing_index.py ./output/<kit-name>/` ➔ Sinh `routing_index.json`
2. `python .agents/scripts/compile_invariants.py ./output/<kit-name>/` ➔ Sinh `invariant_rules.json`
3. `python .agents/scripts/compile_state_schema.py ./output/<kit-name>/` ➔ Sinh `state_schema.json`
4. `python .agents/scripts/compile_execution_policy.py ./output/<kit-name>/` ➔ Sinh `execution_policy.json`
5. `python .agents/scripts/compile_task_classifier.py ./output/<kit-name>/` ➔ Sinh `task_classifier_index.json`
6. `python .agents/scripts/compile_evidence_schemas.py ./output/<kit-name>/` ➔ Sinh `evidence_schemas.json`
7. `python .agents/scripts/dry_run_simulation.py ./output/<kit-name>/` ➔ Chạy giả lập reachability, cycle, coverage
8. `python .agents/scripts/generate_manifest.py ./output/<kit-name>/` & `dependency_graph.py` ➔ Khóa `manifest.lock.json`
