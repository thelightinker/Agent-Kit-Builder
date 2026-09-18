---
name: kit-evolving
description: >
  Phân tích sai lệch (Gap Analysis), thực hiện Delta Patch khi refactor Agent Kit,
  quản lý bộ nhớ dài hạn (memory/), phát hiện quy trình lặp lại để trích xuất skill (skillify),
  tối giản hóa kiến trúc (anti-overengineering), vận hành Unified Feedback Waterfall và Self-Evolving Quality Loop.
when_to_use: "Khi cần sửa đổi, nâng cấp (refactor) Agent Kit, tối giản hóa code, trích xuất skill mới từ workflow, kiểm tra feedback/evolution waterfall hoặc quản lý bộ nhớ MEMORY.md."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.5.0
---

# Kit Evolving

Kỹ năng tiến hóa và nâng cấp Agent Kit theo thời gian, bảo đảm tính tương thích ngược, tích lũy tri thức dài hạn, trích xuất kỹ năng tự động và vận hành vòng lặp tự tiến hóa có kiểm soát.

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

## 3. AUTO-SKILLIFICATION HEURISTICS (`skillify`)

Khi quan sát thấy một chuỗi thao tác được lặp lại $\ge 3$ lần hoặc gồm $\ge 5$ bước tuần tự ổn định:
1. **Phát hiện Pattern**: Xác định trigger, các bước cố định, các biến số thay đổi và format đầu ra mong đợi.
2. **Đề xuất Trích xuất Skill**: Sử dụng chuẩn Anthropic Skill Creator để tạo thư mục `skills/<skill-name>/SKILL.md`.
3. **Tiêu chí Skill Mới**:
   - Có tính tái sử dụng cao qua nhiều phiên làm việc.
   - Frontmatter có `description` pushy và `when_to_use` rõ ràng kèm điều kiện loại trừ.
   - Thân bài `< 500 dòng` có ví dụ cụ thể Input $\rightarrow$ Output.

---

## 4. ANTI-OVERENGINEERING & SIMPLIFICATION HEURISTICS

Trong quá trình refactor hoặc review kit:
- ❌ **Loại bỏ Abstraction thừa**: Không tạo wrapper class chỉ để bọc 1 hàm; không tạo factory khi chỉ có 1 kiểu đối tượng.
- ❌ **Xóa Dead Code**: Loại bỏ import không dùng, code comment cũ, TODO lỗi thời.
- ❌ **Làm phẳng lồng nhau (Flatten Nesting)**: Sử dụng Early Returns và Guard Clauses thay vì lồng `if/else` quá 3 tầng.
- ❌ **Chống phình to Boilerplate**: Giữ prompt và workflow ở Right Altitude (Micro vs Standard vs Suite).

---

## 5. SELF-EVOLVING QUALITY LOOP & HUMAN APPROVAL GATE

Output Kits được trang bị vòng lặp tự học có kiểm soát (Controlled Self-Improvement):

1. **Embedded Evals (`evals/eval_suite.json`)**:
   - Cho phép người dùng chạy kiểm thử hồi quy tức thì (`python scripts/eval_runner.py`).
2. **Golden Run Harvester (`memory/runs/golden-runs.json`)**:
   - Ghi nhận các quỹ đạo thực thi đạt điểm cao (DoD 100%).
3. **⛔ HUMAN / AUDITOR APPROVAL GATE (BẮT BUỘC)**:
   - **TUYỆT ĐỐI KHÔNG** tự động biến `golden-runs.json` hoặc raw feedback thành Rule/Knowledge mới.
   - Trạng thái mặc định: `"gateStatus": "pending_review"`.
   - **CHỈ KHI** có sự phê duyệt rõ ràng từ Human hoặc Auditor (`"gateStatus": "approved_golden"`, `"promotionAllowed": true`) thì tri thức mới được chưng cất và tích hợp vào `memory/domains/` hoặc `rules/`.

---

## 6. UNIFIED FEEDBACK & BATCH RESOLUTION HIERARCHY (4-TIER WATERFALL)

Khi tìm kiếm feedback hoặc đánh giá tiến hóa cho bất kỳ Kit nào, **BẮT BUỘC** đi qua 4 tầng dữ liệu:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   UNIFIED FEEDBACK WATERFALL RESOLUTION                │
├────────────────────────────────────────────────────────────────────────┤
│ 1. ACTIVE BUFFER   : <kit>/.agents/evolution/feedback/feedback.jsonl   │
│    (Phản hồi sống đang tích lũy, chưa đóng gói)                        │
│                                                                        │
│ 2. ENGINE INBOX    : Agent Kit Engine/evolution/inbox/batch-<kit>-*    │
│    (Gói batch đã nộp thành công sang Engine, đang chờ xử lý)           │
│                                                                        │
│ 3. KIT OUTBOX      : <kit>/.agents/evolution/outbox/batch-<kit>-*      │
│    (Bản sao bất biến đã đóng gói tại Kit)                             │
│                                                                        │
│ 4. ENGINE PROCESSING / COMPLETED : evolution/processing/ & completed/  │
│    (Gói batch đang được biên dịch hoặc đã tiến hóa hoàn tất)           │
└────────────────────────────────────────────────────────────────────────┘
```
- **Quy tắc Vàng**: Sau khi chạy `/submit-evolution`, buffer `feedback.jsonl` được xóa rỗng để chống nộp trùng. Gói dữ liệu lúc này nằm tại **Outbox** và **Inbox**. Agent phải đọc batch từ Inbox/Outbox, tuyệt đối không kết luận kit rỗng feedback.

---

## 7. EXAMPLES (VÍ DỤ THỰC THI)

### Example 1: Refactor Delta Patch từ Audit Findings
**Input:**
```json
{
  "code": "frontmatter.required_field",
  "file": "skills/seo-optimizer/SKILL.md",
  "message": "Missing required field: when_to_use"
}
```
**Output:**
```markdown
Thực hiện Delta Patch chỉ thêm trường `when_to_use` vào YAML frontmatter của file `skills/seo-optimizer/SKILL.md`, giữ nguyên 100% nội dung thân bài và nâng patch version từ 1.0.0 lên 1.0.1.
```

### Example 2: Chưng cất Feedback thành Scoped Memory
**Input:** 5 phản hồi thực chiến về lỗi định dạng ngày tháng trong bảng báo cáo.
**Output:** Cập nhật file `memory/domains/reporting.md` với quy tắc chuẩn hóa `YYYY-MM-DD` sau khi có Human Approval.
