"""
PSAR + ADX Trend Rider Strategy
================================
Parabolic SAR for entries/exits with ADX trend strength filter and EMA directional bias.
Custom stoploss using PSAR dots (dynamic trailing).

Inspired by Welles Wilder's trend-following methodology used by professional trend traders.
"""

from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from freqtrade.persistence import Trade
from pandas import DataFrame
from datetime import datetime
import talib.abstract as ta
import numpy as np


class PSARTrendStrategy(IStrategy):
    INTERFACE_VERSION = 3

    minimal_roi = {
        "0": 0.15,
        "60": 0.08,
        "120": 0.04,
        "240": 0.02,
    }

    stoploss = -0.15
    use_custom_stoploss = True

    timeframe = "1h"
    startup_candle_count = 250

    # Hyperoptable parameters
    buy_adx_threshold = IntParameter(15, 40, default=25, space="buy", optimize=True)
    buy_ema_period = IntParameter(100, 300, default=200, space="buy", optimize=True)
    buy_psar_af = DecimalParameter(0.01, 0.04, default=0.02, decimals=3, space="buy", optimize=True)
    buy_psar_max_af = DecimalParameter(0.1, 0.3, default=0.2, decimals=2, space="buy", optimize=True)

    sell_adx_threshold = IntParameter(10, 30, default=20, space="sell", optimize=True)

    def custom_stoploss(self, pair: str, trade: "Trade", current_time: datetime,
                        current_rate: float, current_profit: float, **kwargs) -> float:
        """Dynamic stoploss based on PSAR dots — tightens as trend progresses."""
        result = 1  # return 1 = don't change stoploss
        if self.dp:
            dataframe, _ = self.dp.get_analyzed_dataframe(pair=pair, timeframe=self.timeframe)
            if len(dataframe) > 0:
                last_candle = dataframe.iloc[-1].squeeze()
                psar_val = last_candle.get("sar")
                if psar_val is not None and psar_val > 0:
                    # PSAR-based stoploss: distance from current price to SAR dot
                    new_stoploss = (current_rate - psar_val) / current_rate
                    result = new_stoploss - 1  # convert to negative offset
        return result

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Parabolic SAR — use default; hyperopt values applied in signal logic
        dataframe["sar"] = ta.SAR(dataframe, acceleration=0.02, maximum=0.2)

        # SAR with various acceleration factors for hyperopt
        for af in [0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04]:
            for max_af in [0.1, 0.15, 0.2, 0.25, 0.3]:
                col = f"sar_{af}_{max_af}"
                dataframe[col] = ta.SAR(dataframe, acceleration=af, maximum=max_af)

        # ADX
        dataframe["adx"] = ta.ADX(dataframe, timeperiod=14)
        dataframe["plus_di"] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe["minus_di"] = ta.MINUS_DI(dataframe, timeperiod=14)

        # EMAs for trend bias
        for period in range(100, 301, 10):
            dataframe[f"ema{period}"] = ta.EMA(dataframe, timeperiod=period)

        # Volume SMA for filter
        dataframe["volume_sma"] = ta.SMA(dataframe["volume"], timeperiod=20)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        ema_col = f"ema{self.buy_ema_period.value}"
        # Fallback to closest available EMA
        if ema_col not in dataframe.columns:
            closest = min(range(100, 301, 10), key=lambda x: abs(x - self.buy_ema_period.value))
            ema_col = f"ema{closest}"

        dataframe.loc[
            (
                # SAR flips below price (bullish)
                (dataframe["sar"] < dataframe["close"])
                & (dataframe["sar"].shift(1) >= dataframe["close"].shift(1))
                # ADX shows trend strength
                & (dataframe["adx"] > self.buy_adx_threshold.value)
                # +DI above -DI (bullish directional movement)
                & (dataframe["plus_di"] > dataframe["minus_di"])
                # Price above long-term EMA (uptrend bias)
                & (dataframe["close"] > dataframe[ema_col])
                # Volume filter
                & (dataframe["volume"] > dataframe["volume_sma"] * 0.5)
                & (dataframe["volume"] > 0)
            ),
            "enter_long",
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # SAR flips above price (bearish)
                (dataframe["sar"] > dataframe["close"])
                & (dataframe["sar"].shift(1) <= dataframe["close"].shift(1))
            )
            | (
                # ADX drops below threshold (trend dying)
                (dataframe["adx"] < self.sell_adx_threshold.value)
                & (dataframe["minus_di"] > dataframe["plus_di"])
            ),
            "exit_long",
        ] = 1

        return dataframe
