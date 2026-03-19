#!/bin/bash
# ==============================================================
# OpenClaw Restore Script
# Restores a full agent backup onto a new machine
# ==============================================================
set -euo pipefail

BACKUP_ARCHIVE="${1:?Usage: restore-openclaw.sh <backup.tar.gz>}"
OPENCLAW_DIR="${HOME}/.openclaw"

echo "🔋 OpenClaw Restore"
echo "================================================"
echo "Archive: ${BACKUP_ARCHIVE}"
echo "Target:  ${OPENCLAW_DIR}"
echo ""

# ---- Safety check ----
if [ -f "${OPENCLAW_DIR}/openclaw.json" ]; then
  echo "⚠️  Existing OpenClaw installation detected at ${OPENCLAW_DIR}"
  read -p "Overwrite? (y/N): " confirm
  if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "Aborted."
    exit 1
  fi
fi

# ---- 1. Check prerequisites ----
echo "🔍 Checking prerequisites..."
if ! command -v node &>/dev/null; then
  echo "❌ Node.js not found. Install it first:"
  echo "   curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -"
  echo "   sudo apt-get install -y nodejs"
  exit 1
fi
echo "   Node.js: $(node --version)"

if ! command -v openclaw &>/dev/null; then
  echo "📦 Installing OpenClaw..."
  npm install -g openclaw
fi
echo "   OpenClaw: $(openclaw --version 2>/dev/null || echo 'installed')"

# ---- 2. Extract backup ----
echo "📦 Extracting backup..."
TEMP_DIR=$(mktemp -d)
tar xzf "${BACKUP_ARCHIVE}" -C "${TEMP_DIR}"
BACKUP_DIR=$(ls "${TEMP_DIR}")

echo "📜 Backup info:"
cat "${TEMP_DIR}/${BACKUP_DIR}/backup-info.txt" 2>/dev/null || true
echo ""

# ---- 3. Restore ----
mkdir -p "${OPENCLAW_DIR}"

echo "⚙️  Restoring config..."
cp "${TEMP_DIR}/${BACKUP_DIR}/config/openclaw.json" "${OPENCLAW_DIR}/"
if [ -d "${TEMP_DIR}/${BACKUP_DIR}/config/main-agent" ]; then
  mkdir -p "${OPENCLAW_DIR}/agents/main/agent"
  rsync -a "${TEMP_DIR}/${BACKUP_DIR}/config/main-agent/" "${OPENCLAW_DIR}/agents/main/agent/"
fi

echo "🧠 Restoring workspace..."
rsync -a "${TEMP_DIR}/${BACKUP_DIR}/workspace/" "${OPENCLAW_DIR}/workspace/"

echo "📋 Restoring agent state..."
rsync -a "${TEMP_DIR}/${BACKUP_DIR}/agents/" "${OPENCLAW_DIR}/agents/"

echo "🗄️  Restoring memory..."
rsync -a "${TEMP_DIR}/${BACKUP_DIR}/memory/" "${OPENCLAW_DIR}/memory/" 2>/dev/null || true

echo "⏰ Restoring cron..."
rsync -a "${TEMP_DIR}/${BACKUP_DIR}/cron/" "${OPENCLAW_DIR}/cron/" 2>/dev/null || true

echo "🔐 Restoring identity + credentials..."
rsync -a "${TEMP_DIR}/${BACKUP_DIR}/identity/" "${OPENCLAW_DIR}/identity/" 2>/dev/null || true
rsync -a "${TEMP_DIR}/${BACKUP_DIR}/credentials/" "${OPENCLAW_DIR}/credentials/" 2>/dev/null || true

echo "💬 Restoring channel state..."
rsync -a "${TEMP_DIR}/${BACKUP_DIR}/telegram/" "${OPENCLAW_DIR}/telegram/" 2>/dev/null || true
rsync -a "${TEMP_DIR}/${BACKUP_DIR}/shared/" "${OPENCLAW_DIR}/shared/" 2>/dev/null || true

echo "🖼️  Restoring media..."
rsync -a "${TEMP_DIR}/${BACKUP_DIR}/media/" "${OPENCLAW_DIR}/media/" 2>/dev/null || true

echo "🤖 Restoring runtime state..."
rsync -a "${TEMP_DIR}/${BACKUP_DIR}/subagents/" "${OPENCLAW_DIR}/subagents/" 2>/dev/null || true
rsync -a "${TEMP_DIR}/${BACKUP_DIR}/delivery-queue/" "${OPENCLAW_DIR}/delivery-queue/" 2>/dev/null || true
rsync -a "${TEMP_DIR}/${BACKUP_DIR}/completions/" "${OPENCLAW_DIR}/completions/" 2>/dev/null || true

# Restore fleet workspaces
if [ -d "${TEMP_DIR}/${BACKUP_DIR}/agent-workspaces" ]; then
  echo "🤖 Restoring fleet workspaces..."
  for ws in "${TEMP_DIR}/${BACKUP_DIR}/agent-workspaces"/*/; do
    ws_name=$(basename "$ws")
    rsync -a "$ws" "${OPENCLAW_DIR}/${ws_name}/"
  done
fi

# External configs
if [ -d "${TEMP_DIR}/${BACKUP_DIR}/external-config/gws" ]; then
  echo "🔧 Restoring gws config..."
  mkdir -p "${HOME}/.config/gws"
  rsync -a "${TEMP_DIR}/${BACKUP_DIR}/external-config/gws/" "${HOME}/.config/gws/"
fi

# ---- 4. Fix permissions ----
echo "🔒 Setting permissions..."
chmod 700 "${OPENCLAW_DIR}"
chmod 600 "${OPENCLAW_DIR}/openclaw.json"
find "${OPENCLAW_DIR}/credentials" -type f -exec chmod 600 {} \; 2>/dev/null || true

# ---- 5. Cleanup ----
rm -rf "${TEMP_DIR}"

echo ""
echo "================================================"
echo "✅ Restore complete!"
echo ""
echo "Next steps:"
echo "  1. Review config:  cat ~/.openclaw/openclaw.json"
echo "  2. Update any machine-specific paths in openclaw.json"
echo "  3. Start gateway:  openclaw gateway start"
echo "  4. Reinstall project deps where needed:"
echo "     cd ~/.openclaw/workspace/projects/*/  && npm install"
echo "================================================"
