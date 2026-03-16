from freqtrade.strategy import IStrategy, IntParameter, RealParameter
from pandas import DataFrame
import talib.abstract as ta


class BearShortStrategy(IStrategy):
    """Short-selling strategy for bear markets.

    Entry Short: Price below EMA50, MACD histogram negative and worsening.
    Exit Short:  MACD histogram turns positive or trailing stop.
    Simple approach to ride downtrends.
    """

    INTERFACE_VERSION = 3
    can_short = True

    minimal_roi = {
        "0": 0.10,
        "60": 0.05,
        "120": 0.03,
        "240": 0.01,
    }

    stoploss = -0.08

    trailing_stop = True
    trailing_stop_positive = 0.025
    trailing_stop_positive_offset = 0.05
    trailing_only_offset_is_reached = True

    timeframe = '1h'
    startup_candle_count = 55

    # Hyperopt params
    buy_ema_period = IntParameter(20, 50, default=30, space='buy', optimize=True)
    buy_rsi_low = IntParameter(30, 55, default=40, space='buy', optimize=True)

    sell_rsi_threshold = IntParameter(20, 40, default=30, space='sell', optimize=True)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # EMAs
        for period in range(20, 55):
            dataframe[f'ema{period}'] = ta.EMA(dataframe, timeperiod=period)

        # MACD
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']

        # EMA crossover for short
        dataframe['ema9'] = ta.EMA(dataframe, timeperiod=9)
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)

        # Volume
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        ema_col = f'ema{self.buy_ema_period.value}'

        # Short entry: Simple conditions
        # Price below key EMA + MACD bearish + RSI in mid range (not oversold)
        dataframe.loc[
            (
                (dataframe['close'] < dataframe[ema_col]) &
                (dataframe['macd'] < dataframe['macdsignal']) &
                (dataframe['rsi'] > self.buy_rsi_low.value) &
                (dataframe['ema9'] < dataframe['ema21']) &  # Short-term bearish
                (dataframe['volume'] > 0)
            ),
            'enter_short'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Exit short: RSI oversold or MACD turning bullish
        dataframe.loc[
            (
                (dataframe['rsi'] < self.sell_rsi_threshold.value) |
                (dataframe['macd'] > dataframe['macdsignal'])
            ),
            'exit_short'] = 1

        return dataframe
