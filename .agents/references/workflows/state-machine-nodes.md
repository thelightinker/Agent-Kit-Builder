# State Machine Nodes & Artifacts Isolation

> Đặc tả cấu trúc Node giải phẫu 5 phần và cơ chế cách ly Artifacts trong thiết kế Workflow State Machine.

---

## 1. CẤU TRÚC NODE GIẢI PHẪU 5 THÀNH PHẦN (NODE ANATOMY)

Mọi trạng thái (State Node) trong Workflow bắt buộc phải có đầy đủ 5 thành phần:

```
[STATE: <Tên_Trạng_Thái>]
[Input Artifacts]   — Danh sách khoá dữ liệu/file node được phép đọc.
[Output Artifacts]  — Danh sách khoá dữ liệu/file node sẽ ghi vào.
[DoD]               — Danh sách tiêu chí hoàn thành nhị phân (Pass 100% mới chuyển tiếp).
[Evaluation Loop]   — Vòng lặp tự kiểm tra: Pass ➔ Chuyển tiếp | Fail ➔ Revise (tối đa Max Retry) | Quá hạn ➔ ESCALATE_HUMAN.
```

---

## 2. NGUYÊN TẮC ARTIFACTS ISOLATION

- **Chống Context Bloat**: Node chỉ nạp đúng các Artifacts được liệt kê trong `[Input Artifacts]`. Không nạp toàn bộ lịch sử hay context của cả workflow "cho chắc ăn".
- **Boundary Rõ ràng**: Output của Node này là Input của Node tiếp theo. Việc truyền dữ liệu phải thông qua artifact files cụ thể, không phụ thuộc vào bộ nhớ ngầm định.

---

## 3. QUY TẮC VIẾT DoD CHO STATE NODE

Mỗi dòng Definition of Done trong Node phải vượt qua 3 bài kiểm định:

| Kiểm định | Câu hỏi kiểm tra | Ví dụ đạt | Ví dụ không đạt |
|:---|:---|:---|:---|
| **1. Tính Nhị phân** | Đạt/Không đạt rõ ràng, không cảm tính? | `"File tồn tại và không rỗng"` | `"File có chất lượng tốt"` |
| **2. Đo được từ Output** | Có thể chấm mà không cần hỏi thêm context ngoài? | `"Bảng có đủ 4 cột và >= 5 dòng"` | `"Bảng cung cấp đầy đủ dữ liệu"` |
| **3. Không dừng ở tính từ** | Tính từ đã quy ra tiêu chí định lượng? | `"0 thuật ngữ kỹ thuật, giải thích 3 use cases"` | `"Nội dung trình bày chuyên nghiệp"` |

---

## 4. EVALUATION LOOP & CẠNH NGƯỢC (INVERSE TRANSITIONS)

### Vòng lặp Đánh giá:
```
Node thực thi ➔ Kiểm tra Output theo DoD
  ├─ PASS: Chuyển tiếp sang Node kế tiếp
  ├─ FAIL (lần <= Max Retry): Tự sửa chữa (Revise) và chạy lại Node
  └─ FAIL (> Max Retry): Kích hoạt [ESCALATE_HUMAN], gắn needs_human_review: true
```

### Cạnh ngược tường minh (Inverse Transition Edges):
Nếu một Node ở bước sau phát hiện mâu thuẫn phủ định giả định của Node trước đó:
- Khai báo **cạnh ngược tường minh** trong sơ đồ workflow kèm điều kiện kích hoạt.
- Tuyệt đối không để agent âm thầm quay lại sửa mà không ghi log lý do.
