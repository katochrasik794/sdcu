#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

// Locate python entrypoint relative to CLI
const repoRoot = path.resolve(__dirname, '../../..');
const pythonScript = path.join(repoRoot, 'packages/core/sdcu_core/cli.py');

const args = process.argv.slice(2);
const pythonProcess = spawn('python3', [pythonScript, ...args], {
  stdio: 'inherit',
  env: {
    ...process.env,
    PYTHONPATH: path.join(repoRoot, 'packages/core')
  }
});

pythonProcess.on('close', (code) => {
  process.exit(code || 0);
});

