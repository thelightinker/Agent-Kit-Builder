#!/usr/bin/env python3
"""
Agent Kit Multi-Platform Bundle Exporter
Compiles an Agent Kit into native bundles for:
- Antigravity Plugin Bundle (dist/antigravity-plugin with SHA-256 manifest)
- Cursor (.cursorrules)
- Claude Desktop / Anthropic Projects (claude_instructions.txt + tools.json)
- OpenAI Custom GPTs (gpt_instructions.txt)
"""

import sys
import os
import json
import shutil
import hashlib
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def parse_frontmatter(content):
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    yaml_text = parts[1].strip()
    body = parts[2].strip()
    data = {}
    for line in yaml_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"').strip("'")
    return data, body

def collect_kit_components(kit_dir):
    kit_path = Path(kit_dir)
    # If passed kit root containing .agents, dive into .agents
    if (kit_path / ".agents").is_dir():
        kit_path = kit_path / ".agents"

    agents = {}
    skills = {}
    rules = {}
    workflows = {}

    # Read Agents
    agent_dir = kit_path / "agent"
    if agent_dir.exists():
        for f in agent_dir.glob("*.md"):
            data, body = parse_frontmatter(f.read_text("utf-8", errors="replace"))
            agents[f.stem] = {"meta": data, "body": body, "path": str(f)}

    # Read Skills
    skills_dir = kit_path / "skills"
    if skills_dir.exists():
        for sdir in skills_dir.iterdir():
            if sdir.is_dir():
                sfile = sdir / "SKILL.md"
                if sfile.exists():
                    data, body = parse_frontmatter(sfile.read_text("utf-8", errors="replace"))
                    skills[sdir.name] = {"meta": data, "body": body, "path": str(sfile), "dir": str(sdir)}

    # Read Rules
    rules_dir = kit_path / "rules"
    if rules_dir.exists():
        for f in rules_dir.glob("*.md"):
            data, body = parse_frontmatter(f.read_text("utf-8", errors="replace"))
            rules[f.stem] = {"meta": data, "body": body, "path": str(f)}

    # Read Workflows
    wf_dir = kit_path / "workflows"
    if wf_dir.exists():
        for f in wf_dir.glob("*.md"):
            data, body = parse_frontmatter(f.read_text("utf-8", errors="replace"))
            workflows[f.stem] = {"meta": data, "body": body, "path": str(f)}

    return agents, skills, rules, workflows, kit_path

def export_cursor(agents, skills, rules, output_dir):
    cursor_dir = Path(output_dir) / "cursor"
    cursor_dir.mkdir(parents=True, exist_ok=True)
    out_file = cursor_dir / ".cursorrules"

    lines = ["# Agent Kit Cursor Rules Configuration", ""]
    lines.append("## System Rules")
    for rname, rdata in rules.items():
        lines.append(f"\n### Rule: {rname}")
        lines.append(rdata["body"])

    lines.append("\n## Agent System Prompts")
    for aname, adata in agents.items():
        lines.append(f"\n### Agent: {aname}")
        lines.append(adata["body"])

    lines.append("\n## Skill Directives")
    for sname, sdata in skills.items():
        desc = sdata["meta"].get("description", "")
        lines.append(f"- **{sname}**: {desc}")

    out_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"[+] Cursor bundle written to: {out_file}")
    return str(out_file)

def export_claude(agents, skills, rules, output_dir):
    claude_dir = Path(output_dir) / "claude"
    claude_dir.mkdir(parents=True, exist_ok=True)
    
    out_inst = claude_dir / "claude_instructions.txt"
    out_tools = claude_dir / "tools.json"

    lines = ["# Anthropic Project Instructions", ""]
    lines.append("## Core Rules & System Architecture")
    for rname, rdata in rules.items():
        lines.append(f"\n<rule name=\"{rname}\">")
        lines.append(rdata["body"])
        lines.append("</rule>")

    lines.append("\n## Specialist Agents")
    for aname, adata in agents.items():
        lines.append(f"\n<agent name=\"{aname}\">")
        lines.append(adata["body"])
        lines.append("</agent>")

    lines.append("\n## Skills Library")
    for sname, sdata in skills.items():
        lines.append(f"\n<skill name=\"{sname}\">")
        lines.append(sdata["body"])
        lines.append("</skill>")

    out_inst.write_text("\n".join(lines), encoding="utf-8")

    tools_list = []
    for sname, sdata in skills.items():
        tools_list.append({
            "name": sname,
            "description": sdata["meta"].get("description", f"Skill capability {sname}"),
            "input_schema": {
                "type": "object",
                "properties": {
                    "task": {"type": "string", "description": "Task parameters for skill execution"}
                },
                "required": ["task"]
            }
        })
    out_tools.write_text(json.dumps(tools_list, indent=2, ensure_ascii=False), encoding="utf-8")
    
    print(f"[+] Claude bundle written to: {claude_dir}")
    return str(claude_dir)

def export_openai(agents, skills, rules, output_dir):
    openai_dir = Path(output_dir) / "openai"
    openai_dir.mkdir(parents=True, exist_ok=True)
    out_inst = openai_dir / "gpt_instructions.txt"

    lines = ["# Custom GPT System Instructions", ""]
    for rname, rdata in rules.items():
        lines.append(f"--- RULE: {rname} ---")
        lines.append(rdata["body"])

    for aname, adata in agents.items():
        lines.append(f"\n--- AGENT: {aname} ---")
        lines.append(adata["body"])

    lines.append("\n--- AVAILABLE SKILLS SUMMARY ---")
    for sname, sdata in skills.items():
        desc = sdata["meta"].get("description", "")
        lines.append(f"- {sname}: {desc}")

    out_text = "\n".join(lines)
    if len(out_text) > 7800:
        out_text = out_text[:7800] + "\n\n[Truncated to fit Custom GPT 8000 character instruction limit]"

    out_inst.write_text(out_text, encoding="utf-8")
    print(f"[+] OpenAI Custom GPT bundle written to: {out_inst}")
    return str(out_inst)

def export_antigravity_plugin(kit_dir, agents, skills, rules, workflows, kit_path, output_dir):
    plugin_dir = Path(output_dir) / "antigravity-plugin"
    if plugin_dir.exists():
        shutil.rmtree(plugin_dir, ignore_errors=True)
    plugin_dir.mkdir(parents=True, exist_ok=True)

    v_file = kit_path / "VERSION"
    version = v_file.read_text("utf-8").strip() if v_file.exists() else "1.0.0"

    resolved_path = kit_path.resolve()
    kit_name = resolved_path.parent.name if resolved_path.name == ".agents" else resolved_path.name
    if not kit_name or kit_name in (".", "/"):
        kit_name = "agent-kit"

    ext_config = {
        "name": kit_name,
        "version": version,
        "runtime": "antigravity",
        "description": f"Antigravity Native AI Agent Plugin Bundle - {kit_name}"
    }
    (plugin_dir / "gemini-extension.json").write_text(json.dumps(ext_config, indent=2), encoding="utf-8")

    # Copy rules, skills, agents
    if (kit_path / "skills").is_dir():
        shutil.copytree(kit_path / "skills", plugin_dir / "skills", dirs_exist_ok=True)
    if (kit_path / "agent").is_dir():
        shutil.copytree(kit_path / "agent", plugin_dir / "agents", dirs_exist_ok=True)
    if (kit_path / "rules").is_dir():
        shutil.copytree(kit_path / "rules", plugin_dir / "rules", dirs_exist_ok=True)

    # Copy hooks if present
    hooks_out = plugin_dir / "hooks"
    hooks_out.mkdir(parents=True, exist_ok=True)
    if (kit_path / "hooks.json").exists():
        shutil.copy2(kit_path / "hooks.json", hooks_out / "hooks.json")
    if (kit_path / "hooks" / "validate-tool-call.mjs").exists():
        shutil.copy2(kit_path / "hooks" / "validate-tool-call.mjs", hooks_out / "validate-tool-call.mjs")
    if (kit_path / "mcp_config.json").exists():
        shutil.copy2(kit_path / "mcp_config.json", plugin_dir / "mcp_config.example.json")

    # Inventory & SHA-256
    files_inv = []
    for root, _, files in os.walk(plugin_dir):
        for f in sorted(files):
            fpath = Path(root) / f
            rel = fpath.relative_to(plugin_dir).as_posix()
            files_inv.append({
                "path": rel,
                "sha256": sha256_file(fpath)
            })

    contents_manifest = {
        "name": ext_config["name"],
        "version": version,
        "runtime": "antigravity",
        "counts": {
            "agents": len(agents),
            "skills": len(skills),
            "rules": len(rules),
            "workflows": len(workflows)
        },
        "files": files_inv
    }
    (plugin_dir / "PLUGIN_CONTENTS.json").write_text(json.dumps(contents_manifest, indent=2), encoding="utf-8")
    print(f"[+] Antigravity Plugin bundle written to: {plugin_dir}")
    return str(plugin_dir)

def export_kit(kit_dir, output_dir, target="all", sync_dir=None):
    agents, skills, rules, workflows, kit_path = collect_kit_components(kit_dir)
    print(f"[*] Collected {len(agents)} agents, {len(skills)} skills, {len(rules)} rules, {len(workflows)} workflows from {kit_dir}")

    results = {}
    if target in ("cursor", "all"):
        results["cursor"] = export_cursor(agents, skills, rules, output_dir)
    if target in ("claude", "all"):
        results["claude"] = export_claude(agents, skills, rules, output_dir)
    if target in ("openai", "all"):
        results["openai"] = export_openai(agents, skills, rules, output_dir)
    if target in ("plugin", "all"):
        results["plugin"] = export_antigravity_plugin(kit_dir, agents, skills, rules, workflows, kit_path, output_dir)

    if sync_dir:
        starget = Path(sync_dir)
        starget.mkdir(parents=True, exist_ok=True)
        if "cursor" in results:
            csrc = Path(output_dir) / "cursor" / ".cursorrules"
            cdst = starget / ".cursorrules"
            cdst.write_text(csrc.read_text("utf-8"), encoding="utf-8")
            print(f"[+] Synced Cursor rules to: {cdst}")
        if "claude" in results:
            cld_dir = starget / ".claude"
            cld_dir.mkdir(parents=True, exist_ok=True)
            csrc = Path(output_dir) / "claude" / "claude_instructions.txt"
            cdst = cld_dir / "instructions.txt"
            cdst.write_text(csrc.read_text("utf-8"), encoding="utf-8")
            print(f"[+] Synced Claude instructions to: {cdst}")
        if "openai" in results:
            gpt_dir = starget / ".gpts"
            gpt_dir.mkdir(parents=True, exist_ok=True)
            gsrc = Path(output_dir) / "openai" / "gpt_instructions.txt"
            gdst = gpt_dir / "instructions.txt"
            gdst.write_text(gsrc.read_text("utf-8"), encoding="utf-8")
            print(f"[+] Synced Custom GPT instructions to: {gdst}")

    return results

def main():
    parser = argparse.ArgumentParser(description="Agent Kit Multi-Platform Bundle Exporter")
    parser.add_argument("kit_dir", nargs="?", default=".", help="Path to source Agent Kit directory")
    parser.add_argument("output_dir", nargs="?", default="dist/export", help="Output directory for exported bundles")
    parser.add_argument("--target", choices=["cursor", "claude", "openai", "plugin", "all"], default="all", help="Target platform bundle")
    parser.add_argument("--sync", default=None, help="Target workspace path to directly sync bundle files to")

    args = parser.parse_args()
    export_kit(args.kit_dir, args.output_dir, args.target, sync_dir=args.sync)

if __name__ == "__main__":
    main()
