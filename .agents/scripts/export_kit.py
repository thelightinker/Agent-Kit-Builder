#!/usr/bin/env python3
"""
Agent Kit Multi-Platform Bundle Exporter
Compiles an Agent Kit into native bundles for Cursor (.cursorrules),
Claude Desktop / Anthropic Projects (claude_instructions.txt + tools.json),
and OpenAI Custom GPTs (gpt_instructions.txt).
"""

import sys
import os
import json
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

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
    agents = {}
    skills = {}
    rules = {}

    # Read Agents
    agent_dir = kit_path / "agent"
    if agent_dir.exists():
        for f in agent_dir.glob("*.md"):
            data, body = parse_frontmatter(f.read_text("utf-8"))
            agents[f.stem] = {"meta": data, "body": body}

    # Read Skills
    skills_dir = kit_path / "skills"
    if skills_dir.exists():
        for sdir in skills_dir.iterdir():
            if sdir.is_dir():
                sfile = sdir / "SKILL.md"
                if sfile.exists():
                    data, body = parse_frontmatter(sfile.read_text("utf-8"))
                    skills[sdir.name] = {"meta": data, "body": body}

    # Read Rules
    rules_dir = kit_path / "rules"
    if rules_dir.exists():
        for f in rules_dir.glob("*.md"):
            data, body = parse_frontmatter(f.read_text("utf-8"))
            rules[f.stem] = {"meta": data, "body": body}

    return agents, skills, rules

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

    # Generate tools manifest schema
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
    # Truncate if exceeds GPT limit
    if len(out_text) > 7800:
        out_text = out_text[:7800] + "\n\n[Truncated to fit Custom GPT 8000 character instruction limit]"

    out_inst.write_text(out_text, encoding="utf-8")
    print(f"[+] OpenAI Custom GPT bundle written to: {out_inst}")
    return str(out_inst)

def export_kit(kit_dir, output_dir, target="all", sync_dir=None):
    agents, skills, rules = collect_kit_components(kit_dir)
    print(f"[*] Collected {len(agents)} agents, {len(skills)} skills, {len(rules)} rules from {kit_dir}")

    results = {}
    if target in ("cursor", "all"):
        results["cursor"] = export_cursor(agents, skills, rules, output_dir)
    if target in ("claude", "all"):
        results["claude"] = export_claude(agents, skills, rules, output_dir)
    if target in ("openai", "all"):
        results["openai"] = export_openai(agents, skills, rules, output_dir)

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
    parser.add_argument("--kit-dir", default=".", help="Path to source Agent Kit directory")
    parser.add_argument("--output-dir", default="dist/export", help="Output directory for exported bundles")
    parser.add_argument("--target", choices=["cursor", "claude", "openai", "all"], default="all", help="Target platform bundle")
    parser.add_argument("--sync", default=None, help="Target workspace path to directly sync bundle files to")

    args = parser.parse_args()
    export_kit(args.kit_dir, args.output_dir, args.target, sync_dir=args.sync)

if __name__ == "__main__":
    main()
