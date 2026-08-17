---
name: kit-evolving
description: >
  Phân tích sai lệch (Gap Analysis), thực hiện Delta Patch khi refactor Agent Kit,
  và quản lý bộ nhớ dài hạn (memory/) cho design patterns và golden examples.
  Kích hoạt khi nâng cấp kit có sẵn hoặc lưu trữ bài học kinh nghiệm.
when_to_use: "Khi cần sửa đổi, nâng cấp (refactor) Agent Kit hoặc quản lý bộ nhớ MEMORY.md."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.0.0
---

# Kit Evolving

Kỹ năng tiến hóa và nâng cấp Agent Kit theo thời gian, bảo đảm tính tương thích ngược và tích lũy tri thức dài hạn.

---

## 1. QUY TRÌNH REFACTOR & DELTA PATCH

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐     ┌────────────────┐
│  1. GAP ANALYSIS│ ──> │ 2. DELTA PATCH   │ ──> │ 3. SEMVER BUMP  │ ──> │ 4. RE-AUDIT    │
│  Tìm điểm nghẽn │     │ Chỉ sửa phần lỗi │     │ Nâng version    │     │ Kiểm tra lại   │
└─────────────────┘     └──────────────────┘     └─────────────────┘     └────────────────┘
```

### Nguyên tắc Delta Patch:
- **Không đập đi xây lại**: Chỉ sửa đúng phần cần thay đổi, bảo vệ các logic đang hoạt động ổn định.
- **Tương thích ngược (Backward Compatibility)**: Đảm bảo các component không sửa đổi vẫn hoạt động bình thường.
- **Phiên bản SemVer**:
  - `PATCH` (1.0.0 $\rightarrow$ 1.0.1): Sửa câu chữ prompt, sửa lỗi cú pháp.
  - `MINOR` (1.0.0 $\rightarrow$ 1.1.0): Thêm skill mới, bổ sung tính năng không phá vỡ cấu trúc cũ.
  - `MAJOR` (1.0.0 $\rightarrow$ 2.0.0): Thay đổi hoàn toàn kiến trúc hoặc I/O schema.

---

## 2. QUẢN LÝ BỘ NHỚ DÀI HẠN (MEMORY MANAGEMENT)

Cấu trúc bộ nhớ lưu trữ tại `memory/`:

```
memory/
├── MEMORY.md                 # Chỉ mục chính (Index file, <= 200 dòng)
├── project-conventions.md    # Quy ước của dự án
├── user-preferences.md       # Sở thích và thói quen của người dùng
├── tech-decisions.md         # Các quyết định kiến trúc đã thống nhất
├── feedback-history.md       # Lịch sử phản hồi và bài học kinh nghiệm
├── kit-patterns.md           # Các mẫu thiết kế thành công
└── golden-examples/          # Các Agent Kit mẫu đạt 5 sao
```

### Quy tắc cập nhật Memory:
1. `MEMORY.md` là file chỉ mục nạp đầu tiên, không bao giờ vượt quá 200 dòng.
2. Khi có bài học mới hoặc kit mẫu đạt 5 sao:
   - Tạo file chi tiết tại `memory/golden-examples/<kit-name>.md` hoặc bổ sung vào `memory/kit-patterns.md`.
   - Cập nhật 1 dòng tóm tắt và liên kết tương đối trong `MEMORY.md`.
