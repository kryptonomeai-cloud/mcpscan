from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta


class BearShortOptimised(IStrategy):
    """Hyperopt-optimised short-selling strategy for bear markets.

    Optimised on 3 months (Jan-Mar 2026).
    +2.75% profit in -26.44% bear market.
    Short when price below EMA35, RSI > 48, MACD bearish.
    """

    INTERFACE_VERSION = 3
    can_short = True

    minimal_roi = {
        "0": 0.66,
        "333": 0.231,
        "893": 0.084,
        "1719": 0
    }

    stoploss = -0.136

    trailing_stop = True
    trailing_stop_positive = 0.143
    trailing_stop_positive_offset = 0.204
    trailing_only_offset_is_reached = False

    timeframe = '1h'
    startup_candle_count = 55

    max_open_trades = 5

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # EMAs
        dataframe['ema9'] = ta.EMA(dataframe, timeperiod=9)
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema35'] = ta.EMA(dataframe, timeperiod=35)

        # MACD
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']

        # Volume
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['close'] < dataframe['ema35']) &
                (dataframe['macd'] < dataframe['macdsignal']) &
                (dataframe['rsi'] > 48) &
                (dataframe['ema9'] < dataframe['ema21']) &
                (dataframe['volume'] > 0)
            ),
            'enter_short'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] < 28) |
                (dataframe['macd'] > dataframe['macdsignal'])
            ),
            'exit_short'] = 1
        return dataframe
