"""
RSI Divergence Hunter Strategy
================================
Algorithmically detects bullish/bearish RSI divergences for reversal trading.

Bullish divergence: price makes lower low but RSI makes higher low → buy
Bearish divergence: price makes higher high but RSI makes lower high → sell

Confirmed with MACD histogram. This is a core technique used by professional
traders and prop firms to spot reversals before they happen.

Uses rolling window comparison for peak/trough detection (no scipy dependency).
"""

from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta
import numpy as np


class RSIDivergenceStrategy(IStrategy):
    INTERFACE_VERSION = 3

    minimal_roi = {
        "0": 0.10,
        "60": 0.05,
        "120": 0.03,
        "240": 0.015,
    }

    stoploss = -0.08

    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.04
    trailing_only_offset_is_reached = True

    timeframe = "1h"
    startup_candle_count = 100

    # Hyperoptable parameters
    buy_rsi_period = IntParameter(10, 21, default=14, space="buy", optimize=True)
    buy_divergence_lookback = IntParameter(5, 30, default=14, space="buy", optimize=True)
    buy_rsi_oversold = IntParameter(20, 45, default=35, space="buy", optimize=True)
    buy_pivot_window = IntParameter(2, 7, default=5, space="buy", optimize=True)

    sell_rsi_overbought = IntParameter(60, 85, default=70, space="sell", optimize=True)
    sell_divergence_lookback = IntParameter(5, 30, default=14, space="sell", optimize=True)
    sell_pivot_window = IntParameter(2, 7, default=5, space="sell", optimize=True)

    def _find_pivot_lows(self, series, window: int) -> np.ndarray:
        """Find local minima using rolling window comparison."""
        result = np.zeros(len(series), dtype=bool)
        arr = series.values
        for i in range(window, len(arr) - window):
            if arr[i] == np.min(arr[i - window : i + window + 1]):
                result[i] = True
        return result

    def _find_pivot_highs(self, series, window: int) -> np.ndarray:
        """Find local maxima using rolling window comparison."""
        result = np.zeros(len(series), dtype=bool)
        arr = series.values
        for i in range(window, len(arr) - window):
            if arr[i] == np.max(arr[i - window : i + window + 1]):
                result[i] = True
        return result

    def _bullish_divergence(self, price: np.ndarray, rsi: np.ndarray,
                            pivot_lows: np.ndarray, lookback: int) -> np.ndarray:
        """Detect bullish divergence: price lower low + RSI higher low."""
        result = np.zeros(len(price), dtype=bool)
        pivot_indices = np.where(pivot_lows)[0]

        for i in range(1, len(pivot_indices)):
            curr_idx = pivot_indices[i]
            prev_idx = pivot_indices[i - 1]
            if curr_idx - prev_idx > lookback:
                continue
            # Price makes lower low but RSI makes higher low
            if price[curr_idx] < price[prev_idx] and rsi[curr_idx] > rsi[prev_idx]:
                result[curr_idx] = True

        return result

    def _bearish_divergence(self, price: np.ndarray, rsi: np.ndarray,
                            pivot_highs: np.ndarray, lookback: int) -> np.ndarray:
        """Detect bearish divergence: price higher high + RSI lower high."""
        result = np.zeros(len(price), dtype=bool)
        pivot_indices = np.where(pivot_highs)[0]

        for i in range(1, len(pivot_indices)):
            curr_idx = pivot_indices[i]
            prev_idx = pivot_indices[i - 1]
            if curr_idx - prev_idx > lookback:
                continue
            # Price makes higher high but RSI makes lower high
            if price[curr_idx] > price[prev_idx] and rsi[curr_idx] < rsi[prev_idx]:
                result[curr_idx] = True

        return result

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI for various periods
        for period in range(10, 22):
            dataframe[f"rsi_{period}"] = ta.RSI(dataframe, timeperiod=period)

        # Default RSI
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)

        # MACD for confirmation
        macd = ta.MACD(dataframe)
        dataframe["macd"] = macd["macd"]
        dataframe["macd_signal"] = macd["macdsignal"]
        dataframe["macd_hist"] = macd["macdhist"]

        # EMA trend filter
        dataframe["ema50"] = ta.EMA(dataframe, timeperiod=50)
        dataframe["ema200"] = ta.EMA(dataframe, timeperiod=200)

        # Pivot detection for various windows
        for window in range(2, 8):
            dataframe[f"pivot_low_{window}"] = self._find_pivot_lows(dataframe["low"], window)
            dataframe[f"pivot_high_{window}"] = self._find_pivot_highs(dataframe["high"], window)

            # RSI pivot detection
            dataframe[f"rsi_pivot_low_{window}"] = self._find_pivot_lows(dataframe["rsi"], window)
            dataframe[f"rsi_pivot_high_{window}"] = self._find_pivot_highs(dataframe["rsi"], window)

        # Pre-compute divergences for common parameter combos
        for window in range(2, 8):
            for lookback in [5, 10, 14, 20, 25, 30]:
                pl = dataframe[f"pivot_low_{window}"].values.astype(bool)
                ph = dataframe[f"pivot_high_{window}"].values.astype(bool)

                bull_div = self._bullish_divergence(
                    dataframe["low"].values, dataframe["rsi"].values, pl, lookback
                )
                bear_div = self._bearish_divergence(
                    dataframe["high"].values, dataframe["rsi"].values, ph, lookback
                )

                dataframe[f"bull_div_{window}_{lookback}"] = bull_div.astype(int)
                dataframe[f"bear_div_{window}_{lookback}"] = bear_div.astype(int)

        # Volume SMA
        dataframe["volume_sma"] = ta.SMA(dataframe["volume"], timeperiod=20)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        window = self.buy_pivot_window.value
        lookback = self.buy_divergence_lookback.value

        # Map to pre-computed lookback
        available_lookbacks = [5, 10, 14, 20, 25, 30]
        closest_lb = min(available_lookbacks, key=lambda x: abs(x - lookback))

        bull_col = f"bull_div_{window}_{closest_lb}"
        if bull_col not in dataframe.columns:
            bull_col = "bull_div_5_14"

        dataframe.loc[
            (
                # Bullish RSI divergence detected
                (dataframe[bull_col] == 1)
                # RSI in oversold territory
                & (dataframe["rsi"] < self.buy_rsi_oversold.value)
                # MACD histogram turning positive (momentum confirmation)
                & (
                    (dataframe["macd_hist"] > dataframe["macd_hist"].shift(1))
                    | (dataframe["macd_hist"] > 0)
                )
                # Volume present
                & (dataframe["volume"] > 0)
            ),
            "enter_long",
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        window = self.sell_pivot_window.value
        lookback = self.sell_divergence_lookback.value

        available_lookbacks = [5, 10, 14, 20, 25, 30]
        closest_lb = min(available_lookbacks, key=lambda x: abs(x - lookback))

        bear_col = f"bear_div_{window}_{closest_lb}"
        if bear_col not in dataframe.columns:
            bear_col = "bear_div_5_14"

        dataframe.loc[
            (
                # Bearish RSI divergence detected
                (dataframe[bear_col] == 1)
                # RSI in overbought territory
                & (dataframe["rsi"] > self.sell_rsi_overbought.value)
            )
            | (
                # Strong overbought with MACD turning negative
                (dataframe["rsi"] > 80)
                & (dataframe["macd_hist"] < 0)
                & (dataframe["macd_hist"] < dataframe["macd_hist"].shift(1))
            ),
            "exit_long",
        ] = 1

        return dataframe
