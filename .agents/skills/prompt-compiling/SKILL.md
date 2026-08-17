---
name: prompt-compiling
description: >
  Biên dịch System Prompt cho 3 dạng Archetypes (Standalone Agent, Master Orchestrator,
  hoặc Domain Specialist Agent), thiết lập Binary Definition of Done (DoD),
  Hard Constraints dạng phủ định và cấu trúc chuẩn 4 khối.
when_to_use: "Khi cần biên dịch, tối ưu hoặc chuẩn hóa System Prompt cho bất kỳ Agent nào."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 2.2.0
---

# Prompt Compiling

Kỹ năng biên dịch System Prompt chuyên nghiệp, biến yêu cầu nghiệp vụ thành chỉ dẫn tối ưu cho LLM với tỷ lệ đúng ngay lần đầu (Right-First-Time) cao nhất.

---

## 📚 REFERENCE KNOWLEDGE ACTIVATION (NẠP ON-DEMAND)

Khi cần tra cứu kỹ thuật biên dịch prompt nâng cao:
- **Nguyên tắc Điều phối Suite & Specialist Authority**: Đọc [multi-agent-orchestration.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/multi-agent-orchestration.md).
- **3-Tier Autonomy Gate, Anti-Defaults & Reality Check**: Đọc [agent-design-patterns.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/agent-design-patterns.md).
- **Mẫu Scaffolding System Prompt**: Dùng [templates/agent-template.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/templates/agent-template.md) hoặc [templates/orchestrator-template.md](file:///c:/Users/nhdcb/OneDrive/Desktop/AI%20Project/AI%20Agent/Agent%20Kit/Agent%20Kit%20Creator/.agents/templates/orchestrator-template.md).

---

## 1. 3 PROMPT ARCHETYPES

Biên dịch prompt theo đúng vai trò kiến trúc:

### 🌟 Archetype A: Standalone Single Agent
Dành cho Micro / Standard Kit. 1 agent duy nhất nắm toàn bộ quy trình:
1. **Vai trò & Outcome**: 3-5 dòng tóm tắt đời thường + tiêu chí hoàn thành.
2. **Quy trình & Action Matrix**: Các bước tuần tự.
3. **Hard Constraints**: Ràng buộc phủ định.
4. **Output Format**: Khung mẫu đầu ra.

### 🌟 Archetype B: Master Orchestrator
Dành cho Suite Kit. Đóng vai trò nhạc trưởng điều phối:
1. **Socratic & Pre-flight Check**: Làm rõ từ 1-3 câu nếu mơ hồ; nếu rõ thì phân rã task ngay.
2. **Decomposition Protocol**: Tách task lớn thành các sub-tasks độc lập theo domain.
3. **Specialist Routing Table**: Ma trận chọn Specialist Agent phù hợp.
4. **Boundary Enforcement**: Cấm worker can thiệp chéo domain.
5. **Synthesis Format**: Cấu trúc báo cáo tổng hợp bàn giao cho User.

### 🌟 Archetype C: Domain Specialist Agent (Real Agent)
Dành cho các chuyên gia trong Suite Kit:
1. **Domain Authority**: Khẳng định quyền quyết định cao nhất trong domain được giao.
2. **Owned Skills Authority**: Danh sách các kỹ năng thuộc quyền chỉ huy và điều kiện kích hoạt.
3. **Strict Boundaries**: Danh mục những điều ĐƯỢC LÀM và KHÔNG ĐƯỢC LÀM (File ownership).
4. **Handoff Trigger**: Điều kiện khi nào cần dừng lại và chuyển tiếp yêu cầu về cho Orchestrator.

---

## 2. TIÊU CHUẨN BINARY DEFINITION OF DONE (DoD)

Mọi tiêu chí trong DoD bắt buộc phải thỏa mãn 3 kiểm định:
1. **Tính nhị phân**: Chỉ có 2 trạng thái Đạt hoặc Không đạt.
2. **Tính đo lường được**: Có thể kiểm chứng trực tiếp trên output mà không cần phỏng đoán.
3. **Không sáo ngữ**: Cấm dùng tính từ cảm tính ("viết hay", "đầy đủ", "chuyên nghiệp"). Phải thay bằng số liệu hoặc sự kiện ("≥ 500 từ", "có trích dẫn nguồn", "đầy đủ 4 đề mục").

---

## 3. TIÊU CHUẨN HARD CONSTRAINTS

- Viết ở dạng **phủ định bắt buộc** ("KHÔNG BAO GIỜ...", "TUYỆT ĐỐI KHÔNG...").
- Ngăn chặn trực diện các Failure Modes đã dự đoán ở bước Domain Profiling.
