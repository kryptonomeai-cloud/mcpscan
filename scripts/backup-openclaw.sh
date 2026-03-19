#!/bin/bash
# ==============================================================
# OpenClaw Full Backup Script
# Creates a portable backup of the entire agent state
# Can be restored on any machine with Node.js + OpenClaw
# ==============================================================
set -euo pipefail

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_NAME="openclaw-backup-${TIMESTAMP}"
BACKUP_DIR="/tmp/${BACKUP_NAME}"
OPENCLAW_DIR="${HOME}/.openclaw"

# Destination (default: GPU server)
REMOTE_HOST="${1:-gpu}"
REMOTE_PATH="${2:-/home/kryptonome/openclaw-backups}"

echo "🔋 OpenClaw Full Backup — ${TIMESTAMP}"
echo "================================================"

# ---- 1. Create backup structure ----
echo "📁 Creating backup structure..."
mkdir -p "${BACKUP_DIR}"/{config,workspace,agents,memory,cron,identity,credentials,media,logs,agent-workspaces}

# ---- 2. Core config (essential — this IS the agent) ----
echo "⚙️  Backing up config..."
cp "${OPENCLAW_DIR}/openclaw.json" "${BACKUP_DIR}/config/"
# Auth profiles (API keys, OAuth tokens)
cp -r "${OPENCLAW_DIR}/agents/main/agent/" "${BACKUP_DIR}/config/main-agent/" 2>/dev/null || true

# ---- 3. Workspace (soul, memory, projects, skills, docs) ----
echo "🧠 Backing up workspace (excluding node_modules)..."
rsync -a \
  --exclude='node_modules' \
  --exclude='.next' \
  --exclude='.expo' \
  --exclude='__pycache__' \
  --exclude='.git/objects' \
  --exclude='*.pyc' \
  --exclude='.turbo' \
  --exclude='.vercel' \
  "${OPENCLAW_DIR}/workspace/" "${BACKUP_DIR}/workspace/"

# ---- 4. Agent state (session logs, fleet workspaces) ----
echo "📋 Backing up agent state..."
rsync -a "${OPENCLAW_DIR}/agents/" "${BACKUP_DIR}/agents/"
for ws in workspace-forge workspace-scout workspace-taskmaster workspace-venture workspace-sentinel; do
  if [ -d "${OPENCLAW_DIR}/${ws}" ]; then
    cp -r "${OPENCLAW_DIR}/${ws}" "${BACKUP_DIR}/agent-workspaces/"
  fi
done

# ---- 5. Memory (semantic memory store) ----
echo "🗄️  Backing up memory store..."
rsync -a "${OPENCLAW_DIR}/memory/" "${BACKUP_DIR}/memory/" 2>/dev/null || true

# ---- 6. Cron jobs ----
echo "⏰ Backing up cron jobs..."
rsync -a "${OPENCLAW_DIR}/cron/" "${BACKUP_DIR}/cron/" 2>/dev/null || true

# ---- 7. Identity + credentials ----
echo "🔐 Backing up identity..."
rsync -a "${OPENCLAW_DIR}/identity/" "${BACKUP_DIR}/identity/" 2>/dev/null || true
rsync -a "${OPENCLAW_DIR}/credentials/" "${BACKUP_DIR}/credentials/" 2>/dev/null || true

# ---- 8. Telegram state ----
echo "💬 Backing up channel state..."
rsync -a "${OPENCLAW_DIR}/telegram/" "${BACKUP_DIR}/telegram/" 2>/dev/null || true
rsync -a "${OPENCLAW_DIR}/shared/" "${BACKUP_DIR}/shared/" 2>/dev/null || true

# ---- 9. Media ----
echo "🖼️  Backing up media..."
rsync -a "${OPENCLAW_DIR}/media/" "${BACKUP_DIR}/media/" 2>/dev/null || true

# ---- 10. Subagent + delivery state ----
echo "🤖 Backing up runtime state..."
rsync -a "${OPENCLAW_DIR}/subagents/" "${BACKUP_DIR}/subagents/" 2>/dev/null || true
rsync -a "${OPENCLAW_DIR}/delivery-queue/" "${BACKUP_DIR}/delivery-queue/" 2>/dev/null || true
rsync -a "${OPENCLAW_DIR}/completions/" "${BACKUP_DIR}/completions/" 2>/dev/null || true

# ---- 11. External configs that matter ----
echo "🔧 Backing up external configs..."
mkdir -p "${BACKUP_DIR}/external-config"
cp -r "${HOME}/.config/gws/" "${BACKUP_DIR}/external-config/gws/" 2>/dev/null || true
# Don't backup browser profile (too large)

# ---- 12. Generate manifest ----
echo "📜 Generating manifest..."
cat > "${BACKUP_DIR}/MANIFEST.md" << 'MANIFEST'
# OpenClaw Backup Manifest

## What's Included
- **config/**: openclaw.json + agent auth profiles
- **workspace/**: SOUL.md, MEMORY.md, USER.md, projects, skills, docs, memory/
- **agents/**: Session logs, agent configs (main, forge, scout, taskmaster, etc.)
- **agent-workspaces/**: Fleet agent workspaces
- **memory/**: Semantic memory store
- **cron/**: All cron job definitions + state
- **identity/**: Agent identity
- **credentials/**: Stored credentials
- **telegram/**: Channel state
- **media/**: Cached media files
- **external-config/**: gws OAuth credentials

## What's NOT Included
- node_modules (reinstall with `npm install` per project)
- .git objects (repos can be re-cloned from GitHub)
- Browser profile (~800MB, not portable)
- OpenClaw binary (install via `npm install -g openclaw`)

## Restore Steps
1. Install OpenClaw: `npm install -g openclaw`
2. Copy backup to `~/.openclaw/`: `rsync -a backup/ ~/.openclaw/`
3. Reinstall workspace skills: `cd ~/.openclaw/workspace/skills && ...`
4. Reinstall project deps: `cd project && npm install`
5. Update openclaw.json paths if different machine
6. Start: `openclaw gateway start`
MANIFEST

echo "BACKUP_DATE=${TIMESTAMP}" > "${BACKUP_DIR}/backup-info.txt"
echo "SOURCE_HOST=$(hostname)" >> "${BACKUP_DIR}/backup-info.txt"
echo "OPENCLAW_VERSION=$(cat /opt/homebrew/lib/node_modules/openclaw/package.json | grep '"version"' | head -1)" >> "${BACKUP_DIR}/backup-info.txt"

# ---- 13. Compress ----
echo "📦 Compressing..."
cd /tmp
tar czf "${BACKUP_NAME}.tar.gz" "${BACKUP_NAME}/"
BACKUP_SIZE=$(du -sh "/tmp/${BACKUP_NAME}.tar.gz" | cut -f1)
echo "   Archive: /tmp/${BACKUP_NAME}.tar.gz (${BACKUP_SIZE})"

# ---- 14. Transfer to remote ----
if [ "${REMOTE_HOST}" != "local" ]; then
  echo "🚀 Transferring to ${REMOTE_HOST}:${REMOTE_PATH}..."
  ssh "${REMOTE_HOST}" "mkdir -p ${REMOTE_PATH}"
  rsync -avP "/tmp/${BACKUP_NAME}.tar.gz" "${REMOTE_HOST}:${REMOTE_PATH}/"
  echo "✅ Backup transferred to ${REMOTE_HOST}:${REMOTE_PATH}/${BACKUP_NAME}.tar.gz"
else
  echo "✅ Local backup at /tmp/${BACKUP_NAME}.tar.gz"
fi

# ---- 15. Cleanup temp ----
rm -rf "${BACKUP_DIR}"

echo ""
echo "================================================"
echo "✅ Backup complete: ${BACKUP_NAME}.tar.gz (${BACKUP_SIZE})"
echo "================================================"
