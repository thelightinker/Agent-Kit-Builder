---
name: context-compression
description: >
  Kỹ thuật quản lý và nén ngữ cảnh (Context Compression) trong các phiên làm việc dài (20+ turns).
  BẮT BUỘC kích hoạt khi nhận thấy context phình to, khi AI lặp lại kết quả hoặc khi chuyển pha làm việc
  để chống thoái hóa ngữ cảnh (Context Degradation Defense).
when_to_use: "Khi phiên làm việc vượt quá 20 lượt, khi kết quả tool dài trên 200 dòng, hoặc khi kết thúc một chặng công việc cần tóm tắt. KHÔNG dùng cho phiên hỏi đáp ngắn 1-2 lượt."
allowed-tools: Read, Write, Grep
version: 1.0.0
effort: low
---

# Context Compression — Chống Thoái Hóa Ngữ Cảnh

> Duy trì sự sắc bén và độ chính xác của AI trong các phiên làm việc dài bằng cách nén có cấu trúc các giai đoạn đã hoàn thành và lưu giữ các quyết định then chốt.

---

## 🎯 Tổng Quan & Động Lực (Why)

Trong các phiên tương tác dài (từ 20–30 lượt trở lên), LLM dễ gặp hiện tượng **thoái hóa ngữ cảnh (Context Degradation)**: bắt đầu quên các quyết định ban đầu, lặp lại các đoạn tìm kiếm thừa thãi, hoặc bị phân tâm bởi log thực thi công cụ quá dài.

Kỹ thuật **Context Compression** giúp thu hồi từ 5,000 đến 15,000 tokens bằng cách thay thế log thô bằng các bản tóm tắt ngữ nghĩa cô đọng, giữ cho Context Window luôn tập trung vào mục tiêu đang thực thi.

---

## 🚦 Dấu Hiệu Kích Hoạt Nén Ngữ Cảnh

| Dấu hiệu | Hành động tương ứng |
|:---|:---|
| Phiên làm việc $\ge 20$ lượt | Kích hoạt Session Checkpoint |
| AI bắt đầu nhắc lại các giả định đã bị loại trừ | Kích hoạt Phase Summary ngay lập tức |
| Đầu ra của công cụ (grep/list) dài $\ge 200$ dòng | Kích hoạt Micro-Compact đầu ra |
| Chuyển từ pha Khảo sát (Research) sang pha Thực thi (Implementation) | Nén toàn bộ pha Khảo sát thành 1 khối kết luận |

---

## 🗜️ 3 Cấp Độ Nén Ngữ Cảnh (Compression Levels)

### Cấp 1: Micro-Compact (Nén Đầu Ra Công Cụ)
Thay vì để nguyên 200 dòng grep log làm ô nhiễm context, nén ngay thành kết luận ngữ nghĩa 3–5 dòng:

```
❌ TRƯỚC KHI NÉN (Raw Grep ~200 dòng, ~3,500 tokens):
  src/auth/jwt.ts:15: import { verify } from 'jsonwebtoken'
  src/auth/jwt.ts:23: export function validateToken(token: string) { ... }
  ... (198 dòng lặp lại)

✅ SAU KHI NÉN (Micro-Compact ~50 tokens):
  "Grep 'jwt': Tìm thấy 8 file, 42 kết quả. Điểm cốt lõi: Logic xác thực token nằm tại
   `src/auth/jwt.ts:23-40`. Lỗi hết hạn token xảy ra tại dòng 45 do dùng toán tử `<` thay vì `<=`."
```

### Cấp 2: Phase Summary (Tóm Tắt Chặng Hoàn Thành)
Khi kết thúc một giai đoạn (ví dụ: hoàn thành nghiên cứu), thay toàn bộ chuỗi tìm kiếm bằng 1 khối tóm tắt chặng:

```markdown
## ✅ Research Phase Complete
- **Mục tiêu**: Tối ưu hóa hiệu năng tải trang Dashboard.
- **Phát hiện**: 3 API calls đang chạy tuần tự gây nghẽn mạng 450ms.
- **Quyết định**: Gom lại thành 1 Promise.all() và bật cờ cache SWR.
- **Files liên quan**: `src/api/dashboard.ts` (dòng 12-30).
```

### Cấp 3: Session Checkpoint (Điểm Neo Phiên Làm Việc)
Dành cho phiên làm việc rất dài qua nhiều tác vụ:

```markdown
## 📍 Session Checkpoint (Turn 25)

### Đã Hoàn Thành:
- [x] Khảo sát kiến trúc và phát hiện 3 điểm nghẽn hiệu năng.
- [x] Sửa lỗi so sánh hạn token tại `src/auth/jwt.ts:45`.
- [x] Chạy kiểm thử: 100% test cases pass.

### Quyết Định Đã Thống Nhất:
1. Giữ httpOnly cookie cho bảo mật token.
2. Dùng toán tử `<=` cho kiểm tra thời gian hết hạn.

### Đang Thực Hiện:
- [ ] Refactor API dashboard và tối ưu bundle.
```

---

## 📋 Quy Chuẩn Soạn Bản Nén

1. **Giữ "Why" hơn là "What"**: Lý do tại sao đưa ra một quyết định quan trọng hơn nhiều so với việc liệt kê mọi lệnh terminal đã gõ.
2. **Bảo tồn đường dẫn tệp tin**: Luôn giữ lại chính xác file path và line range trong bản tóm tắt để không phải đọc lại file.
3. **Loại bỏ ngõ cụt**: Các giả định sai hoặc các nhánh tìm kiếm không ra kết quả thì bỏ qua, không đưa vào bản nén.
