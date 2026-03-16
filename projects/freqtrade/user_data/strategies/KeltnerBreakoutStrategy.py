"""
Keltner Channel Breakout Strategy
===================================
Keltner Channels (EMA + ATR-based bands) with Bollinger Band squeeze detection.

Buy: Breakout above upper Keltner channel with volume confirmation.
     Squeeze detection: Keltner inside Bollinger = volatility compression, breakout imminent.
Sell: Price re-enters channel or breaks lower band.

Used by institutional traders for volatility breakouts.
"""

from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta
import numpy as np


class KeltnerBreakoutStrategy(IStrategy):
    INTERFACE_VERSION = 3

    minimal_roi = {
        "0": 0.15,
        "60": 0.08,
        "120": 0.04,
        "240": 0.02,
    }

    stoploss = -0.12

    trailing_stop = True
    trailing_stop_positive = 0.03
    trailing_stop_positive_offset = 0.06
    trailing_only_offset_is_reached = True

    timeframe = "1h"
    startup_candle_count = 50

    # Hyperoptable parameters
    buy_keltner_period = IntParameter(10, 30, default=20, space="buy", optimize=True)
    buy_keltner_atr_mult = DecimalParameter(1.0, 3.0, default=1.5, decimals=1, space="buy", optimize=True)
    buy_volume_mult = DecimalParameter(1.0, 3.0, default=1.5, decimals=1, space="buy", optimize=True)
    buy_squeeze_lookback = IntParameter(3, 15, default=6, space="buy", optimize=True)

    sell_keltner_atr_mult = DecimalParameter(1.0, 3.0, default=1.5, decimals=1, space="sell", optimize=True)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # ATR
        dataframe["atr14"] = ta.ATR(dataframe, timeperiod=14).astype(float)

        # Keltner mid (EMA) for various periods
        for period in range(10, 31):
            dataframe[f"kc_mid_{period}"] = ta.EMA(dataframe, timeperiod=period).astype(float)

        # Bollinger Bands for squeeze detection
        bb = ta.BBANDS(dataframe, timeperiod=20, nbdevup=2.0, nbdevdn=2.0)
        dataframe["bb_upper"] = bb["upperband"].astype(float)
        dataframe["bb_lower"] = bb["lowerband"].astype(float)

        # Default Keltner for squeeze calc
        kc_mid_20 = dataframe["kc_mid_20"]
        dataframe["kc_upper_def"] = kc_mid_20 + (dataframe["atr14"] * 1.5)
        dataframe["kc_lower_def"] = kc_mid_20 - (dataframe["atr14"] * 1.5)

        # Squeeze: BB inside KC = low volatility
        dataframe["squeeze"] = (
            (dataframe["bb_lower"].values > dataframe["kc_lower_def"].values)
            & (dataframe["bb_upper"].values < dataframe["kc_upper_def"].values)
        ).astype(int)

        # Was squeezed recently
        for n in range(3, 16):
            dataframe[f"was_sq_{n}"] = dataframe["squeeze"].rolling(n).sum().ge(1).astype(int)

        # MACD
        macd = ta.MACD(dataframe)
        dataframe["macd_hist"] = macd["macdhist"].astype(float)

        # Volume SMA
        dataframe["vol_sma"] = dataframe["volume"].rolling(20).mean()

        # RSI
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14).astype(float)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        kc_period = self.buy_keltner_period.value
        kc_mid_col = f"kc_mid_{kc_period}"
        if kc_mid_col not in dataframe.columns:
            kc_mid_col = "kc_mid_20"

        mult = float(self.buy_keltner_atr_mult.value)
        kc_upper = dataframe[kc_mid_col] + (dataframe["atr14"] * mult)

        sq_col = f"was_sq_{self.buy_squeeze_lookback.value}"
        if sq_col not in dataframe.columns:
            sq_col = "was_sq_6"

        vol_thresh = dataframe["vol_sma"] * float(self.buy_volume_mult.value)

        dataframe.loc[
            (
                (dataframe["close"] > kc_upper)
                & (dataframe["close"].shift(1) <= (dataframe[kc_mid_col].shift(1) + dataframe["atr14"].shift(1) * mult))
                & (dataframe[sq_col] == 1)
                & (dataframe["volume"] > vol_thresh)
                & (dataframe["macd_hist"] > 0)
                & (dataframe["volume"] > 0)
            ),
            "enter_long",
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        kc_period = self.buy_keltner_period.value
        kc_mid_col = f"kc_mid_{kc_period}"
        if kc_mid_col not in dataframe.columns:
            kc_mid_col = "kc_mid_20"

        mult = float(self.sell_keltner_atr_mult.value)
        kc_lower = dataframe[kc_mid_col] - (dataframe["atr14"] * mult)

        dataframe.loc[
            (
                (dataframe["close"] < dataframe[kc_mid_col])
            )
            | (
                (dataframe["close"] < kc_lower)
            ),
            "exit_long",
        ] = 1

        return dataframe
