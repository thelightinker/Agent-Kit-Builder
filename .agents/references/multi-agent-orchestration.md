# Multi-Agent Orchestration & Suite Architecture

> Cẩm nang thiết kế và điều phối hệ thống Suite Kit phân cấp (Master Orchestrator + Specialist Agents + Domain Skills + Workflows + Scoped Memory) — Chuẩn hóa theo mô hình Orchestrator & Coordinator tối tân.

---

## 1. MÔ HÌNH PHÂN CẤP SUITE HIERARCHY

Trong một hệ thống Suite Kit đa domain:

```
                            [ USER ]
                               │
                               ▼
                      Master Orchestrator
           (Decompose, Briefing, Synthesis, Conflict Gate)
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
     Specialist Agent A                    Specialist Agent B
     (Domain Specialist A)                 (Domain Specialist B)
            │                                     │
     ┌──────┴──────┐                       ┌──────┴──────┐
     ▼             ▼                       ▼             ▼
  Skill A1      Skill A2                Skill B1      Skill B2
 (domain-ops)  (domain-eval)           (feature-ops)  (feature-eval)
```

---

## 2. NGUYÊN TẮC QUAN TRỌNG: OWNERSHIP $\ne$ EXECUTION

| Khía cạnh | Quyền Sở hữu Năng lực (Ownership) | Quy trình Thực thi (Execution) |
|:---|:---|:---|
| **Chủ thể** | **Specialist Agent** | **Workflow / Orchestrator** |
| **Bản chất** | Tĩnh (Static Authority) | Động (Dynamic State Machine) |
| **Quy tắc** | Specialist sở hữu domain & các kỹ năng trực thuộc (`ownedSkills`). Specialist là đơn vị ra quyết định chất lượng trong domain. | 1 Workflow có thể yêu cầu **nhiều Specialist phối hợp liên hoàn**. Orchestrator theo dõi chuyển tiếp State. |

*Chống bẫy:* Specialist Agent không phải là một "vỏ bọc 1 skill". Nó là một Agent thật sở hữu cụm năng lực chuyên môn và ranh giới tệp tin (File Boundaries) rõ ràng.

---

## 3. COORDINATOR LIFECYCLE & CONCURRENCY MATRIX

Master Orchestrator vận hành theo 5 pha chặt chẽ:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│ 1. DECOMPOSE │ ──> │ 2. RESEARCH  │ ──> │ 3. SYNTHESIS │ ──> │ 4. IMPLEMENTATION│ ──> │ 5. VERIFY    │
│ Phân rã task │     │ Đọc song song│     │ Nhạc trưởng  │     │ Ghi tuần tự file │     │ Kiểm thử song│
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────────┘     └──────────────┘
```

### Bảng Ma Trận Phân Luồng Đồng Thời (Concurrency Matrix):
| Thao tác | Mức độ an toàn song song | Quy tắc thực thi |
|:---|:---:|:---|
| **Đọc dữ liệu / Khảo sát codebase** | ✅ An toàn tuyệt đối | Cho phép nhiều worker chạy song song (Parallel Reads). |
| **Kiểm tra bảo mật + Hiệu năng (Read-only)** | ✅ An toàn tuyệt đối | Cho phép chạy song song nhiều specialist. |
| **Ghi đè / Sửa đổi mã nguồn** | ⚠️ Nguy cơ xung đột cao | Bắt buộc tuần tự trên từng cụm file (Sequential Writes). Không cho 2 agent ghi cùng 1 file. |
| **Chạy kiểm thử / Lint / Schema validation** | ✅ An toàn độc lập | Chạy song song sau khi hoàn tất pha Implementation. |

---

## 4. WORKER BRIEFING & "NEVER DELEGATE UNDERSTANDING"

### 🔴 Nguyên Tắc Cốt Lõi:
Master Orchestrator **KHÔNG BAO GIỜ** đẩy trách nhiệm thấu hiểu (synthesis) cho worker. Orchestrator phải tự tìm ra nguyên nhân gốc, định vị file, dòng và phạm vi rồi mới giao việc.

```
❌ PHẢN MẪU (BỊ CẤM):
  - "Dựa trên báo cáo khảo sát, hãy fix lỗi trong hệ thống."
  - "Xem thư mục src rồi refactor lại cho chuẩn."
  - "Based on the findings, implement the fix."

✅ CHUẨN MỰC WORKER BRIEFING:
  - "Bối cảnh: User muốn tối ưu hóa tốc độ tải trang Auth.
     Phát hiện: File `src/auth/jwt.ts` dòng 45 đang fetch dữ liệu tuần tự gây waterfall (thêm 350ms).
     Nhiệm vụ: Sửa dòng 45 sang `Promise.all()` để fetch song song.
     Ranh giới: KHÔNG sửa file middleware hay database schema.
     Kiểm chứng: Chạy `npm test` và kiểm tra không còn console warning."
```

---

## 5. FORK SEMANTICS VS SPAWN SPECIALIST

Khi nào nên Fork ngữ cảnh (Fork Subagent) và khi nào nên gọi Chuyên gia mới (Spawn Specialist):

| Tình huống | Hành động | Rationale |
|:---|:---:|:---|
| Nghiên cứu mở rộng, đào sâu tiếp cùng 1 chủ đề | **Fork Subagent** (kế thừa context) | Tiết kiệm prompt briefing, tận dụng bộ nhớ đệm có sẵn. |
| Khảo sát nhiều nhánh độc lập trong cùng 1 lượt | **Fork Multiple** | Chạy song song các worker đọc nhanh. |
| Thực thi tác vụ thuộc domain chuyên sâu (Security/DB/UI) | **Spawn Specialist** (gọi Role riêng) | Khởi động chuyên gia với system prompt và quy tắc domain chuẩn xác. |
| Cần góc nhìn độc lập thứ hai (Second opinion / Code review) | **Spawn Specialist** (chuyên gia review) | Đảm bảo tính khách quan, không bị bias bởi context cũ. |

---

## 6. THỨ TỰ ƯU TIÊN GIẢI QUYẾT XUNG ĐỘT (CONFLICT RESOLUTION)

Khi các Specialist đưa ra các đề xuất mâu thuẫn:
1. **User Requirements & Security Hard Gates** (Yêu cầu tường minh từ User và tiêu chuẩn bảo mật là số 1).
2. **Executable Evidence & Automated Tests** (Bằng chứng thực thi thực tế thắng mọi suy diễn lý thuyết).
3. **Architecture SSOT & Ownership Matrix** (Tuân thủ ranh giới phân quyền file của từng Specialist).
4. **Specialist Recommendations** (Ý kiến của chuyên gia phụ trách trực tiếp domain).
5. **Minimal-Change Principle** (Ưu tiên giải pháp tinh gọn, ít tác động lan truyền).

---

## 7. KIẾN TRÚC BỘ NHỚ PHÂN TẦNG (SCOPED MEMORY)

```
memory/
├── MEMORY.md                         # File chỉ mục chính (SSOT, ≤ 200 dòng)
├── shared/                           # [SHARED SCOPE] Tri thức nền tảng toàn bộ Suite (Brand voice, conventions)
│   ├── brand-guidelines.md           # (Mọi Specialist đều được đọc)
│   └── project-conventions.md
├── domains/                          # [DOMAIN SCOPE] Tri thức chuyên sâu của từng Specialist
│   ├── specialist-a-rules.md         # (Chỉ Specialist A đọc)
│   └── specialist-b-rules.md         # (Chỉ Specialist B đọc)
└── runs/                             # [SESSION/RUN SCOPE] Trạng thái thực thi đa-phiên & Golden Runs
    └── features-tracker.json         # (DoD theo dõi tiến độ ngoài context window)
```
