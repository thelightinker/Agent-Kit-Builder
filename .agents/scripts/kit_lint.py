import re
from pathlib import Path


def strip_code_fences(text: str) -> str:
    """Replaces lines inside markdown code fences with empty lines, preserving line numbers."""
    lines = text.splitlines(keepends=True)
    out_lines = []
    in_fence = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            out_lines.append(line)
        elif in_fence:
            # Preserve newline characters from the original line if present
            newline = "\n" if line.endswith("\n") else ""
            out_lines.append(newline)
        else:
            out_lines.append(line)
            
    return "".join(out_lines)


def find_placeholders(text: str) -> list[tuple[int, str]]:
    """Finds all uppercase placeholders like {VARIABLE_NAME} outside of code fences.
    
    Returns list of (line_number_1_indexed, token).
    """
    clean_text = strip_code_fences(text)
    pattern = re.compile(r"\{[A-Z][A-Z0-9_]+\}")
    results = []
    
    for line_num, line in enumerate(clean_text.splitlines(), start=1):
        for match in pattern.finditer(line):
            results.append((line_num, match.group(0)))
            
    return results
