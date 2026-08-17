# Multi-Agent Orchestration & Suite Architecture

> Cẩm nang thiết kế và điều phối hệ thống Suite Kit phân cấp (Master Orchestrator + Specialist Agents + Domain Skills + Workflows + Scoped Memory) — lấy cảm hứng từ triết lý `vudovn/ag-kit`.

---

## 1. MÔ HÌNH PHÂN CẤP SUITE HIERARCHY

Trong một hệ thống Suite Kit đa domain:

```
                            [ USER ]
                               │
                               ▼
                      Master Orchestrator
                      (Routing, Socratic, Synthesis)
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
     Specialist Agent A                    Specialist Agent B
     (Domain SEO Specialist)               (Domain Copy Specialist)
            │                                     │
     ┌──────┴──────┐                       ┌──────┴──────┐
     ▼             ▼                       ▼             ▼
  Skill A1      Skill A2                Skill B1      Skill B2
 (seo-audit)   (ai-seo)               (copywriting)   (emails)
```

---

## 2. NGUYÊN TẮC QUAN TRỌNG: OWNERSHIP $\ne$ EXECUTION

| Khía cạnh | Quyền Sở hữu Năng lực (Ownership) | Quy trình Thực thi (Execution) |
|:---|:---|:---|
| **Chủ thể** | **Specialist Agent** | **Workflow / Orchestrator** |
| **Bản chất** | Tĩnh (Static Authority) | Động (Dynamic State Machine) |
| **Quy tắc** | Specialist sở hữu domain & các kỹ năng trực thuộc (`ownedSkills`). Specialist là đơn vị ra quyết định chất lượng trong domain. | 1 Workflow có thể yêu cầu **nhiều Specialist phối hợp liên hoàn**. Orchestrator theo dõi chuyển tiếp State. |

*Chống bẫy:* Specialist Agent không phải là một "vỏ bọc 1 skill". Nó là một Agent thật sở hữu cụm năng lực chuyên môn.

---

## 3. MASTER ORCHESTRATOR PROTOCOL (5 BƯỚC)

1. **Pre-flight & Socratic Check**: Kiểm tra input; nếu mơ hồ, hỏi tối đa 1-3 câu trọng tâm; nếu rõ ràng, phân rã công việc ngay.
2. **Task Decomposition**: Tách mục tiêu lớn thành các sub-tasks độc lập theo từng domain.
3. **Specialist Dispatching**: Giao việc cho đúng Specialist Agent kèm directive cụ thể (file path, line number, scope).
4. **Boundary Enforcement**: Nghiêm cấm worker sửa chéo file thuộc phạm vi của agent khác.
5. **Synthesis & Output Delivery**: Gom kết quả từ các worker, giải quyết xung đột (nếu có) và xuất báo cáo tổng hợp.

---

## 4. KIẾN TRÚC BỘ NHỚ PHÂN TẦNG (SCOPED MEMORY)

Tránh biến bộ nhớ thành "bãi rác context chung", chia thành 3 tầng:

```
memory/
├── MEMORY.md                         # File chỉ mục chính (SSOT, ≤ 200 dòng)
├── shared/                           # [SHARED SCOPE] Tri thức nền tảng toàn bộ Suite
│   ├── brand-guidelines.md           # (Mọi Specialist đều được đọc)
│   └── project-conventions.md
├── domains/                          # [DOMAIN SCOPE] Tri thức chuyên sâu của từng Specialist
│   ├── seo-playbook.md               # (Chỉ SEO Specialist đọc)
│   └── copy-frameworks.md            # (Chỉ Copy Specialist đọc)
└── runs/                             # [SESSION/RUN SCOPE] Trạng thái thực thi đa-phiên
    └── features-tracker.json         # (DoD theo dõi tiến độ ngoài context window)
```
