from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path

HOOK = Path(__file__).resolve().parents[2] / "templates" / "validate-tool-call.mjs"
WS = "/work/proj"


def run_hook(payload):
    raw = payload if isinstance(payload, str) else json.dumps(payload)
    p = subprocess.run(["node", str(HOOK)], input=raw, capture_output=True, text=True, timeout=10)
    return p.returncode, json.loads(p.stdout)


def cmd(line):
    return {"toolCall": {"name": "run_command", "args": {"CommandLine": line, "Cwd": WS}}, "workspacePaths": [WS]}


def write(path, tool="write_to_file", ws=WS):
    return {"toolCall": {"name": tool, "args": {"TargetFile": path}}, "workspacePaths": [ws]}


@unittest.skipUnless(shutil.which("node"), "node required")
class TestHook(unittest.TestCase):
    def test_denies_rm_rf_root(self):
        self.assertEqual(run_hook(cmd("rm -rf /"))[1]["decision"], "deny")

    def test_denies_rm_fr_home(self):
        self.assertEqual(run_hook(cmd("rm -fr ~"))[1]["decision"], "deny")

    def test_denies_mkfs(self):
        self.assertEqual(run_hook(cmd("mkfs.ext4 /dev/sda1"))[1]["decision"], "deny")

    def test_denies_format_drive(self):
        self.assertEqual(run_hook(cmd("format C:"))[1]["decision"], "deny")

    def test_allows_ordinary_commands(self):
        for c in ("ls -la", "npm test", "rm -rf build/"):
            self.assertEqual(run_hook(cmd(c))[1]["decision"], "allow", c)

    def test_allows_write_inside_workspace(self):
        self.assertEqual(run_hook(write(WS + "/docs/a.md"))[1]["decision"], "allow")

    def test_denies_write_outside_workspace(self):
        self.assertEqual(run_hook(write("/etc/passwd"))[1]["decision"], "deny")

    def test_denies_edit_of_hook_files_for_all_write_tools(self):
        for t in ("write_to_file", "replace_file_content", "multi_replace_file_content"):
            self.assertEqual(run_hook(write(WS + "/.agents/hooks.json", t))[1]["decision"], "deny", t)
            self.assertEqual(run_hook(write(WS + "/.agents/hooks/validate-tool-call.mjs", t))[1]["decision"], "deny", t)

    def test_windows_path_outside_workspace_denied(self):
        self.assertEqual(run_hook(write("C:\\Windows\\System32\\x.dll", ws="C:\\work\\proj"))[1]["decision"], "deny")

    def test_windows_path_inside_workspace_case_insensitive(self):
        self.assertEqual(run_hook(write("c:\\WORK\\proj\\notes.md", ws="C:\\work\\proj"))[1]["decision"], "allow")

    def test_fail_closed_on_empty_stdin(self):
        rc, out = run_hook("")
        self.assertEqual((rc, out["decision"]), (0, "deny"))
        self.assertTrue(out["reason"].startswith("fail-closed:"))

    def test_fail_closed_on_malformed_json(self):
        self.assertEqual(run_hook("{not json")[1]["decision"], "deny")

    def test_unknown_tool_allowed(self):
        self.assertEqual(
            run_hook(
                {
                    "toolCall": {"name": "view_file", "args": {"AbsolutePath": "/etc/passwd"}},
                    "workspacePaths": [WS],
                }
            )[1]["decision"],
            "allow",
        )


if __name__ == "__main__":
    unittest.main()
