# Unified Feedback & Learning Hub Specification

> **Trạng thái:** FROZEN & OPTIMIZED (Deep Audit Finalized)  
> **Ngày:** 2026-08-30  
> **Tác giả:** @kit-architect & Sếp  
> **Mục tiêu:** Nâng cấp toàn diện kiến trúc Shared Workspace & Feedback Hub tại `Downloads/Shared Workspace/`, áp dụng Event Sourcing (Append-Only JSONL làm SSOT duy nhất), đóng băng 3 Invariant bất biến, chống rò rỉ file trung gian bằng Whitelist Contract, bảo vệ Concurrency bằng File Lock, và biến verified feedback thành Regression Knowledge phòng ngừa lỗi từ gốc.

---

## 1. Triết Lý Cốt Lõi & 3 Invariants Bất Biến

> **"Không declared → Không được xuất vào outputs."**  
> **"Không evidence → Không được verified."**  
> **"Không lock → Không được concurrent-write feedback."**

### 4 Câu Hỏi Bất Biến Cho Mọi Phản Hồi:
1. **Lỗi gì / Yêu cầu gì?** (`content` + `context`)
2. **Xảy ra ở đâu?** (`target: "agent_kit"` + `agent_kit` hoặc `target: "builder"`)
3. **Đã sửa chưa? Sửa ở đâu?** (`status == "fixed"` kèm `commit` / `version`)
4. **Đã thực sự giải quyết dứt điểm chưa?** (`status == "verified"` kèm `evidence`)

### 6 Nguyên Tắc Vận Hành 80/20:
1. **Whitelist Outputs (Không declared → Không xuất ra outputs)**:
   - Agent chỉ được phép ghi thành phẩm sạch vào `outputs/` nếu artifact đó khớp với định nghĩa trong hợp đồng `manifest.artifact_contracts.produces` (hoặc Output DoD).
   - Mọi file trung gian (intermediate, chunk, temporary, debug log, cache) **bắt buộc nhốt trong `.workspace/`**. Sanitizer đóng vai trò lớp bảo vệ thứ 2 để chặn đứng extension rác (`.tmp`, `.log`, `.cache`, `.*`).
2. **Lock-Protected Append-Only JSONL (Không lock → Không ghi)**:
   - File JSONL là Single Source of Truth (SSOT).
   - Mọi thao tác ghi/append vào `kit_feedback.jsonl` hoặc `builder_feedback.jsonl` **bắt buộc phải qua File Lock** (cross-platform atomic lock) kết hợp `flush()` và `os.fsync()` để ngăn chặn race condition khi nhiều process/agent cùng ghi dữ liệu.
3. **Hard Verification Gate (Không evidence → Không verified)**:
   - Trạng thái `fixed` chưa bao giờ là xong. Ticket chỉ được đóng khi chuyển sang `status: "verified"`.
   - Hàm ghi event **BẮT BUỘC REJECT** nếu event `verified` thiếu trường `evidence` (chứng cứ kiểm thử, lệnh test pass hoặc xác nhận của sếp). Nếu tái kiểm thử thất bại: `fixed` $\rightarrow$ `failed` $\rightarrow$ `retry` $\rightarrow$ `investigating`.
4. **Versioned Shared Promotion (Không overwrite âm thầm)**:
   - Khi chia sẻ (promote) thành phẩm từ `Projects/<Project>/outputs/` lên `Shared/`, luôn sử dụng lệnh COPY, tuyệt đối không MOVE (giữ nguyên tính toàn vẹn của dự án gốc).
   - Nếu tài nguyên đã tồn tại trong `Shared/`, không được ghi đè âm thầm mà phải đánh dấu version rõ ràng (ví dụ: `book-vi-v2.epub`).
5. **Zero-Copy Direct Read**:
   - Khi cần tài nguyên từ `_Dropzone/` hoặc `Shared/`, Agent đọc trực tiếp từ đường dẫn gốc. Tuyệt đối không copy file nặng (video, sách) sang `inputs/` để tránh lãng phí dung lượng ổ đĩa và I/O vô ích.
6. **Purgeable `.workspace/`**:
   - Vùng `.workspace/` là khu vực nháp tạm thời. User hoặc tiện ích dọn dẹp có thể xóa sạch `.workspace/` bất kỳ lúc nào mà không sợ mất mát dữ liệu đầu vào (`inputs/`) hay thành phẩm cuối cùng (`outputs/`).

---

## 2. Bản Đồ Thư Mục Cây Toàn Cục

Nằm trực tiếp trong `Downloads/Shared Workspace/`:

```plaintext
Downloads/Shared Workspace/
│
├── 📥 _Dropzone/              ← Zero-Copy Direct Read (Agent chỉ đọc trực tiếp, không copy bừa bãi)
│
├── 🏛️ Shared/                 ← Thư viện dùng chung (Bản copy đã publish, version rõ ràng, không overwrite)
│   ├── Books/
│   ├── Videos/
│   └── Files/
│
├── 🚀 Projects/               ← Không gian dự án độc lập
│   └── <Project-Name>/
│       ├── inputs/          ← Tài liệu đầu vào của dự án (User sở hữu, không tự ý xóa)
│       ├── outputs/         ← [CONTRACT WHITELIST] Thành phẩm sạch (Khớp artifact_contracts)
│       └── .workspace/      ← [PURGEABLE] Intermediate, chunks, logs (Agent tự do ghi, thoải mái xóa)
│
└── 📋 Feedback/               ← Central Feedback & Learning Hub (SSOT)
    ├── kit_feedback.jsonl     ← [SSOT: LOCK + APPEND + FSYNC] Phản hồi thực chiến từ Agent Kits
    ├── builder_feedback.jsonl ← [SSOT: LOCK + APPEND + FSYNC] Chỉ đạo chiến lược sếp giao Builder
    └── FEEDBACK_BOARD.md      ← [GENERATED VIEW + HASH-GUARD] Tự động render, không rác I/O
```

---

## 3. Cấu Trúc Dữ Liệu & Ràng Buộc Hợp Đồng

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

#### B. Event Đổi Trạng Thái Sửa Lỗi (`status: "fixed"`)
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

#### C. Event Tái Kiểm Thử Thất Bại (`status: "failed"` / `"retry"`)
```json
{
  "event_id": "evt-20260830-161500-003",
  "id": "fb-kit-20260830-001",
  "timestamp": "2026-08-30T16:15:00Z",
  "status": "failed",
  "note": "Kiểm tra lại chương 3 vẫn còn lặp ở trang 12",
  "failed_attempt": {
    "commit": "a413720",
    "reason": "Chưa xử lý trường hợp page break giữa chừng"
  }
}
```

#### D. Event Nghiệm Thu Triệt Để (`status: "verified"` - BẮT BUỘC CÓ EVIDENCE)
```json
{
  "event_id": "evt-20260830-163000-004",
  "id": "fb-kit-20260830-001",
  "timestamp": "2026-08-30T16:30:00Z",
  "status": "verified",
  "verification": {
    "verified_by": "user",
    "evidence": "Chạy lại toàn bộ chương 3 và chương 4, đối soát 0 câu trùng lặp",
    "regression_rule": "Luôn kiểm tra deduplication overlap threshold khi chia nhỏ markdown chapters"
  }
}
```
> ⚠️ **Hàm `append_event` sẽ ném ngoại lệ (REJECT)** nếu `status == "verified"` nhưng trường `verification.evidence` bị rỗng.

---

## 4. Máy Trạng Thái Vòng Đời Hoàn Chỉnh

```
        ┌─────────────────────────────────────────────────────────────┐
        │                                                             │
        ▼                                                             │
     [ new ] ──► [ investigating ] ──► [ fixed ] ──┬──► [ verified ]  │
                                          ▲        │    (Evidence OK) │
                                          │        │                  │
                                          │        └──► [ failed ] ───┘
                                          │               │
                                          └─ [ retry ] ◄──┘
```

1. **`new`**: Phản hồi mới ghi nhận.
2. **`investigating`**: Đang phân tích root cause.
3. **`fixed`**: Đã áp dụng commit/version vá lỗi. **(CHƯA XONG)**
4. **`failed`**: Kiểm thử lại thất bại $\rightarrow$ lưu vết `failed_attempt`.
5. **`retry`**: Mở lại vòng điều tra mới $\rightarrow$ `investigating`.
6. **`verified`**: Cung cấp đủ `evidence` thực nghiệm. Ticket đóng, lưu thành **Regression Knowledge**.

---

## 5. Cơ Chế Chống Xung Đột & Concurrency (Locking Protocol)

Để đảm bảo không bị lỗi đè file trên Windows hoặc Linux khi nhiều Agent/Process cùng ghi JSONL:
1. **FileLock Context Manager**: Sử dụng cơ chế khóa file dựa trên atomic lockfile (`.lock`) và kiểm tra PID / stale lock timeout (3 giây).
2. **Write Sequence**:
   `Acquire Lock` $\rightarrow$ `Open(append)` $\rightarrow$ `Write JSON` $\rightarrow$ `f.flush()` $\rightarrow$ `os.fsync()` $\rightarrow$ `Close` $\rightarrow$ `Release Lock`.
3. **Zero Polling Lock Wait**: Thử khóa tối đa 10 lần (mỗi lần ngủ 50ms). Nếu quá thời gian, báo lỗi rõ ràng thay vì treo vĩnh viễn.

---

## 6. Cơ Chế Whitelist Outputs & Sanitization

1. **Artifact Whitelist**:
   - Khi Agent tạo sản phẩm vào `outputs/`, kiểm tra với khai báo `artifact_contracts.produces` trong `manifest.json`.
   - Nếu artifact không nằm trong hợp đồng hoặc là file tạm, script/agent phải chuyển nó vào `.workspace/`.
2. **Sanitizer Rule trong L1 Linter**:
   - Quét thư mục `outputs/`: Cấm mọi file có đuôi `.tmp`, `.log`, `.cache`, `.chunk`, `.part`, `.bak` hoặc bắt đầu bằng dấu chấm `.*`.
