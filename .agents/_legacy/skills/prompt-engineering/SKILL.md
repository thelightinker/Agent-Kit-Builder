---
name: prompt-engineering
description: ">"
when_to_use: "Kích hoạt khi cần năng lực prompt-engineering trong quy trình tạo hoặc kiểm định Agent Kit."
requires_templates: ["templates/agent-template.md", "templates/orchestrator-template.md"]
requires_references: ["references/agent-design-patterns.md", "references/antigravity-patterns.md"]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# Prompt Engineering

## Overview

Biên dịch yêu cầu và domain analysis thành System Prompt tối ưu — có cấu trúc
chặt chẽ, DoD đo lường được, constraints cụ thể, và output format rõ ràng.
System Prompt là thành phần cốt lõi mà MỌI kit đều có.

---

## Cấu trúc System Prompt (4 Section Căn bản & 6-Pattern Modular Nâng cao)

System Prompt được thiết kế theo cấp độ phức tạp (Complexity Tier). Tham chiếu mẫu chi tiết tại [agent-design-patterns.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/agent-design-patterns.md) và [agent-template.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/templates/agent-template.md).

```markdown
# [TÊN AGENT]

## TÓM TẮT CHO NGƯỜI DÙNG
[3-5 dòng: làm gì / dùng khi nào / giới hạn]

---

# SYSTEM PROMPT: [TÊN AGENT]

## 📑 QUICK NAVIGATION (TOC - Dành cho Agent > 500 dòng)

## 🛑 3-TIER AUTONOMY GATE & ANTI-DEFAULTS
[Tier A: Act immediately | Tier B: Act + Document Assumptions | Tier C: Stop & Ask when uncertainty materially alters outcome]

## 🧠 DOMAIN-AWARE MENTAL ANALYSIS (TRƯỚC KHI THỰC THI)
[UI/UX: Disrupt Cliché Layouts | Backend/Infra: Boring & Stable Tech First | Challenge defaults, not stability]

## 1. VAI TRÒ & OUTCOME ĐÍCH
[Vai trò 1 câu]
[Definition of Done — checklist nhị phân]

## 2. QUY TRÌNH XỬ LÝ & MA TRẬN CHIẾN LƯỢC
[ASCII Flowchart + Ma trận tra cứu chiến lược theo domain]

## 3. HARD CONSTRAINTS
[KHÔNG bao giờ... — cụ thể, verifiable]

## 4. FORMAT ĐẦU RA
[Template output tái sử dụng]

## 🛡️ REALITY CHECK (SPIRIT OVER CHECKLIST)
[Checklist tự kiểm định thực tế: Empirical Evidence, Root Cause Fix, Zero Placeholder]
```

---

## Definition of Done (DoD)

Checklist nhị phân. Mỗi dòng phải pass 3 kiểm định:

| Kiểm định | Pass | Fail |
|:-----------|:-----|:-----|
| **Nhị phân** | "File tồn tại", "≥ 3 items" | "File chất lượng", "Phù hợp" |
| **Đo được** | Có metric cụ thể hoặc binary check | Cần context ngoài để đánh giá |
| **Không sáo ngữ** | Tiêu chí cụ thể | "Chuyên nghiệp", "Đầy đủ", "Tối ưu" |

**Tối thiểu 3 dòng DoD** cho mọi agent.

### Ví dụ chuẩn
- [ ] File đầu ra tồn tại và có dung lượng > 0 bytes
- [ ] Mọi claim có source hoặc gắn [CHƯA XÁC MINH]
- [ ] Không chứa từ khóa placeholder: [TODO], [TBD], [PLACEHOLDER]
- [ ] Output ≥ 500 từ (hoặc metric phù hợp domain)

### Ví dụ FAIL
- [ ] Code sạch sẽ và chạy tốt ← mơ hồ
- [ ] Nội dung đầy đủ và chuyên nghiệp ← sáo ngữ
- [ ] Đảm bảo chính xác ← không verifiable

---

## Nguyên tắc vận hành

Format: **[Outcome cần đạt]** → [Cơ chế để đạt]

```markdown
**Không hallucinate dữ liệu** → Mọi claim phải có source.
Nếu không có, gắn [CHƯA XÁC MINH].

**Chi phí thấp cho task đơn giản** → Phân biệt request đơn giản
(trả trực tiếp) vs phức tạp (chạy full process).
```

**KHÔNG**:
- Liệt kê cơ chế mà agent không dùng
- Dùng ngôn ngữ đời thường trong phần kỹ thuật
- Copy-paste cơ chế từ kit khác mà không customize

---

## Hard Constraints

- Viết dạng negative: "KHÔNG bao giờ..."
- Cụ thể + verifiable
- Không lặp nội dung đã có trong Nguyên tắc vận hành

| ✅ Đúng | ❌ Sai |
|:---------|:-------|
| "KHÔNG bịa số liệu — dùng [CHƯA XÁC MINH]" | "Luôn đảm bảo chính xác" |
| "KHÔNG trả > 2000 từ trừ khi user yêu cầu" | "Giữ output ngắn gọn" |
| "KHÔNG chạy code destructive khi chưa hỏi user" | "Cẩn thận với code" |

**Tối thiểu 2 constraints** cho mọi agent.

---

## Tier-Proportional Sizing

| Kit Type | Prompt Length | DoD Items | Constraints |
|:---------|:-------------|:----------|:-----------|
| Micro | < 300 từ | 3-4 | 2-3 |
| Standard | 300-800 từ | 4-6 | 3-5 |
| Professional | 500-1500 từ | 5-8 | 4-7 |
| Suite (mỗi agent) | 300-1000 từ | 4-6 | 3-5 |

**Cảnh báo**: Micro > 500 từ → kiểm tra over-engineering.

---

## Agent Frontmatter (Professional/Suite)

Với kit phức tạp, agent cần frontmatter cho discovery và routing:

```yaml
---
name: agent-name
description: Mô tả vai trò + khi nào activate
tools: Read, Grep, Glob, Bash, Write, Edit
version: 1.0.0
skills: skill-1, skill-2, skill-3
---
```

---

## TÓM TẮT CHO NGƯỜI DÙNG

| Tiêu chí | Pass | Fail |
|:---------|:-----|:-----|
| Độ dài | 3-5 dòng | < 2 hoặc > 7 dòng |
| Ngôn ngữ | Đời thường, 0 thuật ngữ | Có: prompt, token, schema, API, LLM |
| Nội dung | Trả lời: làm gì / dùng khi nào / giới hạn | Thiếu bất kỳ 1 |

### Ví dụ tốt
```
Hệ thống này giúp bạn viết sách phi hư cấu — từ phác thảo đến bản thảo.
Gồm agent viết + bộ nhớ giữ giọng văn nhất quán + quy trình kiểm tra.
Dùng khi bạn cần soạn chương hoặc kiểm tra lập luận.
Giới hạn: không thay thế biên tập viên, không tự xuất bản.
```

---

## Self-Check

```
□ TÓM TẮT: 3-5 dòng, 0 thuật ngữ, trả lời 3 câu
□ DoD: mọi dòng pass 3 kiểm định (nhị phân, đo được, không sáo ngữ)
□ Constraints: cụ thể, verifiable, không lặp Nguyên tắc
□ Ngôn ngữ khớp input user
□ Provider-agnostic (0 mention provider cụ thể)
□ Tier-proportional (Micro < 300 từ, Standard < 800, etc.)
□ Output format có template cụ thể
```
