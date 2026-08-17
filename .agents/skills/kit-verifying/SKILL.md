---
name: kit-verifying
description: >
  Kiểm định chất lượng Agent Kit theo 3 lớp: L1 Deterministic Linting
  (validate_kit.py, eval_runner.py), L2 Adaptive Scenario Testing (sinh test cases theo domain),
  và L3 Adversarial Stress Testing; kiểm tra tính toàn vẹn của Suite Hierarchy (routing,
  orphan skills, boundary matrix) và kiểm duyệt tiêu chuẩn Anthropic Skill Creator Quality Gate.
  Kích hoạt khi kiểm thử, chấm điểm hoặc nghiệm thu Agent Kit.
when_to_use: "Khi cần kiểm định chất lượng, chạy test suite, kiểm tra chuẩn Skill Creator hoặc chấm điểm Agent Kit mới/refactor."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.3.0
---

# Kit Verifying

Kỹ năng kiểm định chất lượng toàn diện cho Agent Kit, kết hợp giữa công cụ tự động hóa tất định (Deterministic) và đánh giá chất lượng theo chuẩn **Anthropic Skill Creator**.

---

## 📚 REFERENCE KNOWLEDGE ACTIVATION (NẠP ON-DEMAND)

Khi thực hiện kiểm thử và đánh giá chuyên sâu:
- **Chuẩn Anthropic Skill Creator**: Đọc [skill-creator/SKILL.md](file:///C:/Users/nhdcb/.gemini/config/plugins/anthropic-skills/skills/skill-creator/SKILL.md).
- **Nguyên tắc Điều phối Suite & Boundary Matrix**: Đọc [multi-agent-orchestration.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/multi-agent-orchestration.md).
- **Danh mục Lỗi AI để Stress-test L3**: Đọc [failure-modes.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/failure-modes.md).

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

## 2. ANTHROPIC SKILL CREATOR QUALITY GATE

Mọi skill trong `skills/` phải thỏa mãn 4 tiêu chí bắt buộc của Skill Creator:
1. **Pushy Description Gate**: Trường `description` trong YAML frontmatter phải chứa ngữ cảnh kích hoạt cụ thể để chống under-triggering.
2. **Progressive Disclosure Gate**: Thân bài `SKILL.md` không vượt quá **500 dòng**. Mọi tài liệu chuyên sâu phải nằm trong `references/`.
3. **Reference Integrity Gate**: Mọi link trỏ đến `references/` hoặc `scripts/` phải tồn tại thực tế trên filesystem.
4. **Examples Pattern Gate**: Skill phải chứa ví dụ mẫu Input $\rightarrow$ Output hoặc quy trình từng bước rõ ràng.

---

## 3. SUITE INTEGRITY & BOUNDARY CHECKS

- [ ] **Routing Completeness**: Mọi agent trong `delegatesTo` của Orchestrator phải tồn tại trong `agent/`.
- [ ] **No Orphan Skills**: Mọi skill trong `skills/` phải thuộc `ownedSkills` của một Specialist hoặc Orchestrator.
- [ ] **Boundary Clarity**: File Ownership giữa các Specialist Agents không bị trùng lặp hoặc mâu thuẫn.
- [ ] **Runtime Safety Hook**: Tồn tại file `hooks/validate-tool-call.mjs` có khả năng chặn lệnh nguy hiểm.

---

## 4. THANG ĐIỂM RUBRIC 5 SAO

| Tiêu chí | Trọng số | Yêu cầu đạt |
|:---|:---:|:---|
| **Structural & Skill Creator Gate** | 20% | Đủ cấu phần, frontmatter pushy, thân bài < 500 dòng, references hợp lệ |
| **Specificity & Authority**| 25% | DoD nhị phân, Specialist domain authority rõ ràng |
| **Relevance & Altitude**   | 20% | Right Altitude (không over-engineered, không monolithic) |
| **Uniqueness & Boundary**  | 15% | Thể hiện sâu sắc đặc trưng domain, boundary sạch |
| **Usability & Synthesis**  | 20% | Tóm tắt dễ hiểu, synthesis report mạch lạc |
