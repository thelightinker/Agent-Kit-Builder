# Orchestrator Agent Pattern (Master Orchestrator Protocol)

> Hướng dẫn chuẩn hóa việc thiết kế và biên dịch **Agent Điều Phối (Orchestrator Agent / Lead Agent)** cho các bộ Agent Kit nhiều agent (Suite Kits / Multi-Agent Systems).

---

## 🎯 Mục đích & Phạm vi

Khi thiết kế một bộ **Suite Kit** hoặc hệ thống Multi-Agent có 2+ agent phối hợp, Agent Điều phối (**Orchestrator**) giữ vai trò như "Nhạc trưởng". Agent này chịu trách nhiệm:
1. **Kiểm tra khả năng & Ngữ cảnh khởi tạo (Pre-flight Check & Socratic Gate)**.
2. **Bảo vệ Ranh giới Agent (Domain Boundary Enforcement)** - ngăn chặn worker agent can thiệp chéo sang vùng trách nhiệm của nhau.
3. **Phát lệnh theo Chế độ Coordinator (Coordinator Mode)** - điều phối song song (Research/Verification) và tuần tự (Implementation).
4. **Chỉ đạo Worker bằng Quy tắc Vàng (Worker Prompt Golden Rule)** - chỉ định rõ đường dẫn file, dòng code, nội dung thay đổi thay vì câu lệnh mơ hồ.
5. **Tổng hợp & Nén Ngữ cảnh (Synthesis & Context Compression)** - giữ bối cảnh làm việc tinh gọn trong các nhiệm vụ phức tạp.

---

## 📐 Cấu trúc 6 Thành phần Cốt lõi của Orchestrator Prompt

Mọi System Prompt của Agent Điều phối BẮT BỘC tuân thủ cấu trúc sau:

### 1. Frontmatter
```yaml
---
name: orchestrator
description: "Multi-agent coordination and task orchestration with coordinator mode. Use when a task requires multiple perspectives, parallel analysis, or coordinated execution across domains."
tools: [Read, Grep, Glob, Bash, Write, Edit, Agent]
model: inherit
version: 1.0.0
skills: [coordinator-mode, parallel-agents, plan-writing, memory-system, context-compression, verify-changes]
---
```

### 2. Runtime Capability & Pre-flight Check (Step 0)
- **Runtime Check**: Đọc `ARCHITECTURE.md` hoặc danh sách script/skill hiện có để chuẩn bị kích hoạt.
- **Phase 0 Check**: Đọc file kế hoạch `{task-slug}.md` hoặc bối cảnh workspace trước khi phân rã task.
- **Fallback Chống Deadlock**: Nếu thiếu file plan, tự sinh plan ngắn gọn hoặc gọi `project-planner` agent - KHÔNG ĐƯỢC dừng vô thời hạn.

### 3. Socratic Gate (Làm rõ trước khi Điều phối)
- Phân loại Project Type (`WEB`, `MOBILE`, `BACKEND`).
- Nếu yêu cầu mơ hồ, hỏi từ 1-3 câu làm rõ về Scope, Priority, Tech Stack, Design, Constraints.
- Quy tắc "Don't over-ask": Nếu yêu cầu đã đủ rõ, bắt tay thực thi ngay.

### 4. Ranh giới Agent & Quyền Sở hữu File (Strict Domain Boundary Matrix)
Thiết lập bảng phân vùng nghiêm ngặt cho các agent chuyên biệt:
- **Domain Matrix**: Ghi rõ từng Agent **CÓ THỂ LÀM GI** và **KHÔNG ĐƯỢC LÀM GI**.
- **File Ownership Pattern**: Khai báo pattern đường dẫn file thuộc về agent nào (ví dụ: `**/*.test.*` thuộc `test-engineer`, `**/components/**` thuộc `frontend-specialist`).
- **Giao thức Thực thi**: Nếu worker chuẩn bị ghi file thuộc domain của agent khác ➔ DỪNG LẠI và chuyển giao (Reroute) cho agent đúng chủ thể.

### 5. Native Agent Invocation & Coordinator Mode Protocol
- **Cú pháp gọi agent**: Single, Sequential, Chaining with Context, Resume Agent.
- **Fork vs Spawn Semantics**:
  - **Fork**: Kế thừa ngữ cảnh hiện tại. Phù hợp cho Research song song hoặc lấy ý kiến thứ 2.
  - **Spawn**: Khởi tạo Agent mới tinh với System Prompt chuyên biệt. Phù hợp cho công việc sâu theo domain.
- **Quy tắc Fork không block**: Không peek output giữa chừng, chờ thông báo hoàn thành từ hệ thống.
- **Worker Prompt Golden Rule**:
  - ❌ *Sai*: "Dựa trên phát hiện, hãy fix bug giúp tôi."
  - ✅ *Đúng*: "Bug ở file `src/auth/jwt.ts` dòng 45 — kiểm tra hết hạn dùng `<` thay vì `<=`. Đổi dòng 45 từ `if (now < expiry)` thành `if (now <= expiry)`."

### 6. Vòng đời Coordinator & Báo cáo Tổng hợp (Synthesis Report)
1. **Phân rã (Decompose)** ➔ 2. **Phân loại (Classify)** ➔ 3. **Điều phối (Dispatch)** ➔ 4. **Theo dõi (Monitor)** ➔ 5. **Tổng hợp (Synthesize)** ➔ 6. **Xác minh (Verify)**.
- **Quy tắc Song song**:
  - *Research & Verification*: Chạy song song tối đa (Fully parallel).
  - *Synthesis*: Chỉ do Coordinator thực hiện.
  - *Implementation*: Chạy tuần tự theo từng file để tránh xung đột state.
- **Format Output**: Báo cáo tổng hợp kết quả (Tasks finished, Agent findings, Recommendations, Next steps).

---

## 🛠️ Quy trình Kiểm định (Definition of Done cho Orchestrator Prompt)

Mọi Orchestrator Agent Prompt do Agent Kit Creator tạo ra phải vượt qua checklist:

- [ ] **Khai báo `Agent` tool** trong frontmatter để có năng lực điều phối subagent.
- [ ] **Có Step 0 Pre-flight Check** để verify plan file và phòng tránh deadlock.
- [ ] **Có Bảng Ranh giới (Boundary Matrix)** và **Bảng Quyền sở hữu File (File Ownership Patterns)**.
- [ ] **Có Quy tắc Vàng cho Prompt của Worker Agent (Worker Prompt Golden Rule)**.
- [ ] **Có phân biệt rõ Fork (thừa kế context) và Spawn (khởi tạo specialist)**.
- [ ] **Có cơ chế Nén ngữ cảnh (Context Compression) và Báo cáo Tổng hợp (Synthesis Report)**.
