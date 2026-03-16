# Freqtrade Paper Trading Status Check — 2026-03-14 10:05 GMT

## Container Status: ✅ Running

- **Container:** `freqtrade` (ID: 2652c181f0c1)
- **Image:** `freqtradeorg/freqtrade:stable`
- **Version:** 2026.2
- **Uptime:** ~42 minutes (started at 09:23 UTC today — appears to have been **restarted today**, not running continuously since yesterday 2026-03-13)
- **State:** RUNNING (dry_run mode)
- **API:** Running on port 8081 (bound to 127.0.0.1 inside container, mapped to 0.0.0.0:8081 on host)

## Strategy Configuration

| Setting | Value |
|---------|-------|
| Strategy | EMACrossOptimised |
| Exchange | Binance |
| Timeframe | 1h |
| Stake per trade | 100 USDT |
| Max open trades | 5 |
| Pairs | BTC/USDT, ETH/USDT, SOL/USDT |
| Stoploss | -25.2% |
| Trailing stop | Yes (positive: 5.4%, offset: 13%) |
| Minimal ROI | 0: 49.1%, 330min: 9.3%, 1037min: 6%, 2271min: 0% |
| Startup candles | 200 |

## Trades: ❌ None

- **0 trades** in the database (both `trades` and `orders` tables empty)
- No buy/sell/entry/exit signals logged
- Logs show only heartbeat messages since startup

## Profit/Loss: N/A

- No trades executed, so no P&L to report
- `freqtrade profit` subcommand not available in this Docker image version

## ⚠️ Warnings & Notes

1. **Container was restarted today** — only 42 min uptime as of check. If it was started yesterday, it may have crashed/restarted. Previous trade data (if any) would have been in the DB but it's empty.
2. **Security warning:** `jwt_secret_key` is set to default — anyone could log into the API server.
3. **No parameter file found** — strategy is using default hyperopt values from the .py file.
4. **No protection handlers** defined.
5. The strategy requires 200 startup candles (200 hours of 1h data) which needs to download before it can generate signals. Since the container just restarted ~42 min ago, it may still be in the startup candle download phase, which would explain zero trades.

## Recommendations

- Check why the container restarted (was it manually restarted, or did it crash?)
- Consider setting a proper `jwt_secret_key` in the config
- Monitor for a few more hours — the bot needs time to download startup candles and start generating signals on the 1h timeframe
- Check again after 2-3 candle periods (~2-3 hours) to see if signals start firing
