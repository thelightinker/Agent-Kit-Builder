---
name: create-kit
description: "Quy trình tạo Agent Kit mới từ đầu theo chuẩn Evolvable Architecture (Create Kit)."
version: 2.1.0
requires_agents: kit-architect
requires_skills: [domain-profiling, prompt-compiling, skill-architecting, kit-assembling, kit-verifying]
artifact_outputs: [domain_profile, system_prompt, skill_manifest, validation_report]
---

# Workflow: /create-kit

Quy trình chuẩn mực để tạo một Agent Kit mới từ đầu, áp dụng cơ chế kỷ luật quy trình (Process Gate) kết hợp Superpowers.

---

## 🚦 BƯỚC 0: SUPERPOWERS PROCESS & SKILL GATE (BẮT BUỘC)

Trước khi tạo bất kỳ thư mục hoặc file nào trong `./output/<kit-name>/`:

1. **Invoke Brainstorming:** BẮT BUỘC invoke `superpowers:brainstorming`.
2. **Khóa Design Spec:** Thống nhất với User về: Mục tiêu cốt lõi, Complexity Tier, 5 Core Verbs, 80/20 Leverage và Danh sách Cấu phần tối thiểu.
3. **Approval Gate:** Nhận sự phê duyệt (`APPROVED`) từ User cho Design Spec trước khi tiến hành viết Plan.
   - 🚫 **HARD CONSTRAINT:** TUYỆT ĐỐI KHÔNG tự ý viết code, tạo file hay scaffold thư mục khi Design Spec chưa được User phê duyệt.
   - ⚠️ **Quy tắc Bypass:** Chỉ được bỏ qua Bước 0 khi yêu cầu là `FAST_TRACK` (Micro Kit 1-shot đơn lẻ đã có sẵn prompt hoàn chỉnh và không tạo thư mục/skill). Agent tuyệt đối KHÔNG được tự ý phán đoán để bypass khi tạo Standard/Pro/Suite Kit.
4. **Planning & Execution:** Sau khi Design Spec được duyệt ➔ Invoke `superpowers:writing-plans` để lập kế hoạch ➔ Thực thi qua `superpowers:executing-plans`.

---

## 🔄 STATE MACHINE NODES

### Bước 1: Phân tích Nghiệp vụ (Domain Profiling)
- **Role Profile:** `@analyst` | **Skill:** `domain-profiling`
- **[Input Artifacts]:** Yêu cầu của User + Design Spec đã duyệt.
- **[Output Artifacts]:** `domain_profile.md` (Core Verbs, ROI leverage $\ge 1.25$, Predicted Failure Modes).
- **[DoD]:** 
  - [ ] Liệt kê đủ 5-10 Core Verbs kèm 4 tiêu chí đánh giá.
  - [ ] Có ít nhất 1 đòn bẩy 80/20 đạt tỷ lệ ROI $\ge 1.25$.
  - [ ] Dự đoán $\ge 3$ Failure Modes đặc trưng domain.
- **[Evaluation Loop]:** Pass ➔ Chuyển Bước 2 | Fail ➔ Bổ sung phân tích.

---

### Bước 2: Biên dịch System Prompt (Prompt Compiling)
- **Role Profile:** `@compiler` | **Skill:** `prompt-compiling`
- **[Input Artifacts]:** `domain_profile.md`
- **[Output Artifacts]:** System Prompt của Agent (`agent/<name>.md` hoặc `<name>.md`).
- **[DoD]:**
  - [ ] Có phần TÓM TẮT CHO NGƯỜI DÙNG ở đầu (0 thuật ngữ AI, 3-5 dòng).
  - [ ] Có đủ 4 khối chuẩn: Vai trò, Quy trình, Hard Constraints, Format đầu ra.
  - [ ] Binary DoD: 100% nhị phân, đo lường được, 0 tính từ cảm tính.
- **[Evaluation Loop]:** Pass ➔ Chuyển Bước 3 | Fail ➔ Tinh chỉnh prompt.

---

### Bước 3: Thiết kế Kỹ năng & Kiến trúc (Skill Architecting)
*(Chỉ thực hiện cho Standard / Professional / Suite Kits)*
- **Role Profile:** `@architect` | **Skill:** `skill-architecting`
- **[Input Artifacts]:** `domain_profile.md`, System Prompt.
- **[Output Artifacts]:** Thư mục `skills/<skill-name>/SKILL.md`.
- **[DoD]:**
  - [ ] `SKILL.md` có đầy đủ YAML frontmatter hợp lệ.
  - [ ] Chiều dài `SKILL.md` $\le 500$ dòng (tách `references/` nếu dài hơn).
  - [ ] Có ví dụ minh họa và checklist kiểm thử.
- **[Evaluation Loop]:** Pass ➔ Chuyển Bước 4.

---

### Bước 4: Lắp ráp & Đóng gói (Kit Assembling)
- **Skill:** `kit-assembling`
- **[Input Artifacts]:** Toàn bộ components đã tạo.
- **[Output Artifacts]:** `./output/<kit-name>/` hoàn chỉnh kèm `manifest.json`.
- **[DoD]:**
  - [ ] Toàn bộ file nằm trong `./output/<kit-name>/`.
  - [ ] `manifest.json` đồng bộ 100% danh mục files và SemVer `1.0.0`.
- **[Evaluation Loop]:** Pass ➔ Chuyển Bước 5.

---

### Bước 5: Kiểm định Chất lượng 3 Lớp (Quality Verification)
- **Role Profile:** `@auditor` | **Skill:** `kit-verifying`
- **[Input Artifacts]:** `./output/<kit-name>/`
- **[Output Artifacts]:** `validation_report.md`
- **[DoD]:**
  - [ ] L1: `python .agents/scripts/validate_kit.py ./output/<kit-name>` trả về `0 error(s)`.
  - [ ] L2: Chạy thành công 2 kịch bản input thực tế theo domain.
  - [ ] L3: Vượt qua bài test đối kháng (Adversarial stress test).
  - [ ] Điểm Rubric $\ge 4/5$ ⭐.
- **[Evaluation Loop]:** 
  - PASS: Bàn giao kit cho User kèm hướng dẫn sử dụng.
  - FAIL: Kích hoạt `/refactor-kit` để khắc phục lỗi.
