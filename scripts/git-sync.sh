#!/bin/bash
# Auto-sync workspace to GitHub
set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
cd "$WORKSPACE"

if [ ! -d ".git" ]; then
  echo "Not a git repo, skipping sync"
  exit 0
fi

# Check for changes
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
  echo "No changes to sync"
  exit 0
fi

# Stage all changes
git add -A

# Commit
DATE=$(date +"%Y-%m-%d %H:%M")
git commit -m "chore: auto-sync workspace $DATE" --no-verify 2>/dev/null || {
  echo "Nothing to commit"
  exit 0
}

# Push
git push origin main 2>&1 || {
  echo "Push failed — may need auth or remote setup"
  exit 1
}

echo "Workspace synced at $DATE"
