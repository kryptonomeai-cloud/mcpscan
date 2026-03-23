#!/bin/bash
# Daily crypto price history logger
set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
LOG_FILE="${WORKSPACE}/memory/crypto-history.csv"
DATE=$(date -u +"%Y-%m-%d")

# Create header if file doesn't exist
if [ ! -f "$LOG_FILE" ]; then
  echo "date,btc_usd,eth_usd,sol_usd,sys_usd,btc_24h,eth_24h,sol_24h,sys_24h" > "$LOG_FILE"
fi

DATA=$(curl -sf --max-time 15 "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,syscoin&vs_currencies=usd&include_24hr_change=true" 2>/dev/null)

if [ -z "$DATA" ]; then
  echo "Failed to fetch crypto prices"
  exit 1
fi

ROW=$(echo "$DATA" | python3 -c "
import sys, json
d = json.load(sys.stdin)
btc = d.get('bitcoin', {})
eth = d.get('ethereum', {})
sol = d.get('solana', {})
sys_c = d.get('syscoin', {})
print(f'${DATE},{btc.get(\"usd\",0)},{eth.get(\"usd\",0)},{sol.get(\"usd\",0)},{sys_c.get(\"usd\",0)},{btc.get(\"usd_24h_change\",0):.2f},{eth.get(\"usd_24h_change\",0):.2f},{sol.get(\"usd_24h_change\",0):.2f},{sys_c.get(\"usd_24h_change\",0):.2f}')
")

echo "$ROW" >> "$LOG_FILE"
echo "Logged crypto prices for $DATE"
