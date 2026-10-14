---
type: project
created: 2026-07-18
updated: 2026-07-18
---

# Technical Decisions

- Component metadata uses SemVer while the toolkit release keeps CalVer.
- `manifest.json` and `manifest.lock.json` must remain synchronized with component frontmatter.
- Nhóm evolution (`evolution_*`, `equip_evolution`, `snapshot_manager`) ở trạng thái experimental vì phụ thuộc `feedback_collector`/`evolution_submitter` đã bị xóa; chủ repo quyết định phục hồi hoặc xóa.
