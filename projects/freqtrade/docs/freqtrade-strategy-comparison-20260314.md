# Freqtrade Strategy Comparison — 2026-03-14

## Test Parameters
- **Period:** 2026-01-01 → 2026-03-14 (72 days)
- **Pairs:** BTC/USDT, ETH/USDT, SOL/USDT
- **Timeframe:** 1h
- **Wallet:** 1000 USDT, 100 USDT/trade (10%)
- **Market change:** **-26.44%** (strong bear market)

## Results Summary

| Strategy | Trades | Win% | Total P/L | P/L % | Max Drawdown | Best Pair | Worst Pair |
|----------|--------|------|-----------|-------|-------------|-----------|------------|
| **EMACross v1** ★ | 63 | 47.6% | -26.78 USDT | **-2.68%** | 3.71% | ETH -0.52% | BTC -1.19% |
| EMACross v2 (RSI>80 exit) | 42 | 71.4% | -43.11 USDT | -4.31% | 6.36% | BTC -0.95% | SOL -1.83% |
| EMACross v3 (no exit signal) | 50 | 74.0% | -46.18 USDT | -4.62% | 6.08% | ETH -1.42% | SOL -1.78% |
| MultiIndicator (3-of-4) | 98 | 77.6% | -52.78 USDT | -5.28% | 7.80% | SOL -1.42% | BTC -1.97% |
| RSIBollinger (tuned) | — | — | — | **-6.86%** | — | — | — |
| MultiIndicator (strict) | 0 | — | 0 | 0% | 0% | — | — |

## Key Findings

### 1. EMACross v1 is the clear winner (-2.68%)
- Beat the market by **+23.76%** (market dropped -26.44%)
- Simple EMA 9/21 crossover with EMA50 trend filter
- Exit signals (EMA crossunder + RSI > 75) important for cutting losses

### 2. High win rates ≠ better performance
- MultiIndicator had 77.6% win rate but -5.28% P/L
- EMACross v1 had only 47.6% win rate but -2.68% P/L
- Stop loss exits are the main drag (each costs -5% to -10%)
- Fewer losing trades > more winning trades in bear markets

### 3. Exit signals matter in bear markets
- EMACross v1 (with exit signals): -2.68%
- EMACross v3 (no exit signals): -4.62%
- Exit signals cut losses faster, preventing stop-loss hits
- ROI-only exits wait too long and eventually hit stops

### 4. Strict multi-indicator conditions = no trades
- Requiring RSI < 35 + below BB + MACD turning + above EMA200 simultaneously = 0 signals
- Relaxing to 3-of-4 conditions produced trades but too many false entries

### 5. This was a tough bear market
- All long-only strategies lost money in -26.44% market
- EMACross v1's -2.68% is actually excellent relative performance
- Consider adding short strategies or sitting out during confirmed downtrends

## EMACross v1 — Detailed Exit Analysis

| Exit Reason | Exits | Avg Profit | Total USDT | Win% |
|-------------|-------|-----------|------------|------|
| ROI targets | 30 | +1.28% | +38.24 USDT | 100% |
| Exit signal | 33 | -1.97% | -65.01 USDT | 0% |
| **Total** | 63 | -0.43% | -26.78 USDT | 47.6% |

ROI exits are 100% profitable. Exit signal exits are 100% losers — but they prevent bigger losses (without them, trades would hit the -8% stop loss instead of exiting at ~-2%).

## Recommendation

**Do NOT paper trade yet.** No strategy is profitable in the current market conditions.

**Next steps:**
1. Wait for market reversal / ranging conditions to retest
2. Consider adding short strategies for bear markets
3. Look into market regime detection (only trade in uptrends)
4. EMACross v1 is the best candidate for paper trading when market turns bullish
5. Consider wider pair whitelist (more pairs = more opportunities)

## Strategy Files
- `user_data/strategies/EMACrossStrategy.py` — ★ Best performer
- `user_data/strategies/MultiIndicatorStrategy.py` — Multi-confirmation approach
- `user_data/strategies/RSIBollinger.py` — Original strategy (baseline)
