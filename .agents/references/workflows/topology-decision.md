# Workflow Topology & Decision Framework

> Cẩm nang quyết định hình thái kiến trúc (Topology) cho Agent & Workflow — tổng hợp nguyên tắc cốt lõi từ Anthropic, Cognition (Devin), Microsoft Research và LangChain.

---

## 1. RANH GIỚI WORKFLOW VS AGENT

| Đặc tính | Workflow (Quy trình Tĩnh) | Agent (Thực thể Tự trị) |
|:---|:---|:---|
| **Control Flow** | Code path định trước ở compile-time | LLM tự quyết định bước kế tiếp trong loop |
| **Độ đoán trước** | Cao — luôn biết trước trạng thái tiếp theo | Thấp — phụ thuộc ground-truth feedback |
| **Chi phí & Độ trễ** | Thấp, tối ưu, dễ debug | Cao hơn, đánh đổi chi phí lấy độ linh hoạt |

*Nguyên tắc kiến trúc:* Hệ thống tối ưu kết hợp cả hai ở cấp **Node** (Workflow điều phối các bước cố định, bên trong một node có thể là autonomous agent).

---

## 2. THANG ĐỘ PHỨC TẠP (COMPLEXITY LADDER)

Chỉ leo thang độ phức tạp khi có bằng chứng thực tế chứng minh cải thiện outcome:

```
[1] Augmented LLM (Đơn call + JIT Retrieval + Tools) ➔ Đủ cho >60% tác vụ
      │ (nếu chưa đủ)
      ▼
[2] Static Workflow (Prompt Chaining / Routing / Parallelization)
      │ (nếu path không đoán trước được ở compile-time)
      ▼
[3] Orchestrator-Workers (Phân rã sub-task động lúc runtime)
      │ (nếu tác vụ hoàn toàn mở, cần tương tác môi trường)
      ▼
[4] Autonomous Agent Loop (Vòng lặp tự trị có ground-truth feedback + human gate)
```

---

## 3. 6 KHỐI KIẾN TRÚC TOPOLOGY NỀN TẢNG

| Khối Topology | Cơ chế hoạt động | Khi nào áp dụng |
|:---|:---|:---|
| **Prompt Chaining** | Chuỗi bước tuần tự, output bước N là input bước N+1 | Tác vụ chia được thành các bước cố định, kiểm thử độc lập |
| **Routing** | Phân loại input và chuyển đến path/prompt chuyên biệt | Input rơi vào các nhóm phân biệt rõ rệt |
| **Parallelization (Sectioning)** | Chia nhỏ tác vụ thành các sub-task độc lập, chạy đồng thời | Các sub-task không phụ thuộc quyết định của nhau |
| **Parallelization (Voting)** | Chạy nhiều prompt song song để lấy đồng thuận | Cần giảm thiểu variance hoặc cần đa góc nhìn |
| **Orchestrator-Workers** | 1 Lead Agent phân rã task động và giao cho worker | Số lượng và loại sub-task chỉ biết được lúc runtime |
| **Evaluator-Optimizer** | 1 LLM sinh kết quả, 1 LLM đánh giá theo tiêu chí và yêu cầu sửa | Có tiêu chí DoD rõ ràng, việc lặp lại cải thiện đo được |

---

## 4. CÂY QUYẾT ĐỊNH CHỌN TOPOLOGY

```
Trả lời được bằng 1 LLM call + context tốt?
  ├─ CÓ ➔ Augmented LLM (DỪNG)
  └─ KHÔNG ↓
Path xử lý cố định, biết trước từng bước ở compile-time?
  ├─ CÓ:
  │   ├─ Cần phân loại trước khi xử lý? ➔ Routing
  │   ├─ Sub-tasks chạy độc lập được?   ➔ Parallelization
  │   └─ Chuỗi bước tuần tự?            ➔ Prompt Chaining
  └─ KHÔNG ↓
Có tiêu chí đánh giá rõ ràng, đáng lặp lại để tối ưu?
  ├─ CÓ ➔ Evaluator-Optimizer
  └─ KHÔNG ↓
Độ phức tạp chỉ biết được lúc runtime?
  ├─ CÓ ➔ Orchestrator-Workers (Đọc Scale-Out Trigger bên dưới)
  └─ KHÔNG, tác vụ hoàn toàn mở ➔ Autonomous Agent Loop
```

---

## 5. SCALE-OUT TRIGGER: 1 ORCHESTRATOR VS TÁCH SUB-AGENTS

Mặc định kiến trúc tối ưu: **1 Orchestrator + Cognitive Profiles + Focused Skills (Lazy Load) + Deterministic Scripts**.

Chỉ tách thành các Sub-Agent độc lập khi thỏa mãn **$\ge 1$ trong 4 điều kiện cô lập vận hành (Operational Isolation Triggers)**:

| Điều kiện Kích hoạt Tách Agent | Biểu hiện Kỹ thuật | Hành động Kiến trúc |
|:---|:---|:---|
| **1. Permission Boundary (Quyền hạn)** | Agent cần bị CẤM ghi file hoặc CẤM chạy Bash (ví dụ: Read-only Auditor). | Tách thành Sub-Agent riêng với cấu hình `tools:` giới hạn nghiêm ngặt. |
| **2. Parallel Execution (Chạy song song)** | Cần chạy $\ge 2$ luồng nghiên cứu/thực thi độc lập cùng lúc không phụ thuộc nhau. | Tách thành các Worker Agents độc lập (Breadth-First Search). |
| **3. Context Isolation (Chống Context Rot)** | Tác vụ dài qua nhiều phiên (> 30 turns), attention budget cạn kiệt làm agent quên quy tắc. | Tách thành Initializer Agent (tạo feature list) và Coding Agent (reset context mỗi session). |
| **4. Lifecycle & Memory Độc lập** | Mỗi vai trò cần lưu trữ memory, conventions hoặc state riêng biệt không trộn lẫn. | Tách thành Agent Suite với thư mục `memory/` và `manifest.json` độc lập. |

*Cảnh báo Chống Over-Engineering:* Nếu không có nhu cầu về 4 điều kiện trên, việc chia nhỏ thành nhiều Agent chỉ tạo thêm độ trễ handoff và rủi ro context fragmentation.
