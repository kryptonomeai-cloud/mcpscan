import { appendFileSync, existsSync, mkdirSync } from 'node:fs';

const DATA_DIR = new URL('../data/', import.meta.url).pathname;
const AUDIT_FILE = DATA_DIR + 'audit.jsonl';

function ensureDataDir() {
  if (!existsSync(DATA_DIR)) mkdirSync(DATA_DIR, { recursive: true });
}

export function logAudit(entry) {
  ensureDataDir();
  const record = {
    timestamp: new Date().toISOString(),
    ...entry,
  };
  appendFileSync(AUDIT_FILE, JSON.stringify(record) + '\n', 'utf8');
}
