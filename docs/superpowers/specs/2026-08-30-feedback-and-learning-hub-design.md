# Unified Feedback & Learning Hub Specification

> **Trạng thái:** FROZEN (Brainstorming Finalized)  
> **Ngày:** 2026-08-30  
> **Tác giả:** @kit-architect & Sếp  
> **Mục tiêu:** Nâng cấp toàn diện hệ thống Feedback & Learning của Agent Kit Builder tại `Downloads/Shared Workspace/Feedback/`, áp dụng Event Sourcing (Append-Only JSONL làm SSOT duy nhất), phân tách rõ 2 nguồn và 2 đối tượng đích (`source` + `target`), phân định nguồn gốc (`user` vs `system`), quản lý vòng đời nhị phân (`new` → `verified`), biến verified feedback thành regression knowledge phòng ngừa lỗi, và dỡ bỏ triệt để hệ thống feedback cũ cồng kềnh.

---

## 1. Triết Lý Cốt Lõi (Core Principles)

> **"Mọi phản hồi là một Event bất biến. JSONL là Single Source of Truth duy nhất. Chỉ đóng ticket khi có bằng chứng Verified. Mọi feedback đã verified trở thành Regression Knowledge phòng ngừa lỗi từ gốc."**

### 4 Câu Hỏi Bất Biến Cho Mọi Phản Hồi:
1. **Lỗi gì / Yêu cầu gì?** (`content` + `context`)
2. **Xảy ra ở đâu?** (`target: "agent_kit"` + `agent_kit` hoặc `target: "builder"`)
3. **Đã sửa chưa? Sửa ở đâu?** (`status == "fixed"` kèm `commit` / `version`)
4. **Đã thực sự giải quyết dứt điểm chưa?** (`status == "verified"` kèm `evidence`)

### 6 Nguyên Tắc Thiết Kế 80/20:
1. **JSONL Là Single Source of Truth (SSOT)**: Toàn bộ dữ liệu phản hồi nằm trong các file JSONL. `FEEDBACK_BOARD.md` CHỈ là một generated view được render lại bất kỳ lúc nào từ JSONL, tuyệt đối không coi board là nguồn sự thật.
2. **Append-Only Event Stream**: Không bao giờ sửa/ghi đè dòng cũ trong JSONL. Mỗi lần đổi trạng thái (`investigating`, `fixed`, `failed`, `retry`, `verified`) chỉ append 1 dòng event mới cùng `id`. Tránh hoàn toàn race condition, hỏng dữ liệu và mất dấu lịch sử.
3. **Tách Bạch Bằng `source` và `target`**:
   - `source`: `"user"` (người dùng phản ánh chất lượng/nghiệp vụ) vs `"system"` (lỗi crash runtime, timeout kỹ thuật).
   - `target`: `"agent_kit"` (phản hồi tới kit cụ thể) vs `"builder"` (chỉ đạo nâng cấp kiến trúc của Builder).
4. **`fixed` Không Đồng Nghĩa Là Xong**: Trạng thái `fixed` chỉ xác nhận đã có code patch hoặc commit. Ticket CHỈ được đóng khi đạt trạng thái `verified` (có bằng chứng thực nghiệm từ test hoặc xác nhận của sếp). Nếu tái kiểm thử thất bại: chuyển ngay `fixed` $\rightarrow$ `failed` $\rightarrow$ `retry` $\rightarrow$ `investigating`.
5. **Verified Feedback = Regression Knowledge**: Mọi feedback đã `verified` không nằm yên như một tấm vé lưu trữ chết, mà trở thành kho tri thức phòng ngừa (Pre-flight Immunity Knowledge). Khi Builder tạo hoặc nâng cấp Kit trong cùng domain, nó tự động đọc các lỗi cũ để **ngăn chặn lỗi xuất hiện ngay từ đầu**.
6. **Dỡ Bỏ Hệ Thống Cũ (Zero Debt)**: Khai tử hoàn toàn cơ chế 4 tầng Waterfall, inbox/outbox cồng kềnh và các file rác của hệ thống evolution cũ.

---

## 2. Bản Đồ Thư Mục Cây Toàn Cục

Nằm trực tiếp trong `Downloads/Shared Workspace/`:

```plaintext
Downloads/Shared Workspace/
├── 📥 _Dropzone/
├── 🏛️ Shared/
├── 🚀 Projects/
│
└── 📋 Feedback/
    ├── kit_feedback.jsonl       <-- [SSOT] Event stream cho phản hồi sử dụng Agent Kits
    ├── builder_feedback.jsonl   <-- [SSOT] Event stream cho chỉ đạo trực tiếp tới Builder
    └── FEEDBACK_BOARD.md        <-- [GENERATED VIEW] Tự động render từ JSONL, không phải SSOT
```

---

## 3. Cấu Trúc Dữ Liệu Event-Sourced (Data Schema)

### 3.1. Kit Feedback Event Schema (`kit_feedback.jsonl`)

Mỗi dòng trong JSONL là một JSON object độc lập đại diện cho một sự kiện (Event).

#### A. Event Khởi Tạo (`status: "new"`)
```json
{
  "event_id": "evt-20260830-153000-001",
  "id": "fb-kit-20260830-001",
  "source": "user",
  "target": "agent_kit",
  "agent_kit": "vietnamese-book-translator",
  "timestamp": "2026-08-30T15:30:00Z",
  "context": {
    "task": "translate_full",
    "input_file": "inputs/atomic-habits.epub",
    "error_signature": "chunk_dedup_overlap"
  },
  "content": "Dịch chương 3 bị lặp đoạn văn 2 lần ở đầu trang",
  "status": "new"
}
```

#### B. Event Chuyển Trạng Thái (`investigating` / `fixed` / `failed` / `retry`)
```json
{
  "event_id": "evt-20260830-160000-002",
  "id": "fb-kit-20260830-001",
  "timestamp": "2026-08-30T16:00:00Z",
  "status": "fixed",
  "resolution": {
    "commit": "a413720",
    "version": "v2.1.1",
    "fix_summary": "Tăng threshold kiểm tra overlap chunk deduplication"
  }
}
```

#### C. Event Xác Nhận Triệt Để (`status: "verified"`)
```json
{
  "event_id": "evt-20260830-163000-003",
  "id": "fb-kit-20260830-001",
  "timestamp": "2026-08-30T16:30:00Z",
  "status": "verified",
  "verification": {
    "verified_by": "user",
    "evidence": "Chạy lại bản dịch chương 3 không còn hiện tượng lặp đoạn văn",
    "regression_rule": "Luôn kiểm tra deduplication overlap threshold khi chia nhỏ markdown chapters"
  }
}
```

### 3.2. Builder Feedback Event Schema (`builder_feedback.jsonl`)

Dành riêng cho các yêu cầu, quy tắc thiết kế mà sếp giao trực tiếp cho Builder:
```json
{
  "event_id": "evt-20260830-170000-001",
  "id": "fb-bld-20260830-001",
  "source": "user",
  "target": "builder",
  "timestamp": "2026-08-30T17:00:00Z",
  "content": "Mọi Agent Kit sinh ra bắt buộc phải có card README 4 dòng và schema artifact_contracts",
  "scope": "creator_global",
  "status": "verified",
  "resolution": {
    "commit": "5a0a405",
    "version": "v2026.8.25",
    "evidence": "Đã cập nhật template và kiểm định qua test_templates.py"
  }
}
```

---

## 4. Máy Trạng Thái Vòng Đời (Lifecycle State Machine)

```
        ┌─────────────────────────────────────────────────────────────┐
        │                                                             │
        ▼                                                             │
     [ new ] ──► [ investigating ] ──► [ fixed ] ──┬──► [ verified ]  │
                                          ▲        │                  │
                                          │        └──► [ failed ] ───┘ (retry)
                                          └─────────────────┘
```

1. **`new`**: Phản hồi mới ghi nhận (từ user hoặc system auto-log khi crash).
2. **`investigating`**: Builder hoặc Agent đang phân tích root cause.
3. **`fixed`**: Đã áp dụng code patch, nâng version hoặc commit vá lỗi. **Chưa xong! Phải chờ kiểm chứng.**
4. **`verified`**: Đã kiểm chứng thực tế (User xác nhận hoặc test runner pass). Ticket chính thức đóng và chuyển vào **Regression Knowledge**.
5. **`failed`**: Đã vá nhưng khi chạy lại vẫn lỗi $\rightarrow$ chuyển tiếp ngay sang **`retry`** để mở lại vòng điều tra mới.

---

## 5. Bảng Điều Khiển Tự Động (`FEEDBACK_BOARD.md` - Generated View)

`FEEDBACK_BOARD.md` được script `feedback_hub.py` tự động render lại toàn bộ từ JSONL SSOT:

```markdown
# 📋 Feedback & Learning Dashboard (Generated View)

> ⚠️ Đây là bảng hiển thị tự động được sinh từ JSONL. Nguồn sự thật duy nhất nằm tại `kit_feedback.jsonl` và `builder_feedback.jsonl`.  
> Cập nhật tự động lúc: 2026-08-30 16:35:00 UTC

## 🚨 Kit Feedback: Cần Xử Lý (Active & Unverified)
| ID | Kit | Nguồn | Nội Dung | Trạng Thái | Fix Ref | Hành Động Tiếp Theo |
|:---|:---|:---|:---|:---|:---|:---|
| `fb-kit-001` | `vietnamese-book-translator` | 👤 user | Lặp đoạn văn ch.3 | `fixed` | `commit: a413720` | Chờ User / Test verify |
| `fb-kit-002` | `video-editing` | 🤖 system | Timeout render whisper | `new` | — | Phân tích root cause |

## 🛡️ Regression Knowledge: Đã Giải Quyết Triệt Để (Verified)
| ID | Kit | Nội Dung | Đã Sửa Ở | Verified Bởi | Bài Học Phòng Ngừa |
|:---|:---|:---|:---|:---|:---|
| `fb-kit-000` | `writing-book` | Lỗi thiếu frontmatter | `v3.0.0` | 👤 sếp (test passed) | Luôn validate YAML frontmatter trước khi xuất file |

## 🏛️ Builder Feedback (Chỉ Đạo Chiến Lược)
| ID | Nội Dung | Trạng Thái | Bằng Chứng Áp Dụng |
|:---|:---|:---|:---|
| `fb-bld-001` | Card README 4 dòng + artifact_contracts | `verified` | Commit `5a0a405` |
```

---

## 6. Cơ Chế Builder Tự Học & Tự Audit

Khi Builder kích hoạt (`/refactor-kit <kit-name>`, `/validate-kit <kit-name>`, `/create-kit`):

1. **Giai Đoạn Pre-flight Feedback & Knowledge Audit**:
   - Quét `kit_feedback.jsonl`, fold event theo `id`:
     - **Chưa giải quyết / Chưa verified**: Lọc các feedback của kit có latest `status != "verified"` (`new`, `investigating`, `failed`, `retry`, `fixed`). Bắt buộc đưa vào danh sách sửa chữa & kiểm thử.
     - **Regression Knowledge**: Lọc các feedback đã `verified` của kit hoặc domain tương ứng để đọc các `regression_rule`, chủ động chặn đứng lỗi ngay từ khâu thiết kế prompt/code.
   - Báo cáo rõ ràng:
     ```text
     ⚠️ [FEEDBACK_AUDIT] Kit có 1 lỗi fixed chưa verify (fb-kit-001) và 1 bài học phòng ngừa đã verified (fb-kit-000).
     → Builder sẽ kiểm chứng fb-kit-001 và áp dụng bài học của fb-kit-000 trong phiên làm việc này.
     ```
2. **Giai Đoạn Post-fix Verification Gate**:
   - Khi sửa xong: Tự động append event `status: "fixed"` kèm mã commit và version mới.
   - Khi kiểm thử thực tế pass: Append event `status: "verified"` kèm bằng chứng và bài học `regression_rule`.

---

## 7. Kế Hoạch Dỡ Bỏ Hệ Thống Cũ (Deprecation & Clean-up)

1. **Dỡ bỏ Workflows cồng kềnh**:
   - Xóa bỏ các file `/log-feedback.md`, `/submit-evolution.md`, `/process-evolution.md`.
   - Cập nhật `/refactor-kit` và `/evolve-kit` sang kết nối trực tiếp với `Downloads/Shared Workspace/Feedback/`.
2. **Dọn dẹp mã nguồn & thư mục rác**:
   - Xóa `evolution_submitter.py`, `evolution_engine.py`, `feedback_collector.py` cũ, và thư mục `evolution/inbox/`, `evolution/outbox/`.
   - Thay thế bằng **1 script duy nhất**: `.agents/scripts/feedback_hub.py` (Append event, Fold state, Render Board, Query pending/regression knowledge).
3. **Cập nhật Manifest SSOT & Dependency Graph**:
   - Đồng bộ hóa registry, loại bỏ các references chết và tái sinh lockfile sạch sẽ.
