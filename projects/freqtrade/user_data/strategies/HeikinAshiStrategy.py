"""
Heikin Ashi Smoothed Strategy
==============================
Heikin Ashi candles for noise reduction with Stochastic RSI confirmation.

Buy: HA candle turns green + no lower wick (strong bullish) + StochRSI not overbought
Sell: HA turns red + no upper wick (strong bearish) + StochRSI not oversold

Heikin Ashi is used by hedge funds for trend identification due to its noise-filtering
properties. Works great on 1h and 4h timeframes.
"""

from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta
import numpy as np


class HeikinAshiStrategy(IStrategy):
    INTERFACE_VERSION = 3

    minimal_roi = {
        "0": 0.12,
        "60": 0.06,
        "120": 0.03,
        "240": 0.015,
    }

    stoploss = -0.10

    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.05
    trailing_only_offset_is_reached = True

    timeframe = "1h"
    startup_candle_count = 50

    # Hyperoptable parameters
    buy_stoch_rsi_lower = IntParameter(10, 40, default=20, space="buy", optimize=True)
    buy_volume_mult = DecimalParameter(0.5, 2.0, default=1.0, decimals=1, space="buy", optimize=True)
    buy_ha_consecutive = IntParameter(1, 4, default=2, space="buy", optimize=True)

    sell_stoch_rsi_upper = IntParameter(60, 90, default=80, space="sell", optimize=True)
    sell_ha_consecutive = IntParameter(1, 4, default=2, space="sell", optimize=True)

    def _heikin_ashi(self, dataframe: DataFrame) -> DataFrame:
        """Calculate Heikin Ashi candles."""
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
        # Heikin Ashi candles
        ha = self._heikin_ashi(dataframe)
        dataframe["ha_open"] = ha["ha_open"]
        dataframe["ha_close"] = ha["ha_close"]
        dataframe["ha_high"] = ha["ha_high"]
        dataframe["ha_low"] = ha["ha_low"]

        # HA candle color: green (bullish) or red (bearish)
        dataframe["ha_green"] = (dataframe["ha_close"] > dataframe["ha_open"]).astype(int)

        # HA candle characteristics
        # No lower wick = strong bullish (open == low)
        dataframe["ha_no_lower_wick"] = (
            np.abs(dataframe["ha_open"] - dataframe["ha_low"]) < (dataframe["ha_high"] - dataframe["ha_low"]) * 0.05
        ).astype(int)
        # No upper wick = strong bearish (open == high)
        dataframe["ha_no_upper_wick"] = (
            np.abs(dataframe["ha_open"] - dataframe["ha_high"]) < (dataframe["ha_high"] - dataframe["ha_low"]) * 0.05
        ).astype(int)

        # Consecutive green/red HA candles
        for n in range(1, 5):
            green_cols = [dataframe["ha_green"].shift(i) for i in range(n)]
            dataframe[f"ha_green_{n}"] = np.prod(green_cols, axis=0)

            red_cols = [(1 - dataframe["ha_green"]).shift(i) for i in range(n)]
            dataframe[f"ha_red_{n}"] = np.prod(red_cols, axis=0)

        # Stochastic RSI
        rsi = ta.RSI(dataframe, timeperiod=14)
        stoch_rsi_k = (rsi - rsi.rolling(14).min()) / (rsi.rolling(14).max() - rsi.rolling(14).min()) * 100
        dataframe["stoch_rsi_k"] = stoch_rsi_k.rolling(3).mean()
        dataframe["stoch_rsi_d"] = dataframe["stoch_rsi_k"].rolling(3).mean()

        # Volume SMA
        dataframe["volume_sma"] = ta.SMA(dataframe["volume"], timeperiod=20)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        consec_col = f"ha_green_{self.buy_ha_consecutive.value}"
        if consec_col not in dataframe.columns:
            consec_col = "ha_green_2"

        dataframe.loc[
            (
                # HA candle is green (bullish)
                (dataframe[consec_col] == 1)
                # StochRSI not overbought (room to run)
                & (dataframe["stoch_rsi_k"] < self.buy_stoch_rsi_lower.value)
                # Volume above average
                & (dataframe["volume"] > dataframe["volume_sma"] * self.buy_volume_mult.value)
                & (dataframe["volume"] > 0)
            ),
            "enter_long",
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        consec_col = f"ha_red_{self.sell_ha_consecutive.value}"
        if consec_col not in dataframe.columns:
            consec_col = "ha_red_2"

        dataframe.loc[
            (
                # HA candle is red (bearish)
                (dataframe[consec_col] == 1)
                # StochRSI in overbought territory
                & (dataframe["stoch_rsi_k"] > self.sell_stoch_rsi_upper.value)
            ),
            "exit_long",
        ] = 1

        return dataframe
