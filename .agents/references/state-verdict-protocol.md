# State & Verdict Staleness Protocol (CANON 5)

> Giao thức quản lý trạng thái, phiên bản nội dung và chống thoái hóa phán quyết ngữ nghĩa (Semantic Verdict Staleness).

---

## 1. Cấu trúc Bản ghi Phán quyết (Verdict Record)

Mỗi phán quyết ngữ nghĩa trong State bắt buộc gắn liền với phiên bản nội dung (`content_version`):

```json
{
  "verdict_key": "voice_consistent.chapter_3",
  "value": true,
  "evaluator": "developmental-editor",
  "content_version": "v7",
  "timestamp": "2026-08-26T01:30:00Z",
  "stale": false
}
```

---

## 2. Giao thức Vô hiệu hóa Tự động (Staleness Invalidation Protocol)

Khi BẤT KỲ thao tác chỉnh sửa (mutation) nào tác động lên nội dung mà phán quyết tham chiếu:

1. **Auto-Increment Version**: `content_version` của nội dung tự động tăng (ví dụ: `"v7"` $\rightarrow$ `"v8"`).
2. **Auto-Mark Stale**: Mọi phán quyết mang `content_version` cũ (`"v7"`) tự động bị đánh dấu `stale = true`.
3. **Router Blindness**: Router coi `stale == true` tương đương với **phán quyết chưa tồn tại**.
4. **Re-evaluation Scheduling**: Nếu capability yêu cầu phán quyết này làm precondition, Router từ chối chọn capability và kích hoạt Workflow lên lịch re-evaluation qua Evaluator Agent.

---

## 3. Ranh giới Ad-hoc Task & State Mutation

- **Ad-hoc Task**: Được phép chỉnh sửa nội dung nhưng **tuyệt đối KHÔNG được trực tiếp ghi đè `workflow.*` state transitions**.
- Mọi mutation từ ad-hoc task vẫn kích hoạt tăng `content_version` và vô hiệu hóa verdict stale.
