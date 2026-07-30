---
name: {SKILL_NAME}
description: {DYNAMIC_TRIGGER_KEYWORDS_AND_CAPABILITY_SUMMARY}
when_to_use: "Khi {FLEXIBLE_TRIGGER_CONDITION}"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
version: 1.0.0
# Bổ sung linh hoạt nếu cần:
# tags: [backend, database]
# environment_check: {check_command: "python3 --version"}
---

# {SKILL_TITLE} - {SKILL_SUBTITLE}

> {ONE_SENTENCE_PURPOSE}

---

## 🎯 Selective Reading Map (Bản đồ Đọc Chọn lọc)

> 💡 **Mẹo linh hoạt**: Không nạp toàn bộ thư mục. Chỉ đọc các file phù hợp với nhu cầu cụ thể của tác vụ hiện tại.

| Thư mục / File | Mô tả nội dung | Khi nào cần nạp |
|:---|:---|:---|
| `SKILL.md` | Chỉ mục và quy tắc cốt lõi | Mặc định đọc đầu tiên |
| `references/{TOPIC_1}.md` | Kiến thức chuyên sâu về {TOPIC_1} | Khi làm việc với {TOPIC_1} |
| `references/{TOPIC_2}.md` | Hướng dẫn xử lý {TOPIC_2} | Khi phát sinh {TOPIC_2} |
| `scripts/{SCRIPT_NAME}.py` | Script tự động hóa / kiểm thử | Khi cần chạy tự động |

---

## 💡 Nguyên tắc & Kỹ thuật Cốt lõi (Core Principles & Tactics)

### 1. {CORE_TACTIC_1}
* **Mục tiêu**: {TACTIC_1_GOAL}
* **Cách thực hiện**: {TACTIC_1_STEPS}

### 2. {CORE_TACTIC_2}
* **Mục tiêu**: {TACTIC_2_GOAL}
* **Cách thực hiện**: {TACTIC_2_STEPS}

---

## 🛡️ Xử lý Ngoại lệ & Fallback (Edge Cases & Recoveries)

- **Trường hợp thiếu tài nguyên / môi trường lỗi**: {FALLBACK_STRATEGY_1}
- **Trường hợp dữ liệu không khớp**: {FALLBACK_STRATEGY_2}

---

## 🛠️ Code Snippets & Patterns Mẫu

```markdown
{FLEXIBLE_EXAMPLE_OR_PATTERN}
```
