// Reference: references/antigravity-hooks-contract.md
import fs from 'node:fs';

function respond(decision, reason) {
  process.stdout.write(JSON.stringify({ decision, reason }));
  process.exit(0);
}

function normalizePath(p) {
  return p.replace(/\\/g, '/').toLowerCase();
}

function isInsideWorkspace(target, wsList) {
  const normTarget = normalizePath(target);
  for (const ws of wsList) {
    let normWs = normalizePath(ws);
    if (!normWs.endsWith('/')) {
      normWs += '/';
    }
    if (normTarget.startsWith(normWs)) {
      return true;
    }
  }
  return false;
}

function isProtectedPath(target, wsList) {
  const normTarget = normalizePath(target);
  for (const ws of wsList) {
    let normWs = normalizePath(ws);
    if (normWs.endsWith('/')) {
      normWs = normWs.slice(0, -1);
    }
    const protectedPaths = [
      normWs + '/.agents/hooks.json',
      normWs + '/.agents/hooks/',
      normWs + '/.git/',
    ];
    for (const prot of protectedPaths) {
      if (prot.endsWith('/')) {
        if (normTarget.startsWith(prot)) return true;
      } else {
        if (normTarget === prot) return true;
      }
    }
  }
  return false;
}

function checkCommandLine(cmdLine) {
  if (typeof cmdLine !== 'string') return null;
  const line = cmdLine.trim();

  // Pattern 1: rm -rf / or rm -fr ~ or rm -rf *
  // Matches rm with flags including -r and -f targeting /, ~, *, or /* or ~/*
  const rmDestructive = /\brm\s+-[a-zA-Z]*[rf][a-zA-Z]*\s+(?:\/|~|\*|\/\*|~\/)(?:\s|$)/i;
  if (rmDestructive.test(line)) {
    return 'Destructive rm targeting root, home, or wildcard';
  }

  // Pattern 2: mkfs (e.g. mkfs.ext4 /dev/sda1)
  const mkfsPattern = /\bmkfs(?:\.[a-zA-Z0-9]+)?\b/i;
  if (mkfsPattern.test(line)) {
    return 'mkfs filesystem formatting command';
  }

  // Pattern 3: dd ... of=/dev/...
  const ddPattern = /\bdd\b.*?\bof=\/dev\//i;
  if (ddPattern.test(line)) {
    return 'dd write command to device node';
  }

  // Pattern 4: format <drive>: (e.g. format C:)
  const formatPattern = /\bformat\s+[a-zA-Z]:/i;
  if (formatPattern.test(line)) {
    return 'format drive command';
  }

  return null;
}

try {
  let raw = '';
  try {
    raw = fs.readFileSync(0, 'utf-8');
  } catch (err) {
    respond('deny', `fail-closed: cannot read stdin: ${err.message}`);
  }

  if (!raw || !raw.trim()) {
    respond('deny', 'fail-closed: empty stdin payload');
  }

  let payload;
  try {
    payload = JSON.parse(raw);
  } catch (err) {
    respond('deny', `fail-closed: malformed JSON: ${err.message}`);
  }

  if (!payload || typeof payload !== 'object' || !payload.toolCall || typeof payload.toolCall.name !== 'string') {
    respond('deny', 'fail-closed: missing toolCall or toolCall.name');
  }

  const { name, args } = payload.toolCall;
  const toolArgs = args || {};
  const workspacePaths = Array.isArray(payload.workspacePaths) ? payload.workspacePaths : [];

  if (name === 'run_command') {
    const danger = checkCommandLine(toolArgs.CommandLine);
    if (danger) {
      respond('deny', `Forbidden command pattern: ${danger}`);
    }
    respond('allow', 'Command allowed');
  }

  const writeTools = new Set(['write_to_file', 'replace_file_content', 'multi_replace_file_content']);
  if (writeTools.has(name)) {
    const targetFile = toolArgs.TargetFile;
    if (typeof targetFile !== 'string') {
      respond('deny', 'fail-closed: write tool missing TargetFile argument');
    }

    if (workspacePaths.length > 0 && !isInsideWorkspace(targetFile, workspacePaths)) {
      respond('deny', 'TargetFile is outside allowed workspace paths');
    }

    if (isProtectedPath(targetFile, workspacePaths)) {
      respond('deny', 'TargetFile targets protected system or hook path');
    }

    respond('allow', 'File write target allowed');
  }

  // Any other tool allowed
  respond('allow', `Tool ${name} allowed by default`);
} catch (err) {
  respond('deny', `fail-closed: unhandled error in hook: ${err.message}`);
}
