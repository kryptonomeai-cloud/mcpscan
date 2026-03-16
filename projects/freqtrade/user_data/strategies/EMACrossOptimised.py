from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta


class EMACrossOptimised(IStrategy):
    """Hyperopt-optimised EMA crossover strategy.

    Optimised on 6 months of data (Sep 2025 - Mar 2026).
    +1.64% profit in -49.35% bear market.
    94% win rate (16/17), tight drawdown.

    3-month window: +2.97% in -26.44% bear market.
    """

    INTERFACE_VERSION = 3

    # Optimised ROI - let winners run
    minimal_roi = {
        "0": 0.491,
        "330": 0.093,
        "1037": 0.06,
        "2271": 0
    }

    stoploss = -0.252

    trailing_stop = True
    trailing_stop_positive = 0.054
    trailing_stop_positive_offset = 0.13
    trailing_only_offset_is_reached = True

    timeframe = '1h'
    startup_candle_count = 200

    max_open_trades = 5

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Optimised EMAs (6-month hyperopt: fast=7, slow=44, trend=151->150)
        dataframe['ema7'] = ta.EMA(dataframe, timeperiod=7)
        dataframe['ema44'] = ta.EMA(dataframe, timeperiod=44)
        dataframe['ema150'] = ta.EMA(dataframe, timeperiod=150)

        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # Volume
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['ema7'] > dataframe['ema44']) &
                (dataframe['ema7'].shift(1) <= dataframe['ema44'].shift(1)) &
                (dataframe['close'] > dataframe['ema150']) &
                (dataframe['rsi'] > 22) &
                (dataframe['volume'] > dataframe['volume_mean'] * 1.46) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (
                    (dataframe['ema7'] < dataframe['ema44']) &
                    (dataframe['ema7'].shift(1) >= dataframe['ema44'].shift(1))
                ) |
                (dataframe['rsi'] > 62)
            ),
            'exit_long'] = 1
        return dataframe
