---
name: compiling-prompts
description: "Use when generating or refactoring the core System Prompt for an agent, ensuring proper structure, binary Definition of Done, and specific constraints."
when_to_use: "Kích hoạt khi cần năng lực compiling-prompts trong quy trình tạo hoặc kiểm định Agent Kit."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# Compiling Prompts

## Overview
Biên dịch yêu cầu và thiết kế nghiệp vụ thành một System Prompt tối ưu, có cấu trúc chặt chẽ, dễ hiểu đối với LLM và có các tiêu chí đo lường rõ ràng.

## When to Use
- Khi Kit Generator bắt đầu tạo hoặc refactor component `Agent`.
- Khi cần chuẩn hóa cấu trúc prompt theo mẫu chuẩn 4 sections.

### When NOT to use
- Khi đang tạo các components phi văn bản khác như workflow diagram hoặc memory schema.

## Core Pattern & Architectural Upgrades

Mỗi System Prompt tuân thủ cấu trúc 4 phần cốt lõi hoặc Khung **6-Pattern Modular** (nâng cao cho Standard/Professional Agents). Tham chiếu tài liệu kỹ thuật: [agent-design-patterns.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/agent-design-patterns.md).

### 4 Section Cốt lõi (Tier 1 - Micro Agent):
1. **Vai trò & Outcome đích**: Định nghĩa vai trò rõ ràng + Definition of Done (DoD).
   - DoD phải đạt 3 tiêu chuẩn: **Nhị phân** (pass/fail), **Đo được** (metric cụ thể), **Không sáo ngữ** (không dùng tính từ).
2. **Nguyên tắc vận hành**: Hướng dẫn theo format `[Outcome cần đạt] -> [Cơ chế]`.
3. **Hard Constraints**: Các giới hạn bắt đầu bằng "KHÔNG bao giờ..." và có thể verify được.
4. **Format đầu ra**: Template hiển thị mẫu mà agent trả về cho user.

### 5 Architectural Patterns Nâng cao (Tier 2 & 3 - Standard/Professional Agent):
- **📑 Quick Navigation Index**: TOC neo Markdown ở đầu prompt nếu > 500 dòng.
- **🛑 3-Tier Autonomy Gate**: Phân cấp tự chủ (Tier A: Thực thi ngay, Tier B: Tự chủ + Ghi Assumption, Tier C: Stop & Ask khi sự mơ hồ làm thay đổi đáng kể outcome).
- **🧠 Domain-Aware Anti-Default Thinking**: Thách thức ngầm định (UI = Đột phá layout; Backend/Infra = Boring & Stable Tech First).
- **📐 Visual Reasoning & Strategy Matrix**: Sơ đồ ASCII quy trình + ma trận tra cứu chiến lược theo phân loại lỗi/domain.
- **🛡️ Reality Check & Context Leverage**: Kiểm tra bằng chứng thực tế, sửa nguyên nhân gốc rễ và tối ưu đòn bẩy context (Heuristic ROI).

---

## 🎯 Special Case: Biên dịch Orchestrator Agent (Lead Agent)

Khi biên dịch Agent Điều phối (**Orchestrator**) cho bộ Multi-Agent (Suite Kit), BẮT BỘC áp dụng **Master Orchestrator Protocol**:
- Tham chiếu hướng dẫn: [orchestrator-agent-pattern.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/references/orchestrator-agent-pattern.md)
- Template chuẩn: [orchestrator-template.md](file:///c:/Users/nhdcb/OneDrive/Desktop/Agent%20Kit/Agent%20Kit%20Creator/.agents/templates/orchestrator-template.md)

**5 Điểm Bắt buộc cho Orchestrator Prompt**:
1. **Pre-flight Check (Step 0)**: Kiểm tra plan `{task-slug}.md`, fallback tự sinh plan để chống deadlock.
2. **Boundary Matrix**: Phân định CAN / CANNOT DO và File Ownership Pattern (`**/*.test.*` ➔ test agent) cho từng subagent.
3. **Worker Prompt Golden Rule**: Yêu cầu Coordinator cung cấp đúng đường dẫn file, dòng code và thay đổi chi tiết khi giao việc cho worker.
4. **Coordinator Lifecycle**: Chạy Research/Verification song song, Implementation tuần tự theo từng file.
5. **Fork vs Spawn**: Dùng Fork cho research kế thừa context, Spawn cho specialist agent độc lập.

---

## Quick Reference

### Ví dụ DoD chuẩn:
- [ ] File đầu ra tồn tại và có dung lượng > 0 bytes.
- [ ] Không chứa các từ khóa placeholder như [TODO], [TBD].
- [ ] Trả về mã trạng thái `status: done` hoặc `status: failed`.

### Ví dụ DoD không chuẩn:
- [ ] Code sạch sẽ và chạy tốt (mơ hồ, không đo được).
- [ ] Nội dung đầy đủ và chuyên nghiệp (sáo ngữ).

## Common Mistakes
- **Lỗi**: Sử dụng các tính từ cảm tính trong DoD hoặc Constraints.
  - *Khắc phục*: Thay thế bằng con số hoặc sự kiện nhị phân kiểm tra được.
- **Lỗi**: Để phần Format đầu ra trống hoặc quá mơ hồ.
  - *Khắc phục*: Luôn cung cấp một template markdown hoặc JSON cụ thể.
- **Lỗi**: Thiết kế Orchestrator giao nhiệm vụ chung chung cho Subagent (ví dụ: "hãy fix lỗi").
  - *Khắc phục*: Bắt buộc Orchestrator đưa đường dẫn file, dòng code, và nội dung sửa cụ thể theo Worker Prompt Golden Rule.
