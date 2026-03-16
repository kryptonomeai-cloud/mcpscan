# Bull Market Strategy: EMACrossBull

**Date:** 2026-03-14
**Status:** Strategy created, awaiting backtest

## Summary

Created `EMACrossBull` — a bull-market variant of the best-performing `EMACrossOptimised` strategy (+15.5% / +1.64% in bear market).

## Key Changes from EMACrossOptimised → EMACrossBull

### 1. Shorter EMA Periods (faster trend following)
| Parameter | Bear/Sideways | Bull |
|-----------|--------------|------|
| Fast EMA | 7 | **5** |
| Slow EMA | 44 | **21** |
| Trend EMA | 150 | **100** |

**Rationale:** Bull markets move faster. Shorter EMAs react quicker to trend changes, catching uptrends earlier and exiting sooner on reversals.

### 2. Tighter ROI Targets (capture gains frequently)
| Candles | Bear/Sideways | Bull |
|---------|--------------|------|
| 0 (entry) | 49.1% | **15%** |
| ~2h | 9.3% @ 5.5h | **8% @ 2h** |
| ~6h | 6% @ 17h | **4% @ 6h** |
| ~12h | — | **2% @ 12h** |
| Tail | 0% @ 38h | **0% @ 24h** |

**Rationale:** In bull markets, frequent smaller wins compound better than waiting for rare large wins. Reduces exposure time per trade.

### 3. Less Aggressive Trailing Stoploss
| Parameter | Bear/Sideways | Bull |
|-----------|--------------|------|
| Trail rate | 5.4% | **3%** |
| Activation offset | 13% | **6%** |
| Stoploss | -25.2% | **-15%** |

**Rationale:** Bull trends are smoother — a tighter trail captures more profit. The trailing activates earlier (6% vs 13%) so profits are protected sooner.

### 4. New Indicators Added
- **ADX (14):** Trend strength filter — only enters when ADX > 20 (confirmed trend)
- **Volume dual filter:** Both current volume > 1.2× 20-bar average AND 5-bar vol avg > 20-bar vol avg (accelerating volume)
- **MACD:** Calculated for potential future use in exit logic
- **RSI exit raised to 78** (from 62) — lets momentum run further in bull conditions
- **Trend reversal exit:** Exits if price drops below EMA100 (structural break)

### 5. Entry Conditions Comparison

**EMACrossOptimised (bear):**
- EMA7 crosses above EMA44
- Close > EMA150
- RSI > 22
- Volume > 1.46× average

**EMACrossBull (bull):**
- EMA5 crosses above EMA21 (faster signal)
- Close > EMA100 (shorter trend filter)
- ADX > 20 (trend strength gate)
- RSI between 30-70 (healthy range, not extreme)
- Volume > 1.2× 20-bar avg (slightly lower threshold — bull markets have natural volume)
- 5-bar vol avg > 20-bar vol avg (volume acceleration)

## Files Created
- **Strategy:** `user_data/strategies/EMACrossBull.py`
- **Backtest script:** `scripts/backtest_bull_strategy.sh`

## Next Steps
1. Run backtest: `cd projects/freqtrade && ./scripts/backtest_bull_strategy.sh --download`
2. Compare EMACrossBull vs EMACrossOptimised results
3. If promising, run hyperopt on the bull strategy to fine-tune parameters
4. Consider a meta-strategy that switches between bear/bull variants based on market regime (e.g., 200-day MA slope)
