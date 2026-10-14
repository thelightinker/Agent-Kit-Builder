# Prompt Compiling — Suite Architecture & Orchestration Reference

> Hướng dẫn chuyên sâu biên dịch System Prompt cho Master Orchestrator (Archetype B), ACO Lite Orchestration Protocol và Routing Table Injection trong kiến trúc Multi-Agent Suite.

---

## 1. Archetype B: Master Orchestrator (Nhạc Trưởng Điều Phối)

Dành cho Suite Kit. Đóng vai trò nhạc trưởng điều phối với kỷ luật cao nhất:
1. **Socratic & Pre-flight Check**: Làm rõ 1-3 câu về Trade-offs/Edge-cases nếu rủi ro cao; nếu rõ thì phân rã task ngay.
2. **Decomposition & Concurrency Matrix**: Tách task lớn thành các sub-tasks độc lập (Parallel reads cho khảo sát $\rightarrow$ Coordinator synthesis $\rightarrow$ Sequential writes cho chỉnh sửa file).
3. **"Never Delegate Understanding" Hard Gate**: Cấm tuyệt đối việc ủy quyền mù quáng ("Dựa vào findings hãy fix đi"). Orchestrator bắt buộc phải tự phân tích root cause, chỉ định chính xác file path, line range và tiêu chí nghiệm thu trước khi giao việc.
4. **Worker Briefing Contract (Đủ 5 phần)**: Goal & Context, What was ruled out, Specific file scope, Negative boundaries, Verification evidence.
5. **Specialist Routing Table & Boundary Enforcement**: Ma trận chọn Specialist và khóa cứng quyền sở hữu file (File Ownership Matrix).
6. **Synthesis & Conflict Resolution**: Gom kết quả, xử lý mâu thuẫn theo thứ tự ưu tiên (User $\rightarrow$ Evidence/Tests $\rightarrow$ Architecture $\rightarrow$ Specialist) và xuất báo cáo bàn giao.

---

## 2. Orchestration Protocol Compilation (ACO Lite)

Khi biên dịch System Prompt cho **Archetype B (Master Orchestrator)**, BẮT BUỘC biên dịch thêm khối `## Orchestration Protocol` vào Orchestrator prompt theo mẫu trong `templates/orchestrator-template.md`:

1. **Complexity Ladder**: Copy bảng L0-L3 từ template. Tùy chỉnh ví dụ L0 theo domain cụ thể của kit.
2. **Context Handoff**: Giữ nguyên quy tắc artifact reference. Chỉ thay đổi đường dẫn artifact nếu kit dùng thư mục khác thay vì `shared_state/`.
3. **Recovery Cascade**: Giữ nguyên `repair → reroute → replan → STOP`. Tùy chỉnh `retry.max_attempts` trong `execution_policy.json` nếu domain yêu cầu (nhưng KHÔNG VƯỢT QUÁ 3).
4. **Orchestration Invariants**: Giữ nguyên — đây là hard constraints.

Khi biên dịch **Archetype A (Standalone)** hoặc **Archetype C (Specialist)**, KHÔNG chèn Orchestration Protocol section đầy đủ. Chỉ chèn `## Context Handoff Protocol` (xem `templates/agent-template.md`).

---

## 3. Inject Routing Table vào Orchestrator Body (Archetype B)

Khi biên dịch Orchestrator prompt, BẮT BUỘC inject bảng `## 📡 ROUTING TABLE` **đã populated** vào body text. Lấy data trực tiếp từ `routing_table` trong Domain Profile Section 6.

Format bắt buộc (mỗi dòng là data thực, KHÔNG placeholder):
```markdown
## 📡 ROUTING TABLE (COMPILED — DO NOT MODIFY AT RUNTIME)

| User Intent Pattern | Target Agent | Required Skills | Execution Mode |
|:---|:---|:---|:---|
| "phân tích SEO" | `seo-specialist` | `seo-audit` | L1 Routed |
| "tạo chiến dịch toàn phễu" | **STAGED** | Step 1: `seo-specialist` → Step 2: `copy-specialist` | L2 Staged |
| Intent không khớp | **ESCALATE** | — | ⛔ Hỏi user |
```

**HARD RULE:** Routing table PHẢI có ≥1 dòng data thực + 1 dòng ESCALATE fallback. Bảng toàn placeholder = FAIL.
