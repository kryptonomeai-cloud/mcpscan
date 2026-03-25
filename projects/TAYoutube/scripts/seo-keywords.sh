#!/bin/bash
# seo-keywords.sh — Research keywords for a video topic
# Usage: ./seo-keywords.sh "your video topic"
# Uses YouTube search suggest API to find related searches

set -euo pipefail

if [ -z "${1:-}" ]; then
    echo "Usage: $0 \"your video topic\""
    echo "Example: $0 \"self hosting AI locally\""
    exit 1
fi

TOPIC="$1"
ENCODED_TOPIC=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$TOPIC'))")

echo "🔍 Keyword Research: \"${TOPIC}\""
echo "================================="
echo ""

# YouTube Search Suggest
echo "## YouTube Autocomplete Suggestions"
echo ""
SUGGEST=$(curl -sf "https://suggestqueries-clients6.youtube.com/complete/search?client=youtube&ds=yt&q=${ENCODED_TOPIC}" 2>/dev/null || echo "")

if [ -n "$SUGGEST" ]; then
    echo "$SUGGEST" | python3 -c "
import sys, json
data = sys.stdin.read()
# YouTube returns JSONP-like format
try:
    # Try to extract the JSON array
    start = data.index('[')
    json_data = json.loads(data[start:])
    suggestions = json_data[1] if len(json_data) > 1 else []
    for s in suggestions[:15]:
        keyword = s[0] if isinstance(s, list) else s
        print(f'  - {keyword}')
except:
    print('  (Could not parse suggestions)')
" 2>/dev/null || echo "  (Failed to fetch YouTube suggestions)"
else
    echo "  (Failed to fetch YouTube suggestions)"
fi
echo ""

# Google Search Suggest (related queries)
echo "## Google Autocomplete"
echo ""
GOOGLE=$(curl -sf "https://suggestqueries.google.com/complete/search?client=firefox&q=${ENCODED_TOPIC}" 2>/dev/null || echo "")
if [ -n "$GOOGLE" ]; then
    echo "$GOOGLE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for s in data[1][:10]:
    print(f'  - {s}')
" 2>/dev/null || echo "  (Could not parse)"
fi
echo ""

# Variations for title testing
echo "## Title Variations"
echo ""
echo "  - \"I ${TOPIC} (and here's what happened)\""
echo "  - \"How to ${TOPIC} — Complete Guide\""
echo "  - \"${TOPIC} in 2026 — Everything Changed\""
echo "  - \"Why ${TOPIC} is a Game Changer\""
echo "  - \"${TOPIC} — The REAL Truth\""
echo ""

# Long-tail variations
echo "## Long-Tail Ideas (add these words)"
echo ""
for SUFFIX in "tutorial" "for beginners" "in 2026" "step by step" "vs" "best" "free" "at home" "on Linux" "with Docker"; do
    echo "  - \"${TOPIC} ${SUFFIX}\""
done
echo ""
echo "💡 Tip: Use the YouTube suggestion with the highest search volume as your primary keyword in the title."
