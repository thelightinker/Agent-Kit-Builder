# AGENT WORKFLOW MASTER FRAMEWORK

> Tổng hợp nguyên tắc thiết kế agent workflow từ 10 nguồn hàng đầu hiện tại (Anthropic, GitHub Next/Microsoft Research, LangChain, HumanLayer, OpenAI, Cognition, Google) — dùng làm single source of truth để Agent Kit tạo và tự-đánh giá bất kỳ workflow nào, từ pipeline tuyến tính đơn giản tới hệ multi-agent phức tạp.

Cập nhật: 2026-07-11 · Phạm vi: framework kiến trúc và nguyên tắc quyết định, không trói vào 1 codebase/framework cụ thể (LangGraph/ADK/Agent SDK chỉ xuất hiện làm ví dụ implement).

## MỤC LỤC

- Phần 0 — Nguyên tắc nền tảng
- Phần 1 — Cây quyết định Topology
- Phần 2 — State Machine & Definition of Done
- Phần 3 — Context Engineering
- Phần 4 — Thiết kế Tool / ACI
- Phần 5 — Vận hành đa-phiên (Long-running Workflow)
- Phần 6 — Control Flow & Error Handling
- Phần 7 — Guardrails & Security
- Phần 8 — Cấu trúc file workflow (Markdown + Frontmatter)
- Phần 9 — Master Template (điền để tạo workflow bất kỳ)
- Phần 10 — Quy trình tự-kiểm trước khi publish
- Phụ lục A — Bảng tra cứu nhanh
- Nguồn tham khảo

---

## PHẦN 0 — NGUYÊN TẮC NỀN TẢNG

### 0.1 Workflow vs Agent — ranh giới định nghĩa

Anthropic phân định 2 khái niệm hay bị dùng lẫn:

|                         | Workflow                                                                | Agent                                                        |
| ----------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------ |
| Control flow            | Code path định trước, LLM + tool được orchestrate theo path đó | LLM tự định hướng process, tự quyết bước tiếp theo |
| Định nghĩa rút gọn | Predefined code paths                                                   | "LLMs autonomously using tools in a loop"                    |
| Tính đoán trước    | Cao — luôn biết bước kế tiếp                                     | Thấp — model quyết định lúc runtime                    |

Hệ quả thiết kế: một hệ thống có thể chứa cả hai — ví dụ workflow ngoài cùng là chaining 3 bước cố định, nhưng bước giữa lại là 1 autonomous agent con. Không cần chọn phe tuyệt đối; chọn ở cấp NODE, không phải cấp toàn hệ thống.

### 0.2 Complexity Ladder — leo thang khi có bằng chứng, không leo trước

```
Đơn LLM call (+ retrieval, in-context example)
  → đủ cho phần lớn use case. Nếu đủ, DỪNG Ở ĐÂY, không đọc tiếp Phần 1.
Workflow tĩnh (chaining / routing / parallelization)
  → task well-defined, path đoán trước được ở compile-time.
Orchestrator-Workers
  → task có complexity KHÔNG đoán trước được ở compile-time.
Autonomous Agent Loop
  → task mở, cần model-driven decision-making, có ground-truth feedback mỗi bước.
```

Nguyên tắc gốc: tìm giải pháp đơn giản nhất trước, chỉ tăng complexity khi có bằng chứng cụ thể cải thiện outcome. Agentic system đánh đổi latency + cost lấy task performance — đánh đổi đó phải xứng đáng, không mặc định là đúng.

### 0.3 Checklist: có nên build Agent không

3 điều kiện, thiếu 1 → cân nhắc lại trước khi build:

- [ ] **Task Complexity**: nếu vẽ được toàn bộ decision tree tường minh → build workflow tường minh, tối ưu từng node, ĐỪNG dùng agent. Explicit workflow kiểm soát tốt hơn, rẻ hơn, dễ optimize từng điểm quyết định hơn agent tự khám phá đường đi.
- [ ] **Value Justification**: exploration của agent tốn token — giá trị task phải bù được chi phí đó.
- [ ] **Error Cost đã có kế hoạch xử lý**: task có chi phí lỗi cao (tài chính, compliance, không đảo ngược được) KHÔNG đồng nghĩa "không dùng agent" — đồng nghĩa "guardrail + human checkpoint phải nghiêm ngặt hơn tương ứng" (chi tiết ở Phần 7).

### 0.4 ACI đặt trước Prompt Engineering

Trước khi tối ưu prompt, tối ưu Agent-Computer Interface — cách agent "nhìn thấy" tool và môi trường:

- Viết tool doc như tài liệu onboard cho engineer mới: rõ ràng, có ví dụ, không mơ hồ.
- Absolute path/ID thay vì relative/ambiguous reference.
- Test tool bằng cách cho agent thật sự dùng, quan sát lỗi cụ thể, rồi sửa MÔ TẢ TOOL trước — không chỉ vá prompt để né lỗi bề mặt. Chi tiết ở Phần 4.

---

## PHẦN 1 — CÂY QUYẾT ĐỊNH TOPOLOGY

### 1.1 6 khối kiến trúc nền

| Khối                         | Cơ chế                                                                                                                   | Dùng khi                                                                             |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Augmented LLM                 | LLM + retrieval + tool + memory                                                                                            | Building block nền — không phải pattern độc lập                                |
| Prompt Chaining               | Chuỗi bước tuần tự, output bước N là input bước N+1, có gate kiểm tra giữa các bước                        | Task chia được thành bước cố định, mỗi bước verify riêng được         |
| Routing                       | Phân loại input, chuyển tới prompt/path chuyên biệt tương ứng                                                     | Input rơi vào các loại rõ rệt, mỗi loại cần xử lý khác nhau               |
| Parallelization — Sectioning | Chia task thành sub-task ĐỘC LẬP, chạy song song, hợp kết quả                                                      | Sub-task tách được, không phụ thuộc quyết định lẫn nhau                    |
| Parallelization — Voting     | Chạy cùng 1 task nhiều lần song song, lấy đồng thuận                                                               | Cần nhiều góc nhìn / giảm variance của 1 lần chạy đơn                       |
| Orchestrator-Workers          | Orchestrator phân rã task ĐỘNG lúc runtime, giao việc theo tình huống thực tế                                    | Số lượng & loại sub-task không đoán trước được ở compile-time            |
| Evaluator-Optimizer           | 1 LLM sinh, 1 LLM khác đánh giá theo tiêu chí rõ ràng, lặp tới khi đạt                                         | Có tiêu chí đánh giá rõ ràng, cải thiện lặp lại có giá trị đo được |
| Autonomous Agent              | Vòng lặp tự trị, ground-truth feedback từ environment mỗi bước (tool result/code execution), pause tại checkpoint | Task mở, số bước không đoán trước, cần model tự quyết hành động        |

### 1.2 Cây quyết định

```
Trả lời được bằng 1 LLM call + context tốt?
  → CÓ: dùng Augmented LLM, DỪNG.
  → KHÔNG ↓
Path xử lý cố định, biết trước từng bước ở compile-time?
  → CÓ:
     ├─ Input cần phân loại trước khi xử lý?        → Routing
     ├─ Sub-task tách độc lập, chạy song song được?  → Parallelization
     └─ Chuỗi bước tuyến tính, verify từng bước?     → Prompt Chaining
  → KHÔNG (path không đoán trước được) ↓
Có tiêu chí đánh giá output rõ ràng, đáng để lặp cải thiện?
  → CÓ: Evaluator-Optimizer
  → KHÔNG, hoặc cần cả 2 ↓
Độ phức tạp / số sub-task chỉ biết được lúc runtime?
  → CÓ: Orchestrator-Workers (đọc CẢNH BÁO 1.3 trước khi chạy song song)
  → KHÔNG, task hoàn toàn mở ↓
Autonomous Agent Loop (kèm ground-truth feedback + human checkpoint, xem Phần 7)
```

### 1.3 CẢNH BÁO đa-agent — đọc trước khi chọn Orchestrator-Workers song song

Tháng 6/2025, Cognition (Devin) và Anthropic công bố 2 bài gần như đối lập trong vòng 24 giờ. Cả hai đều đúng, ở 2 điều kiện khác nhau — đây không phải mâu thuẫn cần chọn phe, mà là 2 điều kiện biên cần phân biệt.

**Cognition — vì sao đa-agent dễ vỡ:** sub-agent chạy song song thường thiếu context quyết định mà agent khác đã thấy → xung đột khi ghép kết quả. Ví dụ minh hoạ: 2 sub-agent cùng xây 2 phần của 1 sản phẩm nhỏ, không đồng bộ style/quyết định thiết kế, ghép lại không dùng được — dù mỗi phần riêng lẻ đều "đúng". Nguyên tắc sửa của Cognition: nếu bắt buộc dùng sub-agent, sub-agent phải thấy TOÀN BỘ context mà agent chính đã thấy, không phải bản tóm tắt.

**Anthropic — vì sao đa-agent vẫn thắng trong đúng use case:** hệ multi-agent research của Anthropic thắng single-agent 90.2% trên eval nội bộ cho task breadth-first (ví dụ: liệt kê toàn bộ thành viên hội đồng quản trị của các công ty trong 1 index lớn — việc mà single-agent tìm kiếm tuần tự thất bại vì quá chậm và bỏ sót). Điều kiện thắng: sub-task ĐỘC LẬP thật sự, có 1 lead agent duy nhất phân công ranh giới rõ ràng + output format cụ thể cho từng sub-agent, tránh 2 agent trùng nhiệm vụ.

**Dữ liệu ngành 2026 (khảo sát production, không phải benchmark lý thuyết):**

- Princeton NLP: single agent thắng hoặc hoà multi-agent trên 64% task benchmark khi cho cùng tool + cùng context.
- Khoảng 40% multi-agent pilot fail trong 6 tháng đầu production.
- Failure mode phổ biến nhất: infinite handoff loop (A→B→C→A) — không agent nào "sở hữu" task nên liên tục replan.
- Khoảng 86–89% agent pilot nói chung (không riêng multi-agent) fail trước khi vào production — nguyên nhân hàng đầu là thiếu governance/traceability, không phải model yếu.

**Quy tắc quyết định thực dụng:**

```
Sub-task PHỤ THUỘC quyết định lẫn nhau (style, kiến trúc, thiết kế chung)?
  → CÓ: dùng 1 agent tuyến tính, context đầy đủ. KHÔNG chia đa-agent.
  → KHÔNG (sub-task verify độc lập được, kiểu breadth-first search):
     → Chỉ khi đó mới cân nhắc Orchestrator-Workers song song.
     → Bắt buộc: 1 lead agent duy nhất giữ quyền quyết định cuối.
     → Bắt buộc: ranh giới + output format từng sub-agent viết tường minh, không suy luận ngầm.
```

---

## PHẦN 2 — STATE MACHINE & DEFINITION OF DONE

Mọi workflow — dù chọn topology nào ở Phần 1 — nên biểu diễn dưới dạng State Machine tường minh, không phải chuỗi prompt ngầm định mà chỉ agent "hiểu ý".

### 2.1 Node anatomy — bắt buộc 5 thành phần

```
[STATE: <tên>]
[Input Artifacts]   — khoá dữ liệu node được đọc. Đọc ngoài danh sách = vi phạm Artifacts Isolation.
[Output Artifacts]  — khoá dữ liệu node ghi vào.
[DoD]               — checklist nhị phân, đo được, không cảm tính. Pass 100% mới transition.
[Evaluation Loop]   — Evaluate → Fail→Revise / Pass→Done → transition kế tiếp.
```

Artifacts Isolation không phải chi tiết vệ sinh — nó là cơ chế duy nhất triệt tiêu context bloat khi workflow chạy trên project lớn qua MCP. Một node chỉ nên nạp đúng phần dữ liệu DoD của nó cần, không nạp toàn bộ state "cho chắc" (xem lại lý do kiến trúc ở Phần 3.1).

### 2.2 Quy tắc viết DoD — 3 kiểm định

Một dòng DoD hợp lệ phải trả lời được cả 3 câu hỏi:

1. **Nhị phân** — pass/fail rõ ràng, không phụ thuộc cảm tính người/agent đánh giá.
2. **Đo được từ Output Artifact** — không cần hỏi thêm context ngoài để chấm.
3. **Không dừng ở tính từ chất lượng** — "chuyên nghiệp/đầy đủ/tối ưu" phải được quy ra cơ chế cụ thể: số lượng, có/không tồn tại, ngưỡng số.

Sai: "Nội dung phải chuyên nghiệp và đầy đủ."
Đúng: "≥ 2 use-case cụ thể được nêu tên; Prerequisites tham chiếu công cụ có thật trong source, không dùng placeholder."

### 2.3 Evaluation Loop & Escalation

```
Node chạy xong → Evaluate output theo DoD
  → Fail: Revise, quay lại node (tối đa Max Retry lần)
  → Pass: Done, transition sang node kế tiếp
  → Fail vượt Max Retry: → ESCALATE_HUMAN, gắn needs_human_review: true, KHÔNG tự publish
```

Max Retry mặc định = 2. Escalate không phải thất bại của workflow — là 1 exit path hợp lệ, tường minh, cùng tinh thần với "Contact human = tool call" ở Phần 6.

### 2.4 Khi nào cần transition NGƯỢC

State Machine không bắt buộc là DAG một chiều. Nếu 1 node phát hiện mâu thuẫn với output của node trước đó (ví dụ: evidence mới phủ định giả định ban đầu), khai báo tường minh cạnh ngược kèm điều kiện kích hoạt cụ thể — đừng để agent tự "âm thầm" quay lại sửa mà không ghi log lý do, vì điều đó phá vỡ tính audit được của toàn workflow.

---

## PHẦN 3 — CONTEXT ENGINEERING

### 3.1 Context là tài nguyên hữu hạn, không phải kho chứa miễn phí

Mỗi token trong context cạnh tranh "attention budget" với mọi token khác đang có mặt. Context Rot: kiến trúc transformer tạo quan hệ pairwise bậc hai giữa các token — 10.000 token tạo khoảng 100 triệu quan hệ phải track, 100.000 token tạo khoảng 10 tỷ. Đây là thực tế kiến trúc, không phải bug tạm thời chờ được vá. Hệ quả trực tiếp: nhồi thêm context "cho chắc ăn" thường làm GIẢM performance thay vì tăng.

### 3.2 Just-in-time retrieval thay vì pre-load toàn bộ

Giữ identifier nhẹ (file path, ID, query) trong context, load full content lúc thật sự cần dùng — thay vì nạp sẵn toàn bộ dữ liệu "phòng khi cần". Trade-off chấp nhận được: thêm 1 round-trip tool call, đổi lấy context sạch hơn suốt phiên làm việc.

### 3.3 Compaction

Khi context gần đầy: nén history thành summary giữ lại quyết định + open item quan trọng, loại bỏ raw tool output cũ không còn tác dụng. Compaction không hoàn hảo — không đảm bảo truyền hết instruction rõ ràng cho phiên kế tiếp (đây chính là lý do cần thêm cơ chế ngoài context window ở Phần 5, không chỉ dựa vào compaction).

### 3.4 Structured note-taking — bộ nhớ ngoài context window

Ghi trạng thái ra file ngoài (progress notes, feature list) thay vì chỉ dựa vào context window đang chạy. Đây là cơ chế "nhớ" xuyên session, độc lập với compaction. Chi tiết implementation đầy đủ ở Phần 5.

### 3.5 Sub-agent isolation

Agent con nên có context window riêng, sạch — chỉ trả về kết quả đã distill cho agent cha, không trả full trace. Đây là lý do multi-agent THẮNG được single-agent trong đúng điều kiện (xem lại 1.3): mỗi sub-agent tránh được context bloat của các phần việc khác. NHƯNG cơ chế này chỉ có lợi khi sub-task thực sự độc lập — nếu không, đây chính xác là nguyên nhân xung đột mà Cognition cảnh báo, vì "context sạch" của sub-agent cũng đồng nghĩa "thiếu context quyết định" của agent khác.

### 3.6 "Right altitude" cho system prompt

Hai cực cần tránh:

- **Quá cứng**: nhồi if-else cho từng edge case cụ thể → prompt giòn, vỡ khi gặp case chưa lường trước.
- **Quá mơ hồ**: chỉ đưa nguyên tắc trừu tượng → agent tự suy luận sai hướng, không có neo cụ thể.

Mức đúng: hướng dẫn rõ ràng cho hành vi cốt lõi + để lại không gian heuristic cho phần biến thiên. Bắt đầu bằng bản tối giản, mở rộng dựa trên lỗi thực tế quan sát được — không viết đủ mọi trường hợp ngay từ đầu.

---

## PHẦN 4 — THIẾT KẾ TOOL / ACI

### 4.1 Namespacing

Khi agent có quyền truy cập hàng chục tool/MCP server, nhóm tool theo prefix service + resource (ví dụ: `asana_projects_search`, `jira_issues_search`) giúp model chọn đúng tool nhanh hơn. Chọn prefix- hay suffix-based namespacing tạo khác biệt thực đo được trên tool-use eval — không phải chi tiết thẩm mỹ.

### 4.2 Consolidate thay vì liệt kê tool nhỏ lẻ

Vấn đề chính không nằm ở SỐ LƯỢNG tool mà ở độ TƯƠNG ĐỒNG/mơ hồ giữa các tool — tool chồng chéo chức năng gây agent nhầm lẫn dùng tool nào khi nào. Gộp các operation hay đi cùng nhau thành 1 tool cấp cao hơn:

- Sai: `list_users` + `list_events` + `create_event` (3 tool rời, agent phải tự ghép logic giữa chúng)
- Đúng: `schedule_event` (1 tool tự tìm slot trống rồi đặt lịch, gộp cả 3 bước)

### 4.3 Tool response tối giản, tự nhiên với model

Trả về đúng phần liên quan, không phải toàn bộ dữ liệu thô. Ví dụ: `search_logs` nên trả các dòng liên quan + ngữ cảnh xung quanh, không phải nguyên file log — để model không phải tự lọc giữa hàng nghìn dòng nhiễu.

### 4.4 Evaluation-driven tool design

Build vài tool nhắm đúng high-impact workflow trước, generate test case dựa trên use-case thật, đo tỷ lệ agent chọn/dùng đúng tool, rồi lặp lại — sửa MÔ TẢ TOOL dựa trên lỗi quan sát được, không chỉ sửa prompt. Có thể dùng chính 1 agent làm "tool-tester": cho agent thử tool đang lỗi, agent tự viết lại description để tránh lặp lỗi ở lượt sau.

---

## PHẦN 5 — VẬN HÀNH ĐA-PHIÊN (LONG-RUNNING WORKFLOW)

Áp dụng khi task không hoàn thành nổi trong 1 context window (nhiều giờ / nhiều ngày). Compaction (Phần 3.3) không đủ — cần cơ chế bàn giao xuyên phiên, tách biệt khỏi context window đang chạy.

### 5.1 2 vai trò tách biệt

| Vai trò          | Chạy khi nào                 | Nhiệm vụ                                                                                                                              |
| ----------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| Initializer Agent | 1 lần duy nhất, phiên đầu | Dựng feature list đầy đủ (mọi feature mức end-to-end, không chỉ feature đầu tiên), viết`init.sh`, tạo commit khởi tạo |
| Coding Agent      | Mọi phiên sau                | Đọc trạng thái hiện có, chọn ĐÚNG 1 feature ưu tiên cao nhất chưa xong, làm xong, để lại trạng thái sạch            |

Lý do tách vai trò: agent chạy 1 mạch từ prompt cấp cao ("build 1 bản clone của X") có xu hướng one-shot toàn bộ, hết context giữa chừng, để lại tính năng dở dang không ghi chú — phiên sau phải đoán lại chuyện gì đã xảy ra. Tách Initializer ra riêng giải quyết tận gốc bằng cách buộc toàn bộ phạm vi được liệt kê tường minh TRƯỚC khi bất kỳ Coding Agent nào bắt đầu code.

### 5.2 Feature list dạng JSON — DoD ở cấp file

```json
{
  "category": "functional",
  "description": "Nút New Chat tạo hội thoại mới",
  "steps": ["Vào giao diện chính", "Bấm New Chat", "Xác nhận hội thoại mới xuất hiện"],
  "passes": false
}
```

Dùng JSON thay vì Markdown cho danh sách này — model ít khả năng tự ý sửa/xoá field JSON hơn so với sửa tự do 1 dòng markdown. Agent chỉ được đổi field `passes` sau khi tự verify end-to-end — không chỉ unit test hay curl, mà cần browser automation hoặc tương đương để xác nhận hành vi thật hoạt động. Ràng buộc tường minh bắt buộc trong prompt: "không được xoá/sửa test để né lỗi."

### 5.3 Nghi thức đầu phiên — bắt buộc, tiết kiệm token dò lại

```
1. pwd — xác nhận phạm vi thư mục được phép sửa
2. Đọc progress-notes + git log gần nhất — nắm việc đã làm ở phiên trước
3. Đọc feature list — chọn feature ưu tiên cao nhất còn passes:false
4. Chạy init.sh, kiểm tra trạng thái hiện tại CÒN CHẠY ĐƯỢC không, trước khi code thêm bất cứ gì
```

Nghi thức này tồn tại vì: nếu agent bắt đầu implement feature mới trên 1 codebase đang bị lỗi từ phiên trước mà không kiểm tra trước, agent sẽ làm vấn đề nặng thêm thay vì sửa.

### 5.4 Bảng failure mode → giải pháp

| Failure mode                                                 | Initializer Agent xử lý                           | Coding Agent xử lý                                                                                                              |
| ------------------------------------------------------------ | --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Tuyên bố xong toàn bộ project quá sớm                  | Dựng feature list đầy đủ ngay từ đầu        | Đọc feature list đầu phiên, chỉ chọn 1 feature để làm                                                                   |
| Để lại môi trường có bug / tiến độ không ghi chú | Tạo git repo + progress-notes ban đầu            | Đọc progress-notes + git log đầu phiên, test cơ bản trước khi code tiếp; kết phiên bằng commit + cập nhật progress |
| Đánh dấu feature done khi chưa test kỹ                  | Dựng feature list với`passes:false` mặc định | Chỉ set`passes:true` sau khi tự verify end-to-end                                                                             |
| Tốn thời gian dò cách chạy app                          | Viết`init.sh` chạy được ngay                 | Đọc`init.sh` đầu phiên thay vì tự đoán                                                                                 |

---

## PHẦN 6 — CONTROL FLOW & ERROR HANDLING

Chủ đề xuyên suốt: OWNERSHIP — đừng để framework giấu logic điều phối khỏi tầm review của người thiết kế.

- **Own your control flow**: vòng lặp (for + switch/match) do chính bạn viết, không phó mặc framework. Lợi ích cụ thể: hijack được để pause chờ người, serialize context để pause/resume bất kỳ lúc nào.
- **Own your prompts**: prompt là first-class code, versioned, review được — không phải tham số string ẩn bên trong 1 constructor kiểu `Agent(role=..., goal=...)` của framework mà bạn khó dò ngược token thật sự được gửi đi.
- **Tools are just structured outputs**: 1 tool call về bản chất là JSON có cấu trúc do LLM sinh ra để trigger code xác định (deterministic) phía sau — không có "phép màu" nào khác cần trừu tượng hoá thêm.
- **Stateless reducer**: mỗi bước = (state cũ + event mới) → state mới. Nếu 1 lượt chạy KHÔNG biểu diễn được bằng công thức này, debug sẽ thành khảo cổ học — phải đoán lịch sử thay vì đọc thẳng state hiện tại.
- **Compact errors into context**: lỗi phải được nén thành thông tin hữu ích cho bước kế tiếp — không đẩy nguyên raw stack trace vào context làm nhiễu và chiếm attention budget (xem lại 3.1).
- **Contact human = tool call**: escalate về người là 1 hành động tường minh trong luồng chính, cùng cấp với mọi tool call khác — không phải exception xử lý ngoài luồng.
- **Small, focused agents**: agent phạm vi hẹp, nhiều micro-agent chuyên trách dễ debug/dễ review hơn 1 agent ôm hết — nối lại bằng deterministic code ở giữa (deterministic code gọi agent xử lý 1 đoạn hẹp có ranh giới rõ, rồi deterministic code chạy tiếp bước xác định, agent tiếp theo chỉ nhận đúng phần việc của mình).

---

## PHẦN 7 — GUARDRAILS & SECURITY

### 7.1 Risk tiering cho từng tool

Gán mỗi tool 1 mức low/medium/high dựa trên: read-only hay write, khả năng đảo ngược, phạm vi quyền, mức ảnh hưởng tài chính/dữ liệu. Dùng risk tier để quyết định tool nào cần pause chờ người duyệt trước khi thực thi — không áp guardrail đồng đều cho mọi tool, vì làm vậy vừa chậm vừa không tập trung vào đúng chỗ rủi ro thật.

### 7.2 Read-only default + Safe Outputs

Mặc định agent chỉ có quyền đọc. Mọi hành động ghi phải đi qua danh sách "safe output" khai báo trước (ví dụ: chỉ được tạo 1 issue với prefix title cụ thể + label cụ thể — không có quyền ghi nào khác ngoài đó), và output đó được validate ĐỘC LẬP trước khi áp dụng thật vào hệ thống. Đây là 1 Evaluation Gate ở CẤP HỆ THỐNG — khác về bản chất với Evaluation Loop ở Phần 2, vốn là agent tự chấm điểm bài của chính nó.

### 7.3 Defense-in-depth — nhiều lớp độc lập, không dồn vào 1 lớp

```
Lớp 1: Network firewall — chỉ cho phép agent gọi ra domain đã khai báo trước
Lớp 2: Read-only permission mặc định
Lớp 3: Schema validation cho mọi output trước khi áp dụng
Lớp 4: Threat-detection job quét output tìm pattern đáng ngờ
Lớp 5: Action pinning — khoá phiên bản action/dependency, tránh supply-chain drift
```

Nguyên tắc: mỗi lớp độc lập với lớp khác — 1 lớp bị qua mặt không có nghĩa toàn hệ thống mất kiểm soát.

### 7.4 Guardrail deterministic đặt TRƯỚC LLM

Blocklist/regex/giới hạn độ dài input cho các mối đe doạ đã biết trước (SQL injection, prompt-injection pattern quen thuộc) nên chặn ở lớp deterministic, không dựa vào LLM tự nhận diện mỗi lần — rẻ hơn, nhanh hơn, không phụ thuộc việc model có "để ý" ở lượt chạy đó hay không.

---

## PHẦN 8 — CẤU TRÚC FILE WORKFLOW: MARKDOWN + FRONTMATTER

Quy ước từ GitHub Agentic Workflows — áp dụng được cho mọi workflow file, không riêng automation trên GitHub.

### 8.1 2 lớp tách biệt trong 1 file

```yaml
---
on: <trigger>                 # compile-time — khi nào workflow chạy
permissions: read-all         # compile-time — quyền mặc định, càng hẹp càng tốt
tools: [...]                  # compile-time — danh sách tool được cấp
safe-outputs:
  <hành-động-ghi-duy-nhất>: <ràng buộc cụ thể>   # compile-time
---
# Tên workflow

Instruction ngôn ngữ tự nhiên, viết như giải thích cho 1 đồng nghiệp mới:
cụ thể, có ngữ cảnh dự án, có heading dẫn dắt luồng làm việc.
```

- **Frontmatter (YAML)** = phần khai báo, compile-time, xác định trigger/quyền/tool — nên qua review/compile step trước khi chạy thật.
- **Body (Markdown)** = phần vận hành, runtime, agent đọc trực tiếp — sửa được không cần compile lại nếu chỉ đổi instruction, không đổi quyền/trigger.

### 8.2 Nguyên tắc viết instruction

Viết như giải thích cho đồng nghiệp mới vào dự án: cụ thể, có ngữ cảnh (constraint, mục tiêu, dữ liệu liên quan), có heading để agent bám theo đúng thứ tự luồng làm việc thay vì đọc 1 đoạn văn dài không cấu trúc.

### 8.3 Compile step tách biệt = audit trước khi chạy

Tách bước "biên dịch" (từ file khai báo/instruction ra artifact thực thi) khỏi bước "chạy" cho phép audit trước khi hành động — cùng tinh thần với "Own your control flow" ở Phần 6: không có gì chạy ngầm mà không qua bước kiểm tra tường minh trước đó.

---

## PHẦN 9 — MASTER TEMPLATE (điền để tạo workflow bất kỳ)

Khung này gộp toàn bộ Phần 0–8 thành 1 template dùng ngay. Điền vào chỗ `<...>`, xoá phần không áp dụng (ví dụ: bỏ khối SESSION HANDOFF nếu workflow chạy gọn trong 1 phiên).

```markdown
---
# === COMPILE-TIME: FRONTMATTER (Phần 8) ===
workflow_name: <tên-workflow>
topology: <chaining | routing | parallelization | orchestrator-workers | evaluator-optimizer | autonomous-agent>   # chọn theo cây quyết định Phần 1.2
trigger: <manual | schedule | event>
permissions: read-only          # mặc định, mở rộng phải có lý do tường minh (Phần 7.2)
tools_allowed: [<tool_1>, <tool_2>, ...]   # đã namespacing + consolidate (Phần 4)
safe_outputs:
  <hành-động-ghi-duy-nhất>: <ràng buộc cụ thể>
max_retry_per_node: 2
---

# === RUNTIME: MỤC TIÊU (Phần 8.2) ===
<Mô tả mục tiêu bằng ngôn ngữ tự nhiên, như giải thích cho đồng nghiệp mới.
Gồm: bối cảnh dự án, constraint, định nghĩa "xong" ở cấp toàn workflow.>

## [WORKFLOW META]
Shared State: `workflow_state = { <khoá_1>, <khoá_2>, ... }`

## [STATE: INIT]
[Input Artifacts]: <nguồn đầu vào ban đầu>
[Output Artifacts]: workflow_state.<khoá khởi tạo>
[DoD]
- [ ] <điều kiện nhị phân 1 — qua 3 kiểm định ở Phần 2.2>
- [ ] <điều kiện nhị phân 2>
[Evaluation Loop]: Evaluate → Fail → Revise → Done → transition <STATE kế tiếp>

## [STATE: <tên node>]
[Input Artifacts]: <chỉ những khoá node này thực sự cần — Artifacts Isolation, Phần 2.1>
[Output Artifacts]: workflow_state.<khoá node này ghi>
[DoD]
- [ ] <điều kiện nhị phân, đo được, không sáo ngữ>
[Evaluation Loop]: Evaluate → Fail → Revise → Done → transition <STATE kế tiếp>
                    (nếu cần transition ngược: → phát hiện <điều kiện cụ thể> → transition <STATE trước đó>, xem Phần 2.4)

... (lặp lại cho từng node theo topology đã chọn ở Phần 1) ...

## [STATE: NODE_FINALIZE]
[Input Artifacts]: toàn bộ workflow_state
[Output Artifacts]: deliverable cuối cùng
[DoD]
- [ ] Không mâu thuẫn chéo giữa các Output Artifact của các node
- [ ] Mọi safe_output đã validate độc lập trước khi apply (Phần 7.2)
[Evaluation Loop]: Evaluate → Fail → Revise (quay lại node liên quan) → Done → [*]

## [ESCALATE_HUMAN]
Kích hoạt khi: 1 node fail DoD vượt max_retry_per_node.
Output: draft hiện tại + log lý do fail mỗi lần Evaluate + needs_human_review: true.
KHÔNG tự publish khi đang ở trạng thái này.

# === CHỈ THÊM NẾU WORKFLOW CHẠY NHIỀU PHIÊN, Phần 5 ===
## [SESSION HANDOFF]
- progress_file: <đường dẫn>
- feature_list: <đường dẫn, format JSON, field bắt buộc: passes:boolean>
- Nghi thức đầu phiên: pwd → đọc progress + git log → đọc feature list → chọn 1 feature ưu tiên cao nhất
```

---

## PHẦN 10 — QUY TRÌNH TỰ-KIỂM TRƯỚC KHI PUBLISH 1 WORKFLOW MỚI

- [ ] Đã chạy Complexity Ladder (0.2) — xác nhận KHÔNG có giải pháp đơn giản hơn giải quyết được task này?
- [ ] Đã qua Checklist 0.3 — value justification rõ ràng, error cost đã có kế hoạch xử lý?
- [ ] Nếu có ≥ 2 agent chạy song song: đã qua Cảnh báo đa-agent (1.3) — sub-task xác nhận độc lập thật, không phụ thuộc quyết định lẫn nhau?
- [ ] Mọi node đều có đủ 5 thành phần (2.1): STATE / Input Artifacts / Output Artifacts / DoD / Evaluation Loop?
- [ ] Mọi dòng DoD qua được 3 kiểm định ở 2.2 (nhị phân, đo được, không dừng ở tính từ)?
- [ ] Context mỗi node: đã áp just-in-time retrieval, không pre-load thừa (3.2)?
- [ ] Tool: đã namespacing, đã consolidate tool chồng chéo (4.1, 4.2)?
- [ ] Nếu workflow chạy nhiều phiên: đã có feature list JSON + progress file + nghi thức đầu phiên (Phần 5)?
- [ ] Mọi tool có quyền ghi đã gán risk tier, đi qua safe-outputs/read-only default (7.1, 7.2)?
- [ ] Frontmatter tách biệt khỏi instruction body, đã qua compile/audit step (Phần 8)?
- [ ] Escalation path (ESCALATE_HUMAN) đã khai báo tường minh, không phải "hy vọng không xảy ra"?

---

## PHỤ LỤC A — BẢNG TRA CỨU NHANH

| Cần gì                                              | Dùng pattern                         | Chi tiết      |
| ----------------------------------------------------- | ------------------------------------- | -------------- |
| Task well-defined, bước cố định                  | Prompt Chaining                       | Phần 1.1      |
| Input cần phân loại trước khi xử lý            | Routing                               | Phần 1.1      |
| Sub-task độc lập, chạy song song được          | Parallelization                       | Phần 1.1, 1.3 |
| Complexity chỉ biết lúc runtime                    | Orchestrator-Workers                  | Phần 1.1, 1.3 |
| Có tiêu chí đánh giá rõ, cần lặp cải thiện | Evaluator-Optimizer                   | Phần 1.1, 2.3 |
| Task mở, nhiều bước không đoán trước         | Autonomous Agent                      | Phần 1.1      |
| Task dài hơn 1 context window                       | Initializer/Coding Agent split        | Phần 5        |
| Nhiều tool/MCP server, dễ nhầm lẫn                | Namespacing + Consolidate             | Phần 4        |
| Hành động không đảo ngược được             | Risk tiering + Safe Outputs           | Phần 7        |
| Cần audit trước khi chạy                          | Frontmatter/Body split + compile step | Phần 8        |
