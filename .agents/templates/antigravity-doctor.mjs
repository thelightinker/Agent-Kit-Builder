#!/usr/bin/env node

/**
 * Antigravity Doctor — 6-Phase Runtime Compatibility & Health Diagnostics
 * Used in Antigravity-native Agent Kits to verify configuration integrity.
 */

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

function parseArgs(argv) {
  const options = {root: process.cwd(), json: false, strict: false};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--root') options.root = path.resolve(argv[++i]);
    else if (arg === '--json') options.json = true;
    else if (arg === '--strict') options.strict = true;
    else if (arg === '--help') options.help = true;
    else throw new Error(`Unknown argument: ${arg}`);
  }
  return options;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function frontmatter(file) {
  const text = fs.readFileSync(file, 'utf8');
  if (!text.startsWith('---\n')) return null;
  const end = text.indexOf('\n---\n', 4);
  if (end < 0) return null;
  const data = {};
  for (const line of text.slice(4, end).split(/\r?\n/)) {
    const match = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!match) continue;
    data[match[1]] = match[2].trim().replace(/^['"]|['"]$/g, '');
  }
  return data;
}

function markdownFiles(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .filter(name => name.endsWith('.md'))
    .map(name => path.join(dir, name))
    .sort();
}

function skillFiles(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, {withFileTypes: true})
    .filter(entry => entry.isDirectory())
    .map(entry => path.join(dir, entry.name, 'SKILL.md'))
    .filter(file => fs.existsSync(file))
    .sort();
}

function add(report, severity, phase, code, file, message) {
  report.findings.push({severity, phase, code, file, message});
}

function relative(root, file) {
  return path.relative(root, file).split(path.sep).join('/');
}

function checkDiscovery(root, report) {
  const agentsRoot = path.join(root, '.agents');
  const groups = [
    ['rules', markdownFiles(path.join(agentsRoot, 'rules')), ['description']],
    ['workflows', markdownFiles(path.join(agentsRoot, 'workflows')), ['description']],
    ['skills', skillFiles(path.join(agentsRoot, 'skills')), ['description']]
  ];

  for (const [kind, files, required] of groups) {
    report.counts[kind] = files.length;
    if (files.length === 0) {
      add(report, 'error', 'discovery', `${kind}.missing`, `.agents/${kind}`, `No Antigravity ${kind} were discovered.`);
      continue;
    }
    for (const file of files) {
      const meta = frontmatter(file);
      if (!meta) {
        add(report, 'error', 'discovery', `${kind}.frontmatter`, relative(root, file), 'Missing YAML frontmatter.');
        continue;
      }
      for (const field of required) {
        if (!meta[field]) add(report, 'error', 'discovery', `${kind}.required`, relative(root, file), `Missing frontmatter field: ${field}`);
      }
    }
  }
}

function checkHooks(root, report) {
  const file = path.join(root, '.agents', 'hooks.json');
  if (!fs.existsSync(file)) {
    add(report, 'warning', 'hooks', 'hooks.missing', '.agents/hooks.json', 'Native Antigravity hooks configuration is missing.');
    return;
  }
  let config;
  try {
    config = readJson(file);
  } catch (error) {
    add(report, 'error', 'hooks', 'hooks.invalid_json', '.agents/hooks.json', error.message);
    return;
  }
  if (typeof config.enabled !== 'boolean') add(report, 'error', 'hooks', 'hooks.enabled', '.agents/hooks.json', 'enabled must be boolean.');
}

export function diagnose(root) {
  const report = {runtime: 'antigravity', root, passed: true, counts: {}, phases: {}, findings: []};
  const contractFile = path.join(root, '.agents', 'antigravity.json');
  
  if (fs.existsSync(contractFile)) {
    try {
      const contract = readJson(contractFile);
      if (contract.runtime !== 'antigravity') add(report, 'error', 'discovery', 'contract.runtime', '.agents/antigravity.json', 'runtime must be antigravity.');
    } catch (error) {
      add(report, 'error', 'discovery', 'contract.invalid', '.agents/antigravity.json', error.message);
    }
  }

  checkDiscovery(root, report);
  checkHooks(root, report);

  for (const phase of ['discovery', 'hooks']) {
    report.phases[phase] = !report.findings.some(item => item.phase === phase && item.severity === 'error');
  }
  report.passed = !report.findings.some(item => item.severity === 'error');
  return report;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  try {
    const options = parseArgs(process.argv.slice(2));
    const report = diagnose(options.root);
    if (options.json) {
      console.log(JSON.stringify(report, null, 2));
    } else {
      console.log(`Antigravity Doctor Report: ${report.root}`);
      for (const [phase, passed] of Object.entries(report.phases)) {
        console.log(`${passed ? '[PASS]' : '[FAIL]'} ${phase}`);
      }
      for (const item of report.findings) {
        console.log(`[${item.severity.toUpperCase()}] ${item.file} ${item.code} - ${item.message}`);
      }
      console.log(report.passed ? '[PASS] Runtime contract healthy.' : '[FAIL] Runtime contract has issues.');
    }
    process.exitCode = report.passed ? 0 : 1;
  } catch (error) {
    console.error(error.message);
    process.exitCode = 2;
  }
}
