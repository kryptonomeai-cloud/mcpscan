#!/bin/bash
# Crypto price alert - fetches prices and alerts on significant moves (>5%)
set -euo pipefail

COINS="bitcoin,ethereum,solana,syscoin"
THRESHOLD=5

DATA=$(curl -sf --max-time 15 "https://api.coingecko.com/api/v3/simple/price?ids=${COINS}&vs_currencies=usd&include_24hr_change=true" 2>/dev/null)

if [ -z "$DATA" ]; then
  exit 0
fi

ALERTS=""
for coin in bitcoin ethereum solana syscoin; do
  CHANGE=$(echo "$DATA" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('$coin',{}).get('usd_24h_change',0))" 2>/dev/null)
  PRICE=$(echo "$DATA" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('$coin',{}).get('usd',0))" 2>/dev/null)
  
  ABS_CHANGE=$(echo "$CHANGE" | python3 -c "import sys; print(abs(float(sys.stdin.read().strip())))" 2>/dev/null)
  
  if python3 -c "exit(0 if $ABS_CHANGE >= $THRESHOLD else 1)" 2>/dev/null; then
    SYMBOL=$(echo "$coin" | python3 -c "import sys; m={'bitcoin':'BTC','ethereum':'ETH','solana':'SOL','syscoin':'SYS'}; print(m.get(sys.stdin.read().strip(),'?'))")
    DIR=$(python3 -c "print('📈' if $CHANGE > 0 else '📉')")
    ALERTS="${ALERTS}${DIR} ${SYMBOL}: \$${PRICE} (${CHANGE}% 24h)\n"
  fi
done

if [ -n "$ALERTS" ]; then
  echo -e "🚨 Crypto Alert\n${ALERTS}"
fi
