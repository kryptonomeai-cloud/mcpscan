"""
Heikin Ashi Smoothed Strategy — Optimised
==========================================
Based on backtest results showing:
- 1h: +0.98% (81.8% win rate, 11 trades)
- 4h: marginal (too few trades)

Optimised for 1h with relaxed entry conditions for more trade opportunities.
"""

from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta
import numpy as np


class HeikinAshiOptimised(IStrategy):
    INTERFACE_VERSION = 3

    # Optimised ROI
    minimal_roi = {
        "0": 0.08,
        "30": 0.04,
        "60": 0.025,
        "120": 0.01,
    }

    stoploss = -0.07

    trailing_stop = True
    trailing_stop_positive = 0.015
    trailing_stop_positive_offset = 0.035
    trailing_only_offset_is_reached = True

    timeframe = "1h"
    startup_candle_count = 50

    # Optimised parameters — more relaxed for more entries
    buy_stoch_rsi_lower = IntParameter(15, 50, default=35, space="buy", optimize=True)
    buy_volume_mult = DecimalParameter(0.3, 1.5, default=0.6, decimals=1, space="buy", optimize=True)
    buy_ha_consecutive = IntParameter(1, 3, default=1, space="buy", optimize=True)

    sell_stoch_rsi_upper = IntParameter(55, 90, default=65, space="sell", optimize=True)
    sell_ha_consecutive = IntParameter(1, 3, default=1, space="sell", optimize=True)

    def _heikin_ashi(self, dataframe: DataFrame) -> DataFrame:
        ha = DataFrame(index=dataframe.index)
        ha["ha_close"] = (dataframe["open"] + dataframe["high"] + dataframe["low"] + dataframe["close"]) / 4
        ha["ha_open"] = 0.0
        ha["ha_open"].iloc[0] = (dataframe["open"].iloc[0] + dataframe["close"].iloc[0]) / 2
        for i in range(1, len(dataframe)):
            ha["ha_open"].iloc[i] = (ha["ha_open"].iloc[i - 1] + ha["ha_close"].iloc[i - 1]) / 2
        ha["ha_high"] = dataframe[["high"]].join(ha[["ha_open", "ha_close"]]).max(axis=1)
        ha["ha_low"] = dataframe[["low"]].join(ha[["ha_open", "ha_close"]]).min(axis=1)
        return ha

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        ha = self._heikin_ashi(dataframe)
        dataframe["ha_open"] = ha["ha_open"]
        dataframe["ha_close"] = ha["ha_close"]
        dataframe["ha_high"] = ha["ha_high"]
        dataframe["ha_low"] = ha["ha_low"]

        dataframe["ha_green"] = (dataframe["ha_close"] > dataframe["ha_open"]).astype(int)

        # Consecutive green/red
        for n in range(1, 4):
            green_cols = [dataframe["ha_green"].shift(i) for i in range(n)]
            dataframe[f"ha_green_{n}"] = np.prod(green_cols, axis=0)
            red_cols = [(1 - dataframe["ha_green"]).shift(i) for i in range(n)]
            dataframe[f"ha_red_{n}"] = np.prod(red_cols, axis=0)

        # Stochastic RSI
        rsi = ta.RSI(dataframe, timeperiod=14)
        stoch_rsi_k = (rsi - rsi.rolling(14).min()) / (rsi.rolling(14).max() - rsi.rolling(14).min()) * 100
        dataframe["stoch_rsi_k"] = stoch_rsi_k.rolling(3).mean()
        dataframe["stoch_rsi_d"] = dataframe["stoch_rsi_k"].rolling(3).mean()

        # EMA trend filter
        dataframe["ema50"] = ta.EMA(dataframe, timeperiod=50)

        # Volume SMA
        dataframe["volume_sma"] = dataframe["volume"].rolling(20).mean()

        # MACD for momentum
        macd = ta.MACD(dataframe)
        dataframe["macd_hist"] = macd["macdhist"]

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        consec_col = f"ha_green_{self.buy_ha_consecutive.value}"
        if consec_col not in dataframe.columns:
            consec_col = "ha_green_1"

        dataframe.loc[
            (
                (dataframe[consec_col] == 1)
                & (dataframe["stoch_rsi_k"] < self.buy_stoch_rsi_lower.value)
                # HA candle turning from red to green (reversal)
                & (dataframe["ha_green"].shift(1) == 0)
                & (dataframe["volume"] > dataframe["volume_sma"] * self.buy_volume_mult.value)
                & (dataframe["volume"] > 0)
            ),
            "enter_long",
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        consec_col = f"ha_red_{self.sell_ha_consecutive.value}"
        if consec_col not in dataframe.columns:
            consec_col = "ha_red_1"

        dataframe.loc[
            (
                (dataframe[consec_col] == 1)
                & (dataframe["stoch_rsi_k"] > self.sell_stoch_rsi_upper.value)
            ),
            "exit_long",
        ] = 1

        return dataframe
