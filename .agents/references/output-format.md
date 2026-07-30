# Output Format Specification — Meta-AgentKit

Mọi Agent Kit xuất ra gồm **nhiều thành phần** tuỳ Tier và yêu cầu.
Mỗi thành phần có format riêng. User không cần đọc phần kỹ thuật
để biết mình có nhận đúng thứ cần.

---

## 1. Cấu trúc tổng thể

### Tier 1 — Micro (chỉ Agent)

```markdown
# [TÊN AGENT]

## TÓM TẮT CHO NGƯỜI DÙNG
[3-5 dòng, ngôn ngữ đời thường]

---

# SYSTEM PROMPT: [TÊN AGENT] (kỹ thuật)

## 1. VAI TRÒ & OUTCOME ĐÍCH
## 2. NGUYÊN TẮC VẬN HÀNH
## 3. HARD CONSTRAINTS
## 4. FORMAT ĐẦU RA
```

### Tier 2-3 — Multi-component

```markdown
# [TÊN AGENT KIT]

## TÓM TẮT CHO NGƯỜI DÙNG
[3-5 dòng: hệ thống này làm gì / gồm gì / khi nào dùng / giới hạn]

## DANH SÁCH THÀNH PHẦN
| Component | Mô tả | Path/Section |
|:----------|:------|:-------------|

---

[NỘI DUNG TỪNG COMPONENT]
```

---

## 2. TÓM TẮT CHO NGƯỜI DÙNG

### Tiêu chí

| Tiêu chí | Pass | Fail |
|:---------|:-----|:-----|
| Độ dài | 3-5 dòng | < 2 hoặc > 7 dòng |
| Ngôn ngữ | Đời thường, không thuật ngữ | Có: prompt, token, schema, API, LLM, lens |
| Nội dung | Trả lời: làm gì / dùng khi nào / giới hạn | Thiếu bất kỳ 1 |
| Ngôn ngữ | Khớp ngôn ngữ input | Khác ngôn ngữ |

### Ví dụ tốt

```markdown
## TÓM TẮT CHO NGƯỜI DÙNG

Hệ thống này giúp bạn viết sách phi hư cấu — từ phác thảo đến bản thảo hoàn chỉnh.
Gồm agent viết + bộ nhớ giữ giọng văn nhất quán + quy trình kiểm tra chất lượng.
Dùng khi bạn cần soạn chương, duy trì giọng văn, hoặc kiểm tra lập luận.
Giới hạn: không thay thế biên tập viên chuyên nghiệp, không tự xuất bản.
```

### Ví dụ sai

```markdown
## TÓM TẮT
Agent sử dụng multi-state workflow với memory layer và MCP tools
để generate multi-chapter manuscript output qua prompt compilation.
```

---

## 3. SYSTEM PROMPT — 4 Section lõi

### 3.1 VAI TRÒ & OUTCOME ĐÍCH

**Bắt buộc chứa**:
- Vai trò (1 câu)
- Definition of Done: checklist nhị phân

Mỗi dòng DoD pass 3 kiểm định:

| Kiểm định | Pass | Fail |
|:-----------|:-----|:-----|
| Nhị phân | "File tồn tại" | "File chất lượng" |
| Đo được | "≥ 500 từ" | "đầy đủ" |
| Không sáo ngữ | "Mọi claim có source" | "Chuyên nghiệp" |

### 3.2 NGUYÊN TẮC VẬN HÀNH

Format: [Outcome cần đạt] → [Cơ chế]

**KHÔNG** liệt kê lens theo tên (A, B, C...) — viết outcome trực tiếp.

### 3.3 HARD CONSTRAINTS

Viết dạng negative ("KHÔNG bao giờ..."). Cụ thể, verifiable.

### 3.4 FORMAT ĐẦU RA

Template output mà agent dùng. Phải tái sử dụng được.

---

## 4. Khối mở rộng (conditional)

Chỉ thêm khi thực sự áp dụng. Không thêm khối rỗng.

| Khi | Thêm khối |
|:----|:----------|
| Lens D áp dụng | **Kiến trúc ngữ cảnh** (Core/Module/Reference) |
| Lens E áp dụng | **Hợp đồng I/O** (Input/Output/Handoff) |
| Lens F vượt tối thiểu | **Giao thức an toàn** (ngưỡng dừng, giới hạn tự sửa) |
| Dynamic Enhancement | **Đòn bẩy riêng** (tên tự do) |

---

## 5. Component Formats (Tier 2-3)

### Skills

```
skill-name/
├── SKILL.md
├── references/
├── examples/
└── evals/
    └── evals.json
```

Format chi tiết: → `references/component-specs/skill-spec.md`

### Memory

```markdown
## MEMORY ARCHITECTURE

### Schema
[Key-value / Document / Tiered — tuỳ agent]

### Storage
[File-based: path + format]

### Load Rules
[Khi nào nạp memory vào context]

### Update Rules
[Khi nào cập nhật memory]
```

Format chi tiết: → `references/component-specs/memory-spec.md`

### Workflow

```markdown
## WORKFLOW

### States
| State | Mô tả | Entry Criteria | Exit Criteria |
|:------|:------|:---------------|:-------------|

### Transitions
| Từ | Đến | Condition |
|:---|:----|:----------|

### Error Handling
[Xử lý khi transition fail]
```

Format chi tiết: → `references/component-specs/workflow-spec.md`

### Tools (MCP/API)

```markdown
## TOOLS

### [Tool Name]
- **Purpose**: [1 câu]
- **Type**: [MCP Server / API Call / File I/O]
- **Parameters**: [input params]
- **Returns**: [output format]
- **Error Handling**: [khi fail]
```

Format chi tiết: → `references/component-specs/tool-spec.md`

---

## 6. SUITE_BUILD Output

Khi yêu cầu là bộ nhiều agent:
- Mỗi agent có kit riêng (theo format trên)
- 1 Manifest cấp bộ

Chi tiết: → `references/suite-build-protocol.md`

---

## 7. Anti-patterns trong Output

| Anti-pattern | Hậu quả | Sửa |
|:-------------|:--------|:----|
| Tóm tắt dùng thuật ngữ | User không hiểu | Viết lại đời thường |
| Liệt kê lens theo tên | Agent không cần biết framework | Viết outcome trực tiếp |
| Khối mở rộng rỗng | Vi phạm YAGNI | Xoá khối rỗng |
| DoD bằng tính từ | Không verify được | Quy ra tiêu chí nhị phân |
| Provider lock-in | Không portable | Dùng ngôn ngữ agnostic |
| Thiếu output template | User không biết expect gì | Luôn có template |
| Component thừa | Tier 1 có workflow → phình | Chỉ sinh component cần |
