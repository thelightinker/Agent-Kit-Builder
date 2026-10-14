---
name: domain-profiling
description: "Phân tích domain nghiệp vụ cho Agent Kit: trích xuất Core Verbs, tìm đòn bẩy 80/20 (Dynamic Enhancement Discovery), mô hình hóa rủi ro (Risk Profiling) để ánh xạ sang 5 Verification Archetypes, thực hiện Right Altitude Test để chọn Topology trên Spectrum và đề xuất cấu phần tối thiểu. Luôn kích hoạt khi bắt đầu tạo kit mới hoặc đánh giá lại domain."
when_to_use: "Khi cần phân tích nghiệp vụ, hành động cốt lõi, mô hình rủi ro verification, đòn bẩy và topology cho Agent Kit mới hoặc refactor."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.3.0
---

# Domain Profiling

Kỹ năng phân tích chiều sâu miền nghiệp vụ (domain) để xây dựng nền tảng vững chắc cho Agent Kit, mô hình hóa rủi ro thất bại để suy luận cơ chế kiểm định phù hợp, loại bỏ phỏng đoán và ngăn chặn over-engineering ngay từ đầu.

---

## 📚 REFERENCE KNOWLEDGE ACTIVATION (NẠP ON-DEMAND)

Khi cần tra cứu chuyên sâu trong quá trình phân tích:
- **Lý thuyết Verification Abstraction & 5 Archetypes**: Đọc [verification-abstraction.md](../../references/verification-abstraction.md).
- **Cây quyết định Topology & Right Altitude Test**: Đọc [workflow-topologies.md](../../references/workflow-topologies.md).
- **6 Lăng kính Thiết kế & Đòn bẩy ROI**: Đọc [outcome-lenses.md](../../references/outcome-lenses.md).
- **Thư viện 12+ AI Failure Modes**: Đọc [failure-modes.md](../../references/failure-modes.md).

---

## 1. PHÂN TÍCH CORE VERBS

Xác định 5-10 hành động xảy ra thường xuyên nhất trong domain. Mỗi verb đánh giá theo 4 tiêu chí:

| Tiêu chí | Câu hỏi kiểm định | Giá trị |
|:---|:---|:---|
| **Precision vs Creativity** | Cần chính xác tuyệt đối hay cần sáng tạo/linh hoạt? | Precision / Creativity |
| **Knowledge Type** | Cần tri thức chuyên sâu đặc thù hay tư duy logic chung? | Specialized / General |
| **Failure Severity** | Hậu quả nếu Agent thực hiện sai hành động này? | Low / Medium / Critical |
| **Automation Feasibility** | Có thể kiểm chứng tự động bằng script/pattern không? | Deterministic / Semantic |

*Nguyên tắc:* Các verb có `Critical` severity hoặc `Precision` cao bắt buộc phải có Hard Constraints và cơ chế Reality Check bảo vệ.

---

## 2. RISK PROFILING & VERIFICATION ARCHETYPE MAPPING

Đánh giá 3 chiều rủi ro để ánh xạ trực tiếp sang các **Verification Archetypes**:

| Chiều Rủi Ro | Dấu Hiệu Nhận Biết | Verification Archetype Kích Hoạt |
|:---|:---|:---|
| **Omission Risk** | Domain pháp lý, audit, bảo mật, compliance cần quét danh mục bắt buộc. | ➔ **Negative Completeness Matrix** (Kiểm tra cái gì bị thiếu) |
| **Arithmetic Risk** | Domain tài chính, e-commerce growth, data analysis có phép tính $\ge 3$ biến. | ➔ **Deterministic Computation Guard** (Ép chạy script tính toán) |
| **Mutation Risk** | Domain devops, refactor, migration có thao tác ghi đè/xóa/sửa đổi file & DB. | ➔ **Transactional Mutation Pattern** (Snapshot $\rightarrow$ Mutate $\rightarrow$ Rollback) |


---

## 3. DYNAMIC ENHANCEMENT DISCOVERY (ĐÒN BẨY 80/20)

Trả lời 3 câu hỏi cốt lõi — độc lập cho từng agent/specialist cần xây dựng:

1. **Outcome quan trọng nhất** của agent này là gì? *(Kết quả thực tế nào chứng minh agent thành công?)*
2. **Điểm thất vọng phổ biến nhất** của người dùng thực tế khi dùng agent này? *(Đây là đòn bẩy 80/20 ưu tiên hàng đầu).*
3. **Trade-off ROI**: Tính toán tỷ lệ $ROI = \frac{\text{Mức tăng Năng lực}}{\text{Chi phí Token \& Độ phức tạp}}$
   - ✅ **Chấp nhận ($ROI \ge 1.25$):** Tăng năng lực x1.5 mà chi phí chỉ tốn x1.2.
   - ❌ **Từ chối ($ROI < 1.0$ - Over-engineered):** Tăng năng lực x1.5 nhưng token tốn gấp đôi (x2.0).

---

## 4. THE RIGHT ALTITUDE TEST & TOPOLOGY SELECTION

Thay vì ép cứng 3 hộp, xác định vị trí tối ưu trên **Phổ Kiến trúc (Spectrum)**:

$$\mathbf{\text{Coordination Cost (Handoff + Routing)}} < \mathbf{\text{Context/Cognitive Cost Saved (Attention Rot + Confusion)}}$$

| Vị trí trên Spectrum | Điều kiện Thỏa mãn | Cấu trúc Khuyến nghị |
|:---|:---|:---|
| **Micro** | 1 tác vụ đơn lẻ, stateless, 1-shot | 1 System Prompt duy nhất (< 500 từ) |
| **Standard** | 1 domain tập trung, $\le 4-5$ skills, luồng tuyến tính | 1 Single Agent + Skills + Workflows |
| **Mini-Suite** | 2 mảng đối trọng (ví dụ: Maker & Reviewer / Coder & Auditor) | 1 Lead Orchestrator + 2 Specialist Agents |
| **Full Suite Hierarchy** | $\ge 3$ domain độc lập, $\ge 6-15$ skills, cần Scoped Memory | 1 Master Orchestrator + 3–7 Specialist Agents + Scoped Memory |

---

## 5. CAPABILITY SKELETON SYNTHESIS (COMPILER INPUT)

Dựa trên Core Verbs và Risk Profile, xuất ra bộ **Capability Skeleton** làm đầu vào cho compiler:
- **Structural Preconditions**: Các sự thật nhị phân (flags, file paths, state keys) máy có thể kiểm tra trực tiếp.
- **Semantic Preconditions**: Các phán quyết ngữ nghĩa cần Evaluator đánh giá (mang `content_version` theo CANON 5).
- **Negative Boundaries**: Các tài nguyên cấm can thiệp theo CANON 6.

---

## 6. COMPILED ROUTING CONTRACT (BẮT BUỘC — INPUT CHO PROMPT COMPILER)

Domain Profile PHẢI xuất ra 2 khối YAML cấu trúc sau — đây là dữ liệu đầu vào bắt buộc để Prompt Compiler populate capabilities frontmatter và routing instructions trong Agent prompt. Nếu thiếu khối này, routing_index.json sẽ rỗng và kit sẽ FAIL validation.

### 6.1 Routing Table (Cho Orchestrator — nếu topology ≥ Mini-Suite)

```yaml
# routing_table:
- intent_pattern: "phân tích SEO on-page"
  target_agent: seo-specialist
  required_skills: [seo-audit]
  execution_mode: L1_ROUTED
- intent_pattern: "tạo chiến dịch marketing toàn phễu"
  target_agent: STAGED
  steps:
    - agent: seo-specialist
      skills: [seo-audit]
      output_artifact: shared_state/seo_report.json
    - agent: copy-specialist
      skills: [content-writer]
      input_artifact: shared_state/seo_report.json
      output_artifact: outputs/campaign.md
  execution_mode: L2_STAGED
```

### 6.2 Skill Invocation Matrix (Cho MỖI Agent)

```yaml
# skill_invocation_matrix:
seo-specialist:
  - scenario: "Cần phân tích SEO on-page"
    skill: seo-audit
    reason: "Skill chứa checklist 42 tiêu chí chuẩn"
  - scenario: "Cần tối ưu nội dung cho AI search"
    skill: ai-seo-optimizer
    reason: "Skill chứa structured data guidelines mới nhất"
  - scenario: "Task không khớp skill nào"
    action: HANDOFF_ORCHESTRATOR
    reason: "Agent không được vượt domain authority"
```

### Quy tắc:
- Mỗi Agent đã đề xuất ở Section 4 (Topology) PHẢI có ít nhất 1 entry trong `skill_invocation_matrix`.
- Mỗi skill trong matrix PHẢI có `reason` giải thích tại sao phải nạp skill thay vì dùng general reasoning.
- Nếu topology ≥ Mini-Suite, `routing_table` BẮT BUỘC. Nếu Micro/Standard, chỉ `skill_invocation_matrix` là bắt buộc.

---

## 7. REPORT FORMAT

Sau khi phân tích, trả về Domain Profile theo mẫu:

```markdown
# Domain Profile: [Tên Domain / Kit]

## 1. Core Verbs & Risk Profile Matrix
- Core Verbs: ...
- Rủi ro chủ đạo: [Omission / Arithmetic / Mutation / Visual]
- Verification Archetypes chỉ định: [Archetype 1, Archetype 2...]

## 2. Capability Skeleton (Compiler Contract)
- Capability ID: domain.component.action
- Structural Preconditions: [key1, key2]
- Semantic Preconditions: [verdict_name (evaluator)]
- Negative Scope: [cannot_modify]

## 3. 80/20 Leverage & ROI Analysis
- Outcome cốt lõi: ...
- Điểm thất vọng lớn nhất: ...
- Đòn bẩy đề xuất (ROI >= 1.25): ...

## 4. Topology Selection
- Altitude & Spectrum: [Micro | Standard | Mini-Suite | Full Suite]
- Danh sách Agent & Skill đề xuất: ...

## 5. Compiled Routing Contract
### routing_table: (xem Section 6.1)
### skill_invocation_matrix: (xem Section 6.2)
```
