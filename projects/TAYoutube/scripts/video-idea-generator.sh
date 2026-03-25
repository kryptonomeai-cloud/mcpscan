#!/bin/bash
# video-idea-generator.sh — Generate video ideas from today's trends
# Usage: ./video-idea-generator.sh
# Reads latest trends file and appends ideas to video-ideas.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
RESEARCH_DIR="$PROJECT_DIR/research"
IDEAS_FILE="$RESEARCH_DIR/video-ideas.md"
DATE=$(date +%Y-%m-%d)

# Find latest trends file
LATEST_TRENDS=$(ls -t "$RESEARCH_DIR"/trends-*.md 2>/dev/null | head -1)

if [ -z "$LATEST_TRENDS" ]; then
    echo "❌ No trends file found. Run trend-scanner.sh first."
    exit 1
fi

# Initialize ideas file if it doesn't exist
if [ ! -f "$IDEAS_FILE" ]; then
    cat > "$IDEAS_FILE" << 'EOF'
# Video Ideas Backlog

_Score each idea: Timeliness (1-5) | Evergreen (1-5) | Uniqueness (1-5) | Effort (1=easy, 5=hard)_
_Best picks: High timeliness OR evergreen + high uniqueness + low effort_

## Ready to Film 🎬

## Ideas Pool 💡

## Filmed ✅

## Discarded ❌

EOF
fi

# Extract trending topics and format as potential video ideas
echo "" >> "$IDEAS_FILE"
echo "### Ideas from ${DATE} trends" >> "$IDEAS_FILE"
echo "" >> "$IDEAS_FILE"

# Pull HN titles that scored high
grep -E "^\- \*\*" "$LATEST_TRENDS" | head -20 | while IFS= read -r line; do
    TITLE=$(echo "$line" | sed 's/- \*\*\(.*\)\*\*.*/\1/')
    echo "- [ ] ${TITLE} — _from trends ${DATE}_" >> "$IDEAS_FILE"
done

echo "" >> "$IDEAS_FILE"
echo "✅ Ideas appended to ${IDEAS_FILE}"
echo "   Review and score the new ideas, move best to 'Ready to Film'"
