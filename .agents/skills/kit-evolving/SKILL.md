---
name: kit-evolving
description: >
  Phân tích sai lệch (Gap Analysis), thực hiện Delta Patch khi refactor Agent Kit,
  quản lý bộ nhớ dài hạn (memory/) và vận hành Self-Evolving Quality Loop có Human Approval Gate.
  Kích hoạt khi nâng cấp kit có sẵn hoặc lưu trữ bài học kinh nghiệm.
when_to_use: "Khi cần sửa đổi, nâng cấp (refactor) Agent Kit hoặc quản lý bộ nhớ MEMORY.md."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.3.0
---

# Kit Evolving

Kỹ năng tiến hóa và nâng cấp Agent Kit theo thời gian, bảo đảm tính tương thích ngược, tích lũy tri thức dài hạn và vận hành vòng lặp tự tiến hóa có kiểm soát.

---

## 1. QUY TRÌNH REFACTOR & DELTA PATCH

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐     ┌────────────────┐
│  1. GAP ANALYSIS│ ──> │ 2. DELTA PATCH   │ ──> │ 3. SEMVER BUMP  │ ──> │ 4. RE-AUDIT    │
│  Tìm điểm nghẽn │     │ Chỉ sửa phần lỗi │     │ Nâng version    │     │ Kiểm tra lại   │
└─────────────────┘     └──────────────────┘     └─────────────────┘     └────────────────┘
```

---

## 2. QUẢN LÝ BỘ NHỚ SCOPED MEMORY

- `MEMORY.md`: Chỉ mục chính ($\le 200$ dòng).
- `shared/`: Quy ước chung và Brand voice.
- `domains/`: Tri thức chuyên biệt của từng Specialist.
- `runs/`: Lưu trữ tiến độ và Golden Runs.

---

## 3. SELF-EVOLVING QUALITY LOOP & HUMAN APPROVAL GATE

Output Kits được trang bị vòng lặp tự học có kiểm soát (Controlled Self-Improvement):

1. **Embedded Evals (`evals/eval_suite.json`)**:
   - Cho phép người dùng chạy kiểm thử hồi quy tức thì (`python scripts/eval_runner.py`).
2. **Golden Run Harvester (`memory/runs/golden-runs.json`)**:
   - Ghi nhận các quỹ đạo thực thi đạt điểm cao (DoD 100%).
3. **⛔ HUMAN / AUDITOR APPROVAL GATE (BẮT BUỘC)**:
   - **TUYỆT ĐỐI KHÔNG** tự động biến `golden-runs.json` hoặc raw feedback thành Rule/Knowledge mới.
   - Trạng thái mặc định: `"gateStatus": "pending_review"`.
   - **CHỈ KHI** có sự phê duyệt rõ ràng từ Human hoặc Auditor (`"gateStatus": "approved_golden"`, `"promotionAllowed": true`) thì tri thức mới được chưng cất và tích hợp vào `memory/domains/` hoặc `rules/`.
