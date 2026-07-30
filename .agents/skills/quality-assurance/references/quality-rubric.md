# Quality Rubric — Chi tiết Tiêu chuẩn 5 Sao

Tài liệu hướng dẫn chi tiết cách đánh giá và chấm điểm từng ngôi sao cho Agent Kit.

---

## ⭐ Star 1: Structural Check (Cấu trúc Hợp lệ)

**Điều kiện Pass**:
- Đối với Micro Kit: Có đủ TÓM TẮT CHO NGƯỜI DÙNG và 4 section System Prompt cốt lõi. DoD ≥ 3 tiêu chí, Constraints ≥ 2 tiêu chí.
- Đối với Standard Kit trở lên: Có cấu trúc thư mục hợp lệ, không có file rỗng.
- Đối với Professional/Suite Kit: Có manifest.json hợp lệ, định nghĩa rõ ràng dependencies và tools.

**Ví dụ FAIL**:
- Thiếu phần Format đầu ra hoặc để trống.
- DoD chỉ có 1 hoặc 2 dòng.
- Thiếu Frontmatter trong SKILL.md.

---

## ⭐ Star 2: Specificity (Độ Cụ thể & Đo lường được)

DoD và Constraints không được mơ hồ, phải đo lường được một cách nhị phân.

| Tiêu chuẩn | Đạt (Pass) | Không đạt (Fail) |
|:---|:---|:---|
| **Binary Check** | "Kết quả trả về mã JSON `status: success`" | "Code chạy tốt và ổn định" |
| **No Buzzwords** | "Bản thảo có độ dài ≥ 500 từ" | "Bản thảo đầy đủ và chuyên nghiệp" |
| **Verifiable** | "Không sử dụng thư viện ngoài danh sách cho trước" | "Tối ưu hóa tài nguyên hệ thống" |

---

## ⭐ Star 3: Relevance (Tính Thực tiễn & Tinh gọn)

Đảm bảo nguyên tắc YAGNI và loại bỏ Lens Stuffing.

**Các bước kiểm định**:
1. Đọc từng cơ chế/lens trong prompt.
2. Đặt câu hỏi: "Nếu xóa dòng này đi, agent có làm việc kém hiệu quả hơn trong việc đạt mục tiêu chính không?"
3. Nếu "Không" -> Cơ chế thừa -> FAIL.

**Ví dụ FAIL**:
- Micro Agent (như dịch thuật) nhưng lại nạp schema phức tạp hoặc định nghĩa workflow đa bước.
- Skill rỗng hoặc tóm tắt lại những gì đã viết ở System Prompt.

---

## ⭐ Star 4: Uniqueness (Tính Đặc trưng Domain)

Kit phải được xây dựng dựa trên đặc thù của domain, không phải là template generic được đổi tên.

**Cách kiểm định (Ultimate Swap Test)**:
1. Copy System Prompt.
2. Tìm kiếm tên domain hiện tại (ví dụ: "Viết sách") và thay thế bằng một domain khác (ví dụ: "Nấu ăn").
3. Đọc lại prompt. Nếu prompt vẫn có nghĩa và hoạt động bình thường mà không cần sửa đổi lớn -> Kit quá generic -> FAIL.

**Ví dụ Pass**:
- Kit cho domain Viết sách có cơ chế kiểm tra "Độ nhất quán của giọng văn (Voice consistency)".
- Kit cho domain Phân tích tài chính có cơ chế "Đối chiếu nguồn số liệu và cảnh báo sai lệch tính toán".

---

## ⭐ Star 5: Usability (Độ dễ dùng cho Người dùng cuối)

Phần tóm tắt dành cho con người phải hoàn toàn dễ hiểu và không chứa biệt ngữ công nghệ AI.

**Ví dụ tốt (Pass)**:
> Hệ thống này giúp bạn tự động phân tích và tạo báo cáo chi tiêu hàng tháng. Bạn có thể tải lên file giao dịch ngân hàng và nhận lại biểu đồ trực quan cùng gợi ý tiết kiệm. Giới hạn: Chỉ hỗ trợ định dạng file CSV từ các ngân hàng Việt Nam.

**Ví dụ FAIL**:
> Agent sử dụng workflow 3 trạng thái kết hợp lớp memory động để parse JSON payload từ API và compile thành system prompt với token tối ưu.
