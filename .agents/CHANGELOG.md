# Agent Kit Creator Changelog

## 2026.8.22 (Mandatory Skill Creator Gate & Trigger Hardening)
- **Zero-Bypass Mandatory Skill Creator Gate**: Thiết lập quy chuẩn bắt buộc 100% các thao tác tạo mới hoặc sửa đổi `SKILL.md` phải nạp và kích hoạt `skill-creator` (`plugins/anthropic-skills/skills/skill-creator`).
- **Orchestrator Profile Hardening**: Bổ sung Negative Constraint trong profile `@architect` của `kit-architect` cấm sinh `SKILL.md` khi chưa nạp `skill-creator`.
- **Dynamic Routing & Plugin Delegation**: Cập nhật `dynamic-routing` để tự động ủy quyền tới `skill-creator` khi tạo hoặc sửa skill.
- **Workflow & Skill Hardening**: Cập nhật `create-kit` (Bước 3), `refactor-kit` (Bước 2) và `skill-architecting` nâng chuẩn kích hoạt `skill-creator` thành Mandatory Hard Gate.

## 2026.8.17 (v2.0.0 Evolvable Architecture Release)
- **Unified Orchestrator**: Hợp nhất 5 agents thành 1 Orchestrator duy nhất (`kit-architect`) với 4 Dynamic Role Profiles (`@analyst`, `@compiler`, `@architect`, `@auditor`).
- **Focused Skills**: Tinh gọn từ 21 skills xuống 7 Focused Skills (`domain-profiling`, `prompt-compiling`, `skill-architecting`, `kit-assembling`, `kit-verifying`, `kit-exporting`, `kit-evolving`).
- **Lean Rules**: Tinh giản 6 rules xuống 2 lean rules (`core-guardrails`, `dynamic-routing`), giảm context overhead $\ge 75\%$ (dưới 3KB).
- **Workspace Isolation Invariant**: Đảm bảo 100% output ghi cách ly vào `./output/<kit-name>/`.
- **Tách bạch Quyết định vs Thực thi**: Role `@auditor` quyết định phạm vi kiểm thử; script (`validate_kit.py`, `eval_runner.py`) thực thi kiểm thử tất định.
- **Loại bỏ Checkpoint Bloat**: Gỡ bỏ subsystem checkpoint CLI không tương thích IDE, nới lỏng cơ chế khóa cứng lockfile.
- **Adaptive Scenario Testing**: Bổ sung cơ chế sinh test case thích ứng theo domain và tier trong `kit-verifying`.

## 2026.7.20 (v1.0.0 Release)
- Initial release of Agent Kit Creator.
