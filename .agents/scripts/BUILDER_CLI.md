# Builder CLI — Quick Reference

Bảng tra cứu nhanh các script và lệnh CLI của Agent Kit Builder.

## 🚀 Common Workflows

### 1. Kiểm định Kit (Validation & Audit)
```bash
# Lint cấu trúc & schemas (L1)
python .agents/scripts/validate_kit.py

# Xuất kết quả dạng JSON
python .agents/scripts/validate_kit.py --json

# Chạy Audit 3 lớp đầy đủ kèm chấm sao
python .agents/scripts/validate_kit.py --audit <path-to-kit>
```

### 2. Quản lý Manifest & Dependency
```bash
# Tự động sinh manifest.json từ frontmatter
python .agents/scripts/generate_manifest.py

# Kiểm tra tính toàn vẹn manifest mà không ghi đè
python .agents/scripts/generate_manifest.py --check

# Sinh sơ đồ phụ thuộc DEPENDENCY_GRAPH.md
python .agents/scripts/dependency_graph.py
```

### 3. Kiểm thử Tự động (Evals)
```bash
# Chạy eval suite cụ thể
python .agents/scripts/eval_runner.py evals/eval_suite_example.json .agents

# Chạy regression benchmark cho 5 domain chuẩn
python .agents/scripts/eval_runner.py --regression
```

### 4. Đóng gói & Sao chép Kit
```bash
# Xuất bản kit sang plugin/cursor/claude
python .agents/scripts/export_kit.py .agents ./dist --target all

# Sao chép kit an toàn sang thư mục dự án đích
python .agents/scripts/copy_kit.py ./output/<kit-name> --target <target-dir>
```

### 5. Evolution Suite & Feedback
```bash
# Trang bị trọn bộ Evolution Suite cho kit
python .agents/scripts/equip_evolution.py ./output/<kit-name>

# Xem tóm tắt feedback & regression knowledge
python .agents/scripts/feedback_hub.py --summary
```

## 📋 Exit Code Contract
- `0`: Success / Passed
- `1`: Error / Validation Failed
