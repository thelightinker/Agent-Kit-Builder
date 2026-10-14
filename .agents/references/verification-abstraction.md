# 🛡️ Verification Abstraction Layer

> Cẩm nang lý thuyết và kiến trúc: Mô hình hóa rủi ro domain $\rightarrow$ 5 Verification Archetypes $\rightarrow$ Bằng chứng thực thi (Executable Evidence).

---

## 1. NGUYÊN LÝ CỐT LÕI

> **Invariant:** *Không bao giờ gán cố định công cụ kiểm thử (như pytest/eslint) cho mọi domain. Agent Kit Builder phải suy ra cơ chế kiểm chứng từ bản chất rủi ro của domain.*

```
                    USER TASK
                       │
                       ▼
                DOMAIN + RISK (Risk Profiler)
                       │
                       ▼
          VERIFICATION ABSTRACTION ENGINE
                       │
        ┌──────────────┼──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
     Presence       Negative     Deterministic    Visual QA /
      Checks        Coverage      Computation    Mutation Safety
   (Structural)    (Omission)      (Numeric)      (Side-effects)
        │              │              │              │
        └──────────────┴──────┬───────┴──────────────┘
                              ▼
                  Domain-Adaptive Checklist
                  (scripts/checklist.py)
                              │
                              ▼
                     Executable Evidence
                              │
                              ▼
                   PASS / FAIL / ESCALATE
```

---

## 2. RISK MODELING (MÔ HÌNH HÓA RỦI RO)

Trước khi thiết kế checklist cho bất kỳ Agent Kit nào, xác định 4 chiều rủi ro:

| Chiều rủi ro | Câu hỏi định vị | Hậu quả nếu thất bại |
|:---|:---|:---|
| **Omission Risk** (Rủi ro bỏ sót) | Có danh mục điều khoản/yêu cầu bắt buộc nào bị thiếu không? | Vi phạm pháp lý, hở bảo mật, thiếu tính năng |
| **Arithmetic Risk** (Rủi ro số học) | Có phép tính $\ge 3$ biến số hoặc dữ liệu bảng phái sinh không? | Ảo giác tài chính, sai lệch chỉ số CAC/LTV |
| **Mutation Risk** (Rủi ro đột biến) | Thao tác có làm thay đổi/xóa file, database hoặc hạ tầng không? | Mất dữ liệu, sập server, corrupt workspace |
| **Visual Risk** (Rủi ro thị giác) | Sản phẩm đầu ra có giao diện hiển thị cho người dùng không? | Vỡ layout, độ tương phản kém, giao diện cẩu thả |

---

## 3. 5 VERIFICATION ARCHETYPES

### 🔹 Archetype 1: Structural & Presence Check
- **Bản chất:** Kiểm tra sự tồn tại và tính hợp lệ của cấu trúc (File format, YAML frontmatter, headers, section counts).
- **Domain áp dụng:** Tất cả mọi domain.
- **Evidence:** File exists, Schema JSON valid, frontmatter parseable.

### 🔹 Archetype 2: Negative Completeness Matrix (Omission Detection)
- **Bản chất:** Kiểm tra **những gì đáng lẽ phải có nhưng bị thiếu**. Đối chiếu văn bản/code với một ma trận yêu cầu 2 chiều.
- **Domain áp dụng:** Legal Contract Review, Security Compliance, Technical Spec Audit, Research Papers.
- **Evidence:** Bảng đối chiếu `[Required Clause | Found/Missing | Severity | Line Citation]`.

### 🔹 Archetype 3: Deterministic Computation Guard
- **Bản chất:** Chặn đứng LLM tính nhẩm. Mọi phép toán thống kê, tỷ lệ phễu, ROI, định giá phải được tính bằng Python Script hoặc Spreadsheet Tool.
- **Domain áp dụng:** E-commerce Growth, Financial Analysis, Data Analytics, Performance Marketing.
- **Evidence:** Output log từ script Python thực thi phép tính (`python calc.py`).

### 🔹 Archetype 4: Transactional Mutation & Rollback Pattern
- **Bản chất:** Với các tác vụ đột biến (viết file, sửa code, deploy), bắt buộc tuân thủ 4 bước: `Snapshot State` $\rightarrow$ `Execute Mutation` $\rightarrow$ `Verify Invariant` $\rightarrow$ `Commit / Rollback on failure`.
- **Domain áp dụng:** DevOps, Database Migration, Refactor Codebase, System Administration.
- **Evidence:** Exit code 0 + Healthcheck pass; hoặc Rollback log khôi phục snapshot thành công.

---

## 4. MA TRẬN ÁNH XẠ DOMAIN $\rightarrow$ ARCHETYPES

| Domain | Archetypes Bắt Buộc | Checklist Generator Output |
|:---|:---|:---|
| **Content / Copywriting** | Presence + Negative Completeness (CTA, Tone) | Readability score, Banned Words list (anti-AI buzzwords), Word count |
| **Growth / E-commerce** | Presence + Deterministic Computation | Python metric verification script, Funnel math checker |
| **Legal / Compliance** | Presence + Negative Completeness Matrix | 2-way clause coverage checker, Risk severity tagger |
| **DevOps / System** | Presence + Transactional Mutation Safety | Healthcheck runner, Safety pre-hook, Rollback trigger |

| **Software Engineering** | Presence + Deterministic Tests + Mutation | Linter, Static type checker, Unit test runner, Security hook |
