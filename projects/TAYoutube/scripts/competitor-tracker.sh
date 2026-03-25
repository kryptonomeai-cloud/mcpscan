#!/bin/bash
# competitor-tracker.sh — Track competitor YouTube channels via RSS
# Usage: ./competitor-tracker.sh [output_dir]
# YouTube provides RSS feeds for any channel

set -euo pipefail

OUTPUT_DIR="${1:-$(dirname "$0")/../research}"
DATE=$(date +%Y-%m-%d)
OUTPUT_FILE="$OUTPUT_DIR/competitors-${DATE}.md"

mkdir -p "$OUTPUT_DIR"

echo "# Competitor Uploads — ${DATE}" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Channel IDs for competitors (YouTube RSS feeds)
# Format: "ChannelName|ChannelID"
declare -a CHANNELS=(
    "NetworkChuck|UC9x0AN7BWHpCDHSm9NiJFJQ"
    "Fireship|UCsBjURrPoezykLs9EqgamOA"
    "JeffGeerling|UCR-DXc1voovS8nhAvccRZhg"
    "TechnoTim|UCOk-gHyjcWZNj3Br4oxwh0A"
    "DavidBombal|UC0DRpaAg3CzUBRgnJKBPMYQ"
)

for ENTRY in "${CHANNELS[@]}"; do
    NAME="${ENTRY%%|*}"
    CHANNEL_ID="${ENTRY##*|}"
    
    echo "## ${NAME}" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    
    RSS_URL="https://www.youtube.com/feeds/videos.xml?channel_id=${CHANNEL_ID}"
    
    curl -sf "$RSS_URL" 2>/dev/null | python3 -c "
import sys, xml.etree.ElementTree as ET
data = sys.stdin.read()
try:
    root = ET.fromstring(data)
    ns = {'atom': 'http://www.w3.org/2005/Atom', 'yt': 'http://www.youtube.com/xml/schemas/2015', 'media': 'http://search.yahoo.com/mrss/'}
    entries = root.findall('atom:entry', ns)[:5]
    for entry in entries:
        title = entry.find('atom:title', ns).text
        link = entry.find('atom:link', ns).get('href')
        published = entry.find('atom:published', ns).text[:10]
        print(f'- [{published}] **{title}** — {link}')
except Exception as e:
    print(f'_Failed to parse feed: {e}_')
" >> "$OUTPUT_FILE" 2>/dev/null || echo "_Failed to fetch ${NAME} feed_" >> "$OUTPUT_FILE"
    
    echo "" >> "$OUTPUT_FILE"
done

echo "---" >> "$OUTPUT_FILE"
echo "_Tracked at $(date '+%Y-%m-%d %H:%M %Z')_" >> "$OUTPUT_FILE"

echo "✅ Competitor tracking complete → ${OUTPUT_FILE}"
