# Freqtrade Backtest Results — RSIBollinger Strategy

**Date:** 2026-03-14  
**Timerange:** 2026-01-01 → 2026-03-14 (72 days)  
**Exchange:** Binance (dry-run)  
**Starting Balance:** $1,000 USDT  

## Strategy Overview

- **Strategy:** RSIBollinger
- **Timeframe:** 1h
- **Entry:** RSI < 30, price at lower Bollinger Band, above-average volume
- **Exit:** RSI > 70 or price at upper Bollinger Band
- **Stoploss:** -5% (trailing: +1% after +2% offset)
- **ROI:** 5% immediate → 1% after 2h

## Results Summary

| Metric | Value |
|---|---|
| Total Trades | 70 (0.97/day) |
| Final Balance | 910.22 USDT |
| **Total Profit** | **-89.78 USDT (-8.98%)** |
| Win Rate | 47.1% (33W / 37L) |
| Best Day | +4.32 USDT |
| Worst Day | -25.42 USDT |
| Max Drawdown | 93.78 USDT (9.35%) |
| **Market Change** | **-26.44%** |
| Avg Duration | 9h 24m |

## Per-Pair Performance

| Pair | Trades | Avg Profit % | Total Profit | Win Rate |
|---|---|---|---|---|
| BTC/USDT | 18 | -0.98% | -17.48 USDT | 55.6% |
| ETH/USDT | 26 | -1.28% | -33.30 USDT | 42.3% |
| SOL/USDT | 26 | -1.50% | -39.01 USDT | 46.2% |

## Exit Reasons

| Reason | Count | Avg Profit % | Total |
|---|---|---|---|
| ROI | 32 | +1.12% | +35.80 USDT |
| Trailing Stop Loss | 30 | -3.32% | -99.42 USDT |
| Stop Loss | 5 | -5.19% | -25.90 USDT |
| Exit Signal | 3 | -0.09% | -0.26 USDT |

## Analysis

### Market Context
The crypto market dropped **-26.44%** during this period. The strategy lost only **-8.98%**, outperforming buy-and-hold by ~17.5 percentage points.

### Key Observations
1. **ROI exits are profitable** — 32 trades averaging +1.12% each
2. **Trailing stops are too aggressive** — 30 trailing stop exits averaging -3.32% each, accounting for most losses
3. **SOL is the weakest pair** — highest volatility leads to more stop-outs
4. **BTC is the most stable** — best win rate at 55.6%

### Recommendations for Improvement
1. **Widen trailing stop** — `trailing_stop_positive_offset: 0.03` (from 0.02) to let winners run
2. **Tighten main stoploss** — Consider -3.5% instead of -5% to cut losses faster
3. **Add RSI exit threshold** — Currently exits at RSI > 70, could try 65 for earlier profit-taking
4. **Consider removing SOL** — Weakest performer, highest volatility
5. **Add startup_candle_count** — Strategy uses 20-period indicators but has 0 startup candles

### Decision: Paper Trading
**NOT starting paper trading** — the strategy is net negative. While it outperforms the market, a -8.98% loss over 72 days doesn't meet the >0% threshold. The strategy needs parameter tuning before live paper trading.

## Config Changes Made
- Added `pairlists` config (was missing, causing validation error)
- Fixed TA-Lib BBANDS `nbdevup`/`nbdevdn` to use floats (int caused TypeError)
- Changed FreqUI port from 8080 → 8081 (port conflict with CrowdSec)

## Files
- Config: `projects/freqtrade/user_data/config.json`
- Strategy: `projects/freqtrade/user_data/strategies/RSIBollinger.py`
- Docker Compose: `projects/freqtrade/docker-compose.yml`
- Backtest data: `projects/freqtrade/user_data/backtest_results/`
