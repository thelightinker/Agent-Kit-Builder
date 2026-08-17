---
name: eval-running
description: "Automated behavioral eval runner harness. Use ALWAYS whenever testing, evaluating, or running quality benchmark evals on an Agent Kit, validating DoD assertions, or checking edge case failure modes against test suites."
when_to_use: "Kích hoạt khi cần chạy thử nghiệm đánh giá chất lượng hành vi (Behavioral Evals) cho Agent Kit."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# Eval Running Skill

## Overview
Cung cấp năng lực tự động hóa kiểm thử hành vi đối kháng và chấm điểm binary Definition of Done (DoD) bằng script `eval_runner.py`.

## Directives & Execution Pattern
Khi cần chạy kiểm thử hành vi hoặc tự động hóa eval suite cho Agent Kit:
1. Đảm bảo file `eval_suite.json` có sẵn trong thư mục `evals/` hoặc truyền đúng đường dẫn `--eval-file`.
2. Chạy lệnh kiểm thử qua `eval_runner.py`:

```bash
python .agents/scripts/eval_runner.py --eval-file .agents/evals/eval_suite_example.json --target-dir .agents
```

3. Xuất JSON report để tổng hợp dữ liệu kết quả:

```bash
python .agents/scripts/eval_runner.py --eval-file <path-to-eval.json> --target-dir <path-to-kit> --output-report eval_report.json
```

## Supported Assertion Types
- `regex_match`: Phải khớp với mẫu Regex (dùng cho tiêu đề, frontmatter, cấu trúc).
- `contains_keywords`: Bắt buộc phải chứa toàn bộ từ khóa trong danh sách `keywords`.
- `forbidden_keywords`: Bắt buộc KHÔNG được xuất hiện bất kỳ từ khóa cấm/placeholder nào (ví dụ: `TBD`, `TODO`, `tốt nhất`).
- `min_sections`: Đảm bảo tổng số markdown section headings (`#`) đạt hoặc vượt mức tối thiểu `count`.

## Handling Evaluation Results
- Nếu **Score = 100%**: Xác nhận Agent Kit hoàn toàn đạt chuẩn DoD hành vi.
- Nếu **Score < 100%**: Đọc danh sách `logs` bị FAIL trong report JSON, xác định file/dòng vi phạm và thực hiện patch sửa đổi trước khi re-run.
