# Unified Feedback & Learning Hub Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Triển khai Unified Feedback & Learning Hub tại `Downloads/Shared Workspace/Feedback/` dựa trên Event Sourcing (Append-Only JSONL làm SSOT), phân tách `source` + `target`, quản lý vòng đời nhị phân (`new` → `verified`), tích hợp cơ chế Pre-flight Regression Knowledge vào Agent Kit Builder, và dỡ bỏ toàn bộ hệ thống evolution cũ cồng kềnh.

**Architecture:** Tạo script trung tâm `feedback_hub.py` để xử lý append event, fold state theo id, và tự động render `FEEDBACK_BOARD.md`; tích hợp hook pre-flight audit vào `/refactor-kit` và `validate_kit.py`; dỡ bỏ các workflow/script evolution cũ (`log-feedback.md`, `submit-evolution.md`, `process-evolution.md`, `feedback_collector.py`, `evolution_submitter.py`); cập nhật `kit-assembling` và tái sinh registry.

**Tech Stack:** Python 3.12 (unittest, json, datetime, pathlib, argparse), Markdown (Generated Dashboard View), JSON Lines.

## Global Constraints

- **Single Source of Truth:** Chỉ có `kit_feedback.jsonl` và `builder_feedback.jsonl` là SSOT. `FEEDBACK_BOARD.md` là generated view, tuyệt đối không lưu trạng thái vào file board.
- **Append-Only:** Không bao giờ sửa dòng cũ trong JSONL. Mỗi chuyển đổi trạng thái là một event mới cùng `id`.
- **TDD First:** Mọi tính năng logic đều có test case trong `test_feedback_hub.py` trước khi cài đặt code.
- **Binary Definition of Done:** Toàn bộ test suite phải PASS 100% và `validate_kit.py .agents` đạt `0 error(s), 0 warning(s)`.

---

### Task 1: Core Engine: `feedback_hub.py` & Test Suite

**Files:**
- Create: `.agents/scripts/feedback_hub.py`
- Create: `.agents/scripts/tests/test_feedback_hub.py`

**Interfaces:**
- Consumes: Spec `docs/superpowers/specs/2026-08-30-feedback-and-learning-hub-design.md` §3, §4, §5
- Produces:
  - `append_event(jsonl_path, event_dict) -> dict`
  - `load_and_fold_events(jsonl_path) -> dict[str, dict]` (Gộp các event cùng `id` thành snapshot mới nhất kèm `history`)
  - `query_unresolved(jsonl_path, agent_kit=None) -> list[dict]` (Các mục có `status != "verified"`)
  - `query_regression_knowledge(jsonl_path, agent_kit=None) -> list[dict]` (Các mục có `status == "verified"`)
  - `render_feedback_board(hub_dir) -> str` (Sinh `FEEDBACK_BOARD.md`)

- [ ] **Step 1: Write failing test in `test_feedback_hub.py`**

```python
import unittest
import tempfile
import json
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import feedback_hub

class TestFeedbackHub(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.hub_dir = Path(self.temp_dir.name)
        self.kit_file = self.hub_dir / "kit_feedback.jsonl"
        self.bld_file = self.hub_dir / "builder_feedback.jsonl"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_append_and_fold_events(self):
        # 1. New event
        e1 = feedback_hub.append_event(self.kit_file, {
            "id": "fb-001",
            "source": "user",
            "target": "agent_kit",
            "agent_kit": "test-kit",
            "content": "Initial bug",
            "status": "new"
        })
        self.assertEqual(e1["status"], "new")

        # 2. Transition to fixed
        e2 = feedback_hub.append_event(self.kit_file, {
            "id": "fb-001",
            "status": "fixed",
            "resolution": {"commit": "c1", "version": "v1.0"}
        })

        # 3. Fold state
        folded = feedback_hub.load_and_fold_events(self.kit_file)
        self.assertIn("fb-001", folded)
        self.assertEqual(folded["fb-001"]["status"], "fixed")
        self.assertEqual(folded["fb-001"]["resolution"]["commit"], "c1")
        self.assertEqual(len(folded["fb-001"]["history"]), 2)

    def test_lifecycle_failed_retry_verified(self):
        feedback_hub.append_event(self.kit_file, {"id": "fb-002", "agent_kit": "test-kit", "status": "new", "content": "Bug 2"})
        feedback_hub.append_event(self.kit_file, {"id": "fb-002", "status": "fixed", "resolution": {"commit": "c2"}})
        feedback_hub.append_event(self.kit_file, {"id": "fb-002", "status": "failed", "note": "Still reproduced"})
        feedback_hub.append_event(self.kit_file, {"id": "fb-002", "status": "retry"})
        
        # Must be in unresolved
        unresolved = feedback_hub.query_unresolved(self.kit_file, agent_kit="test-kit")
        self.assertEqual(len(unresolved), 1)
        self.assertEqual(unresolved[0]["status"], "retry")

        # Now verify it
        feedback_hub.append_event(self.kit_file, {"id": "fb-002", "status": "verified", "verification": {"evidence": "Pass", "regression_rule": "Rule A"}})
        unresolved_after = feedback_hub.query_unresolved(self.kit_file, agent_kit="test-kit")
        self.assertEqual(len(unresolved_after), 0)

        # Must be in regression knowledge
        knowledge = feedback_hub.query_regression_knowledge(self.kit_file, agent_kit="test-kit")
        self.assertEqual(len(knowledge), 1)
        self.assertEqual(knowledge[0]["verification"]["regression_rule"], "Rule A")

    def test_render_board(self):
        feedback_hub.append_event(self.kit_file, {"id": "fb-001", "agent_kit": "kit-a", "status": "new", "content": "Unresolved bug"})
        board_content = feedback_hub.render_feedback_board(self.hub_dir)
        self.assertIn("Feedback & Learning Dashboard", board_content)
        self.assertIn("fb-001", board_content)
        board_file = self.hub_dir / "FEEDBACK_BOARD.md"
        self.assertTrue(board_file.is_file())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python .agents/scripts/tests/test_feedback_hub.py`  
Expected: FAIL with `ModuleNotFoundError: No module named 'feedback_hub'`

- [ ] **Step 3: Implement `feedback_hub.py`**

Implement `.agents/scripts/feedback_hub.py`:
- `append_event`: Sinh `event_id`, gán `timestamp` ISO 8601 UTC nếu thiếu, append JSON line.
- `load_and_fold_events`: Đọc từng dòng JSONL, gộp theo `id`. Entry ban đầu làm base, các event sau cập nhật đè thuộc tính (như `status`, `resolution`, `verification`) và lưu `history`.
- `query_unresolved`: Trả về danh sách snapshot có `status != "verified"` (có thể filter theo `agent_kit`).
- `query_regression_knowledge`: Trả về danh sách snapshot có `status == "verified"` (có thể filter theo `agent_kit`).
- `render_feedback_board`: Đọc cả `kit_feedback.jsonl` và `builder_feedback.jsonl`, sinh `FEEDBACK_BOARD.md` định dạng Markdown sạch sẽ, không ghi đè SSOT.
- Hỗ trợ CLI: `--hub-dir`, `--add`, `--status-change`, `--audit <kit>`, `--render`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python .agents/scripts/tests/test_feedback_hub.py`  
Expected: PASS (all tests pass).

- [ ] **Step 5: Commit changes**

```bash
git add .agents/scripts/feedback_hub.py .agents/scripts/tests/test_feedback_hub.py
git commit -m "feat(feedback): implement core event-sourced feedback_hub engine and test suite"
```

---

### Task 2: Integrate Pre-Flight Feedback Audit into Workflow & Validator

**Files:**
- Modify: `.agents/workflows/refactor-kit.md`
- Modify: `.agents/scripts/validate_kit.py`
- Test: `.agents/scripts/tests/test_feedback_hub.py`

**Interfaces:**
- Consumes: `feedback_hub.query_unresolved()`, `feedback_hub.query_regression_knowledge()`
- Produces:
  - Step 0 trong `refactor-kit.md` tự động đọc feedback chưa giải quyết từ `Downloads/Shared Workspace/Feedback/kit_feedback.jsonl`.
  - `validate_kit.py` có hàm kiểm tra và cảnh báo feedback tồn đọng của kit.

- [ ] **Step 1: Write test for pre-flight audit integration in `test_feedback_hub.py`**

```python
    def test_audit_kit_summary(self):
        feedback_hub.append_event(self.kit_file, {"id": "fb-101", "agent_kit": "target-kit", "status": "new", "content": "Bug X"})
        feedback_hub.append_event(self.kit_file, {"id": "fb-102", "agent_kit": "target-kit", "status": "fixed", "resolution": {"commit": "c10"}})
        feedback_hub.append_event(self.kit_file, {"id": "fb-103", "agent_kit": "target-kit", "status": "verified", "verification": {"regression_rule": "Rule Z"}})

        audit = feedback_hub.audit_kit_feedback(self.kit_file, "target-kit")
        self.assertEqual(len(audit["unresolved"]), 2)
        self.assertEqual(len(audit["regression_knowledge"]), 1)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python .agents/scripts/tests/test_feedback_hub.py`  
Expected: FAIL with `AttributeError: module 'feedback_hub' has no attribute 'audit_kit_feedback'`

- [ ] **Step 3: Implement `audit_kit_feedback` and update `refactor-kit.md`**

In `feedback_hub.py`:
```python
def audit_kit_feedback(kit_jsonl: Path, kit_name: str) -> dict[str, Any]:
    unresolved = query_unresolved(kit_jsonl, agent_kit=kit_name)
    knowledge = query_regression_knowledge(kit_jsonl, agent_kit=kit_name)
    return {
        "kit_name": kit_name,
        "unresolved": unresolved,
        "regression_knowledge": knowledge
    }
```

In `.agents/workflows/refactor-kit.md`:
Update Bước 0:
```markdown
1. **Pre-flight Feedback & Knowledge Audit**:
   - Chạy `python .agents/scripts/feedback_hub.py --audit <kit-name>`.
   - Nạp toàn bộ feedback chưa giải quyết (`new`, `investigating`, `failed`, `retry`, `fixed`) vào `gap_analysis.md`.
   - Nạp các `regression_rule` đã verified để thiết lập rào chắn phòng ngừa lỗi.
```

In `.agents/scripts/validate_kit.py`:
Add helper function `check_kit_feedback_health(kit_name: str, hub_dir: Path) -> list[str]` to surface active unverified bugs during validation warnings.

- [ ] **Step 4: Run test to verify it passes**

Run: `python .agents/scripts/tests/test_feedback_hub.py`  
Expected: PASS

- [ ] **Step 5: Commit changes**

```bash
git add .agents/scripts/feedback_hub.py .agents/workflows/refactor-kit.md .agents/scripts/validate_kit.py .agents/scripts/tests/test_feedback_hub.py
git commit -m "feat(feedback): integrate pre-flight feedback audit into refactor workflow and validator"
```

---

### Task 3: Deprecate Old Evolution/Feedback Workflows & Scripts

**Files:**
- Delete: `.agents/workflows/log-feedback.md`
- Delete: `.agents/workflows/submit-evolution.md`
- Delete: `.agents/workflows/process-evolution.md`
- Delete: `.agents/scripts/evolution_submitter.py`
- Delete: `.agents/scripts/feedback_collector.py`
- Test: `.agents/scripts/tests/test_structural_anchors.py`

**Interfaces:**
- Consumes: Clean removal of obsolete files
- Produces: Zero broken links or invalid references in remaining files.

- [ ] **Step 1: Remove obsolete files**

```bash
git rm .agents/workflows/log-feedback.md
git rm .agents/workflows/submit-evolution.md
git rm .agents/workflows/process-evolution.md
git rm .agents/scripts/evolution_submitter.py
git rm .agents/scripts/feedback_collector.py
```

- [ ] **Step 2: Clean up references in `dynamic-routing.md` and `core-guardrails.md`**

Remove mentions of `/log-feedback`, `/submit-evolution`, `/process-evolution` and 4-tier waterfall from:
- `.agents/rules/dynamic-routing.md`
- `.agents/rules/core-guardrails.md`
Replace with streamlined reference to `feedback_hub.py` and Central Feedback Hub.

- [ ] **Step 3: Run structural tests to verify no dangling refs**

Run: `python .agents/scripts/tests/test_structural_anchors.py`  
Run: `python .agents/scripts/tests/test_templates.py`  
Expected: PASS

- [ ] **Step 4: Commit deprecation**

```bash
git add -u
git commit -m "chore(feedback): deprecate and remove obsolete evolution workflows and collector scripts"
```

---

### Task 4: Update Kit Assembling & Manifest Contracts

**Files:**
- Modify: `.agents/skills/kit-assembling/SKILL.md`
- Modify: `.agents/templates/agent-template.md`
- Test: `.agents/scripts/tests/test_templates.py`

**Interfaces:**
- Consumes: New Feedback Hub architecture
- Produces: Updated guidelines in `kit-assembling` pointing to `Shared Workspace/Feedback/` instead of local `.agents/evolution/`.

- [ ] **Step 1: Update `kit-assembling/SKILL.md`**

Replace Section 4.4 (`Closed-Loop Evolution Infrastructure` pointing to `feedback_collector.py`) with:
```markdown
4. **Central Feedback & Learning Connectivity**: Mọi kit sinh ra được cấu hình kết nối trực tiếp với `Downloads/Shared Workspace/Feedback/kit_feedback.jsonl` qua `feedback_hub.py` để ghi nhận lỗi runtime (`source: "system"`) và phản hồi người dùng (`source: "user"`).
```

- [ ] **Step 2: Update `agent-template.md`**

In Section 5 of `.agents/templates/agent-template.md`, ensure prompt instructs agent to record critical failures to `Shared Workspace/Feedback/kit_feedback.jsonl` when appropriate.

- [ ] **Step 3: Run template tests**

Run: `python .agents/scripts/tests/test_templates.py`  
Expected: PASS

- [ ] **Step 4: Commit changes**

```bash
git add .agents/skills/kit-assembling/SKILL.md .agents/templates/agent-template.md
git commit -m "feat(kit-assembling): update kit assembling to connect with central feedback hub"
```

---

### Task 5: End-to-End Validation & Decision Graph Recompilation

**Files:**
- Run: `.agents/scripts/generate_manifest.py`
- Run: `.agents/scripts/dependency_graph.py`
- Run: `.agents/scripts/validate_kit.py .agents`

**Interfaces:**
- Consumes: All updated workflows, templates, scripts, rules
- Produces: Clean validation report, synchronized `manifest.json`, `manifest.lock.json`, and `DEPENDENCY_GRAPH.md`.

- [ ] **Step 1: Run all unit test suites**

Run: `python .agents/scripts/tests/test_feedback_hub.py`  
Run: `python .agents/scripts/tests/test_templates.py`  
Run: `python .agents/scripts/tests/test_structural_anchors.py`  
Run: `python .agents/scripts/tests/test_toolkit.py`  
Expected: 100% tests PASS.

- [ ] **Step 2: Recompile manifest and dependency graph**

Run: `python .agents/scripts/generate_manifest.py`  
Run: `python .agents/scripts/dependency_graph.py`  
Expected: Updated cleanly without missing workflow references.

- [ ] **Step 3: Self-validate Toolkit**

Run: `python .agents/scripts/validate_kit.py .agents`  
Expected: `0 error(s), 0 warning(s)`.

- [ ] **Step 4: Commit final synchronization**

```bash
git add .agents/manifest.json .agents/manifest.lock.json .agents/DEPENDENCY_GRAPH.md
git commit -m "chore(registry): recompile manifest and dependency graph after feedback hub upgrade"
```
