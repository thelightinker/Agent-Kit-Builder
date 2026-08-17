# Agent Spec — Chuẩn viết Agent (System Prompt)

Component cốt lõi — mọi Agent Kit đều có. Đây là system prompt mà LLM
nhận để hành động.

---

## Cấu trúc bắt buộc

```markdown
# [TÊN AGENT]

## TÓM TẮT CHO NGƯỜI DÙNG
[3-5 dòng: làm gì / dùng khi nào / giới hạn]

---

# SYSTEM PROMPT: [TÊN AGENT] (kỹ thuật)

## 1. VAI TRÒ & OUTCOME ĐÍCH
[Vai trò 1 câu + Definition of Done]

## 2. NGUYÊN TẮC VẬN HÀNH
[Outcome → Cơ chế — chỉ những cái thực sự áp dụng]

## 3. HARD CONSTRAINTS
[KHÔNG bao giờ... — cụ thể, verifiable]

## 4. FORMAT ĐẦU RA
[Template output tái sử dụng]
```

---

## Definition of Done

Checklist nhị phân. Mỗi dòng pass 3 kiểm định:

| Kiểm định | Câu hỏi | Ví dụ pass | Ví dụ fail |
|:-----------|:--------|:-----------|:-----------|
| Nhị phân | Pass/fail rõ ràng? | "File tồn tại" | "File chất lượng" |
| Đo được | Chấm được mà không context ngoài? | "≥ 500 từ" | "đầy đủ" |
| Không sáo ngữ | Tính từ đã quy ra tiêu chí? | "Mọi claim có source" | "Chuyên nghiệp" |

**Tối thiểu 3 dòng DoD** cho mọi agent.

---

## Nguyên tắc vận hành

Format: **[Outcome cần đạt]** → [Cơ chế để đạt]

```markdown
**Không hallucinate dữ liệu** → Mọi claim phải có source. Nếu không có,
gắn [CHƯA XÁC MINH].

**Chi phí thấp cho task đơn giản** → Phân biệt request đơn giản (trả trực tiếp)
vs phức tạp (chạy full process).
```

**KHÔNG**:
- Liệt kê lens theo tên (A, B, C)
- Viết cơ chế mà agent không dùng
- Dùng ngôn ngữ đời thường trong phần kỹ thuật

---

## Hard Constraints

- Viết dạng negative: "KHÔNG bao giờ..."
- Cụ thể + verifiable
- Không lặp Nguyên tắc vận hành

---

## Khối mở rộng

Chỉ thêm khi lens thực sự áp dụng:

| Trigger | Khối | Format |
|:--------|:-----|:-------|
| Lens D | Kiến trúc ngữ cảnh | Core / Module / Reference layers |
| Lens E | Hợp đồng I/O | Input / Output / Handoff schemas |
| Lens F (nâng cao) | Giao thức an toàn | Ngưỡng dừng / giới hạn retry / escalation |
| Dynamic Enhancement | Đòn bẩy riêng | Outcome / Cơ chế / Kích hoạt |
| Suite Lead Agent | Master Orchestrator Protocol | Pre-flight, Boundary Matrix, Worker Directives, Coordinator Mode (`references/orchestrator-agent-pattern.md`) |

---

## Tier Calibration

| Tier | System Prompt length | DoD items | Constraints |
|:-----|:--------------------|:----------|:-----------|
| 1 | < 300 từ | 3-4 | 2-3 |
| 2 | 300-800 từ | 4-6 | 3-5 |
| 3 | 500-1500 từ | 5-8 | 4-7 |
| 3 (Orchestrator) | 800-2000 từ | 6-10 | 5-8 |

**Cảnh báo**: Tier 1 > 500 từ → kiểm tra over-engineering.
