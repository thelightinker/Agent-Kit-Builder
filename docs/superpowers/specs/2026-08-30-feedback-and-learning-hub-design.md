# Unified Feedback & Learning Hub Specification

> **Trạng thái:** DRAFT (Brainstorming Complete)  
> **Ngày:** 2026-08-30  
> **Tác giả:** @kit-architect & Sếp  
> **Mục tiêu:** Nâng cấp toàn diện hệ thống Feedback & Learning của Agent Kit Builder tại `Downloads/Shared Workspace/Feedback/`, áp dụng Event Sourcing (Append-Only JSONL), phân tách rõ 2 nguồn (Kit Feedback vs. Builder Feedback), phân định nguồn gốc (`user` vs `system`), quản lý vòng đời chặt chẽ (`new` → `verified`), và dỡ bỏ triệt để hệ thống feedback cũ cồng kềnh.

---

## 1. Triết Lý Cốt Lõi (Core Principles)

> **"Mọi phản hồi là một Event bất biến. Trạng thái hiện tại là tổng hòa của lịch sử. Chỉ đóng ticket khi có bằng chứng Verified."**

### 4 Câu Hỏi Bất Biến Cho Mọi Phản Hồi:
1. **Lỗi gì / Yêu cầu gì?** (`content` + `context`)
2. **Xảy ra ở đâu?** (`agent_kit` hoặc `builder`)
3. **Đã sửa chưa? Sửa ở đâu?** (`status == "fixed"` kèm `commit` / `version`)
4. **Đã thực sự giải quyết dứt điểm chưa?** (`status == "verified"` kèm `evidence`)

### 5 Nguyên Tắc Thiết Kế 80/20:
1. **Append-Only Event Stream**: Không bao giờ sửa/ghi đè dòng cũ trong JSONL. Mỗi lần đổi trạng thái (`investigating`, `fixed`, `failed`, `retry`, `verified`) chỉ append 1 dòng event mới cùng `id`. Tránh hoàn toàn race condition, hỏng dữ liệu và mất dấu lịch sử.
2. **Tách Biệt 2 Nguồn Dữ Liệu**:
   - **`kit_feedback.jsonl`**: Phản hồi, lỗi, ma sát thực chiến phát sinh khi chạy từng Agent Kit.
   - **`builder_feedback.jsonl`**: Chỉ đạo chiến lược, yêu cầu trực tiếp sếp giao cho Agent Kit Builder.
3. **Phân Biệt Nguồn Gốc (`user` vs `system`)**: Tách rõ lỗi crash hệ thống (như API timeout, network drop) khỏi phản hồi của người dùng về chất lượng nghiệp vụ để Builder không nhầm lẫn khi học hỏi.
4. **Auto-Audit Trước Khi Sửa**: Khi Builder mở một Kit để refactor hoặc nâng cấp, Builder **BẮT BUỘC** đọc toàn bộ feedback chưa giải quyết và các bản fix chưa verified của Kit đó để lập danh sách kiểm thử hồi quy.
5. **Dỡ Bỏ Hệ Thống Cũ (Zero Debt)**: Khai tử hoàn toàn cơ chế 4 tầng Waterfall, inbox/outbox cồng kềnh và các file rác của hệ thống evolution cũ.

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
    ├── kit_feedback.jsonl       <-- Event stream cho mọi phản hồi của các Agent Kit
    ├── builder_feedback.jsonl   <-- Event stream cho các yêu cầu chỉ đạo tới Builder
    └── FEEDBACK_BOARD.md        <-- Bảng Kanban Markdown tự động render từ event stream
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
  "agent_kit": "vietnamese-book-translator",
  "source": "user",
  "timestamp": "2026-08-30T15:30:00Z",
  "context": {
    "task": "translate_full",
    "input_file": "inputs/atomic-habits.epub",
    "error_signature": "timeout_or_overlap"
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
    "evidence": "Chạy lại bản dịch chương 3 không còn hiện tượng lặp đoạn văn"
  }
}
```

### 3.2. Builder Feedback Event Schema (`builder_feedback.jsonl`)

Dành riêng cho các yêu cầu, quy tắc thiết kế mà sếp giao trực tiếp cho Builder:
```json
{
  "event_id": "evt-20260830-170000-001",
  "id": "fb-bld-20260830-001",
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
3. **`fixed`**: Đã áp dụng code patch, nâng version hoặc commit vá lỗi. **Chưa được coi là xong!**
4. **`verified`**: Đã kiểm chứng thực tế (User xác nhận hoặc chạy pass bài test tái hiện lỗi). Ticket chính thức đóng.
5. **`failed`**: Đã vá nhưng khi chạy lại vẫn lỗi $\rightarrow$ chuyển tiếp ngay sang **`retry`** để lập vòng điều tra mới.

---

## 5. Bảng Điều Khiển Tự Động (`FEEDBACK_BOARD.md`)

Mỗi khi có event mới được ghi vào JSONL, script `feedback_hub.py` tự động đọc, fold (gộp event theo `id` để lấy trạng thái mới nhất) và render ra bảng:

```markdown
# 📋 Feedback & Learning Dashboard

> Cập nhật tự động lúc: 2026-08-30 16:35:00 UTC

## 🚨 Kit Feedback: Cần Xử Lý (Active & Unverified)
| ID | Kit | Nguồn | Nội Dung | Trạng Thái | Fix Ref | Cần Làm |
|:---|:---|:---|:---|:---|:---|:---|
| `fb-kit-001` | `vietnamese-book-translator` | 👤 user | Lặp đoạn văn ch.3 | `fixed` | `commit: a413720` | Chờ User / Test verify |
| `fb-kit-002` | `video-editing` | 🤖 system | Timeout render whisper | `new` | — | Phân tích root cause |

## ✅ Kit Feedback: Đã Giải Quyết Triệt Để (Verified)
| ID | Kit | Nội Dung | Đã Sửa Ở | Verified Bởi |
|:---|:---|:---|:---|:---|
| `fb-kit-000` | `writing-book` | Lỗi thiếu frontmatter | `v3.0.0` | 👤 sếp (test passed) |

## 🏛️ Builder Feedback (Chỉ Đạo Chiến Lược)
| ID | Nội Dung | Trạng Thái | Bằng Chứng Áp Dụng |
|:---|:---|:---|:---|
| `fb-bld-001` | Card README 4 dòng + artifact_contracts | `verified` | Commit `5a0a405` |
```

---

## 6. Cơ Chế Builder Tự Học & Tự Audit

Khi Builder kích hoạt (`/refactor-kit <kit-name>`, `/validate-kit <kit-name>`, `/create-kit`):

1. **Giai Đoạn Pre-flight Feedback Audit**:
   - Quét `kit_feedback.jsonl`, lọc danh sách feedback của kit đang xử lý có trạng thái khác `verified`:
     - Nhóm 1: `new`, `investigating`, `failed`, `retry` (Chưa sửa).
     - Nhóm 2: `fixed` (Đã sửa nhưng chưa kiểm chứng).
   - In cảnh báo nổi bật:
     ```text
     ⚠️ [FEEDBACK_AUDIT] Phát hiện 2 lỗi chưa dứt điểm của kit:
     - fb-kit-001: Lặp đoạn văn ch.3 (fixed @ a413720 -> Chưa verified!)
     - fb-kit-002: Timeout whisper (new)
     → Builder bắt buộc đưa 2 lỗi này vào Verification Checklist của đợt refactor này.
     ```
2. **Giai Đoạn Post-fix Verification Gate**:
   - Khi hoàn thành sửa đổi code:
     - Tự động append event `status: "fixed"` kèm mã commit và version mới.
     - Nếu có test case kiểm thử pass $\rightarrow$ Tự động append event `status: "verified"` kèm bằng chứng.

---

## 7. Kế Hoạch Dỡ Bỏ Hệ Thống Cũ (Deprecation Plan)

Loại bỏ hoàn toàn các cấu phần cồng kềnh không cần thiết của hệ thống evolution cũ:
1. **Dỡ bỏ Workflows**:
   - Xóa `/log-feedback`, `/submit-evolution`, `/process-evolution`.
   - Cập nhật workflow `/refactor-kit` và `/evolve-kit` để tiêu thụ trực tiếp từ `Shared Workspace/Feedback/`.
2. **Dỡ bỏ Scripts & Thư Mục Rác**:
   - Xóa `evolution_submitter.py`, `feedback_collector.py` cũ, `evolution/inbox/`, `evolution/outbox/`.
   - Thay thế bằng duy nhất một script tinh gọn: `.agents/scripts/feedback_hub.py` (chịu trách nhiệm: Append event, Fold state, Render `FEEDBACK_BOARD.md`, Query pending feedback).
3. **Cập Nhật Manifest & Graph**:
   - Xóa bỏ các workflow cũ khỏi `manifest.json` và tái sinh `DEPENDENCY_GRAPH.md`.
