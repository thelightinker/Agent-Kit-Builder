#!/usr/bin/env python3
"""Self-validate an AG Kit installation.

Checks machine-readable configuration, versioned frontmatter contracts,
cross references, generated registries, local Markdown links, memory schema,
Python syntax, and architecture inventory counts.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - optional enhancement
    yaml = None

from component_registry import (
    build_lock,
    build_manifest,
    canonical_json,
    is_semver,
    normalize_list,
    version_satisfies,
)
from dependency_graph import render as render_dependency_graph
from compile_routing_index import compile_routing_index, validate_capability_namespace
from compile_invariants import compile_invariants
from compile_state_schema import compile_state_schema
from compile_task_classifier import compile_task_classifier
from compile_evidence_schemas import compile_evidence_schemas
from compile_execution_policy import compile_execution_policy
from dry_run_simulation import simulate_workflow_graph

try:
    from kit_lint import find_placeholders
except ImportError:
    scripts_dir = Path(__file__).resolve().parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    from kit_lint import find_placeholders


@dataclass
class Finding:
    severity: str
    code: str
    file: str
    line: int
    message: str
    evidence: str = ""
    fix_strategy: str = "escalate_human"  # deterministic | llm_patch | escalate_human
    retryable: bool = False


FIX_STRATEGY_MAP: dict[str, tuple[str, bool]] = {
    # deterministic fixes (zero token cost)
    "manifest.stale": ("deterministic", True),
    "manifest.lock_stale": ("deterministic", True),
    "manifest.missing": ("deterministic", True),
    "graph.stale": ("deterministic", True),
    "graph.missing": ("deterministic", True),
    "architecture.count_mismatch": ("deterministic", True),
    "architecture.count_missing": ("deterministic", True),
    "version.missing": ("deterministic", True),
    "version.invalid_calver": ("deterministic", True),
    "compiler.stale_artifacts": ("deterministic", True),
    "compiler.missing_artifacts": ("deterministic", True),
    "compiler.execution_policy_missing": ("deterministic", True),
    "compiler.execution_policy_stale": ("deterministic", True),
    "docs.generated_stale": ("deterministic", True),
    # llm_patch (JIT context needed)
    "compiler.execution_policy_invalid_mode": ("llm_patch", True),
    "compiler.execution_policy_schema_invalid": ("llm_patch", True),
    "orchestrator.missing_protocol_section": ("llm_patch", True),
    "frontmatter.missing": ("llm_patch", True),
    "frontmatter.required_field": ("llm_patch", True),
    "frontmatter.name_mismatch": ("llm_patch", True),
    "frontmatter.invalid_semver": ("llm_patch", True),
    "skill.progressive_disclosure_exceeded": ("llm_patch", True),
    "skill.description_too_short": ("llm_patch", True),
    "skill.missing_examples": ("llm_patch", True),
    "skill.missing_trigger_context": ("llm_patch", True),
    "workflow.missing_node_anatomy": ("llm_patch", True),
    "workflow.missing_escalation_guard": ("llm_patch", True),
    "agent.missing_role_blocks": ("llm_patch", True),
    "agent.missing_worker_briefing": ("llm_patch", True),
    "agent.missing_dod": ("llm_patch", True),
    "agent.missing_filesystem_contract": ("llm_patch", True),
    "output.sanitizer_violation": ("deterministic", True),
    "memory.missing_required_topics": ("llm_patch", True),
    "reference.unknown_skill": ("llm_patch", True),
    "reference.unknown_agent": ("llm_patch", True),
    "memory.required_field": ("llm_patch", True),
    "memory.invalid_type": ("llm_patch", True),
    "memory.required_topic": ("llm_patch", True),
    "memory.index_too_large": ("llm_patch", True),
    "workflow.no_outputs": ("llm_patch", True),
    "markdown.missing_link": ("llm_patch", True),
    "path.absolute_user_path": ("llm_patch", True),
    "dependency.undeclared": ("llm_patch", True),
    "capability.invalid_namespace": ("llm_patch", True),
    "capability.uncovered_outcome": ("llm_patch", True),
    "graph.unreachable_node": ("llm_patch", True),
    "workflow.dead_state": ("llm_patch", True),
    "state.unknown_key": ("llm_patch", True),
    "negative_scope.conflict": ("llm_patch", True),
    "evidence.missing_schema": ("llm_patch", True),
    # routing integrity (P0 invariants)
    "routing.empty_capabilities": ("llm_patch", True),
    "routing.agent_missing_skill_matrix": ("llm_patch", True),
    "routing.orchestrator_missing_routing_table": ("llm_patch", True),
    "context.budget_exceeded": ("llm_patch", True),
    "placeholder.unfilled": ("llm_patch", True),
    # escalate_human (ambiguous / high-risk)
    "json.invalid": ("escalate_human", False),
    "python.syntax": ("escalate_human", False),
    "script.smoke_failed": ("escalate_human", False),
    "script.smoke_timeout": ("escalate_human", False),
    "frontmatter.invalid_yaml": ("escalate_human", False),
    "frontmatter.not_mapping": ("escalate_human", False),
    "frontmatter.duplicate_name": ("escalate_human", False),
    "manifest.generation_failed": ("escalate_human", False),
    "manifest.incompatible_dependency": ("escalate_human", False),
    "reference.missing_script": ("escalate_human", False),
    "architecture.missing": ("escalate_human", False),
    "memory.index_missing": ("escalate_human", False),
    "memory.missing_topic": ("escalate_human", False),
    "rule.invalid_trigger": ("escalate_human", False),
    "rule.invalid_priority": ("escalate_human", False),
    "rule.missing_description_for_model_decision": ("escalate_human", False),
    "precondition.cycle_detected": ("escalate_human", False),
}


REQUIRED_FIELDS = {
    "agent": {"name", "description", "tools", "model", "skills", "version"},
    "skill": {"name", "description", "when_to_use", "allowed-tools", "version"},
    "workflow": {
        "name",
        "description",
        "version",
        "requires_agents",
        "requires_skills",
        "artifact_outputs",
    },
    "rule": {"name", "trigger", "version", "priority"},
}

RULE_VALID_TRIGGERS = {"always_on", "manual", "model_decision"}
RULE_VALID_PRIORITIES = {"P0", "P1", "P2"}


def add(findings: list[Finding], severity: str, code: str, path: Path, message: str, line: int = 1, evidence: str = "") -> None:
    strategy, retryable = FIX_STRATEGY_MAP.get(code, ("escalate_human", False))
    findings.append(Finding(severity, code, path.as_posix(), line, message, evidence, strategy, retryable))


def extract_frontmatter(path: Path) -> tuple[str | None, int]:
    text = path.read_text("utf-8", errors="replace")
    if not text.startswith("---\n"):
        return None, 1
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, 1
    return text[4:end], 1


def fallback_frontmatter(raw: str) -> dict[str, object]:
    data: dict[str, object] = {}
    for line in raw.splitlines():
        if not line or line[0].isspace() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.groups()
        data[key] = value.strip().strip('"\'')
    return data


def parse_frontmatter(path: Path, findings: list[Finding]) -> dict[str, object] | None:
    raw, _ = extract_frontmatter(path)
    if raw is None:
        add(findings, "error", "frontmatter.missing", path, "Missing or unterminated YAML frontmatter")
        return None
    if yaml is None:
        return fallback_frontmatter(raw)
    try:
        data = yaml.safe_load(raw)
    except Exception as exc:
        line = int(getattr(getattr(exc, "problem_mark", None), "line", 0)) + 2
        add(findings, "error", "frontmatter.invalid_yaml", path, str(exc), line)
        return None
    if not isinstance(data, dict):
        add(findings, "error", "frontmatter.not_mapping", path, "Frontmatter must be a YAML mapping")
        return None
    return data


def validate_json(root: Path, findings: list[Finding]) -> None:
    for path in root.rglob("*.json"):
        if "__pycache__" in path.parts:
            continue
        try:
            json.loads(path.read_text("utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            line = int(getattr(exc, "lineno", 1))
            add(findings, "error", "json.invalid", path.relative_to(root), str(exc), line)


def validate_kit_version(root: Path, findings: list[Finding]) -> None:
    version_path = root / "VERSION"
    if not version_path.is_file():
        add(findings, "error", "version.missing", Path("VERSION"), "VERSION is missing")
        return
    value = version_path.read_text("utf-8").strip()
    if not re.fullmatch(r"\d{4}\.\d{1,2}\.\d{1,2}", value):
        add(findings, "error", "version.invalid_calver", Path("VERSION"), f"Expected YYYY.M.D CalVer, got {value!r}")


def validate_frontmatter(
    root: Path, findings: list[Finding]
) -> tuple[
    dict[str, dict[str, object]],
    dict[str, dict[str, object]],
    dict[str, dict[str, object]],
    dict[str, dict[str, object]],
]:
    agents: dict[str, dict[str, object]] = {}
    skills: dict[str, dict[str, object]] = {}
    workflows: dict[str, dict[str, object]] = {}
    rules: dict[str, dict[str, object]] = {}
    groups = (
        ("agent", sorted((root / "agent").glob("*.md"))),
        ("skill", sorted((root / "skills").glob("*/SKILL.md"))),
        ("workflow", sorted((root / "workflows").glob("*.md"))),
        ("rule", sorted((root / "rules").glob("*.md"))),
    )
    registries = {"agent": agents, "skill": skills, "workflow": workflows, "rule": rules}
    for kind, paths in groups:
        names_seen: set[str] = set()
        for path in paths:
            rel = path.relative_to(root)
            data = parse_frontmatter(path, findings)
            if data is None:
                continue
            missing = REQUIRED_FIELDS[kind] - set(data)
            for field in sorted(missing):
                add(findings, "error", "frontmatter.required_field", rel, f"Missing required field: {field}")
            name = str(data.get("name", ""))
            expected = path.parent.name if kind == "skill" else path.stem
            if name != expected:
                add(findings, "error", "frontmatter.name_mismatch", rel, f"name={name!r}, expected {expected!r}")
            if name:
                if name in names_seen:
                    add(findings, "error", "frontmatter.duplicate_name", rel, f"Duplicate {kind} name: {name}")
                names_seen.add(name)
            version = data.get("version")
            if version is not None and not is_semver(str(version)):
                add(findings, "error", "frontmatter.invalid_semver", rel, f"Invalid SemVer: {version!r}")
            if kind == "skill":
                lines = path.read_text("utf-8", errors="replace").splitlines()
                if len(lines) > 500:
                    add(findings, "error", "skill.progressive_disclosure_exceeded", rel, f"SKILL.md exceeds 500 lines ({len(lines)} lines); move details to references/")
                desc = str(data.get("description", "")).strip()
                if len(desc) < 20:
                    add(findings, "warning", "skill.description_too_short", rel, "Skill description is very short; Anthropic Skill Creator requires pushy trigger context")
            if kind == "rule":
                trigger = str(data.get("trigger", "")).strip()
                if trigger not in RULE_VALID_TRIGGERS:
                    add(
                        findings,
                        "error",
                        "rule.invalid_trigger",
                        rel,
                        f"Invalid rule trigger: {trigger!r}. Must be one of {sorted(RULE_VALID_TRIGGERS)}",
                    )
                priority = str(data.get("priority", "")).strip()
                if priority not in RULE_VALID_PRIORITIES:
                    add(
                        findings,
                        "error",
                        "rule.invalid_priority",
                        rel,
                        f"Invalid rule priority: {priority!r}. Must be one of {sorted(RULE_VALID_PRIORITIES)} (e.g. 'P0', 'P1', 'P2')",
                    )
                if trigger == "model_decision":
                    desc = str(data.get("description", "")).strip()
                    if len(desc) < 20:
                        add(
                            findings,
                            "error",
                            "rule.missing_description_for_model_decision",
                            rel,
                            "Rule with trigger='model_decision' must provide a descriptive 'description' field (>= 20 chars) in frontmatter explaining activation context.",
                        )
            registries[kind][expected] = data
    return agents, skills, workflows, rules


def validate_references(
    root: Path,
    agents: dict[str, dict[str, object]],
    skills: dict[str, dict[str, object]],
    workflows: dict[str, dict[str, object]],
    findings: list[Finding],
) -> None:
    for agent_name, data in agents.items():
        path = Path("agent") / f"{agent_name}.md"
        for skill in normalize_list(data.get("skills")):
            if skill not in skills:
                add(findings, "error", "reference.unknown_skill", path, f"Agent references missing skill: {skill}")

    for workflow_name, data in workflows.items():
        path = Path("workflows") / f"{workflow_name}.md"
        for agent in normalize_list(data.get("requires_agents")):
            if agent not in agents:
                add(findings, "error", "reference.unknown_agent", path, f"Workflow references missing agent: {agent}")
        for skill in normalize_list(data.get("requires_skills")):
            if skill not in skills:
                add(findings, "error", "reference.unknown_skill", path, f"Workflow references missing skill: {skill}")
        if not normalize_list(data.get("artifact_outputs")):
            add(findings, "warning", "workflow.no_outputs", path, "Workflow declares no artifact outputs")

    script_pattern = re.compile(r'["\']((?:skills|scripts)/[^"\']+?\.py)["\']')
    for path in (root / "scripts").glob("*.py"):
        text = path.read_text("utf-8", errors="replace")
        for match in script_pattern.finditer(text):
            if any(char in match.group(1) for char in "*?["):
                continue
            target = root / match.group(1)
            if not target.is_file():
                line = text.count("\n", 0, match.start()) + 1
                add(findings, "error", "reference.missing_script", path.relative_to(root), f"Referenced script does not exist: {match.group(1)}", line)


def validate_manifest(root: Path, findings: list[Finding], auto_heal: bool = False) -> None:
    manifest_path = root / "manifest.json"
    lock_path = root / "manifest.lock.json"
    if not manifest_path.is_file():
        add(findings, "error", "manifest.missing", Path("manifest.json"), "Run scripts/generate_manifest.py")
        return
    try:
        actual_manifest = json.loads(manifest_path.read_text("utf-8"))
    except json.JSONDecodeError:
        return
    try:
        expected_manifest = build_manifest(root)
    except Exception as exc:
        add(findings, "error", "manifest.generation_failed", Path("manifest.json"), str(exc))
        return
    if actual_manifest != expected_manifest:
        if auto_heal:
            (root / "manifest.json").write_text(canonical_json(expected_manifest), "utf-8")
            actual_manifest = expected_manifest
        else:
            add(findings, "error", "manifest.stale", Path("manifest.json"), "Registry differs from component frontmatter; regenerate it")

    if lock_path.is_file():
        try:
            actual_lock = json.loads(lock_path.read_text("utf-8"))
            expected_lock = build_lock(root, expected_manifest)
            if actual_lock != expected_lock:
                if auto_heal:
                    (root / "manifest.lock.json").write_text(canonical_json(expected_lock), "utf-8")
                else:
                    add(findings, "error", "manifest.lock_stale", Path("manifest.lock.json"), "Lock differs from current component files; regenerate it")
        except Exception:
            pass

    skill_versions = {name: data["version"] for name, data in expected_manifest["skills"].items()}
    for agent_name, agent in expected_manifest["agents"].items():
        for skill_name, constraint in agent["requires"]["skills"].items():
            version = skill_versions.get(skill_name)
            if version and not version_satisfies(version, constraint):
                add(
                    findings,
                    "error",
                    "manifest.incompatible_dependency",
                    Path(agent["path"]),
                    f"{skill_name} {version} does not satisfy {constraint}",
                )


def validate_generated_docs(root: Path, findings: list[Finding]) -> None:
    path = root / "DEPENDENCY_GRAPH.md"
    if not path.is_file():
        add(findings, "error", "graph.missing", Path("DEPENDENCY_GRAPH.md"), "Run scripts/dependency_graph.py")
        return
    try:
        expected = render_dependency_graph(root)
    except Exception as exc:
        add(findings, "error", "graph.generation_failed", Path("DEPENDENCY_GRAPH.md"), str(exc))
        return
    if path.read_text("utf-8") != expected:
        add(findings, "error", "graph.stale", Path("DEPENDENCY_GRAPH.md"), "Dependency graph is stale")

    # Check generated SSOT doc blocks
    try:
        import render_docs
        stale_docs = render_docs.apply_generated_blocks(root, check=True)
        if stale_docs:
            add(
                findings,
                "error",
                "docs.generated_stale",
                Path("ARCHITECTURE.md"),
                f"Generated doc blocks are stale in: {', '.join(stale_docs)}. Run render_docs.py to update.",
            )
    except Exception:
        pass


def validate_markdown_links(root: Path, findings: list[Finding]) -> None:
    pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for path in root.rglob("*.md"):
        text = path.read_text("utf-8", errors="replace")
        for match in pattern.finditer(text):
            raw = match.group(1).strip()
            if not raw:
                continue
            target_text = raw.split()[0].strip("<>")
            if target_text.startswith(("#", "http://", "https://", "mailto:", "tel:", "data:")):
                continue
            target_text = unquote(target_text.split("#", 1)[0])
            if not target_text:
                continue
            target = (path.parent / target_text).resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                continue
            if path.relative_to(root).as_posix() == "skills/documentation-templates/SKILL.md" and target_text.startswith("./docs/"):
                continue
            if not target.exists():
                line = text.count("\n", 0, match.start()) + 1
                add(findings, "error", "markdown.missing_link", path.relative_to(root), f"Missing local target: {target_text}", line)


def validate_memory(root: Path, findings: list[Finding]) -> None:
    memory_root = root / "memory"
    index = memory_root / "MEMORY.md"
    required_topics = {"project-conventions.md", "user-preferences.md", "tech-decisions.md", "feedback-history.md"}
    if not index.is_file():
        add(findings, "error", "memory.index_missing", Path("memory/MEMORY.md"), "Memory index is missing")
        return
    lines = index.read_text("utf-8").splitlines()
    if len(lines) > 200:
        add(findings, "error", "memory.index_too_large", Path("memory/MEMORY.md"), f"Memory index has {len(lines)} lines; maximum is 200")
        return
    for line_no, line in enumerate(lines, 1):
        match = re.search(r"\[[^\]]+\]\(\.\/([^)]+)\)", line)
        if not match:
            continue
        target = memory_root / match.group(1)
        if not target.is_file():
            add(findings, "error", "memory.missing_topic", Path("memory/MEMORY.md"), f"Missing topic file: {match.group(1)}", line_no)
    for topic in sorted(required_topics):
        path = memory_root / topic
        if not path.is_file():
            add(findings, "error", "memory.required_topic", Path("memory") / topic, "Required memory topic is missing")
            continue
        data = parse_frontmatter(path, findings)
        if data is None:
            continue
        missing = {"type", "created", "updated"} - set(data)
        for field in sorted(missing):
            add(findings, "error", "memory.required_field", path.relative_to(root), f"Missing required field: {field}")
        if str(data.get("type", "")) not in {"user", "feedback", "project", "reference"}:
            add(findings, "error", "memory.invalid_type", path.relative_to(root), f"Invalid memory type: {data.get('type')!r}")


def _smoke_cwd(script: Path) -> Path:
    """Return the nearest ancestor directory containing SKILL.md; otherwise script.parent."""
    cur = script.parent
    while cur != cur.parent:
        if (cur / "SKILL.md").is_file():
            return cur
        cur = cur.parent
    return script.parent


def validate_python(root: Path, findings: list[Finding]) -> None:
    targets = set(root.rglob("*.py"))
    if root.name == ".agents" and (root.parent / "scripts").is_dir():
        targets.update((root.parent / "scripts").glob("*.py"))

    for path in sorted(targets):
        if "__pycache__" in path.parts:
            continue
        try:
            rel = path.relative_to(root)
        except ValueError:
            rel = path.relative_to(root.parent)
        try:
            text = path.read_text("utf-8", errors="replace")
            ast.parse(text, filename=str(path))
        except (OSError, SyntaxError) as exc:
            add(findings, "error", "python.syntax", rel, str(exc), int(getattr(exc, "lineno", 1) or 1))
            continue

        # Executable Smoke Test: CLI scripts with argparse
        if "argparse" in text and 'if __name__ == "__main__":' in text:
            smoke_cwd = _smoke_cwd(path)
            env = os.environ.copy()
            env["PYTHONPATH"] = str(smoke_cwd) + os.pathsep + env.get("PYTHONPATH", "")
            try:
                res = subprocess.run(
                    [sys.executable, str(path.resolve()), "--help"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    cwd=smoke_cwd,
                    env=env,
                )
                if res.returncode != 0:
                    add(findings, "error", "script.smoke_failed", rel, f"CLI smoke test (--help) returned non-zero code {res.returncode}")
            except subprocess.TimeoutExpired:
                add(findings, "error", "script.smoke_timeout", rel, "CLI smoke test timed out after 5s")
            except Exception as exc:
                add(findings, "error", "script.smoke_failed", rel, f"CLI smoke test failed to invoke: {exc}")


def validate_architecture_counts(root: Path, findings: list[Finding]) -> None:
    path = root / "ARCHITECTURE.md"
    if not path.is_file():
        add(findings, "error", "architecture.missing", Path("ARCHITECTURE.md"), "ARCHITECTURE.md is missing")
        return
    text = path.read_text("utf-8", errors="replace")
    actual = {
        "agents": len(list((root / "agent").glob("*.md"))),
        "skills": len(list((root / "skills").glob("*/SKILL.md"))),
        "workflows": len(list((root / "workflows").glob("*.md"))),
        "skill_scripts": len(list((root / "skills").glob("*/scripts/*.py"))),
    }
    patterns = {
        "agents": r"\*\*Total Agents\*\*\s*\|\s*(\d+)",
        "skills": r"\*\*Total Skills\*\*\s*\|\s*(\d+)",
        "workflows": r"\*\*Total Workflows\*\*\s*\|\s*(\d+)",
        "skill_scripts": r"\*\*Total Skill Scripts\*\*\s*\|\s*(\d+)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if not match:
            add(findings, "error", "architecture.count_missing", Path("ARCHITECTURE.md"), f"Missing inventory field for {key}")
        elif int(match.group(1)) != actual[key]:
            add(findings, "error", "architecture.count_mismatch", Path("ARCHITECTURE.md"), f"{key}: documented {match.group(1)}, actual {actual[key]}")


def validate_structural_anchors(root: Path, findings: list[Finding]) -> None:
    """Validate that created components satisfy standard structural anchors from templates."""
    # 1. Skill Anchors
    for path in sorted((root / "skills").glob("*/SKILL.md")):
        rel = path.relative_to(root)
        text = path.read_text("utf-8", errors="replace")
        raw_fm, _ = extract_frontmatter(path)
        if raw_fm:
            fm_data = fallback_frontmatter(raw_fm) if yaml is None else yaml.safe_load(raw_fm)
            when_to_use = str(fm_data.get("when_to_use", "")).strip() if isinstance(fm_data, dict) else ""
            desc = str(fm_data.get("description", "")).strip() if isinstance(fm_data, dict) else ""
            if not when_to_use and len(desc) < 20:
                add(findings, "error", "skill.missing_trigger_context", rel, "Skill lacks clear 'when_to_use' trigger context or description in frontmatter")

        has_examples = bool(
            re.search(
                r"(?i)(###?\s*examples?|\*\*examples?|\bexample\s*\d+:|\binput\s*:\s*.*\n.*output\s*:|##\s*examples?|###\s*mẫu|##\s*format|```(?:markdown|json|yaml|bash|python)\s*\n[\s\S]*?```)",
                text,
            )
        )
        if not has_examples:
            add(findings, "error", "skill.missing_examples", rel, "Skill lacks concrete Input/Output execution examples (Anthropic Skill Creator Standard)")

    # 2. Workflow Anchors
    for path in sorted((root / "workflows").glob("*.md")):
        rel = path.relative_to(root)
        text = path.read_text("utf-8", errors="replace")
        
        node_matches = list(re.finditer(r"(?m)^###\s+(?:Bước|Step|Node|Phase|\d+[\.:])\s+(.+)$", text))
        if node_matches:
            for i, match in enumerate(node_matches):
                node_title = match.group(0).strip()
                start_pos = match.start()
                end_pos = node_matches[i + 1].start() if i + 1 < len(node_matches) else len(text)
                node_body = text[start_pos:end_pos]
                
                has_input = bool(re.search(r"(?i)(\[\s*input\s*artifacts?\s*\]|\*\*\[?input(?:\s*artifacts?)?\]?\*\*|####?\s*input|\bprerequisites\s*:|đầu\s*vào\s*:)", node_body))
                has_output = bool(re.search(r"(?i)(\[\s*output\s*artifacts?\s*\]|\*\*\[?output(?:\s*artifacts?)?\]?\*\*|####?\s*output|\bdeliverables\s*:|đầu\s*ra\s*:)", node_body))
                has_dod = bool(re.search(r"(?i)(\[\s*dod\s*\]|\*\*\[?dod\]?\*\*|####?\s*definition\s*of\s*done|\bdefinition\s*of\s*done\s*:|tiêu\s*chí\s*hoàn\s*thành|\-\s*\[\s*\])", node_body))
                has_eval = bool(re.search(r"(?i)(\[\s*evaluation\s*loop\s*\]|\*\*\[?evaluation(?:\s*loop)?\]?\*\*|####?\s*evaluation\s*loop|\bevaluation\s*loop\s*:|vòng\s*lặp\s*đánh\s*giá|pass\s*[-–—>]+\s*|fail\s*[-–—>]+\s*)", node_body))
                
                if not (has_input and has_output and has_dod and has_eval):
                    missing_parts = []
                    if not has_input: missing_parts.append("Input Artifacts")
                    if not has_output: missing_parts.append("Output Artifacts")
                    if not has_dod: missing_parts.append("DoD")
                    if not has_eval: missing_parts.append("Evaluation Loop")
                    line_num = text.count("\n", 0, start_pos) + 1
                    add(findings, "error", "workflow.missing_node_anatomy", rel, f"{node_title} lacks 5-Part Node Anatomy: missing {', '.join(missing_parts)}", line=line_num)
        
        has_escalation = bool(re.search(r"(?i)(\[ESCALATE_HUMAN\]|human\s*approval|leo\s*thang|escalat)", text))
        if not has_escalation:
            add(findings, "warning", "workflow.missing_escalation_guard", rel, "Workflow lacks explicit [ESCALATE_HUMAN] escalation fallback anchor")

    # 3. Agent Anchors
    for path in sorted((root / "agent").glob("*.md")):
        rel = path.relative_to(root)
        text = path.read_text("utf-8", errors="replace")
        
        has_role = bool(re.search(r"(?i)(vai\s*trò|role|outcome|trách\s*nhiệm)", text))
        has_process = bool(re.search(r"(?i)(quy\s*trình|process|workflow|state\s*machine|bước\s*\d|worker\s*briefing)", text))
        has_constraints = bool(re.search(r"(?i)(hard\s*constraints?|negative\s*(?:constraints?|boundaries)|ranh\s*giới\s*phủ\s*định|tuyệt\s*đối\s*không|nguyên\s*tắc\s*bất\s*biến|cấm|negative)", text))
        has_output_dod = bool(re.search(r"(?i)(format\s*đầu\s*ra|output\s*format|bàn\s*giao|definition\s*of\s*done|\bdod\b)", text))
        
        if not (has_role and has_process and has_constraints and has_output_dod):
            missing_blocks = []
            if not has_role: missing_blocks.append("Role & Outcome")
            if not has_process: missing_blocks.append("Process/Quy trình")
            if not has_constraints: missing_blocks.append("Hard/Negative Constraints")
            if not has_output_dod: missing_blocks.append("Output Format/DoD")
            add(findings, "error", "agent.missing_role_blocks", rel, f"Agent prompt lacks standard core blocks: missing {', '.join(missing_blocks)}")
            
        is_orchestrator = bool(re.search(r"(?i)(orchestrat|architect|creator|điều\s*phối)", path.stem) or re.search(r"(?i)(master\s*orchestrator|bộ\s*não\s*điều\s*phối)", text))
        if is_orchestrator:
            has_briefing = bool(
                re.search(r"(?i)(worker\s*briefing|briefing\s*protocol|never\s*delegate\s*understanding|goal\s*&\s*context|negative\s*boundaries|file\s*scope|ruled\s*out)", text)
            )
            if not has_briefing:
                add(findings, "error", "agent.missing_worker_briefing", rel, "Master Orchestrator agent lacks Worker Briefing Protocol anchors (Goal & Context, Ruled out, File scope, Negative boundaries, Verification criteria)")

        is_master_orchestrator = bool(
            path.stem in ("kit-architect", "master-orchestrator") or
            re.search(r"(?i)(master\s*orchestrator|delegates_to)", text)
        )
        if is_master_orchestrator:
            has_protocol = bool(re.search(r"(?i)(orchestration\s*protocol|complexity\s*ladder)", text))
            if not has_protocol:
                add(findings, "warning", "orchestrator.missing_protocol_section", rel, "Master Orchestrator agent lacks Orchestration Protocol section (ACO Lite Complexity Ladder)")

        has_fs_contract = bool(
            re.search(r"(?i)(filesystem\s*&\s*workspace\s*contract|\.workspace.*outputs\/|inputs\/.*\.workspace|\.workspace.*inputs\/|outputs\/.*\.workspace)", text)
        )
        if not has_fs_contract:
            add(findings, "warning", "agent.missing_filesystem_contract", rel, "Agent prompt lacks Filesystem & Workspace Contract anchors (inputs/, outputs/, .workspace/)")

    # 4. Memory Anchors
    memory_file = root / "memory" / "MEMORY.md"
    if memory_file.is_file():
        rel = memory_file.relative_to(root)
        text = memory_file.read_text("utf-8", errors="replace")
        has_topics = bool(re.search(r"(?i)(domain|feedback|failure|pattern|convention|checklist|run|evolution)", text))
        if not has_topics:
            add(findings, "warning", "memory.missing_required_topics", rel, "MEMORY.md index lacks links to standard knowledge topic categories")

    # 5. Output Sanitizer Anchor (Invariant 1: Không declared -> không xuất ra outputs)
    outputs_dir = root / "outputs" if (root / "outputs").is_dir() else (root.parent / "outputs" if (root.name == ".agents" and (root.parent / "outputs").is_dir()) else None)
    if outputs_dir and outputs_dir.is_dir():
        FORBIDDEN_EXTENSIONS = {".tmp", ".log", ".cache", ".chunk", ".part", ".bak", ".swp"}
        for item in outputs_dir.rglob("*"):
            if item.is_file():
                rel_file = item.relative_to(outputs_dir)
                if item.suffix.lower() in FORBIDDEN_EXTENSIONS or item.name.startswith("."):
                    add(findings, "error", "output.sanitizer_violation", Path("outputs") / rel_file, f"Forbidden intermediate/temporary file in outputs/: {item.name}. Intermediate files must be placed in .workspace/")


def validate_template_compliance(root: Path, findings: list[Finding]) -> None:
    templates_dir = root / "templates"
    references_dir = root / "references"
    if not templates_dir.is_dir():
        add(findings, "warning", "template.missing_dir", Path("templates"), "Templates directory is missing")
        return
    if not references_dir.is_dir():
        add(findings, "warning", "reference.missing_dir", Path("references"), "References directory is missing")
        return
    required_templates = {
        "agent-template.md",
        "skill-template.md",
        "workflow-template.md",
        "rule-template.md",
        "manifest-template.json",
        "memory-template.md",
        "orchestrator-template.md",
    }
    for template_name in sorted(required_templates):
        if not (templates_dir / template_name).is_file():
            add(findings, "warning", "template.missing_file", Path("templates") / template_name, f"Template file missing: {template_name}")


def validate_compiler_artifacts(root: Path, findings: list[Finding]) -> None:
    """Validate 9 compile-time checks conforming to CANON 10 and Compiler + Runtime Model."""
    def _safe_load_fm(text: str) -> dict | None:
        if yaml is None:
            data = fallback_frontmatter(text)
            return data if isinstance(data, dict) else None
        try:
            data = yaml.safe_load(text)
            return data if isinstance(data, dict) else None
        except yaml.YAMLError:
            return None

    has_capabilities = False
    
    # 1. Validate capability namespace & evidence schema completeness
    for agent_path in sorted((root / "agent").glob("*.md")):
        raw, _ = extract_frontmatter(agent_path)
        if not raw:
            continue
        fm = _safe_load_fm(raw)
        if not fm:
            continue
        caps = fm.get("capabilities", [])
        if isinstance(caps, list):
            for cap in caps:
                if not isinstance(cap, dict):
                    continue
                has_capabilities = True
                cap_id = str(cap.get("id", "")).strip()
                if not cap_id:
                    continue
                if not validate_capability_namespace(cap_id):
                    add(findings, "error", "capability.invalid_namespace", agent_path.relative_to(root), f"Capability ID '{cap_id}' violates namespace format (CANON 9: domain.component.action)")
                
                evidence = cap.get("evidence_schema")
                if not evidence or not isinstance(evidence, dict) or (not evidence.get("structural") and not evidence.get("semantic")):
                    add(findings, "warning", "evidence.missing_schema", agent_path.relative_to(root), f"Capability '{cap_id}' lacks explicit structural/semantic evidence_schema")

    # 2. Run simulation checks (reachability, cycle detection, coverage, dead states)
    sim_report = simulate_workflow_graph(root)
    for unreach in sim_report.get("unreachable_nodes", []):
        add(findings, "error", "graph.unreachable_node", Path("workflows"), f"Unreachable workflow node detected: {unreach}")
    for cycle in sim_report.get("cycles_detected", []):
        add(findings, "error", "precondition.cycle_detected", Path("workflows"), f"Precondition cycle detected: {' -> '.join(cycle)}")
    for uncov in sim_report.get("uncovered_outcomes", []):
        add(findings, "error", "capability.uncovered_outcome", Path("workflows"), f"Workflow required outcome lacks capability coverage: {uncov}")
    for dead in sim_report.get("dead_states", []):
        add(findings, "error", "workflow.dead_state", Path("workflows"), f"Non-terminal workflow state has 0 outgoing transitions: {dead}")

    # 3. Check compiled artifacts freshness if capabilities exist
    if has_capabilities:
        for artifact_name, compiler_fn in [
            ("routing_index.json", compile_routing_index),
            ("invariant_rules.json", compile_invariants),
            ("state_schema.json", compile_state_schema),
            ("execution_policy.json", compile_execution_policy),
            ("task_classifier_index.json", compile_task_classifier),
            ("evidence_schemas.json", compile_evidence_schemas),
        ]:
            artifact_path = root / artifact_name
            if artifact_path.is_file():
                try:
                    actual = json.loads(artifact_path.read_text("utf-8"))
                    expected = compiler_fn(root)
                    if isinstance(actual, dict) and isinstance(expected, dict):
                        actual_norm = {k: v for k, v in actual.items() if k != "generated_at"}
                        expected_norm = {k: v for k, v in expected.items() if k != "generated_at"}
                        if actual_norm != expected_norm:
                            add(findings, "error", "compiler.stale_artifacts", Path(artifact_name), f"Compiled artifact {artifact_name} is stale. Regenerate it.")
                except Exception:
                    pass
        check_execution_policy(root, findings)

    # === ROUTING INVARIANTS (P0) ===
    # Any kit with ≥1 agent MUST have ≥1 compiled capability
    # (Skip if ALL agents are routing_exempt, e.g. meta-agents like kit-architect)
    agent_count = len(list((root / "agent").glob("*.md"))) if (root / "agent").is_dir() else 0
    non_exempt_count = 0
    if (root / "agent").is_dir():
        for ap in (root / "agent").glob("*.md"):
            rf, _ = extract_frontmatter(ap)
            if rf:
                fd = _safe_load_fm(rf)
                if isinstance(fd, dict) and str(fd.get("routing_exempt", "")).lower() not in ("true", "yes"):
                    non_exempt_count += 1
    if non_exempt_count > 0 and not has_capabilities:
        add(findings, "error", "routing.empty_capabilities", Path("agent/"),
            f"Kit has {non_exempt_count} non-exempt agent(s) but 0 compiled capabilities in frontmatter. "
            f"Routing will be blind. Populate 'capabilities:' block in agent frontmatter "
            f"using domain profiling output (Section 6: Compiled Routing Contract).")

    # Orchestrator with delegates_to MUST have routing table in body
    # Agent with skills (non-orchestrator) MUST have skill invocation matrix
    for agent_path in sorted((root / "agent").glob("*.md")):
        raw_fm, _ = extract_frontmatter(agent_path)
        if not raw_fm:
            continue
        fm_data = _safe_load_fm(raw_fm)
        if not fm_data:
            continue
        # Skip routing_exempt agents (meta-agents that route via prose)
        if str(fm_data.get("routing_exempt", "")).lower() in ("true", "yes"):
            continue
        text = agent_path.read_text("utf-8", errors="replace")

        delegates = fm_data.get("delegates_to", [])
        if isinstance(delegates, str):
            delegates = [d.strip() for d in delegates.strip("[]").split(",") if d.strip()]

        if delegates:
            has_routing_table = bool(re.search(
                r"(?i)(routing\s*table|bảng\s*định\s*tuyến|intent.*pattern.*agent|dispatch\s*matrix)",
                text
            ))
            if not has_routing_table:
                add(findings, "error", "routing.orchestrator_missing_routing_table",
                    agent_path.relative_to(root),
                    "Master Orchestrator has delegates_to but no Routing Table section in body. "
                    "Add '## ROUTING TABLE' with populated intent→agent→skill mapping.")
        else:
            skills_declared = fm_data.get("skills", [])
            if isinstance(skills_declared, str):
                skills_declared = [s.strip() for s in skills_declared.strip("[]").split(",") if s.strip()]
            if skills_declared:
                has_skill_matrix = bool(re.search(
                    r"(?i)(skill\s*invocation\s*matrix|ma\s*trận\s*chiến\s*lược|skill\s*loading\s*protocol|strategy\s*matrix.*skill)",
                    text
                ))
                if not has_skill_matrix:
                    add(findings, "error", "routing.agent_missing_skill_matrix",
                        agent_path.relative_to(root),
                        f"Agent declares skills {skills_declared} but has no Skill Invocation Matrix in body. "
                        f"Add '## SKILL INVOCATION MATRIX' with scenario→skill→reason mapping.")


def check_execution_policy(root: Path, findings: list[Finding]) -> None:
    """Verify execution_policy.json exists, is valid, and mode matches topology."""
    ep_file = root / "execution_policy.json"
    if not ep_file.is_file():
        add(findings, "error", "compiler.execution_policy_missing", Path("execution_policy.json"),
            "execution_policy.json is missing. Run compile_execution_policy.py to generate.")
        return

    try:
        data = json.loads(ep_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add(findings, "error", "json.invalid", Path("execution_policy.json"), f"Invalid JSON: {exc}")
        return

    required = {"schemaVersion", "mode", "parallel", "retry", "recovery", "context"}
    missing = required - set(data.keys())
    if missing:
        add(findings, "error", "compiler.execution_policy_stale", Path("execution_policy.json"),
            f"Missing required fields: {', '.join(sorted(missing))}")
        return

    # Real JSON Schema validation
    schema_path = root / "schemas" / "execution-policy.schema.json"
    if not schema_path.is_file():
        schema_path = Path(__file__).resolve().parents[1] / "schemas" / "execution-policy.schema.json"
    if schema_path.is_file():
        try:
            import jsonschema
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            jsonschema.validate(instance=data, schema=schema)
        except ImportError:
            pass
        except Exception as val_err:
            err_msg = getattr(val_err, "message", str(val_err))
            add(findings, "error", "compiler.execution_policy_schema_invalid", Path("execution_policy.json"),
                f"JSON Schema validation failed: {err_msg}")
            return

    agent_count = len(list((root / "agent").glob("*.md"))) if (root / "agent").is_dir() else 0
    mode = data.get("mode", "")
    if agent_count <= 1 and mode not in ("direct", "stage_machine"):
        add(findings, "warning", "compiler.execution_policy_invalid_mode", Path("execution_policy.json"),
            f"Single agent kit has mode='{mode}', expected 'direct' or 'stage_machine'")
    elif agent_count > 1 and mode == "direct":
        add(findings, "warning", "compiler.execution_policy_invalid_mode", Path("execution_policy.json"),
            f"Multi-agent kit has mode='direct', expected 'stage_machine' or 'fork_join'")

    parallel = data.get("parallel", {})
    if parallel.get("writes", False) is not False:
        add(findings, "error", "compiler.execution_policy_stale", Path("execution_policy.json"),
            "parallel.writes must be false — architectural invariant")

    recovery = data.get("recovery", [])
    if len(recovery) > 3:
        add(findings, "error", "compiler.execution_policy_stale", Path("execution_policy.json"),
            f"Recovery cascade has {len(recovery)} entries, max 3 allowed")


def sync_registry(root: Path) -> tuple[int, list[str]]:
    """Synchronize manifest.json, manifest.lock.json, DEPENDENCY_GRAPH.md, and compiled decision artifacts."""
    synced: list[str] = []

    try:
        import render_docs
        mod_docs = render_docs.apply_generated_blocks(root, check=False)
        if mod_docs:
            synced.extend(mod_docs)
    except Exception:
        pass

    manifest = build_manifest(root)
    manifest_text = canonical_json(manifest)
    lock = build_lock(root, manifest)
    lock_text = canonical_json(lock)
    (root / "manifest.json").write_text(manifest_text, "utf-8")
    (root / "manifest.lock.json").write_text(lock_text, "utf-8")
    dep_text = render_dependency_graph(root)
    (root / "DEPENDENCY_GRAPH.md").write_text(dep_text, "utf-8")
    
    synced.extend(["manifest.json", "manifest.lock.json", "DEPENDENCY_GRAPH.md"])
    
    try:
        if (root / "agent").is_dir() and any((root / "agent").glob("*.md")):
            ep = compile_execution_policy(root)
            (root / "execution_policy.json").write_text(canonical_json(ep), "utf-8")
            synced.append("execution_policy.json")

        r_idx = compile_routing_index(root)
        if r_idx.get("capabilities"):
            (root / "routing_index.json").write_text(canonical_json(r_idx), "utf-8")
            synced.append("routing_index.json")
            
            inv = compile_invariants(root)
            (root / "invariant_rules.json").write_text(canonical_json(inv), "utf-8")
            synced.append("invariant_rules.json")

            st = compile_state_schema(root)
            (root / "state_schema.json").write_text(canonical_json(st), "utf-8")
            synced.append("state_schema.json")

            tc = compile_task_classifier(root)
            (root / "task_classifier_index.json").write_text(canonical_json(tc), "utf-8")
            synced.append("task_classifier_index.json")

            ev = compile_evidence_schemas(root)
            (root / "evidence_schemas.json").write_text(canonical_json(ev), "utf-8")
            synced.append("evidence_schemas.json")

            ep = compile_execution_policy(root)
            (root / "execution_policy.json").write_text(canonical_json(ep), "utf-8")
            synced.append("execution_policy.json")
    except Exception:
        pass

    return len(synced), synced


ABSOLUTE_USER_PATH = re.compile(
    r"(?i)(?:[a-z]:[\\/]{1,2}(?:users|documents and settings)[\\/]|file:///[a-z]:/|(?<![\w.:/-])/(?:Users|home)/[^/\s]+/)"
)


def validate_portability(root: Path, findings: list[Finding]) -> None:
    """Detect hardcoded user-specific absolute paths in Markdown, JSON, Python, and JavaScript/MJS files."""
    extensions = {".md", ".json", ".py", ".mjs"}
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix not in extensions:
            continue
        rel = p.relative_to(root).as_posix()
        # skip scripts/tests/
        if rel.startswith("scripts/tests/"):
            continue

        try:
            content = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        for line_num, line in enumerate(content.splitlines(), start=1):
            match = ABSOLUTE_USER_PATH.search(line)
            if match:
                add(
                    findings,
                    "error",
                    "path.absolute_user_path",
                    Path(rel),
                    f"Hardcoded absolute user path detected: {match.group(0)}",
                    line=line_num,
                    evidence=line.strip()[:100],
                )


EXTERNAL_DEP_TOKEN = re.compile(r"superpowers:[a-z-]+|agy-customizations|ponytail")


def validate_dependencies(root: Path, findings: list[Finding]) -> None:
    """Verify that every external plugin/tool token is explicitly declared in DEPENDENCIES.md."""
    dep_file = root / "DEPENDENCIES.md"
    dep_text = dep_file.read_text(encoding="utf-8") if dep_file.is_file() else ""

    extensions = {".md", ".json", ".py", ".mjs"}
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix not in extensions:
            continue
        rel = p.relative_to(root).as_posix()
        if rel == "DEPENDENCIES.md" or rel.startswith("scripts/tests/"):
            continue

        try:
            content = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        for line_num, line in enumerate(content.splitlines(), start=1):
            matches = EXTERNAL_DEP_TOKEN.findall(line)
            for token in matches:
                if token not in dep_text:
                    add(
                        findings,
                        "error",
                        "dependency.undeclared",
                        Path(rel),
                        f"Undeclared external dependency token: {token}",
                        line=line_num,
                        evidence=line.strip()[:100],
                    )


def validate_context_budget(root: Path, findings: list[Finding]) -> None:
    """Validate always-on rules and orchestrator prompts against context byte budgets."""
    try:
        from context_budget import measure, RULES_BUDGET_BYTES, ORCHESTRATOR_BUDGET_BYTES
    except ImportError:
        import sys
        scripts_dir = root / "scripts" if (root / "scripts").is_dir() else Path(__file__).resolve().parent
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))
        from context_budget import measure, RULES_BUDGET_BYTES, ORCHESTRATOR_BUDGET_BYTES

    m = measure(root)
    if m["rules_bytes"] > RULES_BUDGET_BYTES:
        add(
            findings,
            "error",
            "context.budget_exceeded",
            Path("rules"),
            f"Always-on rules budget exceeded: {m['rules_bytes']} bytes > {RULES_BUDGET_BYTES} bytes limit",
        )
    if m["orchestrator_bytes"] > ORCHESTRATOR_BUDGET_BYTES:
        add(
            findings,
            "error",
            "context.budget_exceeded",
            Path("agent"),
            f"Orchestrator prompt budget exceeded: {m['orchestrator_bytes']} bytes > {ORCHESTRATOR_BUDGET_BYTES} bytes limit",
        )


def validate_quick(root: Path) -> list[Finding]:
    """Fast frontmatter and JSON syntax validation for Tier 1 rapid checks."""
    findings: list[Finding] = []
    validate_json(root, findings)
    validate_kit_version(root, findings)
    validate_frontmatter(root, findings)
    validate_structural_anchors(root, findings)
    validate_compiler_artifacts(root, findings)
    validate_portability(root, findings)
    return findings


def validate_placeholders(root: Path, findings: list[Finding]) -> None:
    """Detect unfilled template placeholders in generated kit markdown files."""
    for sub in ("agent", "skills", "workflows", "rules"):
        sub_dir = root / sub
        if not sub_dir.is_dir():
            continue
        for p in sub_dir.rglob("*.md"):
            if not p.is_file():
                continue
            try:
                content = p.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            matches = find_placeholders(content)
            for line_no, ph in matches:
                add(
                    findings,
                    "error",
                    "placeholder.unfilled",
                    p.relative_to(root),
                    f"Unfilled template placeholder '{ph}' detected in kit output",
                    line=line_no,
                )


def validate(root: Path, auto_heal: bool = True, kit_output: bool = False) -> list[Finding]:
    findings: list[Finding] = []
    validate_json(root, findings)
    validate_kit_version(root, findings)
    agents, skills, workflows, _rules = validate_frontmatter(root, findings)
    validate_references(root, agents, skills, workflows, findings)
    validate_manifest(root, findings, auto_heal=auto_heal)
    validate_generated_docs(root, findings)
    validate_markdown_links(root, findings)
    validate_memory(root, findings)
    validate_python(root, findings)
    validate_architecture_counts(root, findings)
    validate_structural_anchors(root, findings)
    validate_template_compliance(root, findings)
    validate_compiler_artifacts(root, findings)
    validate_portability(root, findings)
    validate_dependencies(root, findings)
    validate_context_budget(root, findings)
    if kit_output:
        validate_placeholders(root, findings)
    return findings


def print_audit_report(root: Path, findings: list[Finding]) -> None:
    errors = [item for item in findings if item.severity == "error"]
    warnings = [item for item in findings if item.severity == "warning"]
    
    print("\n============================================================")
    print("               AG KIT QUALITY AUDIT REPORT                  ")
    print("============================================================")
    print(f"Target: {root}\n")
    
    if warnings:
        print(f"[!] Warnings ({len(warnings)}):")
        for item in warnings:
            print(f"  - [{item.code}] {item.file}:{item.line} -> {item.message}")
        print()

    if errors:
        print(f"[-] Structural Errors ({len(errors)}):")
        for item in errors:
            print(f"  - [{item.code}] {item.file}:{item.line} -> {item.message}")
        print()
        print("Verdict: [-] FAIL (Needs fixes before delivery)")
    elif warnings:
        print("Verdict: [4/5 STAR PASS] Kit is structurally valid with minor warnings.")
    else:
        print("Verdict: [5/5 STAR EXEMPLARY] Completely compliant with AG Kit standards!")
    print("============================================================\n")


def run_validation_and_update_lifecycle(root: Path, findings_output: Optional[Path] = None, kit_output: bool = False) -> dict:
    findings = validate(root, kit_output=kit_output)
    errors = [item for item in findings if item.severity == "error"]
    warnings = [item for item in findings if item.severity == "warning"]
    
    score = 5 if not errors and not warnings else (4 if not errors else max(1, 4 - len(errors)))
    pass_status = (len(errors) == 0)
    
    from datetime import datetime, timezone
    findings_data = {
        "pass": pass_status,
        "score": score,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": [item.__dict__ for item in errors],
        "warnings": [item.__dict__ for item in warnings],
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
    }
    
    if findings_output:
        findings_output = Path(findings_output)
        findings_output.parent.mkdir(parents=True, exist_ok=True)
        findings_output.write_text(json.dumps(findings_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        
    try:
        from lifecycle_engine import LifecycleEngine
        engine = LifecycleEngine()
        findings_filename = findings_output.name if findings_output else "audit_findings.json"
        engine.record_validation_verdict(root, pass_status=pass_status, score=score, findings_file=findings_filename)
    except Exception:
        pass
        
    return findings_data


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AG Kit structure and cross references")
    parser.add_argument("path", nargs="?", default=None, help="Path to .agents (defaults to this toolkit)")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Output findings as JSON")
    parser.add_argument("--audit", action="store_true", help="Print structured 5-star quality audit report")
    parser.add_argument("--findings-json", dest="findings_json", default=None, help="Write structured audit_findings.json to specified path")
    parser.add_argument("--sync", action="store_true", help="Auto-sync manifest.json and DEPENDENCY_GRAPH.md before validation")
    parser.add_argument("--quick", action="store_true", help="Fast check of syntax and frontmatter only")
    parser.add_argument("--converge", action="store_true", help="Run bounded self-healing convergence loop (max 3 iterations)")
    parser.add_argument("--no-auto-heal", action="store_false", dest="auto_heal", default=True, help="Disable auto-healing stale lockfiles")
    parser.add_argument("--audit-feedback", action="store_true", help="Audit feedback health from Central Feedback Hub")
    parser.add_argument("--kit-output", action="store_true", help="Enable placeholder detection for generated kit output")
    args = parser.parse_args()
    root = Path(args.path).resolve() if args.path else Path(__file__).resolve().parents[1]
    if not root.is_dir():
        parser.error(f"Toolkit directory does not exist: {root}")
    
    if args.audit_feedback:
        try:
            from feedback_hub import audit_kit_feedback, DEFAULT_HUB_DIR
            kit_name = root.name if root.name != ".agents" else "agent-kit-builder"
            kit_jsonl = DEFAULT_HUB_DIR / "kit_feedback.jsonl"
            audit = audit_kit_feedback(kit_jsonl, kit_name)
            unres = audit["unresolved"]
            know = audit["regression_knowledge"]
            print(f"📋 [FEEDBACK AUDIT] Kit: {kit_name}")
            print(f"   ├─ Chưa giải quyết / Chưa verified: {len(unres)}")
            print(f"   └─ Bài học phòng ngừa (Verified): {len(know)}")
        except Exception as e:
            print(f"ℹ️ Feedback Hub check: {e}")

    if args.sync:
        count, files = sync_registry(root)
        print(f"[+] Synchronized {count} registry files: {', '.join(files)}")
    
    if args.converge:
        from convergence_engine import converge
        report = converge(root, max_iterations=3)
        if args.as_json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            status = "[PASS] Converged successfully" if report["converged"] else "[FAIL] Convergence incomplete"
            print(f"{status} (Iterations: {report['iterations']}, Auto-fixed: {report['auto_fixed_count']}, Escalated: {report['escalated_count']})")
        return 0 if report["converged"] else 1

    if args.findings_json:
        findings_path = Path(args.findings_json)
        result = run_validation_and_update_lifecycle(root, findings_output=findings_path, kit_output=args.kit_output)
        if not args.as_json and not args.audit:
            print(f"[+] Wrote audit findings to {findings_path} (Pass: {result['pass']}, Score: {result['score']}/5)")
        return 0 if result["pass"] else 1

    findings = validate_quick(root) if args.quick else validate(root, auto_heal=args.auto_heal, kit_output=args.kit_output)
    errors = [item for item in findings if item.severity == "error"]
    warnings = [item for item in findings if item.severity == "warning"]
    
    payload = {
        "toolkit": str(root),
        "passed": not errors,
        "summary": {"errors": len(errors), "warnings": len(warnings)},
        "findings": [item.__dict__ for item in findings],
    }
    
    if args.as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    elif args.audit:
        print_audit_report(root, findings)
    else:
        print(f"AG Kit self-validation: {root}")
        for item in findings:
            print(f"[{item.severity.upper()}] {item.file}:{item.line} {item.code} - {item.message}")
        print(f"Summary: {len(errors)} error(s), {len(warnings)} warning(s)")
        print("[PASS] Toolkit is structurally valid." if not errors else "[FAIL] Toolkit validation failed.")
    
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

