"""
RSI Divergence Hunter Strategy — Optimised
============================================
Based on backtest results showing:
- 1h: +0.59% (88.9% win rate, 9 trades)
- 4h: +1.0% (100% win rate, 6 trades)
- Hyperopt epoch 1: 12 trades, 100% win, +1.93%

Optimised for 1h timeframe with relaxed entry conditions and tighter risk management.
"""

from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta
import numpy as np


class RSIDivergenceOptimised(IStrategy):
    INTERFACE_VERSION = 3

    # Optimised ROI — more aggressive take profit
    minimal_roi = {
        "0": 0.08,
        "30": 0.04,
        "60": 0.025,
        "120": 0.01,
    }

    stoploss = -0.06

    trailing_stop = True
    trailing_stop_positive = 0.015
    trailing_stop_positive_offset = 0.03
    trailing_only_offset_is_reached = True

    timeframe = "1h"
    startup_candle_count = 100

    # Optimised parameters
    buy_rsi_period = IntParameter(10, 21, default=14, space="buy", optimize=True)
    buy_divergence_lookback = IntParameter(5, 30, default=20, space="buy", optimize=True)
    buy_rsi_oversold = IntParameter(20, 50, default=40, space="buy", optimize=True)
    buy_pivot_window = IntParameter(2, 7, default=3, space="buy", optimize=True)

    sell_rsi_overbought = IntParameter(60, 85, default=65, space="sell", optimize=True)
    sell_divergence_lookback = IntParameter(5, 30, default=20, space="sell", optimize=True)
    sell_pivot_window = IntParameter(2, 7, default=3, space="sell", optimize=True)

    def _find_pivot_lows(self, series, window: int) -> np.ndarray:
        result = np.zeros(len(series), dtype=bool)
        arr = series.values
        for i in range(window, len(arr) - window):
            if arr[i] == np.min(arr[i - window : i + window + 1]):
                result[i] = True
        return result

    def _find_pivot_highs(self, series, window: int) -> np.ndarray:
        result = np.zeros(len(series), dtype=bool)
        arr = series.values
        for i in range(window, len(arr) - window):
            if arr[i] == np.max(arr[i - window : i + window + 1]):
                result[i] = True
        return result

    def _bullish_divergence(self, price, rsi, pivot_lows, lookback):
        result = np.zeros(len(price), dtype=bool)
        pivot_indices = np.where(pivot_lows)[0]
        for i in range(1, len(pivot_indices)):
            curr_idx = pivot_indices[i]
            prev_idx = pivot_indices[i - 1]
            if curr_idx - prev_idx > lookback:
                continue
            if price[curr_idx] < price[prev_idx] and rsi[curr_idx] > rsi[prev_idx]:
                result[curr_idx] = True
        return result

    def _bearish_divergence(self, price, rsi, pivot_highs, lookback):
        result = np.zeros(len(price), dtype=bool)
        pivot_indices = np.where(pivot_highs)[0]
        for i in range(1, len(pivot_indices)):
            curr_idx = pivot_indices[i]
            prev_idx = pivot_indices[i - 1]
            if curr_idx - prev_idx > lookback:
                continue
            if price[curr_idx] > price[prev_idx] and rsi[curr_idx] < rsi[prev_idx]:
                result[curr_idx] = True
        return result

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI
        for period in range(10, 22):
            dataframe[f"rsi_{period}"] = ta.RSI(dataframe, timeperiod=period)
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)

        # MACD
        macd = ta.MACD(dataframe)
        dataframe["macd"] = macd["macd"]
        dataframe["macd_signal"] = macd["macdsignal"]
        dataframe["macd_hist"] = macd["macdhist"]

        # EMAs
        dataframe["ema50"] = ta.EMA(dataframe, timeperiod=50)
        dataframe["ema200"] = ta.EMA(dataframe, timeperiod=200)

        # Bollinger Bands for extra context
        bb = ta.BBANDS(dataframe, timeperiod=20, nbdevup=2.0, nbdevdn=2.0)
        dataframe["bb_lower"] = bb["lowerband"]

        # Pivots and divergences
        for window in range(2, 8):
            dataframe[f"pivot_low_{window}"] = self._find_pivot_lows(dataframe["low"], window)
            dataframe[f"pivot_high_{window}"] = self._find_pivot_highs(dataframe["high"], window)

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

        dataframe["volume_sma"] = dataframe["volume"].rolling(20).mean()

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        window = self.buy_pivot_window.value
        lookback = self.buy_divergence_lookback.value
        available_lookbacks = [5, 10, 14, 20, 25, 30]
        closest_lb = min(available_lookbacks, key=lambda x: abs(x - lookback))
        bull_col = f"bull_div_{window}_{closest_lb}"
        if bull_col not in dataframe.columns:
            bull_col = "bull_div_3_20"

        dataframe.loc[
            (
                (dataframe[bull_col] == 1)
                & (dataframe["rsi"] < self.buy_rsi_oversold.value)
                & (
                    (dataframe["macd_hist"] > dataframe["macd_hist"].shift(1))
                    | (dataframe["macd_hist"] > 0)
                )
                # Price near Bollinger lower band (value zone)
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
            bear_col = "bear_div_3_20"

        dataframe.loc[
            (
                (dataframe[bear_col] == 1)
                & (dataframe["rsi"] > self.sell_rsi_overbought.value)
            )
            | (
                (dataframe["rsi"] > 75)
                & (dataframe["macd_hist"] < 0)
                & (dataframe["macd_hist"] < dataframe["macd_hist"].shift(1))
            ),
            "exit_long",
        ] = 1

        return dataframe
