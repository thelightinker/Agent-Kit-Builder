# Workflow Error Resilience & Long-Running Sessions

> Cẩm nang xử lý lỗi, kiểm soát luồng và cơ chế duy trì phiên làm việc dài hạn (Long-Running Sessions) cho Agent Workflows.

---

## 1. GIAO THỨC VẬN HÀNH ĐA-PHIÊN (LONG-RUNNING SESSIONS)

Khi một tác vụ vượt quá 1 context window (chạy nhiều giờ hoặc nhiều phiên làm việc), việc nén context (Compaction) là không đủ. Cần tách bạch 2 vai trò:

| Vai trò | Thời điểm thực thi | Trách nhiệm cốt lõi |
|:---|:---|:---|
| **Initializer Agent** | Chạy 1 lần duy nhất ở phiên đầu | Dựng toàn bộ danh mục tính năng (Feature List dạng JSON), tạo cấu trúc thư mục, tạo baseline commit. |
| **Coding / Worker Agent** | Chạy ở mỗi phiên tiếp theo | Đọc trạng thái, chọn ĐÚNG 1 feature chưa hoàn thành có ưu tiên cao nhất, thực hiện xong, kiểm thử và commit trạng thái sạch. |

### Quản lý trạng thái qua JSON Feature List:
Lưu danh sách tính năng ra file `features.json` với trạng thái `pending`, `in_progress`, `completed` — đóng vai trò là Definition of Done ở cấp độ file ngoài context window.

---

## 2. KIỂM SOÁT LỖI & ESCALATION (HUMAN AS A TOOL)

### Human in the Loop như một Tool Call:
Khi gặp bế tắc, thiếu quyền truy cập hoặc thất bại vượt quá Max Retry:
- Kích hoạt cơ chế `[ESCALATE_HUMAN]`.
- Trả về câu hỏi cụ thể kèm bối cảnh tối thiểu cần thiết để người dùng ra quyết định.
- Gắn cờ `needs_human_review: true` thay vì đoán mò hoặc dừng vô thời hạn.

### Idempotency (Tính bất biến khi chạy lại):
Mọi bước trong workflow phải có tính idempotent — chạy lại nhiều lần với cùng input không tạo ra side-effect ngoài ý muốn hoặc làm nhân bản dữ liệu rác.

---

## 3. PHÒNG NGỪA VÒNG LẶP VÔ HẠN (DEADLOCK & INFINITE HANDOFF)

- **Infinite Handoff Loop ($A \rightarrow B \rightarrow C \rightarrow A$)**: Xảy ra khi không agent nào sở hữu trách nhiệm cuối cùng. Phòng ngừa bằng cách bắt buộc **1 Lead Agent duy nhất** giữ quyền tổng hợp và ra quyết định kết thúc.
- **Max Retry Threshold**: Luôn đặt giới hạn thử lại tối đa (mặc định = 2 lần cho mỗi node).
- **Graceful Degradation**: Khi mất kết nối hoặc thiếu dữ liệu ngoài, trả kết quả hữu ích nhất có thể kèm nhãn cảnh báo rõ ràng `[DỮ LIỆU CHƯA XÁC MINH]`.
