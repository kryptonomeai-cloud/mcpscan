from freqtrade.strategy import IStrategy, IntParameter, RealParameter
from pandas import DataFrame
import talib.abstract as ta
import numpy as np


class MomentumTrendStrategy(IStrategy):
    """Momentum strategy using MACD and RSI in trending conditions.

    Entry: MACD histogram turns positive, RSI in mid-range (not overbought),
           EMA alignment confirms trend direction.
    Exit:  MACD histogram turns negative or RSI overbought.
    Simpler conditions for more trade signals.
    """

    INTERFACE_VERSION = 3

    minimal_roi = {
        "0": 0.08,
        "60": 0.04,
        "120": 0.02,
        "240": 0.01,
    }

    stoploss = -0.08

    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.04
    trailing_only_offset_is_reached = True

    timeframe = '1h'
    startup_candle_count = 30

    # Hyperopt params
    buy_rsi_low = IntParameter(25, 50, default=35, space='buy', optimize=True)
    buy_rsi_high = IntParameter(50, 70, default=60, space='buy', optimize=True)

    sell_rsi_threshold = IntParameter(60, 85, default=72, space='sell', optimize=True)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # MACD
        macd = ta.MACD(dataframe, fastperiod=12, slowperiod=26, signalperiod=9)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']
        dataframe['macdhist_prev'] = dataframe['macdhist'].shift(1)

        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # EMAs
        dataframe['ema12'] = ta.EMA(dataframe, timeperiod=12)
        dataframe['ema26'] = ta.EMA(dataframe, timeperiod=26)

        # Volume
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['macdhist'] > 0) &
                (dataframe['macdhist_prev'] <= 0) &  # MACD histogram just turned positive
                (dataframe['rsi'] > self.buy_rsi_low.value) &
                (dataframe['rsi'] < self.buy_rsi_high.value) &
                (dataframe['ema12'] > dataframe['ema26']) &
                (dataframe['volume'] > dataframe['volume_mean'] * 0.5) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (
                    (dataframe['macdhist'] < 0) &
                    (dataframe['macdhist_prev'] >= 0)
                ) |
                (dataframe['rsi'] > self.sell_rsi_threshold.value)
            ),
            'exit_long'] = 1
        return dataframe
