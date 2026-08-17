# Kit Types — Chi tiết

Mỗi kit type có đặc điểm, component set, và anti-patterns riêng.
Chọn đúng type là bước quan trọng nhất — over-engineer Micro thành
Professional phí token, under-engineer Professional thành Micro thiếu cơ chế.

---

## Micro Kit

**Khi nào**: 1 tác vụ, input/output cố định, không cần nhớ, không cần skill riêng.

**Components**: Agent system prompt only (1 file markdown).

**Quy mô**: < 300 từ system prompt, 3-4 DoD items, 2-3 constraints.

**Ví dụ phù hợp**:
- Agent tóm tắt email
- Agent dịch văn bản với style guide cố định
- Agent format dữ liệu từ format A sang format B

**Anti-patterns**:
- Thêm memory cho agent không cần nhớ gì
- Thêm workflow cho agent chỉ làm 1 bước
- System prompt > 500 từ

**Template**:
```markdown
# [TÊN AGENT]

## TÓM TẮT CHO NGƯỜI DÙNG
[3-5 dòng đời thường]

---

# SYSTEM PROMPT: [TÊN AGENT]

## 1. VAI TRÒ & OUTCOME ĐÍCH
[Vai trò 1 câu]

### Definition of Done
- [ ] [Tiêu chí 1 — nhị phân, đo được]
- [ ] [Tiêu chí 2]
- [ ] [Tiêu chí 3]

## 2. NGUYÊN TẮC VẬN HÀNH
[Outcome → Cơ chế — 2-3 nguyên tắc]

## 3. HARD CONSTRAINTS
- KHÔNG [constraint 1 — cụ thể, verifiable]
- KHÔNG [constraint 2]

## 4. FORMAT ĐẦU RA
[Template output]
```

---

## Standard Kit

**Khi nào**: Nhiều tác vụ, hoặc cần context/memory, hoặc cần skill riêng
cho capability phức tạp (> 100 từ instructions).

**Components**: Agent + Skills và/hoặc Memory. Có thể có Workflow đơn giản.

**Quy mô**: System prompt 300-800 từ, 4-6 DoD items, 3-5 constraints.

**Ví dụ phù hợp**:
- Agent viết sách cần memory giữ giọng văn
- Agent phân tích tài chính cần skill đọc báo cáo
- Agent hỗ trợ code cần skill review + skill test

**Anti-patterns**:
- Tạo manifest cho kit chỉ có 1 agent + 1 skill
- Thêm routing rules khi chỉ có 1 agent
- Scripts phức tạp cho task đơn giản

**Directory structure**:
```
kit-name/
├── README.md
├── agent/
│   └── [agent-name].md
├── skills/
│   └── [skill-name]/
│       ├── SKILL.md
│       └── references/     # nếu cần
└── memory/                 # nếu cần
    └── [memory-files]
```

---

## Professional Kit

**Khi nào**: Hệ thống đa thành phần — nhiều agents (có thể 1 agent chính
+ nhiều specialist agents), cần validation, rules, scripts, manifest.

**Components**: Full set — Agents + Skills + Memory + Workflows + Rules +
Scripts + Manifest + Architecture doc.

**Quy mô**: Mỗi agent 500-1500 từ, manifest-driven, scripts cho validation.

**Ví dụ phù hợp**:
- Bộ toolkit phát triển web (frontend + backend + test + devops agents)
- Hệ thống AI content pipeline (research + write + edit + publish)
- Platform quản lý dự án (plan + execute + monitor + report)

**Đặc trưng của Professional Kit chất lượng cao**
(trích xuất từ demo kit — bộ kit có 20 agents, 47 skills, 13 workflows):

1. **Versioned Frontmatter**: Mọi component có SemVer, tools, triggers
2. **Manifest Registry**: `manifest.json` map agents → skills → tools
3. **Request Routing**: Rules phân loại request → route đúng agent
4. **Skill Loading Protocol**: Conditional loading dựa trên `when_to_use`
5. **Core Protocol**: Rules bắt buộc (Read → Understand → Apply)
6. **Agent Boundary Enforcement**: Rõ scope, banned agents per context
7. **Validation Scripts**: `validate_kit.py`, `generate_manifest.py`
8. **Memory System**: `MEMORY.md` index + structured memory files
9. **Architecture Doc**: Tổng quan hệ thống, agent roster, skill catalog

**Directory structure**:
```
kit-name/
├── README.md
├── ARCHITECTURE.md
├── VERSION
├── manifest.json
├── manifest.lock.json     # optional: integrity hashes
├── agent/
│   ├── orchestrator.md    # nếu multi-agent
│   └── [agents].md
├── skills/
│   └── [skill-folders]/
├── workflows/
│   └── [workflows].md
├── rules/
│   ├── core-protocol.md
│   ├── request-routing.md  # nếu multi-agent
│   └── [domain-rules].md
├── memory/
│   ├── MEMORY.md
│   └── [memory-files]
├── schemas/                # optional: JSON schemas
│   └── [schemas].json
└── scripts/
    ├── validate_kit.py
    └── [other-scripts]
```

---

## Suite Kit

**Khi nào**: Nhiều agent độc lập cần phối hợp — có handoff protocol,
shared context, và lead agent điều phối.

**Components**: Như Professional, thêm handoff protocol và orchestrator.

**Quy mô**: Mỗi agent 300-1000 từ, orchestrator có quyền quyết định cuối.

**Đặc trưng Suite Kit**:
1. **Lead Agent Designation (Chỉ định Lead Agent)**: Bắt buộc chỉ định 1 agent duy nhất giữ quyền quyết định cuối cùng, phân rã công việc cho các sub-agents, thu nhận kết quả và giải quyết mâu thuẫn (synthesis).
2. **Parallel Guard Rules**: 
   * *Khi nào chạy song song*: Các sub-task độc lập, không quyết định chéo đến thiết kế/giao diện của nhau (ví dụ: Security audit + Performance check).
   * *Khi nào bắt buộc tuần tự*: Các sub-task phụ thuộc hoặc có quyết định chéo (ví dụ: API design -> Frontend implementation).
3. **Explicit Handoff Protocol (Hợp đồng Handoff)**: Định nghĩa rõ ràng luồng truyền tin.
   Format: `[Từ Agent] -> [Đến Agent] | [Điều kiện kích hoạt (Trigger)] | [Dữ liệu gửi đi (Payload)] | [Định dạng dữ liệu (Format)]`
4. **Manifest Blueprint**: Có file `manifest.json` đăng ký đầy đủ thông tin Suite.

### Blueprint Manifest cho Suite Kit
```markdown
# MANIFEST: [TÊN BỘ AGENT]

## TÓM TẮT CHO NGƯỜI DÙNG
[3-5 dòng đời thường: bộ này làm gì / gồm mấy agent / giới hạn]

---

## CHI TIẾT KỸ THUẬT

### Agent Roster (Danh sách Agent)
| Agent | Vai trò | Ranh giới (Sở hữu gì / Không sở hữu gì) |
|:------|:--------|:----------------------------------------|
| [Lead Agent] | Điều phối & Synthesis | Hợp nhất kết quả / Phân rã task |
| [Specialist A] | Thực thi A | Sở hữu tác vụ A / KHÔNG can thiệp B |

### Luồng chạy & Parallel Guard
- Luồng tuần tự: Lead Agent -> Specialist A -> Lead Agent.
- Song song: Specialist B & Specialist C chạy song song khi nhận brief từ Lead.

### Handoff Table
| Từ | Đến | Trigger (Khi nào) | Payload (Gửi gì) | Format (Định dạng) |
|:---|:----|:------------------|:-----------------|:-------------------|
| Lead | Agent A | Task được phân rã | Code snippet + test case | JSON schema |

### Escalation Path
[Quy tắc dừng toàn bộ hệ thống để hỏi ý kiến người dùng khi gặp lỗi lặp hoặc thiếu dữ liệu đầu vào]
```

---

## Kit Type Decision Matrix

```
Yêu cầu user
    │
    ├── 1 tác vụ, đơn giản? → MICRO
    │
    ├── Nhiều tác vụ hoặc cần context? → STANDARD
    │
    ├── Cần validation, scripts, nhiều rules?
    │   ├── 1 agent chính? → PROFESSIONAL
    │   └── Nhiều agent phối hợp? → SUITE
    │
    └── Không rõ? → Default STANDARD, hỏi user confirm
```
