# Agent Kit Creator Scripts

## Entry points

### `validate_kit.py`

Tự kiểm định cấu trúc và liên kết của Agent Kit. Kiểm tra JSON schema, SemVer frontmatter, tham chiếu chéo workflow/agent/skill, bộ đăng ký manifest/lock, Markdown links, cú pháp Python, v.v.

```bash
python .agents/scripts/validate_kit.py
python .agents/scripts/validate_kit.py --json
```

### `generate_manifest.py`

Tạo bộ đăng ký `manifest.json` và `manifest.lock.json` tự động từ frontmatter của các cấu phần.

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

### `audit_kit.py`

Đánh giá chất lượng Agent Kit theo quy trình Audit 3 lớp và thang điểm Rubric 5 sao.

```bash
python .agents/scripts/audit_kit.py
```

## Exit-code contract

- `0`: kiểm tra đạt (pass)
- `1`: phát hiện lỗi (fail)
