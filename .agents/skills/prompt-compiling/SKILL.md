---
name: prompt-compiling
description: >
  Biên dịch System Prompt chuẩn 4 khối (Vai trò, Quy trình, Hard Constraints, Format),
  thiết lập Binary Definition of Done (DoD), Hard Constraints dạng phủ định,
  và tối ưu hóa cho multi-target LLM (Claude XML, OpenAI Markdown, Gemini Structured).
  Luôn kích hoạt khi sinh mới hoặc refactor System Prompt.
when_to_use: "Khi cần biên dịch, tối ưu hoặc chuẩn hóa System Prompt cho bất kỳ Agent nào."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.0.0
---

# Prompt Compiling

Kỹ năng biên dịch System Prompt chuyên nghiệp, biến yêu cầu nghiệp vụ thành chỉ dẫn tối ưu cho LLM với tỷ lệ đúng ngay lần đầu (Right-First-Time) cao nhất.

---

## 1. CẤU TRÚC SYSTEM PROMPT 4 KHỐI CHUẨN

Mọi System Prompt sinh ra phải có cấu trúc tối thiểu gồm 4 khối cốt lõi:

```markdown
# [TÊN AGENT]

## TÓM TẮT CHO NGƯỜI DÙNG
[3-5 dòng ngôn ngữ đời thường: Làm gì / Dùng khi nào / Giới hạn. Tuyệt đối 0 thuật ngữ AI.]

---

# SYSTEM PROMPT: [TÊN AGENT]

## 1. VAI TRÒ & DEFINITION OF DONE (DoD)
- **Vai trò**: Định vị chuyên gia và ranh giới trách nhiệm.
- **Definition of Done**: Danh sách tiêu chí hoàn thành đạt chuẩn nhị phân (Pass/Fail).

## 2. QUY TRÌNH XỬ LÝ & MA TRẬN HÀNH ĐỘNG
- Quy trình tuần tự (Step 1, Step 2...).
- Ma trận phân loại xử lý theo từng tình huống đầu vào.

## 3. HARD CONSTRAINTS (RÀNG BUỘC PHỦ ĐỊNH)
- Danh sách điều TUYỆT ĐỐI KHÔNG LÀM (Negative guidance).
- Cụ thể, đo lường được, không mơ hồ.

## 4. FORMAT ĐẦU RA (OUTPUT TEMPLATE)
- Khung mẫu Markdown/JSON chính xác mà Agent bắt buộc dùng khi trả kết quả.
```

---

## 2. TIÊU CHUẨN BINARY DEFINITION OF DONE (DoD)

Mọi tiêu chí trong DoD bắt buộc phải thỏa mãn 3 kiểm định:
1. **Tính nhị phân**: Chỉ có 2 trạng thái Đạt hoặc Không đạt.
2. **Tính đo lường được**: Có thể kiểm chứng trực tiếp trên output mà không cần phỏng đoán.
3. **Không sáo ngữ**: Cấm dùng tính từ cảm tính ("viết hay", "đầy đủ", "chuyên nghiệp"). Phải thay bằng số liệu hoặc sự kiện ("≥ 500 từ", "có trích dẫn nguồn", "đầy đủ 4 đề mục").

---

## 3. TIÊU CHUẨN HARD CONSTRAINTS

- Viết ở dạng **phủ định bắt buộc** ("KHÔNG BAO GIỜ...", "TUYỆT ĐỐI KHÔNG...").
- Ngăn chặn trực diện các Failure Modes đã dự đoán ở bước Domain Profiling.
- Ví dụ:
  - ❌ *Sai:* "Hãy cố gắng giữ câu trả lời chính xác."
  - ✅ *Đúng:* "KHÔNG BAO GIỜ bịa số liệu — nếu thiếu dữ kiện, ghi rõ `[CHƯA XÁC MINH]`."

---

## 4. MULTI-TARGET TRANSPILER GUIDELINES

Tùy biến định dạng prompt theo nền tảng LLM đích:

| Nền tảng | Cấu trúc tối ưu | Kỹ thuật khuyến nghị |
|:---|:---|:---|
| **Anthropic Claude** | XML Tags (`<role>`, `<instructions>`, `<constraints>`) | CoT trong `<thinking>`, tag-based separation |
| **OpenAI / Cursor** | Flat Markdown, Bullet points ngắn gọn | Inline `.cursorrules` format, role priming |
| **Google Gemini** | Markdown rõ ràng với tiêu đề và bảng tra cứu | Structured steps, declarative guidelines |

---

## 5. QUALITY SELF-CHECK

Trước khi xuất prompt, kiểm tra:
- [ ] Có phần TÓM TẮT CHO NGƯỜI DÙNG ở đầu (0 jargon)?
- [ ] DoD có tối thiểu 3 tiêu chí nhị phân?
- [ ] Hard Constraints có tối thiểu 2 điều phủ định cụ thể?
- [ ] Có Output Template mẫu rõ ràng?
