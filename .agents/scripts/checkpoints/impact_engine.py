def classify_blast_radius(path: str, operation: str) -> tuple[str, str, str]:
    """
    Classifies risk based on 2D Matrix (Path Sensitivity x Operation).
    Returns (blast_radius, reason_code, risk_tier).
    """
    op = operation.lower()
    path_clean = path.replace("\\", "/")

    # Delete operation always escalates to T3
    if op == "delete":
        return "HIGH", "IRREVERSIBLE_ACTION", "T3"

    # Path Sensitivity Check
    is_high_path = any(keyword in path_clean for keyword in [".agents/rules/", "ARCHITECTURE.md", "manifest.json"])
    
    # Check draft status relative to output directory or filename
    rel_path = path_clean.split("output/")[-1] if "output/" in path_clean else path_clean
    is_draft_path = "draft" in rel_path or "tmp" in rel_path

    is_medium_path = ("output/" in path_clean or path_clean.startswith("output/") or path_clean.startswith("./output/")) and not is_draft_path

    if is_high_path:
        if op in ("modify", "delete"):
            return "HIGH", "POLICY_BOUNDARY", "T3"
        return "MEDIUM", "EXTERNAL_WRITE", "T2"

    if is_medium_path:
        return "MEDIUM", "EXTERNAL_WRITE", "T2"

    if is_draft_path:
        return "LOW", "INTERNAL_DRAFT", "T1"

    # Default fallback
    return "LOW", "INTERNAL_DRAFT", "T1"

def prioritize_and_truncate_diff(raw_diff: str, max_lines: int = 15) -> str:
    """
    Prioritizes deletions (-) and core rule modifications before addition/context lines.
    Truncates to max_lines.
    """
    lines = [line.strip() for line in raw_diff.splitlines() if line.strip()]

    p1_deletions = [l for l in lines if l.startswith("-")]
    p2_additions = [l for l in lines if l.startswith("+")]
    p3_context = [l for l in lines if not l.startswith("+") and not l.startswith("-")]

    ordered = p1_deletions + p2_additions + p3_context
    truncated_lines = ordered[:max_lines]

    return "\n".join(truncated_lines)

def generate_impact_summary(target_files: list[str], operations: list[str], reason_code: str) -> str:
    """Generates plain language Vietnamese impact summary for Low-Tech UX."""
    files_str = ", ".join([f"`{f}`" for f in target_files[:3]])
    if len(target_files) > 3:
        files_str += f" (và {len(target_files) - 3} file khác)"

    if reason_code == "IRREVERSIBLE_ACTION":
        return f"- Thao tác XÓA dữ liệu trên {files_str}. Thao tác này không thể hoàn tác tự động."
    elif reason_code == "POLICY_BOUNDARY":
        return f"- Sửa đổi trực tiếp file quy tắc Core hệ thống trên {files_str}."
    elif reason_code == "EXTERNAL_WRITE":
        return f"- Tạo mới/sửa đổi file cấu hình và tài nguyên tại {files_str}."
    else:
        return f"- Thay đổi bản nháp nội bộ tại {files_str}."
