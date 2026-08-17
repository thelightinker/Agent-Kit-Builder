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
  ├─ CÓ ➔ Orchestrator-Workers (Đọc cảnh báo Cognition vs Anthropic bên dưới)
  └─ KHÔNG, tác vụ hoàn toàn mở ➔ Autonomous Agent Loop
```

---

## 5. CẢNH BÁO MULTI-AGENT: COGNITION VS ANTHROPIC

- **Cognition Warning (Context Fragmentation)**: Chia đa-agent song song dễ làm vỡ tính nhất quán vì các worker thiếu context quyết định của nhau. Nếu các sub-task **phụ thuộc logic/kiến trúc** $\rightarrow$ Dùng **1 agent tuyến tính với full context**.
- **Anthropic Condition (Breadth-First Independence)**: Đa-agent chỉ vượt trội khi các sub-task **hoàn toàn độc lập** (ví dụ: research song song trên nhiều nguồn độc lập), có 1 Lead Agent điều phối và ranh giới output tường minh.
