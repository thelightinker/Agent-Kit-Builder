from pathlib import Path

GOOD_AGENT_BODY = """# Demo Agent
An agent for testing and verification.

## Negative Boundaries & Scope
- Cấm sửa đổi file ngoài phạm vi được chỉ định.
- Cấm tự tiện sinh code không qua kiểm định.

## Definition of Done (DoD)
1. 100% test cases pass với 0 warnings.
2. Thời gian phản hồi dưới 300ms.
"""

GOOD_SKILL_DESC = "This is a high quality skill description that contains more than 40 characters for testing triggers."

def make_kit(
    tmp: Path,
    *,
    agent_body: str = GOOD_AGENT_BODY,
    skill_description: str = GOOD_SKILL_DESC,
    skill_ref: str = "demo-skill"
) -> Path:
    agent_dir = tmp / "agent"
    agent_dir.mkdir(parents=True, exist_ok=True)
    
    agent_file = agent_dir / "demo.md"
    agent_content = f"""---
name: demo
skills:
  - {skill_ref}
---
{agent_body}
"""
    agent_file.write_text(agent_content, encoding="utf-8")
    
    skill_dir = tmp / "skills" / "demo-skill"
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    skill_file = skill_dir / "SKILL.md"
    skill_content = f"""---
name: demo-skill
description: "{skill_description}"
when_to_use: "Use when performing testing or baseline verification."
---
# demo-skill
Skill instructions here.
"""

    skill_file.write_text(skill_content, encoding="utf-8")
    
    return tmp
