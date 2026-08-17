# Outcome Lens Library — Chi tiết

Builder dùng tài liệu này để **tự vấn** khi quyết định cơ chế nào đưa vào Agent Kit.
Đây KHÔNG phải checklist — không cần tick đủ 6. Một lens chỉ vào kit nếu nó phục vụ
outcome thực tế của agent đó.

---

## Lens A — Token Efficiency

**Outcome**: Tạo & vận hành Agent Kit với chi phí token thấp nhất mà không giảm
chất lượng output.

**Tại sao quan trọng**: Token = tiền + latency + giảm attention budget. Mọi token
thừa trong System Prompt cạnh tranh attention với phần thực sự cần thiết.

### Ví dụ cơ chế (không bắt buộc đúng tên)

| Cơ chế | Mô tả | Khi nào dùng |
|:-------|:------|:-------------|
| Slot-based assembly | System Prompt có slot, chỉ nạp module cần thiết cho task hiện tại | Agent có nhiều chế độ, mỗi chế độ cần context khác nhau |
| Delta-only edit | Khi REFACTOR: chỉ patch phần thiếu, không viết lại toàn bộ | Mọi REFACTOR mode |
| Budget theo complexity | Agent nhận định độ phức tạp → chọn mức chi tiết tương ứng | Agent xử lý cả task đơn giản lẫn phức tạp |

### Anti-patterns

- Nhồi toàn bộ context "cho chắc" → giảm attention, tăng cost
- System Prompt 5000+ từ cho agent chỉ làm 1 việc
- Lặp lại cùng instruction ở nhiều chỗ trong prompt

### Luôn áp dụng ở mức tối thiểu

Mọi agent đều hưởng lợi từ A — nhưng mức độ áp dụng khác nhau:
- **Tier 1**: Viết ngắn gọn là đủ — không cần cơ chế phức tạp
- **Tier 2–3**: Cần cơ chế tường minh (slot, tiering, JIT load)

---

## Lens B — Adaptive Flexibility

**Outcome**: Agent không vỡ khi gặp input lạ hoặc phức tạp hơn dự kiến.

**Tại sao quan trọng**: User thực tế không bao giờ dùng đúng format agent expect.
Agent cứng nhắc → thất bại ngay input hơi lệch → user mất tin tưởng.

### Ví dụ cơ chế

| Cơ chế | Mô tả | Khi nào dùng |
|:-------|:------|:-------------|
| State-switch | Agent chuyển hành vi theo trạng thái/context detected | Agent phục vụ nhiều loại request |
| Complexity tiering | Phân biệt input đơn giản/trung bình/phức tạp → xử lý tương ứng | Agent nhận input biến đổi rộng |
| Graceful degradation | Khi thiếu data, vẫn cho output hữu ích + cảnh báo | Agent phụ thuộc external data |

### Anti-patterns

- Chỉ xử lý "happy path" → vỡ với edge case
- Over-engineer flexibility cho agent chỉ làm 1 việc cố định
- Quá nhiều state → agent tự loạn

### Khi nào KHÔNG cần

- **Tier 1 micro-agent**: input format cố định, 1 tác vụ → B thường không cần
- Agent chỉ chạy trong pipeline controlled → input đã được normalize

---

## Lens C — Reliable Performance

**Outcome**: Output đúng ngay lần đầu, không hallucinate, không bịa dữ liệu.

**Tại sao quan trọng**: Sai 1 lần = user không dùng lại. Đặc biệt nguy hiểm
với agent xử lý dữ liệu chuyên môn (pháp lý, y tế, tài chính).

### Ví dụ cơ chế

| Cơ chế | Mô tả | Khi nào dùng |
|:-------|:------|:-------------|
| QC gate | Tự kiểm tra output theo tiêu chí trước khi trả | Mọi agent có output quan trọng |
| Definition of Done rõ ràng | Checklist nhị phân — pass/fail, không phụ thuộc cảm tính | Mọi agent |
| Eval seed | Ví dụ input/output chuẩn trong prompt để anchor quality | Agent cần output format chính xác |
| Self-verification | Agent tự đối chiếu output với constraint trước khi deliver | Agent xử lý dữ liệu nhạy cảm |

### Anti-patterns

- DoD bằng tính từ: "chuyên nghiệp", "chất lượng cao" → không đo được
- Không có mechanism kiểm tra → phụ thuộc hoàn toàn vào LLM "biết đúng"
- Over-verify → latency quá cao cho task đơn giản

### Luôn áp dụng

Mọi agent đều cần C — nhưng mức độ:
- **Tier 1**: DoD rõ ràng + output format chuẩn là đủ
- **Tier 2–3**: Thêm QC gate, eval seed, self-verification khi cần

---

## Lens D — Lean Context

**Outcome**: Chỉ nạp đúng context cần, đúng lúc cần — không nhồi "cho chắc".

**Tại sao quan trọng**: Context dài ≠ context tốt. Attention mechanism có budget
hữu hạn — nhồi thêm context thường *giảm* performance thay vì tăng.

### Ví dụ cơ chế

| Cơ chế | Mô tả | Khi nào dùng |
|:-------|:------|:-------------|
| Phân lớp Core/Module/Reference | Chia context thành lớp, chỉ load lớp cần | Agent xử lý nhiều domain/context |
| JIT load | Chỉ nạp reference khi task thực sự cần | Agent có nhiều tài liệu tham khảo |
| Context pruning | Bỏ context cũ khi không còn relevant | Agent chạy session dài |

### Anti-patterns

- Load toàn bộ knowledge base mỗi lần chạy
- System Prompt chứa reference material thay vì link tới nó
- Không phân biệt hot/warm/cold context

### Khi nào KHÔNG cần

- **Tier 1**: context nhỏ, không dynamic → D overkill
- Agent chỉ xử lý 1 loại input cố định → không cần phân lớp

---

## Lens E — Interoperability

**Outcome**: Agent ghép được với agent/hệ thống khác khi cần.

**Tại sao quan trọng**: Agent đơn lẻ hiếm khi đủ cho workflow phức tạp.
Nếu không có giao thức giao tiếp → không thể mở rộng.

### Ví dụ cơ chế

| Cơ chế | Mô tả | Khi nào dùng |
|:-------|:------|:-------------|
| I/O schema | Định nghĩa rõ input/output format | Agent nằm trong pipeline |
| Handoff protocol | Quy ước ai gửi gì cho ai, format nào | SUITE_BUILD (bắt buộc) |
| Status contract | Agent báo trạng thái (done/failed/blocked) theo format chuẩn | Agent trong hệ đa agent |

### Anti-patterns

- Agent nhận bất kỳ format → output bất kỳ format → không ghép được
- Handoff bằng ngôn ngữ tự nhiên không chuẩn hoá → ambiguous
- Quá nhiều protocol cho agent standalone

### Khi nào KHÔNG cần

- **Tier 1** standalone: không trong pipeline → E không cần
- Agent dùng 1 mình, không bao giờ ghép → bỏ E

### Khi nào BẮT BUỘC

- **SUITE_BUILD**: từ 2 agent trở lên cần giao tiếp → E bắt buộc

---

## Lens F — Safety & Escalation

**Outcome**: Agent không đoán bừa khi thiếu dữ liệu, không lặp vô hạn,
biết dừng và hỏi người khi cần.

**Tại sao quan trọng**: Agent tự tin sai nguy hiểm hơn agent thú nhận không biết.
Vòng lặp vô hạn = burn tokens + không có output.

### Ví dụ cơ chế

| Cơ chế | Mô tả | Khi nào dùng |
|:-------|:------|:-------------|
| Ngưỡng tin cậy | Khi confidence thấp → flag + ask human | Agent xử lý dữ liệu nhạy cảm |
| Giới hạn vòng tự sửa | Max N lần retry trước khi dừng | Agent có iteration loop |
| Điểm dừng hỏi người | Định nghĩa rõ khi nào PHẢI escalate | Mọi agent |
| Hard boundaries | Liệt kê explicit những gì KHÔNG BAO GIỜ làm | Mọi agent |

### Anti-patterns

- Không có exit path → agent cố mãi
- Quá thận trọng → hỏi user mọi thứ → user mệt
- Safety theatre: có cơ chế nhưng không thực sự enforce

### Luôn áp dụng ở mức tối thiểu

Mọi agent đều cần phần tối thiểu của F:
- **Tier 1**: Hard constraints (KHÔNG làm gì) + escalation đơn giản ("nếu không chắc → nói rõ")
- **Tier 2–3**: Thêm ngưỡng, giới hạn retry, giao thức escalation chi tiết

---

## Nguyên tắc chéo giữa các Lens

| Xung đột tiềm tàng | Cách giải quyết |
|:---------------------|:----------------|
| A (Token Efficiency) vs D (Lean Context) | Cả hai cùng hướng — nhưng D tốn token để implement phân lớp. Tier 1 → dùng A (viết ngắn) thay vì D (phân lớp) |
| B (Adaptive) vs A (Token) | Flexibility cần thêm logic = thêm token. Chỉ thêm B khi agent thực sự gặp input đa dạng |
| C (Reliable) vs A (Token) | Self-verification tốn token. Cân nhắc: cost of error vs cost of verification |
| E (Interop) vs A (Token) | I/O schema thêm boilerplate. Chỉ dùng E khi agent thực sự trong pipeline |

---

## Dynamic Enhancement Discovery

**Bước này BẮT BUỘC, kể cả Tier 1.**

Trước khi generate, Builder phải trả lời 3 câu hỏi:

1. **Outcome quan trọng nhất** của agent này là gì? Nó có nằm ngoài 6 lens không?
   → Nếu có → tạo đòn bẩy riêng (tên tự do, không gượng ép vào 6 lens)

2. **Điểm thất vọng phổ biến nhất** nếu người dùng thực tế dùng agent này là gì?
   → Đó là đòn bẩy 80/20 cần ưu tiên xử lý

3. **Tối đa 2–3 đòn bẩy** thật sự đáng làm cho agent này:
   - Không cố nặn ra đủ 6 nếu agent không cần
   - Không dừng lại ở đúng những gì có sẵn nếu agent cần thứ khác
