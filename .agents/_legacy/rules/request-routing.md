---
name: request-routing
version: 1.0.0
priority: P0
trigger: always_on
description: "Tự động phân loại yêu cầu của người dùng và định tuyến đến đúng Workflow, Skill hoặc Agent tương ứng trong Agent Kit Creator."
---

# Request Routing - Agent Kit Creator

> Rule luôn luôn kích hoạt. Phân loại mọi ý tưởng/yêu cầu của người dùng và tự động định tuyến đến luồng xử lý hoặc skill tối ưu nhất.

---

## 📥 BẢNG ĐỊNH TUYẾN YÊU CẦU (REQUEST CLASSIFIER)

Mỗi khi nhận yêu cầu, phân loại và kích hoạt luồng xử lý tương ứng:

| Loại Yêu cầu | Từ khóa Trigger | Luồng xử lý / Workflow | Skill & Công cụ Cần nạp | Output mong muốn |
| :--- | :--- | :--- | :--- | :--- |
| **TẠO KIT MỚI** | "tạo kit", "viết agent", "xây dựng kit", "tạo prompt agent mới" | `/create-kit` (`workflows/create-kit.md`) | `domain-analysis` ➔ `prompt-engineering` ➔ `skill-crafting` ➔ `kit-assembly` | Agent Kit hoàn chỉnh theo Kit Type |
| **NÂNG CẤP / FIX KIT** | "nâng cấp", "refactor", "sửa kit", "thêm tính năng cho kit", "tối ưu token" | `/refactor-kit` (`workflows/refactor-kit.md`) | `kit-evolution` ➔ `prompt-engineering` / `skill-crafting` | Delta Patch & Bản tổng hợp nâng cấp |
| **KIỂM ĐỊNH / AUDIT** | "kiểm định", "kiểm tra kit", "validate", "chấm điểm kit", "đánh giá" | `/validate-kit` (`workflows/validate-kit.md`) | `quality-assurance` (Audit 3 lớp & Rubric 5 sao) | Báo cáo Đánh giá Audit Report |
| **LƯU BỘ NHỚ / BÀI HỌC** | "lưu bài học", "lưu kit mẫu", "ghi nhớ pattern", "đút rút kinh nghiệm" | `/remember-kit` (`workflows/remember-kit.md`) | Cập nhật `memory/kit-patterns.md` hoặc `memory/golden-examples/` | Bộ nhớ dài hạn được lưu vết |

---

## 💧 MA TRẬN ĐỊNH TUYẾN TÀI NGUYÊN (DYNAMIC HYDRATION ROUTER MATRIX)

Khi thực thi tác vụ tạo mới/nâng cấp cấu phần, **chỉ nạp duy nhất** Template và Reference tương ứng theo bảng dưới đây (On-Demand Hydration):

| Loại Cấu phần (Target Component) | Template Cần Nạp (`templates/`) | Reference Tri thức Cần Nạp (`references/`) |
| :--- | :--- | :--- |
| **System Prompt / Agent Prompt** | `agent-template.md` | `agent-design-patterns.md` |
| **Skill mới** | `skill-template.md` | `component-specs/skill-spec.md` |
| **Workflow mới** | `workflow-template.md` | `workflow-master-framework.md` |
| **Orchestrator Agent** | `orchestrator-template.md` | `orchestrator-agent-pattern.md` + `suite-build-protocol.md` |
| **Rule / Protocol mới** | `rule-template.md` | `file-standards.md` |
| **Memory System** | `memory-template.md` | `component-specs/memory-spec.md` |
| **Sửa lỗi / Refactor Task** | *(Không nạp template)* | `failure-modes.md` + `outcome-lenses.md` |
| **Kiểm định / Audit Kit** | *(Không nạp template)* | `quality-standards.md` |

---

## 🤖 QUY TRÌNH KÍCH HOẠT VÀ THÔNG BÁO SKILL (SKILL ANNOUNCEMENT PROTOCOL)

1. **Xác định Skill & Tài nguyên**: Ngay sau khi phân loại yêu cầu, chọn danh sách skill và cặp `(Template, Reference)` tương ứng từ Hydration Matrix.
2. **Thông báo công khai (MANDATORY)**: Thông báo cho người dùng trước khi thực thi:
   ```markdown
   📚 **Using skill: `@[skill-name]`...**
   ```
   *(Hoặc nạp nhiều skill: `📚 Using skills: @domain-analysis + @prompt-engineering...`)*
3. **Thực thi phân cấp (Selective Reading)**: Đọc file `SKILL.md` trước, chỉ đọc thêm đúng Template / Reference được chỉ định từ Hydration Matrix khi đến bước khởi tạo file.

