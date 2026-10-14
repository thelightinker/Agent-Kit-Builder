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

## 2. PHỔ KIẾN TRÚC LIÊN TỤC (CONTINUOUS ARCHITECTURE SPECTRUM)

Không ép kiến trúc vào 3 hộp cứng nhắc, Builder nhìn topology như một **dải phổ liên tục (Spectrum)**:

```
[ MICRO PROMPT ] ──────► [ STANDARD AGENT ] ──────► [ HYBRID / MINI-SUITE ] ──────► [ FULL SUITE HIERARCHY ]
  1-shot, stateless       1 Agent + 1–4 Skills       1 Orchestrator + 2 Specialists      1 Master Orchestrator
  0 thư mục               1 Workflow tuyến tính       + Shared Memory                    + 3–7 Specialists
                                                                                         + Multi-workflows + Scoped Memory
```

- **0 Specialist (Single Agent)**: Đủ cho 1 domain nghiệp vụ tập trung.
- **2 Specialists (Mini-Suite)**: Khi có 2 mảng nghiệp vụ đối trọng (ví dụ: Writer & Auditor).
- **3–7 Specialists (Full Suite)**: Khi hệ thống bao gồm nhiều mảng chức năng độc lập (ví dụ: Growth Suite gồm SEO, Copy, Ads, CRO, Analytics).

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

## 4. THE RIGHT ALTITUDE TEST (TIÊU CHUẨN RA QUYẾT ĐỊNH TOPOLOGY)

Quy tắc cốt lõi: **Chỉ leo thang sang Multi-Agent Suite khi chi phí điều phối nhỏ hơn chi phí context/nhận thức được tiết kiệm:**

$$\mathbf{\text{Coordination Cost (Handoff Latency + Routing)}} < \mathbf{\text{Context/Cognitive Cost Saved (Attention Rot + Tool Confusion)}}$$

### 3 Bài kiểm tra Cân bằng (Balance Checks):
1. **Tính kết nối Dữ liệu (Coupling Check)**:
   - Các sub-tasks có phụ thuộc logic/dữ liệu cực chặt (Tight Coupling)?
   - ➔ **GIỮ SINGLE AGENT**: 1 context window duy nhất đảm bảo tính nhất quán (tránh vỡ context theo Cognition Principle).
2. **Tính cô lập Vận hành (Operational Isolation Check)**:
   - Có xung đột quyền hạn công cụ (ví dụ: Dev Write vs Security Read-Only)?
   - Có nhu cầu chạy song song độc lập (Breadth-First Search)?
   - Có tác vụ dài hạn cần Session Reset để chống Attention Rot?
   - ➔ **TÁCH SPECIALIST AGENT**: Phân định ranh giới bảo mật & context an toàn.
3. **Độ phức tạp Nhận thức (Cognitive Overhead Check)**:
   - Nếu nhồi toàn bộ 15 skills + 5 domains vào 1 prompt, LLM có bị quá tải và nhầm lẫn công cụ không?
   - ➔ **NẾU CÓ: TÁCH SPECIALIST CLUSTERS**: Gom nhóm skills theo domain sở hữu.

---

## 5. ÁNH XẠ MỨC ĐỘ PHỨC TẠP & THUẬT NGỮ (LEGACY VOCABULARY MAPPING)

| Legacy Term | Target Architecture | Đặc tả kiến trúc |
|:---|:---|:---|
| Tier 1 | Micro | 1-shot prompt, stateless |
| Tier 2 | Standard | 1 Agent + 1–4 Skills, workflow tuyến tính |
| Tier 3 / SUITE_BUILD | Mini-Suite (2 agents) hoặc Full Suite (≥3 agents) | 1 Lead/Orchestrator + Specialists + Shared/Scoped Memory |

