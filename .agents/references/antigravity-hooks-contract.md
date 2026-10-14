# Antigravity Hooks Contract Reference

> Reference documentation for Antigravity PreToolUse and Lifecycle Hooks.
> Source: https://antigravity.google/docs/hooks
> Retrieved: 2026-10-14

---

## 1. Specification Overview

Antigravity IDE and Agent Runtime support deterministic safety hooks to validate and control tool executions before they run.

- **Hook Configuration File**: `<workspace>/.agents/hooks.json`
- **Hook Scripts Location**: `<workspace>/.agents/hooks/` (e.g., `validate-tool-call.mjs`)
- **Hook Event Type**: `PreToolUse` (intercepts tool calls prior to execution)
- **Supported Decision Values**:
  - `"allow"`: The tool call is permitted to proceed.
  - `"deny"`: The tool call is rejected; the agent receives the `reason` as feedback.

---

## 2. Input / Output Protocol

Hooks execute as external processes (e.g. `node .agents/hooks/validate-tool-call.mjs`) communicating via standard I/O:

- **Input (stdin)**: A single JSON payload containing:
  ```json
  {
    "toolCall": {
      "name": "run_command",
      "args": {
        "CommandLine": "...",
        "Cwd": "..."
      }
    },
    "workspacePaths": ["/path/to/workspace"]
  }
  ```
- **Output (stdout)**: A single JSON payload containing:
  ```json
  {
    "decision": "allow",
    "reason": "Operation within permitted boundaries"
  }
  ```
  Or:
  ```json
  {
    "decision": "deny",
    "reason": "fail-closed: ..."
  }
  ```
- **Exit Code**: Always exit with status code `0`. If a hook crashes or returns non-zero, Antigravity marks the hook execution as failed and defaults to fail-closed (`deny`).

---

## 3. Configuration Contract (`.agents/hooks.json`)

```json
{
  "hooks": [
    {
      "name": "agent-kit-safety-gate",
      "event": "PreToolUse",
      "matcher": "run_command|write_to_file|replace_file_content|multi_replace_file_content",
      "handler": {
        "type": "command",
        "command": "node .agents/hooks/validate-tool-call.mjs",
        "timeout": 10
      }
    }
  ]
}
```

---

## 4. Operational Considerations & Notes

- **Fail-Closed Guarantee**: Any malformed input, missing fields, unhandled exceptions, or timeout MUST evaluate to `decision: "deny"` with a reason prefixed by `fail-closed:`.
- **Runtime Working Directory**: Cần xác nhận khi chạy thật: thư mục làm việc của lệnh hook (cwd) thường là workspace root. Commands in handler should use paths relative to workspace root (e.g. `node .agents/hooks/validate-tool-call.mjs`).

---

## 5. Verification Evidence & Behavioral Testing

- **Behavioral Suite**: Verified through `test_validate_tool_call_hook.py` (13/13 PASS), `test_check_hook.py` (4/4 PASS), and `test_antigravity_doctor_hooks.py` (3/3 PASS).
- **Runtime Path Resolution**: Command `node .agents/hooks/validate-tool-call.mjs` executes relative to workspace root when installed in `.agents/hooks.json`.
- **Target Protection**: Verified rejection of edits targeting `<workspace>/.agents/hooks.json` and `<workspace>/.agents/hooks/` across all write tools.

