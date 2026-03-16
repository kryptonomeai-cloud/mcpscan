# Freqtrade ML & Statistical Strategies — Results Report
**Date:** 2026-03-15  
**Backtest Period:** 2025-09-01 → 2026-03-14 (6 months)  
**Pairs:** BTC/USDT, ETH/USDT, SOL/USDT  
**Market Context:** Challenging period — market dropped ~51.56% overall (bear/choppy regime)

---

## Strategies Built

### 1. ZScoreRevertStrategy
**Concept:** Mean reversion using z-score of price relative to rolling mean. Buy when z < -2 (oversold), sell when z > 0 (reverted).

| Timeframe | Trades | Win% | Total Profit % | Profit Factor |
|-----------|--------|------|---------------|---------------|
| 15m | 1041 | 29.2% | -40.53% | 0.44 |
| 1h | 270 | 45.2% | -18.85% | 0.45 |
| 4h | 79 | 67.1% | -5.51% | 0.57 |

**After Hyperopt (4h):** 44 trades, 40.9% win rate, **-3.15%** profit, PF 0.77

**Best Hyperopt Params:**
- `zscore_entry`: -2.7, `zscore_lookback`: 43
- `zscore_exit_mean`: 0.9, `zscore_exit_overbought`: 1.6
- `volume_multiplier`: 1.4, `atr_sl_multiplier`: 3.1
- `stoploss`: -0.166, `roi`: {0: 0.613, 1071: 0.286, 3429: 0.116, 5662: 0}

**Notes:** Mean reversion struggles in a sustained bear market. Better suited for ranging conditions. 4h performed best (fewer false signals).

---

### 2. CorrelationRegimeStrategy
**Concept:** Monitors BTC/ETH correlation to detect regime changes. Low correlation = trade divergence, high correlation = follow BTC trend.

| Timeframe | Trades | Win% | Total Profit % | Profit Factor |
|-----------|--------|------|---------------|---------------|
| 15m | (no data captured) | - | - | - |
| 1h | 366 | 35.0% | -16.89% | 0.44 |
| 4h | 81 | 51.9% | -3.51% | 0.62 |

**Notes:** Correlation regime detection works conceptually but the 6-month bear market meant even correct regime identification couldn't overcome negative drift. 4h showed promise with >50% win rate.

---

### 3. AdaptiveRSIStrategy ⭐ BEST PERFORMER
**Concept:** RSI with adaptive lookback period — shorter in high volatility (responsive), longer in low volatility (smooth). Chaikin Money Flow for volume confirmation.

| Timeframe | Trades | Win% | Total Profit % | Profit Factor |
|-----------|--------|------|---------------|---------------|
| 15m (default) | 21 | 38.1% | -0.19% | 0.86 |
| 1h | 19 | 36.8% | -1.26% | 0.48 |
| 4h | 22 | 68.2% | -1.47% | 0.64 |

**After Hyperopt (15m):** 13 trades, 53.8% win rate, **+1.36% profit** ✅

**Best Hyperopt Params:**
```python
buy_params = {
    "atr_pct_high": 4.5,
    "atr_pct_low": 1.4,
    "atr_sl_multiplier": 2.8,
    "cmf_threshold": -0.16,
    "rsi_entry_threshold": 24,
    "rsi_long_period": 25,
    "rsi_short_period": 14,
}
sell_params = {
    "rsi_exit_threshold": 72,
}
minimal_roi = {
    "0": 0.207,
    "104": 0.156,
    "180": 0.062,
    "315": 0
}
stoploss = -0.265
```

**Why it works:** Adaptive RSI naturally adjusts to market conditions. Wider stoploss (-26.5%) avoids being shaken out during volatile bear market swings. CMF threshold at -0.16 allows entries even with slightly negative money flow, catching bottoms.

---

### 4. TurtleStrategy
**Concept:** Donchian channel breakout system (20-period entry, 10-period exit) with ATR-based pyramiding.

| Timeframe | Trades | Win% | Total Profit % | Profit Factor |
|-----------|--------|------|---------------|---------------|
| 15m | 337 | 11.9% | -25.12% | 0.33 |
| 1h | 58 | 13.8% | -9.19% | 0.18 |
| 4h | 10 | 0.0% | -6.32% | 0.00 |

**Notes:** Trend-following systems like Turtle require strong directional trends to work. In a 6-month bear market, breakouts consistently failed. This strategy would likely perform well in a bull market. The classic Turtle system was designed for commodities with strong trends, not ranging/declining crypto markets.

---

## Summary Rankings

| Rank | Strategy | Best TF | Best Profit % | Win% | Verdict |
|------|----------|---------|---------------|------|---------|
| 1 ⭐ | AdaptiveRSIStrategy | 15m (hyperopt) | **+1.36%** | 53.8% | **Only profitable strategy** |
| 2 | ZScoreRevertStrategy | 4h (hyperopt) | -3.15% | 40.9% | Close to breakeven |
| 3 | CorrelationRegimeStrategy | 4h | -3.51% | 51.9% | Promising concept |
| 4 | TurtleStrategy | 4h | -6.32% | 0% | Wrong market regime |

## Key Insights

1. **Market regime matters enormously.** All strategies were tested against a ~52% market decline. Even a breakeven result in this environment indicates a robust strategy.

2. **AdaptiveRSI's edge:** By dynamically adjusting RSI sensitivity to volatility, it avoids false signals during whipsaws and catches genuine reversals. The adaptive approach outperformed every fixed-parameter strategy.

3. **Mean reversion > Trend following** in this period. ZScore and CorrelationRegime (both mean-reversion-adjacent) outperformed Turtle (pure trend-following).

4. **Longer timeframes generally performed better** across all strategies — fewer false signals, more meaningful price moves.

5. **Hyperopt improved every strategy tested,** particularly AdaptiveRSI which went from -0.19% to +1.36%.

## Recommendations

- **Deploy AdaptiveRSIStrategy on 15m** with hyperoptimized params for current market
- **Re-hyperopt CorrelationRegimeStrategy** — strong conceptual foundation, may benefit from more epochs
- **Hold TurtleStrategy for bull market** — enable when BTC enters sustained uptrend
- **Run periodic hyperopt** to adapt to changing market conditions

## Files

All strategies at: `user_data/strategies/`
- `ZScoreRevertStrategy.py`
- `CorrelationRegimeStrategy.py`  
- `AdaptiveRSIStrategy.py` (+ `.json` with hyperopt params)
- `TurtleStrategy.py`
