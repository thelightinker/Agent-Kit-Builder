
# Agent Kit Builder Upgrades Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Làm cho repo tự chứng minh được nó đúng (verify trung thực + CI), chạy được trên máy khác, có test end-to-end thật cho kit đầu ra, giảm context nạp mỗi lượt, và hết lệch số liệu/từ vựng.

**Architecture:** Giữ nguyên topology (1 orchestrator + 5 role profile). Thêm một lớp xác minh nhỏ bằng Python stdlib quanh `validate_kit.py` hiện có: luật lint mới, một fixture kit vàng, một `verify_all.py` làm cổng duy nhất cho local và CI. Thay đổi prompt (Task 9) chỉ làm sau khi lưới an toàn của Task 1–8 đã xanh.

**Tech Stack:** Python 3.12 (stdlib cho `.agents/scripts/`), `unittest` (runner chính), `pytest` + `jsonschema` chỉ ở dev (`requirements-dev.txt`), GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-10-14-agent-kit-builder-upgrades-design.md` (nội dung = `agent-kit-builder-upgrade-spec.md`, commit vào đường dẫn này trước khi bắt đầu). Executor đọc cả spec lẫn mục "Spec corrections" bên dưới.

## Spec corrections (phát hiện khi đọc code để lập plan)

| #  | Spec nói                                                       | Thực tế                                                                                                                                                                                                                                                                                                             | Hệ quả cho plan                                                                        |
| :- | :-------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------- |
| C1 | Nâng cấp 3: "thêm luật `routing.empty_capabilities`"      | Luật **đã có** (`validate_kit.py:732`). Creator thoát luật nhờ `routing_exempt: true` ở `kit-architect.md`                                                                                                                                                                                        | Task 6 chỉ thêm test chứng minh luật bắn, không thêm luật                        |
| C2 | A2: 8 module test lỗi do `feedback_collector`                | Chỉ 4 module do `feedback_collector`; các module còn lại lỗi do thiếu dev dependency (`pytest`, `jsonschema`), repo không có `requirements*`                                                                                                                                                          | Task 8 thêm `requirements-dev.txt`                                                    |
| C3 | A5: test ghi đè file                                          | Nguyên nhân: `validate(root)` mặc định `auto_heal=True` ghi lockfile; `test_sync_registry` gọi `sync_registry(TOOLKIT)` trên repo thật                                                                                                                                                                | Task 1 chạy test trên bản sao                                                         |
| C4 | A13: nhóm evolution "ít người gọi"                         | Nặng hơn: `evolution_engine.py` crash khi chạy (`import feedback_collector`), và `equip_evolution.py:256-257` gọi `shutil.copy2` cho 2 file không tồn tại (`feedback_collector.py`, `evolution_submitter.py`). `create-kit` Bước 4 gọi script này (đọc code; chưa chạy trên kit thật) | Task 6 đưa nhóm này sang `EXPERIMENTAL`, không còn là bước mặc định        |
| C5 | A1: 3 script `skill-creator` "fail `--help`"                | Do validator chạy sai thư mục (`from scripts.utils import ...` cần cwd là thư mục skill)                                                                                                                                                                                                                     | Task 5 sửa cwd của smoke test, không sửa script                                      |
| C6 | Nâng cấp 4: giảm ~45–55%                                    | Với cắt thực tế (Task 9) ngân sách là 8,192 B (rule) + 10,240 B (orchestrator) = 18,432 B so với 28,515 B hiện tại, tức **giảm ~35%**                                                                                                                                                               | Con số mục tiêu được hạ; ngân sách là hằng số duy nhất, chỉnh ở một chỗ |
| C7 | Nâng cấp 4 mục 4: `ui-ux-pro-max` thành module tùy chọn | 3.8 MB là file dữ liệu không nạp vào context; chỉ `SKILL.md` (6 KB) được nạp theo mô tả                                                                                                                                                                                                                | Bỏ khỏi plan (không có lợi ích đo được)                                        |
| C8 | Nâng cấp 5: không còn "Tier 1/2/3" ngoài bảng ánh xạ    | Viết lại toàn bộ là phạm vi lớn                                                                                                                                                                                                                                                                                | Dùng test "ratchet": allowlist chỉ được co lại                                     |

## Global Constraints

- Mọi script trong `.agents/scripts/` chỉ dùng Python stdlib (core-guardrails điều 5: "Zero third-party dependency leak nếu tuyên bố stdlib"). `pytest` và `jsonschema` chỉ nằm ở `requirements-dev.txt`.
- Chỉ ghi vào `.agents/` khi sửa repo; mọi test phải chạy trên bản sao tạm, không ghi vào `.agents/` thật.
- Code và comment viết tiếng Anh; tài liệu người dùng viết tiếng Việt (core-guardrails "Output").
- Mọi đường dẫn nội bộ là đường dẫn tương đối (`feedback-history.md` 2026-09-06: "Never hardcode user-specific absolute paths").
- Mã thoát: `0` = pass, `1` = fail, `2` = thiếu điều kiện chạy (dev dependency).
- Ngân sách context: `RULES_BUDGET_BYTES = 8192`, `ORCHESTRATOR_BUDGET_BYTES = 10240` (Task 9).
- Version của toolkit lấy từ `.agents/VERSION` (CalVer `YYYY.M.D`); component dùng SemVer.
- File văn bản sinh ra dùng UTF-8 và LF.
- Chạy lệnh từ thư mục gốc repo. Chạy test: `python -m unittest discover -s .agents/scripts/tests -p "<file>.py" -v`.
- Mỗi task kết thúc bằng một commit; commit message theo `type(scope): ...` như lịch sử repo.

## Review Focus

Các tình huống spec ngụ ý nhưng test của spec chưa phủ; mỗi dòng đã có test ở task chủ.

1. **Đường dẫn Windows trong JSON/Python, không chỉ Markdown** (người dùng gốc ở Windows): linter phải bắt cả `.json`/`.py`, và không báo nhầm URL như `https://x.com/home/a/b` → Task 3.
2. **`verify_all.py` chạy từ thư mục bất kỳ** (không chỉ từ gốc repo) → Task 8.
3. **Thiếu `pytest`/`jsonschema`** phải ra thông báo hành động được và mã thoát `2`, không phải traceback → Task 8.
4. **Windows CRLF và console cp1252**: file sinh ra phải LF, chạy lại không đổi (idempotent), và script in tiếng Việt không crash → Task 10 (CRLF) và Task 8 (CI chạy cả `windows-latest`).
5. **Cắt rule làm rơi âm thầm một bất biến P0** → Task 9 (test đếm 10 bất biến).

---

## File Structure

| File                                                              | Trách nhiệm                                                                                                                                   |
| :---------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| `.agents/scripts/tests/support.py` (mới)                       | `copy_toolkit()`, hằng `REPO_ROOT`, `TOOLKIT`: mọi test dùng chung để không ghi vào repo thật                                     |
| `.agents/scripts/validate_kit.py` (sửa)                        | Thêm luật: `path.absolute_user_path`, `dependency.undeclared`, `context.budget_exceeded`, `docs.generated_stale`; sửa cwd smoke test |
| `.agents/scripts/preflight.py` (mới)                           | Kiểm tra điều kiện tiên quyết của `/create-kit`                                                                                        |
| `.agents/scripts/context_budget.py` (mới)                      | Đo byte của nội dung always-on                                                                                                               |
| `.agents/scripts/render_docs.py` (mới)                         | Sinh khối số liệu/version trong README, ARCHITECTURE từ manifest/VERSION                                                                    |
| `.agents/scripts/verify_all.py` (mới)                          | Cổng duy nhất: preflight → validate → test → benchmark → kiểm cây sạch                                                                 |
| `.agents/scripts/benchmark_behavior.py` (sửa)                  | Verdict tính từ kết quả; mã thoát đúng                                                                                                  |
| `.agents/DEPENDENCIES.md` (mới)                                | Danh mục phụ thuộc ngoài, bắt buộc/tùy chọn, phương án dự phòng                                                                    |
| `.agents/scripts/tests/fixtures/golden-kit/` (mới)             | Kit mẫu nhỏ, hợp lệ                                                                                                                         |
| `.agents/evals/golden_kit_suite.json` (mới)                    | Eval cấu trúc theo schema thật của `eval_runner.py`                                                                                       |
| `.agents/references/role-profiles.md` (mới)                    | Chi tiết 5 role profile (chuyển từ orchestrator)                                                                                             |
| `requirements-dev.txt`, `.github/workflows/verify.yml` (mới) | Dev deps và CI                                                                                                                                 |

---

### Task 1: Test không ghi vào repo thật

**Files:**

- Create: `.agents/scripts/tests/support.py`
- Modify: `.agents/scripts/tests/test_toolkit.py` (hằng `TOOLKIT`; dòng gọi `validate_kit.validate(TOOLKIT)` ~34 và `validate_kit.sync_registry(TOOLKIT)` ~117) và mọi module test mà bước 3 liệt kê
- Test: `.agents/scripts/tests/test_working_tree_clean.py`

**Interfaces:**

- Produces: `support.REPO_ROOT: Path`, `support.TOOLKIT: Path` (= `REPO_ROOT/".agents"`), `support.copy_toolkit(dest: Path) -> Path` (sao chép `.agents` vào `dest/.agents`, bỏ qua `__pycache__`, `*.pyc`, `skills/ui-ux-pro-max/data`; trả về `dest/.agents`).

- [ ] **Step 1: Write the failing test** (`test_working_tree_clean.py`)

```python
class TestToolkitTestsDoNotMutateRepo(unittest.TestCase):
    TRACKED = ("manifest.lock.json", "ARCHITECTURE.md", "execution_policy.json")

    def test_validate_and_sync_on_copy_leave_real_toolkit_untouched(self):
        before = {n: (TOOLKIT / n).read_bytes() for n in self.TRACKED}
        with tempfile.TemporaryDirectory() as tmp:
            kit = copy_toolkit(Path(tmp))
            validate_kit.validate(kit)          # auto_heal=True writes into the copy only
            validate_kit.sync_registry(kit)
        self.assertEqual(before, {n: (TOOLKIT / n).read_bytes() for n in self.TRACKED})

    def test_test_toolkit_never_passes_real_toolkit_to_mutating_calls(self):
        src = (TESTS_DIR / "test_toolkit.py").read_text("utf-8")
        for call in ("validate_kit.validate(TOOLKIT)", "validate_kit.sync_registry(TOOLKIT)"):
            self.assertNotIn(call, src)
```

- [ ] **Step 2: Run to verify it fails**

Run: `python -m unittest discover -s .agents/scripts/tests -p "test_working_tree_clean.py" -v`
Expected: `ImportError` (support chưa có), sau khi tạo `support.py` thì test thứ hai FAIL.

- [ ] **Step 3: Implement `copy_toolkit` in `support.py`** (dùng `shutil.copytree(..., ignore=shutil.ignore_patterns(...))`), rồi trong `test_toolkit.py` thay hai lời gọi bằng bản sao tạo ở `setUpClass`.
- [ ] **Step 4: Tìm mọi module test còn ghi vào repo thật.**

Run: `for f in .agents/scripts/tests/test_*.py; do python -m unittest discover -s .agents/scripts/tests -p "$(basename $f)" >/dev/null 2>&1; git status --short -- .agents | sed "s|^|$(basename $f): |"; git checkout -q -- .agents; done`
Expected: danh sách module làm bẩn cây (ghi vào commit message). Với mỗi module trong danh sách, thay đường dẫn `TOOLKIT` bằng `copy_toolkit(...)`; lặp lại lệnh cho đến khi không còn dòng nào.

- [ ] **Step 5: Run** `python -m unittest discover -s .agents/scripts/tests -p "test_working_tree_clean.py" -v`. Expected: PASS.
- [ ] **Step 6: Commit** `git add .agents/scripts/tests && git commit -m "test: run toolkit tests against a temp copy, never the real .agents"`

---

### Task 2: Benchmark nói thật

**Files:**

- Modify: `.agents/scripts/benchmark_behavior.py` (`benchmark_convergence` ~197, `run_benchmark` ~294, khối verdict ~339-347, `__main__`)
- Test: `.agents/scripts/tests/test_benchmark_verdict.py`

**Interfaces:**

- Produces: `benchmark_convergence() -> list[tuple[str, bool]]` (nhãn, đạt/không); `_verdict_lines(routing_ok: bool, jit_min_pct: float, jit_max_pct: float, dag: dict, compat: dict, convergence: list[tuple[str, bool]]) -> list[tuple[bool, str]]`; `run_benchmark() -> int` (0 nếu mọi dòng đạt, ngược lại 1). `__main__` gọi `raise SystemExit(run_benchmark())`.

- [ ] **Step 1: Write the failing tests**

```python
def test_verdict_line_fails_when_any_convergence_case_fails(self):
    lines = _verdict_lines(True, 82.4, 88.6, DAG_OK, COMPAT_OK,
                           [("Healthy Kit Baseline", False), ("Chaos 1", True)])
    ok, text = lines[-1]
    self.assertFalse(ok)
    self.assertIn("1/2", text)

def test_run_benchmark_returns_1_when_convergence_fails(self):
    with mock.patch.object(benchmark_behavior, "benchmark_convergence",
                           return_value=[("x", False)]), contextlib.redirect_stdout(io.StringIO()) as out:
        self.assertEqual(1, benchmark_behavior.run_benchmark())
    self.assertNotIn("✓ Convergence", out.getvalue())

def test_jit_range_is_not_a_literal(self):
    self.assertNotIn("82.4% - 88.6%", (SCRIPTS_DIR / "benchmark_behavior.py").read_text("utf-8"))
```

- [ ] **Step 2: Run** `python -m unittest discover -s .agents/scripts/tests -p "test_benchmark_verdict.py" -v`. Expected: FAIL (`_verdict_lines` chưa có).
- [ ] **Step 3: Implement.** Mỗi chỗ `benchmark_convergence` in `[✓]`/`[✗]` thì đồng thời append `(label, ok)` rồi trả list. Trong vòng lặp JIT của `run_benchmark`, thu `saving_pct` để tính `min`/`max`. Dòng cuối của mỗi nhóm trong verdict in `✓` hoặc `✗` theo `ok`, với phân số `passed/total` thật.
- [ ] **Step 4: Run** lại file test. Expected: PASS. Chạy `python .agents/scripts/benchmark_behavior.py; echo $?`. Expected tạm thời: in `✗` cho convergence và mã `1` (sẽ xanh sau Task 5–8).
- [ ] **Step 5: Commit** `git commit -am "fix(benchmark): derive verdict and exit code from measured results"`

---

### Task 3: Linter đường dẫn tuyệt đối và dọn 6 file

**Files:**

- Modify: `.agents/scripts/validate_kit.py` (thêm hàm + gọi trong `validate` và `validate_quick`; thêm khóa vào `FIX_STRATEGY_MAP`)
- Modify (dọn đường dẫn): `.agents/agent/kit-architect.md`, `.agents/workflows/create-kit.md`, `.agents/workflows/refactor-kit.md`, `.agents/skills/skill-architecting/SKILL.md:18`, `.agents/skills/kit-verifying/SKILL.md:19`, `.agents/memory/golden-examples/README.md:7-10`
- Test: `.agents/scripts/tests/test_portability_lint.py`

**Interfaces:**

- Produces: `ABSOLUTE_USER_PATH: re.Pattern`; `validate_portability(root: Path, findings: list[Finding]) -> None` phát `Finding(severity="error", code="path.absolute_user_path")`. Quét `*.md`, `*.json`, `*.py`, `*.mjs` dưới `root`, bỏ qua `scripts/tests/` và `skills/ui-ux-pro-max/`. `FIX_STRATEGY_MAP["path.absolute_user_path"] = ("llm_patch", True)`.

- [ ] **Step 1: Write the failing tests**

```python
CASES_BAD = [
    ("a.md",   r"[x](file:///C:/Users/nhdcb/x.md)"),
    ("b.json", r'{"p": "C:\\Users\\bob\\x"}'),
    ("c.py",   'P = "/Users/alice/proj/x"'),
    ("d.md",   "see /home/carol/work/x"),
    ("e.md",   "file:///c:/Users/nhdcb/OneDrive/Desktop/x.md"),
]
def test_flags_absolute_user_paths_in_md_json_py(self):
    for name, text in CASES_BAD:
        with self.subTest(name):
            findings = self._scan(name, text)
            self.assertIn("path.absolute_user_path", [f.code for f in findings])

def test_does_not_flag_urls_or_relative_paths(self):
    for text in ("https://example.com/home/x/y", "[a](../skill-creator/SKILL.md)", ".agents/skills/x"):
        with self.subTest(text):
            self.assertEqual([], self._scan("ok.md", text))

def test_real_toolkit_has_no_absolute_user_paths(self):
    findings = []
    validate_kit.validate_portability(TOOLKIT, findings)
    self.assertEqual([], findings)
```

- [ ] **Step 2: Run** file test. Expected: FAIL (hàm chưa có).
- [ ] **Step 3: Implement `validate_portability`.** Regex gợi ý: `(?i)(?:[a-z]:[\\/]{1,2}(?:users|documents and settings)[\\/]|file:///[a-z]:/|(?<![\w.:/-])/(?:Users|home)/[^/\s]+/)`. Với mã JSON, so khớp trên văn bản thô nên `C:\\Users` (đã escape) cũng bị bắt.
- [ ] **Step 4: Run** file test. Expected: 2 test đầu PASS, `test_real_toolkit...` FAIL và liệt kê đúng 6 file.
- [ ] **Step 5: Dọn 6 file.** Trong `skills/*/SKILL.md` dùng link tương đối `../skill-creator/SKILL.md`; trong `agent/` và `workflows/` dùng đường dẫn văn bản `.agents/skills/skill-creator/SKILL.md`; trong `golden-examples/README.md` dùng tên file tương đối cùng thư mục.
- [ ] **Step 6: Run** file test. Expected: PASS. Run `python .agents/scripts/validate_kit.py .agents --no-auto-heal | grep -c "missing_link\|absolute_user_path"`. Expected: `0`.
- [ ] **Step 7: Commit** `git commit -am "feat(validator): lint absolute user paths; remove hardcoded paths"`

---

### Task 4: Dependency contract và preflight

**Files:**

- Create: `.agents/DEPENDENCIES.md`, `.agents/scripts/preflight.py`
- Modify: `.agents/scripts/validate_kit.py` (`validate_dependencies`, gọi trong `validate`), `.agents/workflows/create-kit.md` (thêm "Bước -1: Preflight" trước "BƯỚC 0" và câu dự phòng trong Bước 0)
- Test: `.agents/scripts/tests/test_dependency_contract.py`

**Interfaces:**

- Produces: `preflight.REQUIRED_FILES: tuple[str, ...]` (đường dẫn tương đối tới `.agents/`: `skills/skill-creator/SKILL.md` và 8 template ở `templates/`: `workflow-template.md`, `orchestrator-template.md`, `agent-template.md`, `skill-template.md`, `rule-template.md`, `memory-template.md`, `manifest-template.json`, `design-spec-template.md`); `check_preflight(root: Path) -> list[str]` (danh sách file thiếu; rỗng = ổn); CLI `python .agents/scripts/preflight.py [path]` thoát `1` nếu thiếu. `validate_dependencies(root: Path, findings: list[Finding]) -> None` phát `dependency.undeclared` (error, `("llm_patch", True)`) cho mỗi token khớp `superpowers:[a-z-]+|agy-customizations|ponytail` có trong repo nhưng không có trong `DEPENDENCIES.md`.
- `DEPENDENCIES.md` là bảng Markdown, mỗi hàng: tên | `required`/`optional` | dùng ở đâu | phương án dự phòng. Các hàng khởi tạo: `superpowers:brainstorming` (optional; dự phòng: hỏi tối đa 3 câu về mục tiêu, tier, core verbs rồi chờ `APPROVED`), `superpowers:writing-plans` và `superpowers:executing-plans` (optional; dự phòng: lập kế hoạch ngắn trong chat), `agy-customizations` (optional), `ponytail` (optional), `context7 MCP` (optional; cần điền khóa API trong `mcp_config.json`).

- [ ] **Step 1: Write the failing tests**

```python
def test_preflight_reports_missing_skill_creator(self):
    kit = self._temp_kit_without("skills/skill-creator/SKILL.md")
    self.assertEqual(["skills/skill-creator/SKILL.md"], preflight.check_preflight(kit))

def test_undeclared_external_dependency_is_an_error(self):
    kit = self._temp_kit_with_text("workflows/x.md", "use superpowers:made-up-skill")
    findings = []
    validate_kit.validate_dependencies(kit, findings)
    self.assertEqual(["dependency.undeclared"], [f.code for f in findings])

def test_every_external_token_in_real_toolkit_is_declared(self):
    findings = []
    validate_kit.validate_dependencies(TOOLKIT, findings)
    self.assertEqual([], findings)

def test_create_kit_runs_preflight_before_step_zero(self):
    text = (TOOLKIT / "workflows/create-kit.md").read_text("utf-8")
    self.assertLess(text.index("preflight.py"), text.index("BƯỚC 0"))
    self.assertIn("dự phòng", text.lower())
```

- [ ] **Step 2: Run** file test. Expected: FAIL.
- [ ] **Step 3: Implement** `preflight.py` (stdlib, `argparse`, thoát `1` nếu thiếu), `validate_dependencies`, `DEPENDENCIES.md`, và sửa `create-kit.md`.
- [ ] **Step 4: Run** file test. Expected: PASS. Run `python .agents/scripts/preflight.py .agents; echo $?`. Expected: `0`.
- [ ] **Step 5: Commit** `git commit -am "feat(deps): declare external dependencies, add preflight and fallback"`

---

### Task 5: Validator xanh trên chính repo

**Files:**

- Modify: `.agents/scripts/validate_kit.py` (smoke test trong `validate_python`, ~475-490), `.agents/skills/skill-creator/SKILL.md` (frontmatter)
- Regenerate: `.agents/manifest.lock.json`, `.agents/manifest.json`, `.agents/DEPENDENCY_GRAPH.md`, `.agents/ARCHITECTURE.md` (qua `--sync`)
- Test: `.agents/scripts/tests/test_smoke_cwd.py`

**Interfaces:**

- Produces: `_smoke_cwd(script: Path) -> Path` trong `validate_kit.py`: trả về thư mục tổ tiên gần nhất chứa `SKILL.md`; nếu không có thì `script.parent`. Smoke test chạy `python <script> --help` với `cwd=_smoke_cwd(script)`.

- [ ] **Step 1: Write the failing test**

```python
def test_script_importing_sibling_package_passes_smoke_when_run_from_skill_dir(self):
    kit = make_kit(tmp)  # reuse _make_kit/_write_skill pattern from test_routing_validation
    skill = kit / "skills/demo"
    (skill / "scripts").mkdir(parents=True)
    (skill / "scripts/__init__.py").write_text("")
    (skill / "scripts/utils.py").write_text("def f():\n    return 1\n")
    (skill / "scripts/run.py").write_text(
        "import argparse\nfrom scripts.utils import f\n"
        "if __name__ == '__main__':\n    argparse.ArgumentParser().parse_args()\n")
    findings = []
    validate_kit.validate_python(kit, findings)
    self.assertNotIn("script.smoke_failed", [f.code for f in findings])
```

- [ ] **Step 2: Run** file test. Expected: FAIL (`script.smoke_failed`).
- [ ] **Step 3: Implement `_smoke_cwd`** và dùng nó trong `subprocess.run(..., cwd=...)` của smoke test.
- [ ] **Step 4: Thêm vào frontmatter của `skills/skill-creator/SKILL.md`** ba trường còn thiếu: `when_to_use`, `allowed-tools`, `version: 1.0.0` (giữ nguyên `name` và `description`; ghi lý do trong commit: bản vendored, không đổi nội dung).
- [ ] **Step 5: Đồng bộ số đếm và lockfile có chủ đích:** `python .agents/scripts/validate_kit.py .agents --sync`.
- [ ] **Step 6: Run** `python .agents/scripts/validate_kit.py .agents --no-auto-heal`. Expected: `Summary: 0 error(s)` và `[PASS]`.
- [ ] **Step 7: Run** file test. Expected: PASS.
- [ ] **Step 8: Commit** `git add -A .agents && git commit -m "fix(validator): smoke-run vendored scripts from their skill dir; complete skill-creator frontmatter; sync registry"`

---

### Task 6: Golden kit E2E và cách ly nhóm evolution

**Files:**

- Create: `.agents/scripts/tests/fixtures/golden-kit/` gồm 1 agent `golden-writer` (capability `golden.outline.draft`, `negative_scope.cannot_modify: [approved_outline]`), 1 skill `outline-drafting`, 1 workflow `draft-outline`, rules và memory đủ để validator hài lòng
- Modify: `.agents/workflows/create-kit.md` (Bước 4: mục "Dynamic Evolution Suite" và lệnh `equip_evolution.py`)
- Test: `.agents/scripts/tests/test_golden_kit_e2e.py`

**Interfaces:**

- Consumes: `support.copy_fixture(name: str, dest: Path) -> Path` (thêm vào `support.py` ở task này, tương tự `copy_toolkit`); `compile_routing_index(root) -> dict` (khóa `capabilities`, `intent_map`), `compile_invariants(root) -> dict` (`global_invariants`, `negative_boundaries`), `compile_state_schema(root) -> dict` (`state_keys`, `verdict_keys`), `compile_task_classifier(root) -> dict` (`ad_hoc_intents`, `workflow_bound_intents`), `compile_evidence_schemas(root) -> dict` (`schemas`), `validate_kit.validate(root, auto_heal=False)`, `export_kit.export_kit(kit_dir, output_dir, target="all", sync_dir=None)`.
- Quy trình dựng fixture: viết theo `templates/agent-template.md`, `templates/skill-template.md`, `templates/workflow-template.md` và `references/capability-declaration-guide.md`; lặp `python .agents/scripts/validate_kit.py <fixture> --no-auto-heal` cho đến khi `0 error(s)`.

- [ ] **Step 1: Write the failing tests**

```python
def test_fixture_validates_clean(self):
    errs = [f for f in validate_kit.validate(self.kit, auto_heal=False) if f.severity == "error"]
    self.assertEqual([], errs)

def test_compilers_emit_non_empty_artifacts(self):
    self.assertIn("golden.outline.draft", compile_routing_index(self.kit)["capabilities"])
    self.assertTrue(compile_routing_index(self.kit)["intent_map"])
    self.assertTrue(compile_state_schema(self.kit)["state_keys"])
    self.assertTrue(compile_evidence_schemas(self.kit)["schemas"])
    self.assertTrue(compile_task_classifier(self.kit)["workflow_bound_intents"])
    self.assertEqual(["approved_outline"],
        compile_invariants(self.kit)["negative_boundaries"]["golden-writer"]["cannot_modify"])

def test_removing_capabilities_triggers_routing_empty_capabilities(self):
    agent = self.kit / "agent/golden-writer.md"
    agent.write_text(re.sub(r"(?s)capabilities:.*?\n(?=\w[\w-]*:|---)", "", agent.read_text("utf-8")), "utf-8")
    codes = [f.code for f in validate_kit.validate(self.kit, auto_heal=False)]
    self.assertIn("routing.empty_capabilities", codes)

def test_export_writes_cursor_rules(self):
    out = self.tmp / "dist"
    export_kit.export_kit(self.kit, out, target="all")
    self.assertTrue(any(out.rglob(".cursorrules")))

def test_create_kit_marks_equip_evolution_experimental(self):
    for line in (TOOLKIT / "workflows/create-kit.md").read_text("utf-8").splitlines():
        if "equip_evolution.py" in line:
            self.assertIn("EXPERIMENTAL", line)
```

- [ ] **Step 2: Run** file test. Expected: FAIL (fixture chưa có; riêng test cuối FAIL vì `create-kit.md` gọi `equip_evolution.py` như bước mặc định).
- [ ] **Step 3: Tạo fixture** theo mục Interfaces cho đến khi `test_fixture_validates_clean` PASS.
- [ ] **Step 4: Run** file test. Expected: 4 test đầu PASS. Nếu `test_compilers_emit_non_empty_artifacts` FAIL vì một compiler thật sự trả rỗng trên fixture hợp lệ, đó là lỗi của compiler: sửa compiler, không sửa test (ghi vào commit).
- [ ] **Step 5: Sửa `create-kit.md` Bước 4:** bỏ `equip_evolution.py` và "Dynamic Evolution Suite" khỏi Output Artifacts và DoD mặc định; thêm một dòng "`[EXPERIMENTAL]` (chỉ khi người dùng yêu cầu `--with-evolution`): `python .agents/scripts/equip_evolution.py <target-dir>`". Ghi quyết định vào `memory/tech-decisions.md`: "Nhóm evolution (`evolution_*`, `equip_evolution`, `snapshot_manager`) ở trạng thái experimental vì phụ thuộc `feedback_collector`/`evolution_submitter` đã bị xóa; chủ repo quyết định phục hồi hoặc xóa."
- [ ] **Step 6: Run** file test. Expected: PASS (5/5).
- [ ] **Step 7: Commit** `git add -A .agents && git commit -m "test(e2e): golden kit fixture; quarantine evolution suite from default create-kit"`

---

### Task 7: Eval cấu trúc theo schema thật

**Files:**

- Create: `.agents/evals/golden_kit_suite.json`
- Move: `.agents/evals/evals.json` → `.agents/evals/legacy/evals-v3-prompts.json`
- Modify: `.agents/scripts/eval_runner.py` (mỗi result mang thêm `failure_mode`; docstring đổi "Behavioral" thành "Structural"), `README.md`, `.agents/README.md` (từ "Behavioral Eval" → "Structural Eval")
- Test: `.agents/scripts/tests/test_eval_suites.py`

**Interfaces:**

- Consumes: `eval_runner.run_eval_suite(eval_file_path, target_dir=".") -> dict` (khóa `total`, `passed`, `failed`, `score_pct`, `results`), schema suite: `{"suite_name", "test_cases": [{"id","name","target_file","failure_mode","assertions":[{"type","description",...}]}]}`, 4 loại assertion `regex_match`, `contains_keywords`, `forbidden_keywords`, `min_sections`.
- Produces: mỗi phần tử `results[i]` có thêm khóa `"failure_mode": str`.

- [ ] **Step 1: Write the failing tests**

```python
def test_every_active_suite_is_runnable_by_eval_runner(self):
    for path in (TOOLKIT / "evals").glob("*.json"):
        with self.subTest(path.name):
            self.assertIn("test_cases", json.loads(path.read_text("utf-8")))

def test_golden_suite_passes_and_tags_failure_modes(self):
    report = eval_runner.run_eval_suite(str(TOOLKIT / "evals/golden_kit_suite.json"), str(FIXTURE))
    self.assertEqual(report["total"], report["passed"])
    self.assertGreaterEqual(report["total"], 5)
    self.assertTrue(all(r["failure_mode"] for r in report["results"]))

def test_docs_do_not_claim_behavioral_evals(self):
    for p in ("README.md", ".agents/README.md", ".agents/scripts/eval_runner.py"):
        self.assertNotIn("Behavioral Eval", (REPO_ROOT / p).read_text("utf-8"))
```

- [ ] **Step 2: Run** file test. Expected: FAIL.
- [ ] **Step 3: Viết `golden_kit_suite.json`** (5–8 ca, mỗi ca một `failure_mode` lấy từ `references/failure-modes.md`, ví dụ `Phantom Routing (F5)`: agent có khối `capabilities`; `Vague DoD`: `forbidden_keywords` ["chuyên nghiệp","chất lượng cao"] trên DoD; `Skill Amnesia (F2)`: có `Skill Invocation Matrix`; `Provider Lock-in`: `forbidden_keywords` ["GEMINI.md"]). Chuyển `evals.json` sang `legacy/` và sửa `eval_runner.py`.
- [ ] **Step 4: Run** file test và `python .agents/scripts/eval_runner.py --eval-file .agents/evals/golden_kit_suite.json --target-dir .agents/scripts/tests/fixtures/golden-kit`. Expected: PASS và `Score: 100.0%`.
- [ ] **Step 5: Commit** `git add -A . && git commit -m "feat(evals): runnable structural eval suite tagged by failure mode; archive legacy v3 prompts"`

---

### Task 8: `verify_all.py`, dev deps, quarantine, CI

**Files:**

- Create: `.agents/scripts/verify_all.py`, `.agents/scripts/tests/EXPERIMENTAL.txt`, `requirements-dev.txt`, `.github/workflows/verify.yml`
- Modify: `README.md` (thay badge tĩnh bằng badge workflow)
- Test: `.agents/scripts/tests/test_verify_all.py`

**Interfaces:**

- Produces: `StepResult` (dataclass: `name: str`, `returncode: int`, `seconds: float`); `run_step(name: str, argv: list[str], cwd: Path) -> StepResult`; `missing_dev_dependencies() -> list[str]` (kiểm `pytest`, `jsonschema` bằng `importlib.util.find_spec`); `main(argv: list[str] | None = None) -> int` với cờ `--only {preflight,validate,tests,benchmark,tree}` (lặp được). Thứ tự mặc định: preflight → validate (`--no-auto-heal`) → tests → benchmark → tree. Bước `tree` so sánh `git status --porcelain -- .agents` trước/sau, bỏ qua nếu không có git. Dòng cuối luôn là `VERIFY: PASS` hoặc `VERIFY: FAIL`.
- `EXPERIMENTAL.txt`: mỗi dòng một tên module, khởi tạo với `test_closed_loop_evolution`, `test_e2e_evolution_lifecycle`, `test_evolution_engine`, `test_evolution_orchestrator`. Bước `tests` dựng suite bằng `unittest.TestLoader().discover(...)` rồi bỏ các module này.

- [ ] **Step 1: Write the failing tests**

```python
def test_missing_dev_dependency_exits_2_with_actionable_message(self):
    with mock.patch.object(verify_all, "missing_dev_dependencies", return_value=["pytest"]), \
         contextlib.redirect_stderr(io.StringIO()) as err:
        self.assertEqual(2, verify_all.main([]))
    self.assertIn("requirements-dev.txt", err.getvalue())

def test_runs_from_any_working_directory(self):
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run([sys.executable, str(SCRIPTS_DIR / "verify_all.py"), "--only", "preflight"],
                           cwd=tmp, capture_output=True, text=True)
    self.assertEqual(0, r.returncode, r.stderr)

def test_any_failed_step_makes_verdict_fail(self):
    results = [StepResult("a", 0, 0.1), StepResult("b", 1, 0.1)]
    self.assertEqual(1, verify_all.exit_code(results))

def test_readme_has_no_static_status_badges(self):
    text = (REPO_ROOT / "README.md").read_text("utf-8")
    for needle in ("Toolkit_Validation", "Unit_Tests-"):
        self.assertNotIn(needle, text)
```

(Thêm `exit_code(results: list[StepResult]) -> int` vào Interfaces: `0` nếu mọi `returncode == 0`, ngược lại `1`.)

- [ ] **Step 2: Run** file test. Expected: FAIL.
- [ ] **Step 3: Implement** `verify_all.py` (đường dẫn tính từ `Path(__file__)`, không từ cwd; stdout `reconfigure(encoding="utf-8")` như các script khác), `requirements-dev.txt` (`pytest>=8`, `jsonschema>=4`), `EXPERIMENTAL.txt`.
- [ ] **Step 4: Cài dev deps và chạy toàn bộ:** `python -m pip install -r requirements-dev.txt && python .agents/scripts/verify_all.py`. Expected lần đầu: một số test còn FAIL.
- [ ] **Step 5: Triage test còn lỗi.** Với từng test fail còn lại (danh sách ban đầu: `test_scale_invariants.test_adding_30_components_requires_zero_core_modifications`, `test_templates.test_workflow_template_structure`, `test_toolkit.test_chaos_fatal_syntax_trap_escalates`, `test_chaos_multi_fault_recovery`, `test_converge_on_healthy_kit`, `test_validate_quick`, `test_compile_execution_policy.test_strict_jsonschema_conformance`; nhiều test trong số này dự kiến tự xanh sau Task 3–6): chạy `-v`, phân loại **thiếu dev dep / kỳ vọng cũ / lỗi thật**, sửa nguyên nhân gốc (kỳ vọng cũ thì cập nhật test kèm lý do trong commit; lỗi thật thì sửa code). Không dùng `skip` để làm xanh. Đây là bước có độ bất định cao nhất của plan.
- [ ] **Step 6: Tạo `.github/workflows/verify.yml`:** trigger `push` và `pull_request`; ma trận `os: [ubuntu-latest, windows-latest]`, Python `3.12`; các bước checkout, `setup-python`, `pip install -r requirements-dev.txt`, `python .agents/scripts/verify_all.py`. Trong `README.md` thay hai badge tĩnh bằng `![verify](https://github.com/thelightinker/Agent-Kit-Builder/actions/workflows/verify.yml/badge.svg)`.
- [ ] **Step 7: Run** `python .agents/scripts/verify_all.py; echo $?`. Expected: dòng cuối `VERIFY: PASS`, mã `0`.
- [ ] **Step 8: Commit** `git add -A . && git commit -m "feat(verify): single verify gate, dev deps, CI on Linux and Windows"`

---

### Task 9: Context diet có ngân sách

**Files:**

- Create: `.agents/scripts/context_budget.py`, `.agents/references/role-profiles.md`
- Modify: `.agents/scripts/validate_kit.py` (`validate_context_budget`), `.agents/scripts/benchmark_behavior.py` (in dòng baseline always-on), `.agents/rules/collaboration-protocol.md` (frontmatter `trigger`), `.agents/agent/kit-architect.md` (mục `## 2. DYNAMIC ROLE PROFILES`)
- Test: `.agents/scripts/tests/test_context_budget.py`

**Interfaces:**

- Produces: `RULES_BUDGET_BYTES = 8192`, `ORCHESTRATOR_BUDGET_BYTES = 10240`; `measure(root: Path) -> dict` với khóa `rules_bytes: int` (tổng byte các rule có `trigger: always_on`), `orchestrator_bytes: int` (byte file agent có `routing_exempt: true`; nếu kit không có thì `0`), `files: list[str]`; `validate_context_budget(root: Path, findings: list[Finding]) -> None` phát `context.budget_exceeded` (error, `("llm_patch", True)`); `P0_INVARIANTS: tuple[str, ...]` (10 cụm: `Workspace Isolation`, `Topology & Node-Contract Reconciliation`, `Verification Feasibility`, `Sequential Context Isolation`, `Legacy Intake & Tri-Bucket Scope`, `Executable Script Smoke Test`, `Targeted Grounding`, `Worker Briefing`, `Verification Abstraction`, `Universal Filesystem & Workspace Contract`).

- [ ] **Step 1: Write the failing tests**

```python
def test_always_on_rules_within_budget(self):
    self.assertLessEqual(measure(TOOLKIT)["rules_bytes"], RULES_BUDGET_BYTES)

def test_orchestrator_within_budget(self):
    self.assertLessEqual(measure(TOOLKIT)["orchestrator_bytes"], ORCHESTRATOR_BUDGET_BYTES)

def test_budget_violation_is_reported_by_validator(self):
    kit = copy_fixture("golden-kit", self.tmp)
    (kit / "rules/big.md").write_text(
        "---\nname: big\nversion: 1.0.0\npriority: P1\ntrigger: always_on\ndescription: \"x\"\n---\n" + "x" * 9000, "utf-8")
    findings = []
    validate_kit.validate_context_budget(kit, findings)
    self.assertEqual(["context.budget_exceeded"], [f.code for f in findings])

def test_no_p0_invariant_is_dropped_or_duplicated_across_always_on_files(self):
    files = [TOOLKIT / f for f in measure(TOOLKIT)["files"]]
    texts = {f.name: f.read_text("utf-8") for f in files}
    for phrase in P0_INVARIANTS:
        holders = [n for n, t in texts.items() if phrase in t]
        with self.subTest(phrase):
            self.assertGreaterEqual(len(holders), 1)
```

(`context_budget.measure`: nếu đọc được `trigger` thì dùng parser frontmatter sẵn có của `validate_kit` qua import, không viết parser mới.)

- [ ] **Step 2: Run** file test. Expected: FAIL (budget: 15,462 B > 8,192 B; orchestrator 13,053 B > 10,240 B).
- [ ] **Step 3: Chụp đường cơ sở hành vi trước khi cắt:** `python -m unittest discover -s .agents/scripts/tests -p "test_golden_kit_e2e.py"` và `eval_runner` trên fixture. Expected: PASS (lưới an toàn của Task 6–7).
- [ ] **Step 4: Cắt bước 1:** đổi `collaboration-protocol.md` thành `trigger: model_decision` (đã có `description`; validator yêu cầu field này). Run `python -m unittest ... -p "test_context_budget.py" -k rules`. Expected: test rule PASS (3,852 + 3,486 = 7,338 B).
- [ ] **Step 5: Cắt bước 2:** chuyển nguyên văn mục `## 2. DYNAMIC ROLE PROFILES` (~4,161 B) của `kit-architect.md` sang `references/role-profiles.md` (không đổi nội dung); thay bằng bảng 5 dòng (profile, kích hoạt khi, `Đọc references/role-profiles.md#<profile>`). Run `python .agents/scripts/validate_kit.py .agents --sync`. Expected: orchestrator ≤ 10,240 B.
- [ ] **Step 6: Gọi `validate_context_budget` trong `validate`; thêm vào `benchmark_behavior.run_benchmark` dòng `Always-on baseline: N bytes`.**
- [ ] **Step 7: Run** `python .agents/scripts/verify_all.py`. Expected: `VERIFY: PASS`, và E2E + eval fixture không đổi so với Step 3.
- [ ] **Step 8: Commit** `git add -A . && git commit -m "perf(context): enforce always-on byte budget; demote collaboration-protocol; move role profiles to references"`

---

### Task 10: Một nguồn sự thật cho số liệu, version, mode, từ vựng

**Files:**

- Create: `.agents/scripts/render_docs.py`, `.agents/scripts/tests/legacy_vocab_allowlist.txt`
- Modify: `README.md`, `.agents/ARCHITECTURE.md` (thêm marker sinh tự động), `.agents/agent/kit-architect.md` (mục 3 "INPUT PIPELINE": bỏ danh sách 5 mode, trỏ sang `rules/dynamic-routing.md`), `.agents/references/workflow-topologies.md` (thêm bảng ánh xạ), `.agents/references/failure-modes.md` (tiêu đề), `.agents/scripts/validate_kit.py` (`docs.generated_stale`)
- Test: `.agents/scripts/tests/test_single_source.py`

**Interfaces:**

- Produces: marker `<!-- GENERATED:inventory -->…<!-- /GENERATED:inventory -->` và `<!-- GENERATED:version -->…<!-- /GENERATED:version -->`; `render_inventory(root: Path) -> str` (bảng Markdown giữ đúng định dạng `| **Total Skills** | 11 |` mà `validate_architecture_counts` đang đọc); `apply_generated_blocks(root: Path, check: bool = False) -> list[str]` (trả về tên file đã đổi, hoặc sẽ đổi nếu `check=True`; ghi UTF-8, LF). Bảng ánh xạ: `Tier 1 → Micro`, `Tier 2 → Standard`, `Tier 3 và SUITE_BUILD → Mini-Suite (2 agent) hoặc Full Suite (≥3 agent)`.

- [ ] **Step 1: Write the failing tests**

```python
def test_generation_is_idempotent_and_lf_only(self):
    kit = copy_toolkit(self.tmp)
    (kit.parent / "README.md").write_bytes((REPO_ROOT / "README.md").read_bytes().replace(b"\n", b"\r\n"))
    render_docs.apply_generated_blocks(kit)
    self.assertEqual([], render_docs.apply_generated_blocks(kit))
    self.assertNotIn(b"\r\n", (kit / "ARCHITECTURE.md").read_bytes())

def test_one_version_value_in_readme_and_architecture(self):
    version = (TOOLKIT / "VERSION").read_text("utf-8").strip()
    for p in (REPO_ROOT / "README.md", TOOLKIT / "ARCHITECTURE.md"):
        self.assertEqual({version}, set(re.findall(r"2026\.\d+\.\d+", p.read_text("utf-8"))), p.name)

def test_orchestrator_modes_are_a_subset_of_dynamic_routing_and_there_are_ten(self):
    routing = set(re.findall(r"`([A-Z_]+_TRACK)`", (TOOLKIT / "rules/dynamic-routing.md").read_text("utf-8")))
    orch = set(re.findall(r"`([A-Z_]+_TRACK)`", (TOOLKIT / "agent/kit-architect.md").read_text("utf-8")))
    self.assertEqual(10, len(routing))
    self.assertLessEqual(orch, routing)

def test_legacy_vocab_only_in_allowlisted_files_and_allowlist_has_no_stale_entries(self):
    allow = set((TESTS_DIR / "legacy_vocab_allowlist.txt").read_text("utf-8").split())
    pattern = re.compile(r"\bTier [123]\b|SUITE_BUILD")
    holders = {p.relative_to(TOOLKIT).as_posix() for p in TOOLKIT.rglob("*.md") if pattern.search(p.read_text("utf-8"))}
    self.assertEqual(set(), holders - allow)
    self.assertEqual(set(), allow - holders)

def test_failure_modes_title_has_no_stale_version(self):
    self.assertNotIn("v3.0", (TOOLKIT / "references/failure-modes.md").read_text("utf-8").splitlines()[0])
```

- [ ] **Step 2: Run** file test. Expected: FAIL.
- [ ] **Step 3: Implement `render_docs.py`**, thêm marker vào README (khối cây thư mục `# CalVer (…)`, badge version, dòng License) và ARCHITECTURE (bảng Metric, dòng tiêu đề version), rồi chạy `python .agents/scripts/render_docs.py`.
- [ ] **Step 4: Sửa orchestrator mục 3** (bỏ danh sách 5 mode, trỏ sang `rules/dynamic-routing.md`; chuyển cách nói "Tier 1/2/3" ở mục này sang Micro/Standard/Full Suite), thêm bảng ánh xạ vào `workflow-topologies.md`, sửa tiêu đề `failure-modes.md`.
- [ ] **Step 5: Tạo allowlist** bằng đúng lệnh `grep -rlE "Tier [123]|SUITE_BUILD" .agents --include=*.md | sed 's|^\.agents/||' | sort > .agents/scripts/tests/legacy_vocab_allowlist.txt` (sau Step 4). Các lần sau chỉ được xóa dòng khỏi file này, không thêm.
- [ ] **Step 6: Thêm `validate_kit.docs.generated_stale`** gọi `apply_generated_blocks(root, check=True)`; phát lỗi nếu danh sách không rỗng. Thêm `render_docs.py --check` vào bước `validate` của `verify_all.py`.
- [ ] **Step 7: Run** `python .agents/scripts/verify_all.py`. Expected: `VERIFY: PASS`.
- [ ] **Step 8: Commit** `git add -A . && git commit -m "feat(docs): generate counts/version from manifest; single mode table; legacy vocab ratchet"`

---

## Self-Review

**1. Spec coverage**

| Spec                                                                            | Task                                                                                                                                      |
| :------------------------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------- |
| N1 Truth Gate (verify, benchmark, test không ghi, CI, quyết định evolution) | 1, 2, 5, 6 (quyết định evolution), 8                                                                                                   |
| N2 Portability (path, linter, DEPENDENCIES, preflight, `YOUR_API_KEY`)        | 3, 4 (`context7` ghi là optional trong `DEPENDENCIES.md`; không đổi `mcp_config.json`, vì spec cho phép "ghi rõ tùy chọn") |
| N3 Golden Kit + eval thật                                                      | 6, 7 (luật `routing.empty_capabilities` đã có, xem C1)                                                                              |
| N4 Context Diet                                                                 | 9 (hạ mục tiêu theo C6; bỏ `ui-ux-pro-max` theo C7)                                                                                 |
| N5 SSOT                                                                         | 10 (ratchet thay vì xóa sạch từ vựng cũ, C8)                                                                                        |

Không có yêu cầu nào của spec thiếu task, ngoại trừ các điều chỉnh đã nêu trong "Spec corrections".

**2. Step scan:** các bước "Triage" (Task 8 Step 5) và "dựng fixture" (Task 6 Step 3) có kết quả cuối kiểm được bằng lệnh (`VERIFY: PASS`, `0 error(s)`) nhưng nội dung sửa phụ thuộc phát hiện lúc chạy; đã đánh dấu là điểm bất định.

**3. Type consistency:** `copy_toolkit` (Task 1) và `copy_fixture` (Task 6) cùng nằm trong `support.py`; `StepResult`/`exit_code` (Task 8) khớp giữa Interfaces và test; `measure`/`validate_context_budget` (Task 9) dùng đúng khóa đã khai báo.

**4. Review Focus:** 5 dòng đều có test ở task chủ (Task 3, 8, 8, 10, 9).

**5. Proportion:** plan chỉ chứa chữ ký, tên test và assertion; thân hàm không có trừ regex gợi ý ở Task 3.
