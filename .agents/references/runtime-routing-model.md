# Runtime Routing Model (6 Roles Architecture)

> Mô hình điều phối và ra quyết định thời gian thực trong Agent Kit.

---

## 1. Bản Đồ 6 Vai Trò (The Six Roles)

Hệ thống phân rã rạch ròi thành 6 vai trò:

| Vai Trò | Bản Chất | Thẩm Quyền | Giới Hạn Cấm |
|:---|:---|:---|:---|
| **Workflow** (Constitution) | Hiến pháp hệ thống | Khai báo mục tiêu cần đạt (`required_outcome`), Invariants, Human Gates | ❌ Cấm chỉ định tên Agent / Cách làm (`how`) |
| **Router** (Strategist) | Bộ não chiến lược | Đọc State + `routing_index.json` $\rightarrow$ Chọn Capability tối ưu | ❌ Cấm tự gọi Evaluator (CANON 2) |
| **Invariant Guard** (Referee) | Trọng tài kiểm soát | Duyệt routing decision đối chiếu với Global Invariants & Negative Scopes | ❌ Không dùng AI inference (Compiled Rules) |
| **Agent** (Executor) | Chuyên gia thực thi | Nạp Skill, thao tác file trong Positive Scope, xuất Evidence | ❌ Cấm tự quyết định kiến trúc hệ thống |
| **State** (Truth) | Nguồn sự thật | Lưu trữ Facts, Metrics, Verdicts kèm `content_version` | ❌ Không phải là log tự do |
| **Evidence** (Proof) | Bằng chứng nghiệm thu | Khớp `evidence_schema`, chứng minh kết quả thực thi | ❌ Cấm nghiệm thu bằng phỏng đoán |

---

## 2. Vòng đời Xử lý Task (Execution Flow)

```
User Input
    │
    ▼
Intent Normalizer (LLM: chuẩn hóa input thành canonical_intent)
    │
    ▼
Task Classifier (Compiled rules: phân loại workflow_bound vs ad_hoc)
    │
    ▼
Router (Đọc State + routing_index.json → chọn capability + emit routing_rationale)
    │
    ▼
Invariant Guard (Kiểm tra global invariants + negative boundaries → APPROVE / BLOCK)
    │
    ▼
Agent Execution (Nạp Skill → thực thi → xuất Evidence)
    │
    ▼
Evidence Validation (Kiểm tra structural schema & semantic evaluation)
    │
    ▼
State Update & Workflow Transition (Cập nhật State → Invalidate stale verdicts → Chuyển Node)
```
