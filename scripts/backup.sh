#!/bin/bash
# MiniClaw Daily Backup Script
# Backs up OpenClaw config, workspace, docker configs, services, and system state
# to iCloud Drive for off-machine redundancy.

set -euo pipefail

BACKUP_BASE=~/Library/Mobile\ Documents/com~apple~CloudDocs/MiniClaw-Backup
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="$BACKUP_BASE/backup-$TIMESTAMP"
WORKSPACE=~/.openclaw/workspace

echo "=== MiniClaw Backup: $TIMESTAMP ==="

# Create backup directory
mkdir -p "$BACKUP_DIR"/{docker,gpu-server,services,workspace}

# 1. Generate manifest (full file listing of workspace)
echo "Generating manifest..."
find "$BACKUP_DIR" -type f > "$BACKUP_DIR/MANIFEST.txt" 2>/dev/null || true

# 2. Brew packages
echo "Capturing brew state..."
brew list --formula 2>/dev/null > "$BACKUP_DIR/brew-packages.txt" || echo "brew list failed"
brew list --cask 2>/dev/null > "$BACKUP_DIR/brew-casks.txt" || echo "brew cask list failed"

# 3. OpenClaw config
echo "Backing up OpenClaw config..."
cp ~/.openclaw/openclaw.json "$BACKUP_DIR/openclaw.json" 2>/dev/null || true

# 4. Exec approvals
cp ~/.openclaw/exec-approvals.json "$BACKUP_DIR/exec-approvals.json" 2>/dev/null || true

# 5. Cron jobs (export via openclaw if available, otherwise copy state)
if command -v openclaw &>/dev/null; then
    openclaw cron list --json 2>/dev/null > "$BACKUP_DIR/cron-jobs.json" || echo "{}" > "$BACKUP_DIR/cron-jobs.json"
else
    echo "{}" > "$BACKUP_DIR/cron-jobs.json"
fi

# 6. Docker compose files and configs
echo "Backing up Docker configs..."
for d in ~/docker/*/; do
    [ -d "$d" ] || continue
    name=$(basename "$d")
    for f in docker-compose.yml docker-compose.yaml .env; do
        [ -f "$d/$f" ] && cp "$d/$f" "$BACKUP_DIR/docker/${name}-${f}" 2>/dev/null || true
    done
done
# Also grab any compose files from common locations
for f in /opt/docker/*/docker-compose.yml; do
    [ -f "$f" ] && cp "$f" "$BACKUP_DIR/docker/$(basename $(dirname $f))-docker-compose.yml" 2>/dev/null || true
done
# Specific known configs
for cfg in searxng-settings.yml paperless-ngx-watch-inbox.sh paperless-ngx-ftp-server.py; do
    find ~/docker -name "$cfg" -exec cp {} "$BACKUP_DIR/docker/$cfg" \; 2>/dev/null || true
done

# 7. GPU server services (if reachable)
echo "Checking GPU server..."
timeout 5 ssh -o ConnectTimeout=3 gpu "systemctl list-units --type=service --state=running --no-pager 2>/dev/null" > "$BACKUP_DIR/gpu-server/services.txt" 2>/dev/null || echo "GPU server unreachable" > "$BACKUP_DIR/gpu-server/services.txt"

# 8. LaunchAgent plists
echo "Backing up LaunchAgents..."
cp ~/Library/LaunchAgents/*.plist "$BACKUP_DIR/services/" 2>/dev/null || true

# 9. Workspace (the big one)
echo "Backing up workspace..."
rsync -a --exclude='.git' \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='.venv' \
    --exclude='*.pyc' \
    --exclude='sessions/' \
    --exclude='data/doc-rag/*.db' \
    "$WORKSPACE/" "$BACKUP_DIR/workspace/" 2>/dev/null || true

# 10. Regenerate manifest with all files
find "$BACKUP_DIR" -type f > "$BACKUP_DIR/MANIFEST.txt" 2>/dev/null || true

# 11. Update latest symlink
ln -sfn "$BACKUP_DIR" "$BACKUP_BASE/latest"

# Stats
FILE_COUNT=$(find "$BACKUP_DIR" -type f | wc -l | tr -d ' ')
BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)

echo ""
echo "=== Backup Complete ==="
echo "Location: $BACKUP_DIR"
echo "Files: $FILE_COUNT"
echo "Size: $BACKUP_SIZE"
echo "Timestamp: $TIMESTAMP"
