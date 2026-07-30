# Agent Kit Creator

Agent Kit Creator là bộ công cụ chuyên dụng để tư vấn, thiết kế, xây dựng, cải tiến và kiểm định chất lượng các **Agent Kit** cho các mô hình AI Agent (Gemini, Claude, Antigravity IDE, v.v.).

## Quick start

1. Đọc `.agents/rules/GEMINI.md` và `.agents/rules/quick-reference.md` để nắm các quy định và danh mục tài nguyên.
2. Định tuyến yêu cầu qua 4 Workflows chính:
   - `/create-kit`: Tạo Agent Kit mới từ đầu
   - `/refactor-kit`: Cải tiến & nâng cấp Agent Kit sẵn có
   - `/validate-kit`: Kiểm định chất lượng 3 lớp & chấm điểm Rubric 5 sao
   - `/remember-kit`: Lưu đúc rút kinh nghiệm vào bộ nhớ dài hạn MEMORY.md
3. Kiểm định Agent Kit sau khi chỉnh sửa:

```bash
python .agents/scripts/generate_manifest.py
python .agents/scripts/dependency_graph.py
python .agents/scripts/validate_kit.py
```

## Core concepts

- **Agents (5)**: Master Compiler, Domain Analyst, Kit Generator, Skill Architect, Quality Auditor.
- **Skills (17)**: Năng lực chuyên môn phân cấp theo Progressive Disclosure.
- **Workflows (4)**: Quy trình xử lý theo slash command.
- **Rules (6)**: Quy tắc toàn hệ thống và định tuyến yêu cầu.
- **Memory**: Bộ nhớ dài hạn lưu vết mẫu kit 5 sao và kinh nghiệm.
- **Registry & Lock**: Quản lý phiên bản SemVer và SHA-256 hash của toàn bộ cấu phần.

## Documentation

- [Architecture and inventory](ARCHITECTURE.md)
- [Generated dependency graph](DEPENDENCY_GRAPH.md)
- [Runtime scripts](scripts/README.md)
- [Quick reference](rules/quick-reference.md)
