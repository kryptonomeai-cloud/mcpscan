"""Supertrend Strategy - ATR-based trend following.

Multiple Supertrend periods for confirmation (10,3 and 11,2).
ADX filter for trend strength. Clean signals, minimal whipsaws.
"""

from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta
import numpy as np


class SupertrendStrategy(IStrategy):
    INTERFACE_VERSION = 3

    minimal_roi = {
        "0": 0.15,
        "120": 0.08,
        "360": 0.04,
        "720": 0.01
    }

    stoploss = -0.07
    trailing_stop = True
    trailing_stop_positive = 0.025
    trailing_stop_positive_offset = 0.05
    trailing_only_offset_is_reached = True

    timeframe = '1h'
    startup_candle_count = 50

    # Hyperoptable parameters
    buy_st1_period = IntParameter(7, 14, default=10, space='buy')
    buy_st1_mult = DecimalParameter(2.0, 4.0, default=3.0, decimals=1, space='buy')
    buy_st2_period = IntParameter(8, 15, default=11, space='buy')
    buy_st2_mult = DecimalParameter(1.5, 3.5, default=2.0, decimals=1, space='buy')
    buy_adx_min = IntParameter(15, 30, default=20, space='buy')
    sell_adx_max = IntParameter(10, 25, default=15, space='sell')

    def _supertrend(self, dataframe: DataFrame, period: int, multiplier: float):
        """Calculate Supertrend indicator using numpy arrays for speed."""
        atr = ta.ATR(dataframe, timeperiod=period).values
        close = dataframe['close'].values
        high = dataframe['high'].values
        low = dataframe['low'].values
        hl2 = (high + low) / 2.0

        n = len(dataframe)
        upper = hl2 + multiplier * atr
        lower = hl2 - multiplier * atr
        supertrend = np.zeros(n)
        direction = np.zeros(n)

        # Initialize
        supertrend[0] = upper[0]
        direction[0] = -1

        for i in range(1, n):
            # Band adjustment
            if not np.isnan(lower[i]) and not np.isnan(lower[i-1]):
                if lower[i] < lower[i-1] and close[i-1] > lower[i-1]:
                    lower[i] = lower[i-1]
            if not np.isnan(upper[i]) and not np.isnan(upper[i-1]):
                if upper[i] > upper[i-1] and close[i-1] < upper[i-1]:
                    upper[i] = upper[i-1]

            # Direction logic
            if direction[i-1] == -1:  # Was downtrend
                if close[i] > upper[i]:
                    direction[i] = 1
                    supertrend[i] = lower[i]
                else:
                    direction[i] = -1
                    supertrend[i] = upper[i]
            else:  # Was uptrend
                if close[i] < lower[i]:
                    direction[i] = -1
                    supertrend[i] = upper[i]
                else:
                    direction[i] = 1
                    supertrend[i] = lower[i]

        return supertrend, direction

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Supertrend 1
        st1, dir1 = self._supertrend(dataframe, self.buy_st1_period.value, self.buy_st1_mult.value)
        dataframe['supertrend_1'] = st1
        dataframe['st_direction_1'] = dir1

        # Supertrend 2
        st2, dir2 = self._supertrend(dataframe, self.buy_st2_period.value, self.buy_st2_mult.value)
        dataframe['supertrend_2'] = st2
        dataframe['st_direction_2'] = dir2

        # ADX
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)

        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # ATR for stoploss
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)

        # EMA trend filter
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)

        # Volume
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Primary supertrend bullish
                (dataframe['st_direction_1'] == 1) &
                # Just flipped bullish (entry signal)
                (dataframe['st_direction_1'].shift(1) == -1) &
                # RSI not overbought
                (dataframe['rsi'] < 70) &
                # Volume
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Either supertrend turns bearish
                (
                    (dataframe['st_direction_1'] == -1) &
                    (dataframe['st_direction_1'].shift(1) == 1)
                ) |
                (
                    (dataframe['st_direction_2'] == -1) &
                    (dataframe['st_direction_2'].shift(1) == 1)
                ) |
                # Weak trend
                (dataframe['adx'] < self.sell_adx_max.value)
            ),
            'exit_long'] = 1
        return dataframe

    def custom_stoploss(self, pair: str, trade, current_time, current_rate, current_profit, **kwargs) -> float:
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        if len(dataframe) < 1:
            return self.stoploss
        last_candle = dataframe.iloc[-1]
        # Use supertrend as dynamic stop
        st1 = last_candle.get('supertrend_1', 0)
        if st1 > 0 and last_candle.get('st_direction_1', 0) == 1:
            st_stop = (st1 - current_rate) / current_rate
            return max(st_stop, self.stoploss)
        return self.stoploss
