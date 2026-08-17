---
name: {SKILL_NAME}
description: >
  {PUSHY_DESCRIPTION_EXPLAINING_WHAT_IT_DOES_AND_EXPLICIT_TRIGGER_CONTEXTS_TO_PREVENT_UNDER_TRIGGERING}
when_to_use: "Khi {TRIGGER_CONDITION}"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
version: 1.0.0
---

# {SKILL_TITLE}

> {ONE_SENTENCE_CORE_PURPOSE}

---

## 1. Quick Overview & Workflow

Describe the step-by-step process using imperative instructions and explaining the reasoning ("why"):

1. **Step 1 - Preparation & Context**: {STEP_1_DESCRIPTION}
2. **Step 2 - Execution**: {STEP_2_DESCRIPTION}
3. **Step 3 - Verification & Delivery**: {STEP_3_DESCRIPTION}

---

## 2. Progressive Disclosure References

When deeper domain knowledge is required, consult these bundled references:
- `references/{TOPIC_1}.md`: {TOPIC_1_DESCRIPTION}
- `references/{TOPIC_2}.md`: {TOPIC_2_DESCRIPTION}

---

## 3. Concrete Examples (Few-Shot Pattern)

### Example 1: {EXAMPLE_1_TITLE}
**Input:**
```
{EXAMPLE_1_INPUT}
```

**Output:**
```
{EXAMPLE_1_OUTPUT}
```

---

## 4. Quality Standards & Output Checklist

- [ ] Output satisfies all primary requirements.
- [ ] No generic AI placeholders or unverified assertions.
- [ ] Clear actionable summary provided to user.
