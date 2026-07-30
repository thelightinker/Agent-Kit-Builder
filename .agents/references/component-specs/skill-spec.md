# Skill Spec — Chuẩn tạo Skill Folder

Skill = reusable capability tách biệt cho agent. Không phải agent chỉ cần
1 skill (hoặc không cần skill nào) — chỉ tạo khi agent thực sự cần.

---

## Khi nào tạo Skill

| Tình huống | Tạo skill? |
|:-----------|:-----------|
| Agent cần 1 capability phức tạp, tái sử dụng | ✅ Có |
| Capability cần instructions > 100 từ | ✅ Có |
| Capability cần scripts/templates/references riêng | ✅ Có |
| Capability đơn giản, viết vào system prompt đủ | ❌ Không |
| Agent Tier 1, 1 tác vụ | ❌ Không |

---

## Cấu trúc Skill Folder

```
skill-name/
├── SKILL.md              # Required
├── references/            # Docs loaded as needed
│   └── [topic].md
├── examples/              # Reference implementations
│   └── [example].md
├── evals/                 # Test cases
│   └── evals.json
├── scripts/               # Helper scripts (optional)
│   └── [script].py
└── assets/                # Templates, icons (optional)
```

---

## SKILL.md Format

### Frontmatter (bắt buộc)

```yaml
---
name: skill-name-lowercase
description: >
  Mô tả skill làm gì + khi nào trigger.
  Viết "pushy" — liệt kê contexts trigger rõ ràng.
  Include cả edge cases mà skill nên trigger.
---
```

### Body

- Dưới 500 dòng
- Imperative form
- Giải thích WHY, không chỉ nói MUST
- Dùng progressive disclosure: metadata → body → references

---

## Description Standards

Description quyết định triggering accuracy. Phải:

1. **Nói rõ** skill làm gì
2. **Liệt kê** trigger contexts cụ thể (phrases, file types, scenarios)
3. **"Pushy"** — include edge cases
4. **Differentiate** — nói rõ khác gì skills tương tự

**Ví dụ tốt**:
```
Use this skill whenever the user wants to create, read, edit, or
manipulate Word documents (.docx files). Triggers include: any mention
of 'Word doc', '.docx', or requests to produce professional documents.
```

**Ví dụ sai**:
```
Helps with document creation.
```

---

## Evals Format

```json
{
  "skill_name": "skill-name",
  "evals": [
    {
      "id": 1,
      "eval_name": "descriptive-name",
      "prompt": "Realistic user prompt",
      "expected_output": "Description of expected result",
      "files": [],
      "assertions": [
        {
          "name": "assertion-name",
          "check": "What to verify"
        }
      ]
    }
  ]
}
```

**Tiêu chí**:
- Tối thiểu 3 eval cases
- Prompts thực tế (giống user thật nói)
- Assertions objectively verifiable
- Cover happy path + edge cases

---

## Antigravity Compatibility

- Đặt trong `skills/` directory (global hoặc project)
- Auto-discovered — không cần registration
- SKILL.md là entry point duy nhất
- References tham chiếu bằng relative path

---

## Quality Checklist

```
□ SKILL.md < 500 dòng
□ Frontmatter có name + description
□ Description "pushy" — trigger contexts rõ ràng
□ Progressive disclosure đúng
□ evals.json có ≥ 3 test cases
□ Assertions objectively verifiable
□ Giải thích WHY thay vì chỉ MUST
□ Antigravity-compatible path structure
```
