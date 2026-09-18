# UPGRADE GATE: HIẾN PHÁP NÂNG CẤP HỆ THỐNG

> **“Không tối ưu từng capability. Tối ưu hệ thống.”**

Tài liệu này là Hiến pháp SSOT bắt buộc cho mọi hoạt động nâng cấp, refactor và mở rộng kiến trúc của Agent Kit Creator và các Agent Kit con.

---

## 🏛️ 1. ARCHITECTURAL INVARIANT: HARD GATES TRƯỚC, NET GAIN SAU

Mọi nâng cấp phải đi qua chu trình kiểm định nhị phân, không phụ thuộc vào LLM self-grading:

$$\text{Evidence Extraction} \longrightarrow \text{Hard Gate Filter} \longrightarrow \text{Weighted Net Gain} \longrightarrow \text{Deterministic Decision}$$

```
┌────────────────────────┐     ┌────────────────────────┐     ┌──────────────────────────┐     ┌──────────────────────┐
│ 1. Evidence Extraction │ ──> │ 2. Hard Constraints    │ ──> │ 3. Weighted Net System   │ ──> │ 4. Final Decision    │
│    (Provenance & Proof)│     │    (Anti-Bloat Traps)  │     │    Gain Calculation      │     │    (KEEP/ADAPT/...)  │
└────────────────────────┘     └────────────────────────┘     └──────────────────────────┘     └──────────────────────┘
```

---

## 🚦 2. NĂM CÂU HỎI CỐT LÕI (5 VALUE PILLARS)

1. **POWER**: Có làm output / reasoning / orchestration mạnh hơn thực chất không?
2. **FLEXIBILITY**: Có mở rộng khả năng mà không khóa hệ thống vào một domain/tool không?
3. **AUTOMATION**: Có giảm thao tác thủ công hoặc tăng khả năng tự vận hành không?
4. **OPTIMIZATION**: Có giảm token, latency, complexity, duplication hoặc maintenance cost không?
5. **COLLABORATION**: Có phối hợp tốt hơn với Human / Agent / Plugin / MCP mà không tạo conflict không?

---

## ⚖️ 3. NGUYÊN TẮC LÃI RÒNG & ĐÁNH ĐỔI CÓ LÃI (PROFITABLE TRADE-OFF)

Upgrade chỉ được chấp nhận khi $\text{Net System Gain} > 0$:

$$\text{Gross Value} = 0.25 \cdot \text{power} + 0.20 \cdot \text{flexibility} + 0.25 \cdot \text{automation} + 0.15 \cdot \text{optimization} + 0.15 \cdot \text{collaboration}$$
$$\text{Total Cost} = 0.20 \cdot \frac{\max(0, \Delta \text{token}\%)}{100} + 0.20 \cdot \frac{\max(0, \Delta \text{latency}\%)}{100} + 0.25 \cdot \max(0, \Delta \text{complexity}) + 0.25 \cdot \text{human\_attention} + 0.10 \cdot \text{regression\_risk}$$
$$\text{Net Gain} = \text{Gross Value} - \text{Total Cost}$$

- **Đánh đổi có lãi:** Cho phép giảm 1 trục (ví dụ Flexibility giảm nhẹ do chuẩn hóa schema) nếu Automation tăng vọt và chi phí bảo trì giảm sâu.
- **LOC chỉ là proxy:** Không coi `-LOC` là thước đo tuyệt đối. Mã nguồn tốt có thể dài hơn nhưng giảm coupling, triệt tiêu lỗi và giảm tải cho con người.

---

## 🚫 4. HARD GATES CẤM MERGE (INSTANT REJECTION TRAPS)

Tự động **REJECT** ngay lập tức nếu vi phạm bất kỳ tiêu chí nào sau đây:

1. **Missing Evidence Trap (`MISSING_EVIDENCE`)**: Đề xuất không kèm ít nhất 1 Benchmark, Automated Test hoặc Measurable Metric.
2. **Blind Copy Trap (`BLIND_COPY_VIOLATION`)**: Sao chép pattern đặc thù mà không qua chu trình `BEFORE → WHY → GENERALIZE → UPGRADE`.
3. **Approval Fatigue Trap (`APPROVAL_FATIGUE_TRAP`)**: Tăng can thiệp thủ công của con người (`human_attention > 0.5`) mà không tăng tự động hóa, hoặc `human_attention >= 1.5`.
4. **Performance Blowout (`PERFORMANCE_BLOWOUT`)**: Độ trễ tăng $> 100\%$ hoặc token tăng $> 150\%$.
5. **Doraemon Bloat Trap (`DORAEMON_BLOAT_TRAP`)**: Tăng độ phức tạp mã nguồn (`complexity > 1.0`) mà không mang lại giá trị tương xứng ($\text{power} + \text{automation} < 1.0$).
6. **Goodhart LOC Gaming (`GOODHART_LOC_GAMING_TRAP`)**: Cắt giảm LOC giả tạo để làm đẹp chỉ số nhưng đẩy rủi ro hệ thống tăng cao mà không có test suite bảo vệ.

---

## 🎯 5. UPGRADE DECISION MATRIX

| Quyết định | Ngưỡng Net Gain & Điều Kiện | Hành Động |
|:---|:---|:---|
| **`KEEP`** | $\text{Net Gain} \ge 0.35$, không có trục nào $< -0.5$, 100% Hard Gates PASS. | Merge vào kiến trúc chính thức. |
| **`ADAPT`** | $\text{Net Gain} > 0.10$, Hard Gates PASS, chấp nhận trade-off hợp lệ. | Tinh chỉnh kiến trúc để tối ưu chi phí biên trước khi merge. |
| **`DEFER`** | $0.0 \le \text{Net Gain} \le 0.10$ hoặc bằng chứng chưa đủ độ tin cậy. | Tạm hoãn, thu thập thêm dữ liệu benchmark thực tế. |
| **`REJECT`** | Vi phạm Hard Gate hoặc $\text{Net Gain} \le 0.0$. | Bác bỏ hoàn toàn. |

---

## 🛠️ 6. THẨM ĐỊNH THỰC THI (EXECUTABLE EVALUATION)

Mọi đề xuất nâng cấp bắt buộc phải được mô tả qua file `upgrade_proposal.json` chuẩn schema [`schemas/upgrade_proposal.schema.json`](schemas/upgrade_proposal.schema.json) và được kiểm chứng bởi:

```bash
python .agents/scripts/upgrade_gate_evaluator.py upgrade_proposal.json
```
