---
name: kit-verifying
description: "Kiểm định chất lượng Agent Kit theo 3 lớp: L1 Deterministic Linting (validate_kit.py, eval_runner.py), L2 Adaptive Scenario Testing (sinh test cases theo domain), và L3 Adversarial Stress Testing; kiểm tra tính toàn vẹn của Suite Hierarchy (routing, Worker Briefing compliance, orphan skills, boundary matrix), kiểm tra Verification Abstraction Layer, Execution-First Verification và kiểm duyệt tiêu chuẩn Anthropic Skill Creator Quality Gate."
when_to_use: "Khi cần kiểm định chất lượng, chạy test suite, kiểm tra chuẩn Skill Creator hoặc chấm điểm Agent Kit mới/refactor."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.7.0
---

# Kit Verifying

Kỹ năng kiểm định chất lượng toàn diện cho Agent Kit, kết hợp giữa công cụ tự động hóa tất định (Deterministic), nguyên lý **Verification Abstraction Layer** và đánh giá chất lượng theo chuẩn **Anthropic Skill Creator**.

---

## 📚 REFERENCE KNOWLEDGE ACTIVATION (NẠP ON-DEMAND)

Khi thực hiện kiểm thử và đánh giá chuyên sâu:
- **Lý thuyết Verification Abstraction & 5 Archetypes**: Đọc [verification-abstraction.md](../../references/verification-abstraction.md).
- **Chuẩn Anthropic Skill Creator**: Đọc [skill-creator/SKILL.md](../skill-creator/SKILL.md).
- **Nguyên tắc Điều phối Suite & Boundary Matrix**: Đọc [multi-agent-orchestration.md](../../references/multi-agent-orchestration.md).
- **Danh mục Lỗi AI để Stress-test L3**: Đọc [failure-modes.md](../../references/failure-modes.md).
- **Error Resilience & Escalation Protocol**: Đọc [error-resilience.md](../../references/error-resilience.md) để kiểm thử cơ chế phục hồi lỗi và thoát vòng lặp.

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

## 2. NGUYÊN LÝ "VERIFICATION BY EXECUTION"

Kiểm thử bằng chạy lệnh thực tế thay vì phỏng đoán bằng mắt:
- **Tồn tại $\ne$ Hoạt động**: File tồn tại hoặc cú pháp đúng không đồng nghĩa với logic chạy đúng.
- **Domain-Adaptive Execution Checklist**: Bộ kit đạt chuẩn phải cung cấp `scripts/checklist.py` sinh theo Risk Profile của domain (chạy text linter, math checker, negative completeness hoặc unit tests) để cung cấp bằng chứng (evidence) rõ ràng.

---

## 3. VERIFICATION ABSTRACTION & REGRESSION PROTECTION

- **Domain-Risk Alignment**: Xác thực xem `checklist.py` có khớp với rủi ro cốt lõi của domain không (ví dụ: cấm chạy `pytest` cho content kit; bắt buộc chạy `Negative Completeness Matrix` cho legal kit).
- **Regression Benchmark Guard**: Sau các đợt nâng cấp, chạy `python scripts/eval_runner.py --regression` để kiểm tra độ tin cậy trên 5 bài test chuẩn (Content, Growth, UI/UX, Legal, DevOps).

---

## 4. ANTHROPIC SKILL CREATOR & SUITE INTEGRITY GATE

Mọi skill và agent trong Kit phải thỏa mãn:
1. **Pushy Description Gate**: `description` trong YAML frontmatter phải chứa ngữ cảnh kích hoạt cụ thể để chống under-triggering.
2. **Progressive Disclosure Gate**: Thân bài `SKILL.md` không vượt quá **500 dòng**. Mọi tài liệu chuyên sâu phải nằm trong `references/`.
3. **Reference Integrity Gate**: Mọi link trỏ đến `references/` hoặc `scripts/` phải tồn tại thực tế trên filesystem.
4. **Worker Briefing Compliance**: Master Orchestrator không chứa các câu ủy quyền mù quáng, mà phải có cấu trúc Worker Briefing đầy đủ 5 phần.
5. **No Orphan Skills**: Mọi skill trong `skills/` phải thuộc `ownedSkills` của một Specialist hoặc Orchestrator.
6. **Runtime Safety Hook**: Tồn tại file `hooks/validate-tool-call.mjs` có khả năng chặn lệnh nguy hiểm.
7. **Execution Policy Contract**: Tồn tại file `execution_policy.json`, valid theo `schemas/execution-policy.schema.json`, và `mode` khớp với topology thực tế (single agent → `direct`, multi-agent → `stage_machine` hoặc `fork_join`).
8. **Orchestration Protocol Presence**: Nếu Kit là Multi-Agent Suite, Master Orchestrator prompt **BẮT BUỘC** chứa section `## Orchestration Protocol` hoặc `## 🎯 ORCHESTRATION PROTOCOL`.

---

## 5. THANG ĐIỂM RUBRIC 5 SAO

| Tiêu chí | Trọng số | Yêu cầu đạt |
|:---|:---:|:---|
| **Structural & Skill Creator Gate** | 20% | Đủ cấu phần, frontmatter pushy, thân bài < 500 dòng, references hợp lệ |
| **Specificity & Authority**| 25% | DoD nhị phân, Worker Briefing chuẩn, Specialist domain authority rõ ràng |
| **Relevance & Altitude**   | 20% | Right Altitude (không over-engineered, không monolithic) |
| **Verification & Evidence**| 20% | Có domain-adaptive checklist runner thực thi chứng minh kết quả |
| **Usability & Synthesis**  | 15% | Tóm tắt dễ hiểu, synthesis report mạch lạc, không biệt ngữ AI |

---

## 6. EXAMPLES (VÍ DỤ THỰC THI)

### Example 1: Kiểm định Kit L1 Deterministic Linting
**Input:** Chạy lệnh `python scripts/validate_kit.py ./output/ecommerce-growth/`.
**Output:** Báo cáo 0 lỗi (Pass), cập nhật `audit_findings.json` và chuyển `lifecycle_state: "VALIDATED"`.

### Example 2: Stress-test L3 Adversarial Boundary
**Input:** Đưa input đầu vào cố tình vi phạm Hard Constraints (ví dụ: yêu cầu tính nhẩm trực tiếp).
**Output:** Specialist Agent từ chối tính nhẩm và chuyển giao quyền tính toán sang script Python tất định theo đúng Deterministic Computation Guardrail.
