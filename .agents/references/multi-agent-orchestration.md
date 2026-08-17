# Multi-Agent Orchestration & Suite Architecture

> Cẩm nang thiết kế và điều phối hệ thống nhiều Agent (Suite Kits / Multi-Agent Systems) — chuẩn hóa Lead Orchestrator Protocol và cơ chế phân rã nhiệm vụ.

---

## 1. VAI TRÒ CỦA LEAD ORCHESTRATOR

Trong hệ thống Suite Kit có 2+ agent chuyên biệt, **1 Lead Orchestrator duy nhất** giữ quyền kiểm soát:
1. **Pre-flight Check**: Kiểm tra môi trường và file kế hoạch trước khi phân rã task.
2. **Socratic Gate**: Phân loại loại dự án, hỏi làm rõ từ 1-3 câu nếu yêu cầu mơ hồ; nếu rõ ràng thì hành động ngay.
3. **Domain Boundary Enforcement**: Ngăn chặn worker can thiệp chéo sang vùng trách nhiệm của agent khác.
4. **Synthesis & Context Compression**: Tổng hợp báo cáo cuối cùng từ các worker mà không làm phình context.

---

## 2. STRICT DOMAIN BOUNDARY MATRIX & FILE OWNERSHIP

Mọi Suite Kit phải định nghĩa rõ ma trận phân quyền:

| Agent | Vùng trách nhiệm (Scope) | Quyền sở hữu File (Ownership Pattern) | Điều TUYỆT ĐỐI KHÔNG LÀM |
|:---|:---|:---|:---|
| **Lead Orchestrator** | Điều phối, giao việc, tổng hợp | `manifest.json`, `orchestrator.md` | Không tự viết code chi tiết thay worker |
| **Frontend Worker** | UI/UX, components, styling | `src/components/**`, `src/styles/**` | Không sửa đổi backend DB schema |
| **Backend Worker** | API, database, business logic | `src/api/**`, `src/db/**` | Không can thiệp vào CSS/frontend layouts |
| **Test Engineer** | Unit test, integration, E2E | `tests/**`, `*.spec.ts` | Không tự sửa production code nếu chưa báo cáo |

*Giao thức chuyển giao:* Nếu worker phát hiện task thuộc domain của agent khác ➔ Dừng lại và yêu cầu Orchestrator chuyển tiếp.

---

## 3. NATIVE AGENT INVOCATION: FORK VS SPAWN

- **Fork Semantics**: Kế thừa ngữ cảnh hiện tại. Phù hợp cho Research song song hoặc lấy góc nhìn độc lập thứ 2.
- **Spawn Semantics**: Khởi tạo Agent mới hoàn toàn với System Prompt chuyên biệt. Phù hợp cho việc thực thi sâu theo domain.
- **Quy tắc Vàng chỉ đạo Worker (Worker Prompt Golden Rule)**:
  - ❌ *Sai:* "Hãy kiểm tra và sửa lỗi auth giúp tôi."
  - ✅ *Đúng:* "Sửa lỗi ở file `src/auth/jwt.ts` dòng 45: kiểm tra hết hạn dùng `<` thay vì `<=`. Đổi từ `if (now < expiry)` thành `if (now <= expiry)`."
