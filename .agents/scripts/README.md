# Agent Kit Creator Scripts

## Entry points

### `validate_kit.py`
Tự kiểm định cấu trúc và liên kết của Agent Kit. Kiểm tra JSON schema, SemVer frontmatter, tham chiếu chéo workflow/agent/skill, bộ đăng ký manifest, Markdown links, cú pháp Python, v.v. Kèm cờ `--audit` để đánh giá chất lượng Audit 3 lớp.

```bash
python .agents/scripts/validate_kit.py
python .agents/scripts/validate_kit.py --json
python .agents/scripts/validate_kit.py --audit <path-to-kit>
```

### `generate_manifest.py`
Tạo bộ đăng ký `manifest.json` tự động từ frontmatter của các cấu phần.

```bash
python .agents/scripts/generate_manifest.py
python .agents/scripts/generate_manifest.py --check
```

### `dependency_graph.py`
Tự động sinh sơ đồ phụ thuộc `DEPENDENCY_GRAPH.md` từ thông tin các workflow và agent.

```bash
python .agents/scripts/dependency_graph.py
python .agents/scripts/dependency_graph.py --check
```

### `eval_runner.py`
Chạy tự động các bộ kiểm thử eval suite (`evals/*.json`) và tính điểm benchmark.

```bash
python .agents/scripts/eval_runner.py evals/eval_suite_example.json .agents
python .agents/scripts/eval_runner.py --regression
```

### `export_kit.py`
Đóng gói và xuất bản Agent Kit sang Cursor, Claude Desktop, OpenAI Custom GPTs.

```bash
python .agents/scripts/export_kit.py .agents ./dist --target all
```

### `feedback_hub.py`
Append-only event stream JSONL cho feedback thực chiến của Kit và Builder.

```bash
python .agents/scripts/feedback_hub.py --summary
```

## Exit-code contract

- `0`: kiểm tra đạt (pass)
- `1`: phát hiện lỗi (fail)

Xem thêm bảng tra cứu nhanh tại [`BUILDER_CLI.md`](BUILDER_CLI.md).
