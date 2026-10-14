# External Dependencies Contract

Danh mục phụ thuộc ngoài, mức độ bắt buộc, vị trí sử dụng và phương án dự phòng khi môi trường không có sẵn tiện ích.

| Tên phụ thuộc | Bắt buộc / Tùy chọn | Dùng ở đâu | Phương án dự phòng |
| :--- | :--- | :--- | :--- |
| `superpowers:brainstorming` | optional | `workflows/create-kit.md`, `rules/dynamic-routing.md` | Hỏi trực tiếp sếp tối đa 3 câu về mục tiêu, tier/độ phức tạp, core verbs rồi chờ `APPROVED` |
| `superpowers:writing-plans` | optional | `workflows/create-kit.md` | Lập kế hoạch ngắn gọn trực tiếp trong khung chat |
| `superpowers:executing-plans` | optional | `workflows/create-kit.md` | Thực thi từng bước tuần tự trong phiên làm việc hiện tại |
| `agy-customizations` | optional | `rules/dynamic-routing.md` | Tra cứu tài liệu và quy ước cấu trúc của Antigravity IDE |
| `ponytail` | optional | `rules/dynamic-routing.md` | Tối giản hóa cấu trúc thủ công theo nguyên tắc YAGNI và Anti-Overengineering |
| `context7 MCP` | optional | `mcp_config.json` | Cần cấu hình API key; nếu không có thì tra cứu tài liệu tĩnh offline |
