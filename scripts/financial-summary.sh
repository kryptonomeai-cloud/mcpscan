#!/bin/bash
# Financial summary for morning briefing - crypto + market data
set -euo pipefail

echo "💰 Financial Summary — $(date +%Y-%m-%d)"
echo ""

# Crypto prices
CRYPTO=$(curl -sf --max-time 15 "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,syscoin&vs_currencies=usd,gbp&include_24hr_change=true" 2>/dev/null)

if [ -n "$CRYPTO" ]; then
  echo "📊 Crypto:"
  echo "$CRYPTO" | python3 -c "
import sys, json
d = json.load(sys.stdin)
coins = [('BTC', 'bitcoin'), ('ETH', 'ethereum'), ('SOL', 'solana'), ('SYS', 'syscoin')]
for sym, cid in coins:
    c = d.get(cid, {})
    price = c.get('usd', 0)
    change = c.get('usd_24h_change', 0)
    arrow = '▲' if change > 0 else '▼'
    fmt = f'\${price:,.2f}' if price >= 1 else f'\${price:.4f}'
    print(f'  {sym}: {fmt} ({arrow}{abs(change):.1f}%)')
"
else
  echo "  ⚠️ Crypto data unavailable"
fi

echo ""

# Market indices (Yahoo Finance)
echo "📈 Markets:"
for symbol in "^GSPC:S&P 500" "^IXIC:NASDAQ" "^FTSE:FTSE 100"; do
  SYM="${symbol%%:*}"
  NAME="${symbol##*:}"
  QUOTE=$(curl -sf --max-time 10 "https://query1.finance.yahoo.com/v8/finance/chart/${SYM}?interval=1d&range=1d" 2>/dev/null)
  if [ -n "$QUOTE" ]; then
    echo "$QUOTE" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    meta = d['chart']['result'][0]['meta']
    price = meta.get('regularMarketPrice', 0)
    prev = meta.get('chartPreviousClose', 0)
    if prev > 0:
        change = ((price - prev) / prev) * 100
        arrow = '▲' if change > 0 else '▼'
        print(f'  ${NAME}: {price:,.0f} ({arrow}{abs(change):.1f}%)')
    else:
        print(f'  ${NAME}: {price:,.0f}')
except:
    print(f'  ${NAME}: unavailable')
" 2>/dev/null
  else
    echo "  ${NAME}: unavailable"
  fi
done
