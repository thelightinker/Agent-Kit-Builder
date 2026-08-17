---
name: refactor-kit
description: "Cải tiến & Nâng cấp Agent Kit đã có sẵn (Refactor Kit)."
version: 2.0.0
requires_agents: kit-architect
requires_skills: kit-evolving, kit-verifying, prompt-compiling, skill-architecting
artifact_outputs: refactored-kit-spec
---

# Workflow: Refactor Kit (Cải tiến & Nâng cấp Kit)

Sử dụng khi người dùng yêu cầu nâng cấp, sửa đổi hoặc thêm tính năng cho một Agent Kit đã có sẵn.

---

## Các bước thực hiện

### Bước 1: Tiếp nhận & Đánh giá hiện trạng
1. Đọc toàn bộ cấu trúc của Agent Kit hiện tại.
2. Chạy workflow: `workflows/validate-kit.md` trên kit hiện tại để tìm điểm yếu, lỗi cấu trúc hoặc sự thiếu hụt.
3. Xác định yêu cầu nâng cấp của user: Bổ sung skill, sửa lỗi prompt, tối ưu hóa token.

---

### Bước 2: Phân tích sự lệch pha (Gap Analysis)
1. Kích hoạt skill: `skills/kit-evolving/SKILL.md`.
2. Xác định mức độ thay đổi:
   - *Patch* (1.0.0 $\rightarrow$ 1.0.1): Sửa lỗi nhỏ/câu chữ prompt.
   - *Minor* (1.0.0 $\rightarrow$ 1.1.0): Thêm skill phụ / workflow mới.
   - *Major* (1.0.0 $\rightarrow$ 2.0.0): Đổi cấu trúc kit hoặc ranh giới kiến trúc.

---

### Bước 3: Thực hiện chỉnh sửa chọn lọc (Delta Patch)
1. **Chỉ sửa phần cần thiết**: Không viết lại toàn bộ các file lớn nếu không được yêu cầu.
2. Nếu sửa System Prompt: Kích hoạt `skills/prompt-compiling/SKILL.md`.
3. Nếu thêm Skill mới: Kích hoạt `skills/skill-architecting/SKILL.md`.
4. Cập nhật SemVer trong frontmatter của các thành phần bị ảnh hưởng.
5. Cập nhật `manifest.json` (nếu có).

---

### Bước 4: Tái kiểm định (Re-Audit)
1. Chạy lại workflow: `workflows/validate-kit.md` trên kit sau khi chỉnh sửa.
2. Đảm bảo kit mới đạt ít nhất **4/5 ⭐** và không vi phạm tính tương thích ngược.

---

### Bước 5: Bàn giao (Delivery)
Bàn giao kèm theo bản tóm tắt các thay đổi (Changelog/Delta summary) và phần **TÓM TẮT CHO NGƯỜI DÙNG** ở đầu.
