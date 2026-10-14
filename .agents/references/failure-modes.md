# Failure Modes — AgentKit Builder

Các lỗi phổ biến khi build hoặc vận hành Agent Kit, phân theo mức nghiêm trọng.
Builder dùng tài liệu này để phòng ngừa và phát hiện lỗi.

---

## 🔴 Critical — Agent Kit không dùng được

| Failure Mode | Triệu chứng | Nguyên nhân | Đòn bẩy khắc phục |
|:-------------|:-------------|:------------|:------------------|
| **Lens Stuffing** | System Prompt phình, chứa cơ chế agent không dùng | Builder tick đủ 6 lens thay vì chọn theo nhu cầu | Ultimate Test (b): xoá mọi cơ chế không phục vụ outcome thực tế |
| **Human Summary Failure** | User low-tech đọc Tóm tắt vẫn không biết agent làm gì | Tóm tắt dùng thuật ngữ kỹ thuật hoặc quá vague | Test: đưa Tóm tắt cho người không biết AI đọc. Họ hiểu? |
| **Provider Lock-in** | Agent Kit chỉ chạy trên 1 provider | System Prompt dùng syntax đặc thù (GEMINI.md, claude artifacts...) | Review: tìm và xoá mọi provider-specific reference |
| **Missing Core Mechanism** | Agent fail ở task cốt lõi | Dynamic Enhancement Discovery bị skip hoặc chạy qua loa | Bắt buộc chạy 3 câu hỏi Discovery trước generate |
| **Template-Replaceable** | Agent Kit generic, swap domain nào cũng được | Builder không customize theo domain | Ultimate Test (a): so với template generic — phải khác |

---

## 🟡 Serious — Agent Kit hoạt động nhưng chất lượng thấp

| Failure Mode | Triệu chứng | Nguyên nhân | Đòn bẩy khắc phục |
|:-------------|:-------------|:------------|:------------------|
| **Vague DoD** | Output "đạt chuẩn" phụ thuộc người chấm | DoD dùng tính từ thay vì tiêu chí nhị phân | 3 kiểm định: nhị phân, đo được, không sáo ngữ |
| **Over-Engineered Micro** | Tier 1 agent có 2000+ từ System Prompt | Builder không phân Tier, áp đồng loạt | Kiểm tra Tier → Tier 1 chỉ cần A+C+minimal F |
| **Guided Intake Skip** | User low-tech bị hỏi "North Star là gì?" | Builder không detect tech level | Auto-detect: input đời thường → Guided Intake |
| **Tone Mixing** | Phần kỹ thuật viết đời thường, phần user viết kỹ thuật | Không tách biệt 2 tone | Kiểm tra: Tóm tắt 0 thuật ngữ, System Prompt 0 giải thích cho người mới |
| **REFACTOR Rewrite** | Audit agent sẵn có → viết lại toàn bộ thay vì patch | Builder không áp Delta-Only | Liệt kê cụ thể phần thiếu/thừa/sai → chỉ patch đó |

---

## 🟢 Minor — Cải thiện được nhưng không blocking

| Failure Mode | Triệu chứng | Nguyên nhân | Đòn bẩy khắc phục |
|:-------------|:-------------|:------------|:------------------|
| **Missing Domain Lever** | Agent thiếu cơ chế domain-specific (Voice Consistency, Source Ranking...) | Dynamic Enhancement Discovery tìm thấy nhưng không implement | Thêm khối Đòn bẩy riêng trong output |
| **No Output Template** | User không biết expect format gì từ agent | FORMAT ĐẦU RA section trống hoặc thiếu | Luôn có template cụ thể trong Section 4 |
| **Redundant Constraints** | HARD CONSTRAINTS lặp nội dung đã có trong Nguyên tắc | Copy-paste thay vì differentiate | Constraints = KHÔNG BAO GIỜ. Nguyên tắc = CÁCH LÀM. Không overlap |

---

## Failure Modes đặc trưng SUITE_BUILD

| Failure Mode | Triệu chứng | Nguyên nhân | Đòn bẩy khắc phục |
|:-------------|:-------------|:------------|:------------------|
| **Infinite Handoff Loop** | Agent A → B → C → A mãi không xong | Không agent nào "sở hữu" quyết định cuối | 1 lead agent duy nhất có quyền quyết định cuối |
| **Merge Conflict** | 2 agent cho kết quả mâu thuẫn, không ai giải quyết | Sub-agent thiếu shared context | Lead agent viết brief thống nhất trước dispatch |
| **Context Drift** | Mỗi agent hiểu task hơi khác | Handoff không chuẩn hoá | Handoff protocol: trigger + payload + format |
| **Dead Letter** | Agent gửi handoff nhưng không ai nhận | Handoff map thiếu | Mọi handoff phải map tới agent cụ thể trong Manifest |
| **Overhead > Value** | Bộ 5 agent cho task 1 agent làm đủ | Không kiểm tra: multi-state agent có đủ không? | Check: nếu 1 agent multi-state đủ → không cần SUITE_BUILD |

## 🔴 Critical — Routing Architecture Failures (P0)

| Failure Mode | Triệu chứng | Nguyên nhân | Đòn bẩy khắc phục |
|:-------------|:-------------|:------------|:-------------------|
| **Silent Agent Bypass (F1)** | Task cần Agent nhưng hệ thống xử lý inline, không gọi Agent | Orchestrator thiếu Routing Table hoặc Entry Gate | Populate Routing Table trong Orchestrator prompt từ Domain Profile routing_table |
| **Skill Amnesia (F2)** | Agent được gọi nhưng không nạp Skill, xử lý bằng general reasoning | Agent thiếu Skill Invocation Matrix hoặc Hard Loading Rule | Inject Skill Invocation Matrix vào mọi Agent prompt, kèm HARD RULE đọc SKILL.md |
| **Orchestrator Paralysis (F3)** | Orchestrator được kích hoạt nhưng không biết phân bổ task cho Agent nào | routing_index.json rỗng, capabilities frontmatter là placeholder | Bắt buộc Domain Profiling xuất routing_table, Prompt Compiler populate capabilities |
| **Broken Composition (F4)** | Task multi-step chỉ step 1 chạy, step 2+ bị bỏ qua | Thiếu Execution Plan Protocol, không track dependency giữa steps | Inject Execution Plan Composition vào Orchestrator với dependency graph |
| **Phantom Routing (F5)** | routing_index.json tồn tại nhưng rỗng, kit pass validation giả | Compiler compile placeholder thành empty, validator không check empty | Thêm routing.empty_capabilities lint rule: ≥1 agent → ≥1 capability bắt buộc |

---

## Self-Check trước khi deliver

Builder chạy qua danh sách này trước khi hoàn thành Agent Kit:

```
□ Ultimate Test: 4 điều kiện thất bại đều KHÔNG vi phạm?
□ Human Summary: người không biết AI đọc có hiểu?
□ System Prompt: mọi cơ chế phục vụ outcome thực tế?
□ DoD: mọi dòng pass 3 kiểm định?
□ Constraints: cụ thể, verifiable, không lặp Nguyên tắc?
□ Provider: không lock-in?
□ Tier: phù hợp complexity?
□ Dynamic Enhancement: đã chạy, findings đã xử lý?
□ Routing Table: Orchestrator prompt có bảng routing đã populated (không placeholder)?
□ Skill Invocation Matrix: Mọi Agent prompt có bảng scenario→skill→reason?
□ routing_index.json: ≥1 capability (không rỗng)?
```

