from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta
import numpy as np


class MomentumOptimised(IStrategy):
    """Hyperopt-optimised Momentum strategy.

    Optimised on 6 months of data (Sep 2025 - Mar 2026).
    +1.45% profit in -51.82% bear market.
    MACD histogram crossover with RSI confirmation.
    """

    INTERFACE_VERSION = 3

    minimal_roi = {
        "0": 0.246,
        "240": 0.211,
        "690": 0.051,
        "2003": 0
    }

    stoploss = -0.111

    trailing_stop = True
    trailing_stop_positive = 0.279
    trailing_stop_positive_offset = 0.311
    trailing_only_offset_is_reached = True

    timeframe = '1h'
    startup_candle_count = 30

    max_open_trades = 5

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
                (dataframe['macdhist_prev'] <= 0) &
                (dataframe['rsi'] > 40) &
                (dataframe['rsi'] < 59) &
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
                (dataframe['rsi'] > 80)
            ),
            'exit_long'] = 1
        return dataframe
