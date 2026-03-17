#!/bin/bash
# Setup autoresearch on GPU server (5x RTX 3090, 128GB RAM)
# Run this script on the GPU server after transferring the repo

set -e

REPO_DIR="$HOME/autoresearch"
GPU_SERVER="gpu"

echo "=== Transferring autoresearch to GPU server ==="
rsync -avz --exclude='.git' --exclude='node_modules' \
  /Users/miniclaw/.openclaw/workspace/projects/autoresearch/ \
  ${GPU_SERVER}:${REPO_DIR}/

echo "=== Setting up on GPU server ==="
ssh ${GPU_SERVER} << 'REMOTE'
set -e
cd ~/autoresearch

# Install uv if not present
if ! command -v uv &>/dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Install dependencies
echo "Installing Python dependencies..."
uv sync

# Prepare data (downloads training data + trains tokenizer)
echo "Preparing data (this takes ~2 minutes)..."
uv run prepare.py

echo ""
echo "=== Setup complete! ==="
echo "To start autoresearch, SSH into the GPU server and run:"
echo "  cd ~/autoresearch"
echo "  # Start a tmux session so it survives disconnects"
echo "  tmux new -s autoresearch"
echo "  # Then point Claude Code / Codex at program.md and let it go"
echo ""
echo "For a single 3090 (24GB VRAM), consider:"
echo "  - Reducing DEPTH from 8 to 4-6 in train.py"
echo "  - Reducing MAX_SEQ_LEN in prepare.py constants"
echo "  - Using WINDOW_PATTERN = 'L' instead of 'SSSL'"
echo "  - Lowering TOTAL_BATCH_SIZE to 2**14 or 2**15"
REMOTE

echo ""
echo "Done! Next steps:"
echo "1. Power on GPU server"
echo "2. Run: ssh gpu 'cd ~/autoresearch && tmux new -s autoresearch'"
echo "3. Point an AI agent at program.md and let it run overnight"
