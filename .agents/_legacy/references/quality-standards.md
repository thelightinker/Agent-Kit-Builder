# Quality Standards — Tiêu chuẩn 5 sao

Rubric đánh giá Agent Kit. Quality Auditor dùng tài liệu này để chấm điểm.
Kit Generator dùng để tự kiểm tra trước khi submit.

---

## Rubric tổng quan

| Sao | Tiêu chí | Mô tả |
|:----|:---------|:------|
| ⭐ | **Structural** | Cấu trúc đầy đủ, format đúng |
| ⭐ | **Specificity** | DoD + Constraints cụ thể, đo được |
| ⭐ | **Relevance** | Mọi cơ chế phục vụ outcome thực tế |
| ⭐ | **Uniqueness** | Domain-specific, không template generic |
| ⭐ | **Usability** | User low-tech hiểu 100% |

---

## Chi tiết từng sao

### ⭐ Structural (1 sao)

**Pass khi**:
- TÓM TẮT CHO NGƯỜI DÙNG có (3-5 dòng)
- SYSTEM PROMPT có đủ 4 section lõi
- Definition of Done tồn tại, ≥ 3 tiêu chí
- HARD CONSTRAINTS ≥ 2 constraints
- FORMAT ĐẦU RA có template
- Ngôn ngữ khớp input
- Components phù hợp Tier

**Fail khi**: Thiếu bất kỳ item nào ở trên

---

### ⭐ Specificity (1 sao)

**Pass khi**:
- Mọi dòng DoD pass 3 kiểm định (nhị phân, đo được, không sáo ngữ)
- Mọi constraint cụ thể, verifiable
- Constraints không lặp Nguyên tắc vận hành

**Fail khi**:
- DoD chứa: "chuyên nghiệp", "chất lượng cao", "tối ưu", "đầy đủ", "phù hợp"
- Constraint chứa: "luôn đảm bảo", "giữ mức tốt", "cẩn thận khi"

**Ví dụ**:

| ⭐ Pass | ❌ Fail |
|:--------|:-------|
| "Output ≥ 500 từ" | "Output đầy đủ" |
| "Mọi claim có source hoặc gắn [CHƯA XÁC MINH]" | "Đảm bảo chính xác" |
| "KHÔNG bịa số liệu — dùng [CHƯA XÁC MINH]" | "Luôn trung thực" |
| "Tối đa 2 lần tự sửa" | "Không sửa quá nhiều lần" |

---

### ⭐ Relevance (1 sao)

**Pass khi**:
- Mọi cơ chế/lens trong kit → trả lời được "Agent THỰC SỰ cần cơ chế này vì [lý do cụ thể]"
- Tier phù hợp: Tier 1 không có cơ chế Tier 3
- Dynamic Enhancement Discovery đã chạy
- Không có component thừa (Skills/Memory/Workflow/Tools chỉ khi cần)

**Fail khi**:
- Có cơ chế "cho chắc" mà agent không dùng → Lens Stuffing
- Tier 1 micro-agent có context architecture hoặc I/O schema
- Component thêm vào "cho đủ" mà không phục vụ outcome
- Dynamic Enhancement Discovery bị skip

**Test**: Bỏ cơ chế X → agent có thất bại ở outcome quan trọng không?
- Nếu KHÔNG → cơ chế thừa

---

### ⭐ Uniqueness (1 sao)

**Pass khi**:
- Agent Kit chứa ≥ 1 domain-specific mechanism (đòn bẩy riêng hoặc cơ chế đặc trưng)
- Thay domain → Kit không còn hoạt động đúng
- DoD chứa tiêu chí domain-specific

**Fail khi**:
- Swap domain (e.g., "viết sách" → "nấu ăn") → Kit vẫn hoạt động y nguyên
- Không có đòn bẩy riêng hoặc cơ chế đặc trưng domain
- Kit là template generic thêm tên domain

**Test**: Thay [tên domain] bằng domain bất kỳ. Kit vẫn make sense?
- Nếu CÓ → quá generic → fail

---

### ⭐ Usability (1 sao)

**Pass khi**:
- TÓM TẮT CHO NGƯỜI DÙNG: 0 thuật ngữ kỹ thuật
- Đọc TÓM TẮT → biết: agent làm gì / khi nào dùng / giới hạn gì
- Tone kỹ thuật và tone người dùng TÁCH BIỆT
- Nếu multi-component: DANH SÁCH THÀNH PHẦN dễ hiểu

**Fail khi**:
- TÓM TẮT chứa: prompt, token, schema, API, LLM, topology, lens, tier
- Đọc TÓM TẮT xong vẫn không biết agent làm gì
- Tone trộn lẫn (kỹ thuật trong phần user, đời thường trong system prompt)

---

## Verdict Matrix

| Score | Verdict | Action |
|:------|:--------|:-------|
| 5/5 | ✅ **EXEMPLARY** | Deliver + thêm vào golden examples |
| 4/5 | ✅ **PASS** | Deliver |
| 3/5 | ⚠️ **CONDITIONAL** | Revise specific findings → re-audit |
| 2/5 | ❌ **FAIL** | Major revision → re-audit |
| 1/5 | ❌ **CRITICAL FAIL** | Re-build from scratch |

---

## Quick Self-Check (cho Kit Generator)

Trước khi submit cho Quality Auditor, Kit Generator tự hỏi:

```
□ Tôi có thể thay domain mà Kit vẫn chạy? → NẾU CÓ → chưa unique
□ DoD có từ mơ hồ nào? → NẾU CÓ → chưa specific
□ Có cơ chế nào bỏ được mà agent vẫn OK? → NẾU CÓ → lens stuffing
□ Mẹ tôi đọc TÓM TẮT có hiểu không? → NẾU KHÔNG → chưa usable
□ Có component nào thêm vì "nên có"? → NẾU CÓ → YAGNI violation
```
