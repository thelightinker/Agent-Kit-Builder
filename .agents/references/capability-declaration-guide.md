# Capability Declaration Guide (Compiler + Runtime Model)

> Hướng dẫn tác giả và compiler khai báo năng lực chuyên môn (Capability Declarations) cho Agent và Skill trong Agent Kit.

---

## 1. Cấu trúc Khai báo Năng lực (Capability Anatomy)

Mỗi Agent hoặc Skill tự mô tả năng lực của mình trong khối YAML Frontmatter:

```yaml
capabilities:
  - id: domain.component.action                 # Mandatory namespace format (CANON 9)
    intent_patterns:                            # Trigger keywords & phrasing
      - "keyword 1"
      - "phrase 2"
    preconditions:                              # Điều kiện tiên quyết trước khi thực thi
      structural:                               # Binary / Deterministic checks (Máy kiểm tra được)
        - key: outline_approved
          value: true
      semantic:                                 # AI Evaluation / Judge verdicts (Đọc từ State)
        - name: voice_consistent
          evaluator: developmental-editor
          required: true
    postconditions:                             # Trạng thái State thay đổi sau khi hoàn thành
      - key: "chapter_draft_exists.{chapter_id}"
        value: true
    evidence_schema:                            # Hợp đồng bằng chứng thực thi bắt buộc
      structural:
        - check: file_exists
          path: "chapters/{chapter_id}/draft.md"
        - check: word_count_min
          value: 2000
      semantic:
        - name: narrative_coherence
          evaluator: developmental-editor
    failure_policy:                             # Chiến lược xử lý lỗi compiled (CANON 8)
      on_structural_failure: "retry(max=2) → escalate_human"
      on_semantic_rejection: "route_to(writing.chapter.revise) → retry(max=1) → escalate_human"
      on_no_capability_match: "escalate_human"
    checkpoint_resume_policy:                   # Khôi phục từ checkpoint bán phần
      checkpoint_supported: true
      resume_condition: "checkpoint_valid"
    negative_scope:                             # Vùng cấm can thiệp rõ ràng (CANON 6)
      cannot_modify:
        - approved_outline
        - locked_character_profiles
      cannot_trigger_state_transition:
        - WORKFLOW_COMPLETE
```

---

## 2. Nguyên tắc Bất biến (CANON Compliance)

1. **CANON 6 (Explicit Negative Scope)**: Mọi capability bắt buộc phải khai báo `negative_scope`. Không được để trống vùng cấm.
2. **CANON 8 (Compiled Failure Policy)**: Chính sách phục hồi lỗi là hợp đồng máy đọc được, không để AI suy luận ngẫu hứng lúc runtime.
3. **CANON 9 (Namespace Mandatory)**: Mọi ID bắt buộc có dạng `domain.component.action` (ví dụ: `writing.chapter.draft`, `video.timeline.cut`).
