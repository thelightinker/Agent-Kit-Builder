---
name: architecture-mapping
description: "Phương pháp luận Khảo sát & Định vị Bản đồ Kiến trúc Sống (Living Architecture Mapping & Blast Radius Assessment) cho Agent Kit. Kích hoạt khi cần đọc hiểu kiến trúc hệ thống trước khi refactor/nâng cấp, định vị chính xác layer bị tác động và đồng bộ lại bản đồ sau thay đổi."
version: 1.0.0
when_to_use: "Kích hoạt khi cần khảo sát kiến trúc hệ thống, phân tích phạm vi ảnh hưởng (Blast Radius) và đồng bộ hóa Bản đồ Kiến trúc Sống map.md."
allowed-tools: [Read, Grep, Glob]
---

# Architecture Mapping & Blast Radius Assessment (Phương Pháp Luận Bản Đồ Kiến Trúc Sống)

Kỹ thuật khảo sát, phân tích phạm vi ảnh hưởng (Blast Radius) và đồng bộ hóa Bản đồ Kiến trúc Sống (`map.md`) của KitBuilder nhằm bảo vệ tính toàn vẹn hệ thống trước và sau mọi quyết định nâng cấp.

---

## 🧭 1. Nguyên Tắc Cốt Lõi: Map Is Methodology, Not Knowledge Dump

1. **Map-First Law**: Bắt buộc đọc `map.md` trước khi chạm vào bất kỳ file code, prompt hay workflow nào.
2. **Deterministic Layering**: Mọi thay đổi phải được gán chính xác vào 1 trong 7 tầng quyền lực (Author $\rightarrow$ Constitution $\rightarrow$ Craft $\rightarrow$ Writer $\rightarrow$ Sensor $\rightarrow$ Editor $\rightarrow$ Release).
3. **Blast Radius Minimization**: Giới hạn phạm vi tác động ở mức tối thiểu cần thiết; không để thay đổi ở tầng dưới làm lung lay tầng trên.
4. **Post-Change Map Synchronization**: Mọi sự thay đổi về component, contract hoặc tool đều phải được cập nhật lại vào `map.md` như một điều kiện nghiệm thu bắt buộc (DoD).

---

## 🔍 2. Quy Trình 4 Bước Khảo Sát & Cập Nhật

```
[BƯỚC 1: READ MAP] ────────▶ Đọc map.md để nạp ngữ cảnh kiến trúc và các Invariants bất biến.
        │
        ▼
[BƯỚC 2: LOCATE LAYER] ────▶ Định vị chính xác tầng & component mục tiêu cần sửa đổi.
        │
        ▼
[BƯỚC 3: ASSESS RADIUS] ───▶ Đánh giá ma trận phụ thuộc: Component này liên kết với đâu?
        │
        ▼
[BƯỚC 4: SYNC MAP] ────────▶ Cập nhật lại map.md sau khi kiểm thử 100% PASS.
```

### Chi Tiết Từng Bước:
1. **Read Map**: Đọc phần `Authority Hierarchy`, `Topology Map` và `Invariants` trong `map.md`.
2. **Locate Layer**:
   - Thay đổi triết lý/luật $\rightarrow$ Tầng *Governance / Constitution*.
   - Thay đổi ngòi bút/kỹ thuật viết $\rightarrow$ Tầng *Craft Intelligence*.
   - Thay đổi định dạng/regex $\rightarrow$ Tầng *Signal Sensor*.
   - Thay đổi tiêu chí chấm điểm $\rightarrow$ Tầng *Diagnosis / Editor*.
   - Thay đổi xuất bản/file $\rightarrow$ Tầng *Release Pipeline*.
3. **Assess Blast Radius**:
   - Trực tiếp: Những component nào phụ thuộc trực tiếp vào component này?
   - Gián tiếp: Có làm thay đổi `CHAPTER_CONTRACT.json`, `manifest.json` hay các bài test hiện có không?
4. **Sync Map**: Ghi lại phiên bản mới, cấu phần mới và cập nhật sơ đồ liên kết trong `map.md`.

---

## 🚫 3. Bảng Phân Định Ranh Giới (Trigger Discrimination)

```markdown
### ✅ CẦN KÍCH HOẠT (Should Trigger):
- "Trước khi sửa clutter_checker, hãy đọc map.md và đánh giá xem có ảnh hưởng tới workflow không."
- "Tôi vừa thêm 1 script mới, hãy hướng dẫn tôi cập nhật lại map.md."
- "Phân tích blast radius nếu chúng ta đổi schema của CHAPTER_CONTRACT.json."

### ❌ KHÔNG KÍCH HOẠT (Should Not Trigger):
- "Viết tiếp bản thảo Chương 2 cho cuốn sách." ➔ Đây là tác vụ sản xuất nội dung, KHÔNG kích hoạt mapping.
- "Chạy script kiểm tra sáo ngữ cho file draft.md." ➔ Sử dụng `prose-cadence-mastery` / `clutter_checker.py`.
- "Tạo mới một Agent Kit từ đầu." ➔ Sử dụng workflow `/create-kit` và skill `kit-assembling`.
```
