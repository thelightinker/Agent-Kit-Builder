---
name: kit-verifying
description: >
  Kiểm định chất lượng Agent Kit theo 3 lớp: L1 Deterministic Linting
  (validate_kit.py, eval_runner.py), L2 Adaptive Scenario Testing (sinh test cases theo domain),
  và L3 Adversarial Stress Testing; kiểm tra tính toàn vẹn của Suite Hierarchy (routing,
  orphan skills, boundary matrix). Kích hoạt khi kiểm thử, chấm điểm hoặc nghiệm thu Agent Kit.
when_to_use: "Khi cần kiểm định chất lượng, chạy test suite hoặc chấm điểm Agent Kit mới/refactor."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.2.0
---

# Kit Verifying

Kỹ năng kiểm định chất lượng toàn diện cho Agent Kit, kết hợp giữa công cụ tự động hóa tất định (Deterministic) và đánh giá ngữ nghĩa thích ứng (Adaptive Evaluation).

---

## 📚 REFERENCE KNOWLEDGE ACTIVATION (NẠP ON-DEMAND)

Khi thực hiện kiểm thử và đánh giá chuyên sâu:
- **Nguyên tắc Điều phối Suite & Boundary Matrix**: Đọc [multi-agent-orchestration.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/multi-agent-orchestration.md).
- **Danh mục Lỗi AI để Stress-test L3**: Đọc [failure-modes.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/failure-modes.md).
- **Quy chuẩn Xử lý Lỗi & Escalation**: Đọc [error-resilience.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/error-resilience.md).

---

## 1. QUY TRÌNH KIỂM ĐỊNH 3 LỚP (3-LAYER AUDIT)

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: L1 Deterministic Linting (validate_kit.py)     │ -> 0 errors bắt buộc
├─────────────────────────────────────────────────────────┤
│ Layer 2: L2 Adaptive Scenario Testing (Domain-Specific) │ -> 2-4 Test cases
├─────────────────────────────────────────────────────────┤
│ Layer 3: L3 Adversarial Stress Testing (Loopholes/Edge) │ -> DoD & Constraints
└─────────────────────────────────────────────────────────┘
```

---

## 2. LAYER 1: DETERMINISTIC LINTING & SUITE INTEGRITY

Sử dụng script để kiểm tra các thuộc tính cấu trúc cứng:

```bash
# Kiểm tra toàn vẹn cấu trúc và tham chiếu
python .agents/scripts/validate_kit.py ./output/<kit-name>

# Chạy eval suite (nếu có)
python .agents/scripts/eval_runner.py evals/eval_suite_example.json ./output/<kit-name>
```

### Suite Integrity Checks (Khi kit là Multi-Agent):
- [ ] **Routing Completeness**: Mọi agent trong `delegatesTo` của Orchestrator phải tồn tại trong `agent/`.
- [ ] **No Orphan Skills**: Mọi skill trong `skills/` phải thuộc `ownedSkills` của một Specialist hoặc Orchestrator.
- [ ] **Boundary Clarity**: File Ownership giữa các Specialist Agents không bị trùng lặp hoặc mâu thuẫn.

---

## 3. LAYER 2: ADAPTIVE SCENARIO TESTING

Sinh kịch bản kiểm thử thích ứng theo topology và domain:
- **Single Agent Kit**: 2 Happy-path + 2 Edge-case inputs.
- **Suite Kit**: 3 End-to-end multi-agent flows (Orchestrator phân rã ➔ Specialist thực thi ➔ Orchestrator tổng hợp).

---

## 4. LAYER 3: ADVERSARIAL STRESS TESTING

- Thử nghiệm input chứa yêu cầu cross-domain $\rightarrow$ Specialist có kích hoạt Handoff Trigger về Orchestrator không?
- Thử nghiệm input thiếu dữ kiện $\rightarrow$ Orchestrator có kích hoạt Socratic Questioning không?
- Thử nghiệm phá vỡ Boundary Matrix $\rightarrow$ Specialist có từ chối sửa file ngoài domain không?

---

## 5. THANG ĐIỂM RUBRIC 5 SAO & KẾT LUẬN

| Tiêu chí | Trọng số | Yêu cầu đạt |
|:---|:---:|:---|
| **Structural & Topology** | 20% | Đủ cấu phần theo Topology, frontmatter & manifest hợp lệ |
| **Specificity & Authority**| 25% | DoD nhị phân, Specialist domain authority rõ ràng |
| **Relevance & Altitude**   | 20% | Right Altitude (không over-engineered, không monolithic) |
| **Uniqueness & Boundary**  | 15% | Thể hiện sâu sắc đặc trưng domain, boundary sạch |
| **Usability & Synthesis**  | 20% | Tóm tắt dễ hiểu, synthesis report mạch lạc |
