from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter, RealParameter
from pandas import DataFrame
import talib.abstract as ta


class EMACrossStrategy(IStrategy):
    """EMA crossover strategy with trend filter — hyperoptable version.

    Entry: EMA fast crosses above EMA slow, price above EMA trend (trend filter).
    Exit:  EMA fast crosses below EMA slow, or RSI > sell threshold.
    """

    INTERFACE_VERSION = 3

    # Hyperoptable ROI
    minimal_roi = {
        "0": 0.10,
        "30": 0.05,
        "60": 0.03,
        "120": 0.01,
    }

    stoploss = -0.08

    trailing_stop = True
    trailing_stop_positive = 0.025
    trailing_stop_positive_offset = 0.06
    trailing_only_offset_is_reached = True

    timeframe = '1h'
    startup_candle_count = 300

    # Hyperopt parameters
    buy_ema_fast = IntParameter(5, 30, default=9, space='buy', optimize=True)
    buy_ema_slow = IntParameter(15, 50, default=21, space='buy', optimize=True)
    buy_ema_trend = IntParameter(100, 300, default=50, space='buy', optimize=True)
    buy_rsi_threshold = IntParameter(20, 45, default=30, space='buy', optimize=True)
    buy_volume_factor = RealParameter(0.3, 1.5, default=0.5, space='buy', optimize=True)

    sell_rsi_threshold = IntParameter(60, 85, default=75, space='sell', optimize=True)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Compute EMAs for all possible period values
        for period in range(5, 51):
            dataframe[f'ema{period}'] = ta.EMA(dataframe, timeperiod=period)
        for period in range(100, 301, 5):
            dataframe[f'ema{period}'] = ta.EMA(dataframe, timeperiod=period)

        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # Volume
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        fast_col = f'ema{self.buy_ema_fast.value}'
        slow_col = f'ema{self.buy_ema_slow.value}'
        # Round trend to nearest 5
        trend_val = round(self.buy_ema_trend.value / 5) * 5
        trend_col = f'ema{trend_val}'

        dataframe.loc[
            (
                (dataframe[fast_col] > dataframe[slow_col]) &
                (dataframe[fast_col].shift(1) <= dataframe[slow_col].shift(1)) &
                (dataframe['close'] > dataframe[trend_col]) &
                (dataframe['rsi'] > self.buy_rsi_threshold.value) &
                (dataframe['volume'] > dataframe['volume_mean'] * self.buy_volume_factor.value) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        fast_col = f'ema{self.buy_ema_fast.value}'
        slow_col = f'ema{self.buy_ema_slow.value}'

        dataframe.loc[
            (
                (
                    (dataframe[fast_col] < dataframe[slow_col]) &
                    (dataframe[fast_col].shift(1) >= dataframe[slow_col].shift(1))
                ) |
                (dataframe['rsi'] > self.sell_rsi_threshold.value)
            ),
            'exit_long'] = 1
        return dataframe
