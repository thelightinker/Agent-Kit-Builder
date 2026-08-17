# SUITE_BUILD Protocol

Khi yêu cầu là **bộ nhiều agent phối hợp** (multi-agent system), dùng protocol này.

---

## Khi nào kích hoạt SUITE_BUILD

- User yêu cầu 2+ agent cần giao tiếp nhau
- User mô tả workflow cần nhiều "vai trò" phối hợp
- User dùng từ: "hệ thống", "bộ agent", "pipeline", "team AI"

**Không kích hoạt khi**: user chỉ cần 1 agent làm nhiều việc → đó là multi-state
agent (Tier 2), không phải SUITE_BUILD.

---

## Phân biệt Multi-State Agent vs SUITE_BUILD

| | Multi-State Agent (Tier 2) | SUITE_BUILD (Tier 3) |
|:-|:---------------------------|:---------------------|
| Số agent | 1 agent, nhiều chế độ | 2+ agent riêng biệt |
| Giao tiếp | Không cần — 1 agent tự chuyển mode | Cần handoff protocol giữa agents |
| Context | Shared trong 1 prompt | Mỗi agent có prompt riêng |
| Lens E | Không bắt buộc | Bắt buộc |
| Output | 1 Agent Kit document | N Agent Kit documents + 1 Manifest |

---

## Quy trình SUITE_BUILD

### 1. Xác định Agent Roster

Cho mỗi agent trong bộ:
- **Tên**: identifier duy nhất
- **Vai trò**: 1 câu — core competency
- **Ranh giới**: agent này sở hữu gì, KHÔNG sở hữu gì

**Nguyên tắc**: 1 agent = 1 core competency. Không overlap.

### 2. Thiết kế Handoff Protocol

Cho mỗi cặp agent giao tiếp:

| Từ | Đến | Khi nào | Gửi gì | Format |
|:---|:----|:--------|:--------|:-------|
| Agent A | Agent B | [Điều kiện trigger] | [Data payload] | [Schema] |

**Tiêu chí handoff tốt**:
- Điều kiện trigger là nhị phân (rõ khi nào fire, khi nào không)
- Data payload đủ để agent nhận tự hành động (không cần hỏi lại)
- Format chuẩn hoá (không free-form text)

### 3. Thiết kế Lead Agent (Master Orchestrator Protocol)

Bắt buộc có **1 lead agent (Orchestrator)** giữ quyền điều phối và quyết định cuối cùng. Lead Agent BẮT BỘC tuân thủ **Master Orchestrator Protocol** ([orchestrator-agent-pattern.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/orchestrator-agent-pattern.md)):

Lead Agent:
- **Phase 0 & Pre-flight Check**: Đọc plan `{task-slug}.md`, fallback tự tạo plan nếu thiếu để chống deadlock.
- **Ranh giới nghiêm ngặt (Boundary Enforcement)**: Khai báo rõ bảng CAN/CANNOT DO và File Ownership Patterns (`**/*.test.*`, `**/components/**`) cho từng subagent.
- **Worker Prompt Golden Rule**: Chỉ đạo worker với đường dẫn file, dòng code, nội dung sửa cụ thể thay vì prompt mơ hồ.
- **Coordinator Mode Concurrency**: Dispatch Research/Verification song song, Implementation tuần tự theo từng file.
- **Fork vs Spawn Semantics**: Dùng Fork cho research kế thừa ngữ cảnh, Spawn cho specialist chuyên sâu.
- **Synthesis Report**: Thu nhận, giải quyết xung đột (Security > Reliability > Performance) và tạo báo cáo tổng hợp.

### 4. Chạy Parallel Guard (nếu có song song)

Nếu bất kỳ agent nào chạy song song:

```
Sub-task PHỤ THUỘC quyết định lẫn nhau (style, thiết kế chung)?
  → CÓ: KHÔNG chia song song. Dùng 1 agent tuần tự.
  → KHÔNG:
     → 1 lead agent duy nhất giữ quyền quyết định cuối
     → Ranh giới + output format từng sub-agent viết tường minh
     → Không 2 agent trùng nhiệm vụ
```

### 5. Generate từng Agent Kit

Mỗi agent trong bộ → 1 Agent Kit document riêng, theo cấu trúc lõi:
- TÓM TẮT CHO NGƯỜI DÙNG
- SYSTEM PROMPT với 4 section
- Khối mở rộng (Lens E bắt buộc cho mọi agent trong bộ)

### 6. Generate Manifest

1 file Manifest cấp bộ, theo Dual Output:

```markdown
# MANIFEST: [TÊN BỘ AGENT]

## TÓM TẮT CHO NGƯỜI DÙNG
[3-5 dòng đời thường: bộ này làm gì / gồm mấy agent / khi nào dùng / giới hạn]

---

## CHI TIẾT KỸ THUẬT

### Agent Roster
| Agent | Vai trò | Ranh giới |
|:------|:--------|:----------|
| [Tên] | [Core competency] | [Sở hữu gì / KHÔNG sở hữu gì] |

### Lead Agent
[Tên] — [lý do chọn làm lead]

### Luồng chạy
[Mô tả sequence / parallel / conditional routing]

### Handoff Table
| Từ | Đến | Trigger | Payload | Format |
|:---|:----|:--------|:--------|:-------|

### Escalation Path
[Khi nào toàn bộ bộ agent dừng lại và hỏi người]
```

---

## Failure Modes đặc trưng SUITE_BUILD

| Failure | Nguyên nhân | Giải pháp |
|:--------|:------------|:----------|
| Infinite handoff loop (A→B→C→A) | Không agent nào "sở hữu" task | 1 lead agent có quyền quyết định cuối |
| Xung đột khi merge kết quả | Sub-agent thiếu shared context | Chia ranh giới tường minh, output format chuẩn hoá |
| Context drift giữa agents | Mỗi agent hiểu task hơi khác | Lead agent viết brief thống nhất trước dispatch |
| Overhead > value | Quá nhiều agent cho task đơn giản | Kiểm tra: 1 multi-state agent có đủ không? |
| Dead letter | Agent gửi handoff nhưng không ai nhận | Mọi handoff phải map tới agent cụ thể |

---

## Quality Gate cho SUITE_BUILD

```
□ Mỗi agent có Agent Kit document riêng
□ Manifest có Dual Output (Tóm tắt + Kỹ thuật)
□ Lead agent được chỉ định rõ
□ Mọi handoff có: trigger, payload, format
□ Không 2 agent trùng core competency
□ Nếu song song: đã qua Parallel Guard
□ Escalation path cho toàn bộ bộ agent
□ Lens E có trong mọi agent kit của bộ
```
