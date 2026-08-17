---
name: skill-crafting
description: ">"
when_to_use: "Kích hoạt khi cần năng lực skill-crafting trong quy trình tạo hoặc kiểm định Agent Kit."
requires_templates: ["templates/skill-template.md"]
requires_references: ["references/component-specs/skill-spec.md"]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
version: 1.0.0
---

# Skill Crafting

## Overview

Thiết kế và viết skill folders chất lượng cao cho Agent Kit. Skill là
reusable capability tách biệt — chỉ tạo khi agent thực sự cần, không
tạo "cho đủ". Skill tốt giúp agent thông minh hơn; skill kém chỉ tốn token.

---

## Khi nào tạo Skill

| Tình huống | Tạo? |
|:-----------|:-----|
| Capability phức tạp, cần instructions > 100 từ | ✅ |
| Capability cần scripts/templates/references riêng | ✅ |
| Capability tái sử dụng giữa nhiều agents trong kit | ✅ |
| Capability đơn giản, viết vào system prompt đủ | ❌ |
| Kit type là Micro (1 tác vụ) | ❌ |

---

## Skill Anatomy

```
skill-name/
├── SKILL.md              # Required — entry point
├── references/            # Docs loaded khi cần (> 300 dòng content)
│   └── [topic].md
├── scripts/               # Helper scripts (optional)
│   └── [script].py
└── evals/                 # Test cases (optional nhưng recommended)
    └── evals.json
```

---

## SKILL.md Structure

### Frontmatter (bắt buộc)

```yaml
---
name: skill-name-lowercase
description: >
  Mô tả skill làm gì + khi nào trigger. Viết "pushy" — liệt kê rõ
  contexts nên trigger, kể cả khi user không nói rõ tên skill.
  Include edge cases. Differentiate từ skills tương tự.
---
```

**Description phải**:
1. Nói rõ skill làm gì (1-2 câu)
2. Liệt kê trigger contexts cụ thể (phrases, file types, scenarios)
3. Hơi "pushy" — include edge cases mà skill vẫn nên trigger
4. Differentiate — nói rõ KHÔNG dùng khi nào
5. Dưới 500 ký tự

**Ví dụ tốt**:
```yaml
description: >
  Use this skill whenever the user wants to create, read, edit, or
  manipulate Word documents (.docx). Triggers include: any mention of
  'Word doc', '.docx', or requests to produce professional documents.
  NOT for PDFs, spreadsheets, or Google Docs.
```

**Ví dụ sai**:
```yaml
description: Helps with document creation.
```

### Body (markdown instructions)

- Dưới 500 dòng — quá dài thì tách sang `references/`
- Viết imperative form
- Giải thích WHY thay vì chỉ nói MUST
- Dùng progressive disclosure: giữ body lean, chi tiết vào references

---

## Progressive Disclosure

3 tầng loading giúp tối ưu token:

| Tầng | Content | Khi nào load | Budget |
|:-----|:--------|:-------------|:-------|
| **Metadata** | name + description | Luôn (trong skill list) | ~100 từ |
| **Body** | SKILL.md instructions | Khi skill trigger | < 500 dòng |
| **References** | references/*.md | Khi body chỉ dẫn đọc | Không giới hạn |

### Khi nào tách sang references/
- Content > 300 dòng
- Content chỉ dùng trong 1 số cases nhất định
- Content là lookup table / spec chi tiết / API reference
- Content là domain-specific patterns library

---

## Writing Patterns

### Output format trong skill
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

### Examples trong skill
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### Giải thích WHY
- ❌ "ALWAYS check the output format"
- ✅ "Output format consistency matters because users build expectations
  after 2-3 interactions — if the format shifts, they lose trust and
  spend time re-parsing instead of acting on the content."

---

## Versioned Frontmatter (Professional/Suite Kit)

Khi skill nằm trong Professional hoặc Suite Kit, thêm versioning:

```yaml
---
name: skill-name
description: ...
when_to_use: "Khi nào dùng. KHÔNG cho X."
allowed-tools: Read, Grep, Glob, Bash
version: 1.0.0
---
```

---

## Eval Generation

Mỗi skill nên có evals để kiểm tra chất lượng:

```json
{
  "skill_name": "skill-name",
  "evals": [
    {
      "id": 1,
      "eval_name": "descriptive-name",
      "prompt": "Prompt thực tế giống user thật sẽ nói",
      "expected_output": "Mô tả output expected",
      "assertions": [
        {
          "name": "assertion-name",
          "check": "Điều kiện kiểm tra cụ thể"
        }
      ]
    }
  ]
}
```

**Tiêu chí eval tốt**:
- Prompt thực tế — giống user thật, có context cụ thể
- Assertions objectively verifiable
- Tối thiểu 3 cases: happy path + edge case + negative case

---

## Self-Check

```
□ SKILL.md < 500 dòng
□ Frontmatter có name + description
□ Description "pushy" — trigger contexts rõ ràng
□ Description nói rõ khi nào KHÔNG dùng
□ Progressive disclosure đúng — heavy content trong references/
□ Giải thích WHY, không chỉ MUST
□ Không có file/directory rỗng
□ Mỗi cơ chế trong skill phục vụ outcome cụ thể
```
