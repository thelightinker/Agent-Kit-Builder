import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable

try:
    import yaml
except ImportError:
    yaml = None

# Support importing kit_lint when run directly or as module
scripts_dir = Path(__file__).resolve().parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from kit_lint import find_placeholders


def _get_kit_md_files(kit_dir: Path) -> list[Path]:
    files = []
    for sub in ("agent", "skills", "workflows", "rules"):
        d = kit_dir / sub
        if d.is_dir():
            files.extend(d.rglob("*.md"))
    return files


def _extract_frontmatter(text: str) -> str | None:
    lines = text.splitlines(keepends=True)
    if not lines:
        return None
    first = lines[0].strip()
    if first != "---":
        return None
    fm_lines = []
    for line in lines[1:]:
        if line.strip() == "---":
            return "".join(fm_lines)
        fm_lines.append(line)
    return None


def check_q1_no_placeholders(kit_dir: Path) -> bool:
    for f in _get_kit_md_files(kit_dir):
        text = f.read_text(encoding="utf-8", errors="replace")
        if find_placeholders(text):
            return False
    return True


def check_q2_frontmatter_parses(kit_dir: Path) -> bool:
    if yaml is None:
        raise RuntimeError("PyYAML is required for check_q2_frontmatter_parses")
    for f in _get_kit_md_files(kit_dir):
        text = f.read_text(encoding="utf-8", errors="replace")
        fm_text = _extract_frontmatter(text)
        if fm_text is None:
            return False
        try:
            parsed = yaml.safe_load(fm_text)
            if not isinstance(parsed, dict):
                return False
        except yaml.YAMLError:
            return False
    return True


def check_q3_skill_refs_resolve(kit_dir: Path) -> bool:
    if yaml is None:
        raise RuntimeError("PyYAML is required for check_q3_skill_refs_resolve")
    skills_dir = kit_dir / "skills"
    
    agent_and_wf_files = []
    for sub in ("agent", "workflows"):
        d = kit_dir / sub
        if d.is_dir():
            agent_and_wf_files.extend(d.rglob("*.md"))
            
    for f in agent_and_wf_files:
        text = f.read_text(encoding="utf-8", errors="replace")
        fm_text = _extract_frontmatter(text)
        if not fm_text:
            continue
        try:
            data = yaml.safe_load(fm_text)
        except yaml.YAMLError:
            continue
        if not isinstance(data, dict):
            continue
            
        skill_refs = []
        for key in ("skills", "requires_skills"):
            val = data.get(key)
            if isinstance(val, list):
                skill_refs.extend(val)
            elif isinstance(val, str):
                skill_refs.append(val)
                
        for ref in skill_refs:
            skill_file = skills_dir / str(ref) / "SKILL.md"
            if not skill_file.is_file():
                return False
    return True


def check_q4_dod_has_numbers(kit_dir: Path) -> bool:
    for f in _get_kit_md_files(kit_dir):
        text = f.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        in_dod = False
        dod_has_digit = False
        for line in lines:
            if line.startswith("#"):
                if re.search(r"\b(DoD|Definition of Done)\b", line, re.IGNORECASE):
                    in_dod = True
                    continue
                elif in_dod:
                    in_dod = False
            if in_dod and re.search(r"\d", line):
                dod_has_digit = True
                break
        if dod_has_digit:
            return True
    return False


def check_q5_negative_boundaries(kit_dir: Path) -> bool:
    pattern = re.compile(r"negative\s+(boundaries|scope)|ranh\s*giới", re.IGNORECASE)
    for f in _get_kit_md_files(kit_dir):
        text = f.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            if line.startswith("#") and pattern.search(line):
                return True
    return False


def check_q6_skill_trigger_present(kit_dir: Path) -> bool:
    skills_dir = kit_dir / "skills"
    if not skills_dir.is_dir():
        return False
    skill_files = list(skills_dir.rglob("SKILL.md"))
    if not skill_files:
        return False
        
    for sf in skill_files:
        text = sf.read_text(encoding="utf-8", errors="replace")
        fm_text = _extract_frontmatter(text)
        if not fm_text:
            return False
        if yaml is not None:
            try:
                data = yaml.safe_load(fm_text)
                if not isinstance(data, dict):
                    return False
                desc = str(data.get("description", ""))
                when_to_use = str(data.get("when_to_use", ""))
                if len(desc) < 40:
                    return False
                if not when_to_use.strip():
                    return False
            except yaml.YAMLError:
                return False
        else:
            return False
    return True


CRITERIA: dict[str, tuple[str, Callable[[Path], bool] | None]] = {
    "Q1_no_placeholders": ("No uppercase placeholders outside code fences", check_q1_no_placeholders),
    "Q2_frontmatter_parses": ("All frontmatter blocks parse valid YAML dict", check_q2_frontmatter_parses),
    "Q3_skill_refs_resolve": ("Agent/workflow skill references point to real SKILL.md", check_q3_skill_refs_resolve),
    "Q4_dod_has_numbers": ("DoD section exists with quantitative digits", check_q4_dod_has_numbers),
    "Q5_negative_boundaries": ("Explicit negative boundaries heading exists", check_q5_negative_boundaries),
    "Q6_skill_trigger_present": ("Skills have description >= 40 chars and when_to_use", check_q6_skill_trigger_present),
    "M7_answers_brief": ("Kit content accurately answers user brief", None),
    "M8_no_toolkit_vocabulary": ("Kit is free of builder internal meta-vocabulary", None),
}


def score_kit(kit_dir: Path) -> dict[str, bool | None]:
    scores: dict[str, bool | None] = {}
    for crit_id, (_, fn) in CRITERIA.items():
        if fn is None:
            scores[crit_id] = None
        else:
            scores[crit_id] = fn(kit_dir)
    return scores


def main():
    parser = argparse.ArgumentParser(description="Score an Agent Kit against quality baseline criteria")
    parser.add_argument("kit_dir", type=Path, help="Path to kit directory")
    parser.add_argument("--brief", type=str, required=True, help="Brief ID (e.g. b1-micro)")
    parser.add_argument("--append", action="store_true", help="Append row to .agents/evals/baseline.md")
    args = parser.parse_args()

    kit_dir = args.kit_dir.resolve()
    if not kit_dir.exists():
        print(f"Error: kit directory not found: {kit_dir}", file=sys.stderr)
        sys.exit(1)

    scores = score_kit(kit_dir)
    print(f"Scores for brief '{args.brief}' at {kit_dir}:")
    for k, v in scores.items():
        val_str = "None (manual)" if v is None else ("PASS" if v else "FAIL")
        print(f"  {k}: {val_str}")

    if args.append:
        try:
            commit_hash = subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"], text=True
            ).strip()
        except Exception:
            commit_hash = "unknown"

        baseline_file = Path(".agents/evals/baseline.md")
        baseline_file.parent.mkdir(parents=True, exist_ok=True)
        
        headers = ["brief", "commit"] + list(CRITERIA.keys())
        if not baseline_file.exists():
            table_header = "| " + " | ".join(headers) + " |\n"
            table_sep = "| " + " | ".join(["---"] * len(headers)) + " |\n"
            baseline_file.write_text(table_header + table_sep, encoding="utf-8")

        def fmt(val: bool | None) -> str:
            if val is True:
                return "1"
            if val is False:
                return "0"
            return "?"

        row_vals = [args.brief, commit_hash] + [fmt(scores[c]) for c in CRITERIA.keys()]
        row_str = "| " + " | ".join(row_vals) + " |\n"
        with baseline_file.open("a", encoding="utf-8") as f:
            f.write(row_str)
        print(f"Appended score row to {baseline_file}")


if __name__ == "__main__":
    main()
