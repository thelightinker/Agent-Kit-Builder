# Agent Kit Creator — Memory Index

Bộ nhớ dài hạn (persistent memory) của Agent Kit Creator. Được đọc ở đầu mỗi phiên làm việc để nạp các khuôn mẫu thiết kế, bài học kinh nghiệm và các ví dụ chất lượng cao.

---

## Danh mục bộ nhớ

### 1. Khuôn mẫu thiết kế (Design Patterns)
*   **File**: `memory/kit-patterns.md`
*   **Mục đích**: Lưu trữ các kỹ thuật, pattern thiết kế được rút ra từ thực tế và các bộ kit chất lượng cao (như demo kit).

### 2. Ví dụ mẫu chất lượng cao (Golden Examples)
*   **File**: `memory/golden-examples/README.md`
*   **Mục đích**: Lưu giữ danh sách các ví dụ Agent Kit đạt chuẩn 5 sao để tham khảo làm mốc chất lượng (eval seed).
*   **Các ví dụ hiện có**:
    *   `memory/golden-examples/writing-book-agent-v3.md` (Evolved Full Suite — Decoupled Goldilocks Workflows + 5 Craft Doctrines + Zero Voice Mutation + World Cup Winner 🏆)
    *   `memory/golden-examples/writing-book-agent-v2.md` (Full Suite — 6 Specialists + SVG Engine + 6 Workflows)
    *   `memory/golden-examples/book-writing-kit.md` (Standard Kit)
    *   `memory/golden-examples/micro-agent-example.md` (Micro Kit)
    *   `memory/golden-examples/short-video-builder-kit.md` (Pipeline Kit — Idea→MP4)

---

## Hướng dẫn cập nhật bộ nhớ
1.  **Khi hoàn thành 1 Agent Kit xuất sắc (đạt 5/5 ⭐)**:
    *   Lưu trữ kit đó vào thư mục `memory/golden-examples/`.
    *   Cập nhật thông tin mô tả vào `memory/golden-examples/README.md`.
2.  **Khi đúc rút được bài học mới về thiết kế prompt/skill**:
    *   Ghi nhận trực tiếp bài học và cách khắc phục vào `memory/kit-patterns.md`.
