"""
Z-Score Mean Reversion Strategy

Mathematical foundation: price deviations from the mean are temporary.
When price moves >2 standard deviations from its rolling mean, it's
statistically likely to revert.

Buy:  z-score < -2.0 (oversold) with volume confirmation
Sell: z-score > 0 (reverted to mean) or z-score > 2.0 (overbought)
"""

from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta
import numpy as np


class ZScoreRevertStrategy(IStrategy):

    INTERFACE_VERSION = 3

    minimal_roi = {
        "0": 0.08,
        "60": 0.04,
        "120": 0.02,
        "240": 0.01,
    }

    stoploss = -0.10

    timeframe = '1h'
    startup_candle_count = 100

    # --- Hyperoptable parameters ---
    zscore_lookback = IntParameter(20, 100, default=50, space='buy', optimize=True)
    zscore_entry = DecimalParameter(-3.0, -1.0, default=-2.0, decimals=1, space='buy', optimize=True)
    zscore_exit_mean = DecimalParameter(-0.5, 1.0, default=0.0, decimals=1, space='sell', optimize=True)
    zscore_exit_overbought = DecimalParameter(1.5, 3.0, default=2.0, decimals=1, space='sell', optimize=True)
    volume_multiplier = DecimalParameter(1.0, 3.0, default=1.5, decimals=1, space='buy', optimize=True)
    atr_sl_multiplier = DecimalParameter(1.0, 4.0, default=2.5, decimals=1, space='buy', optimize=True)

    use_custom_stoploss = True

    def custom_stoploss(self, pair: str, trade, current_time, current_rate, current_profit, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        if len(dataframe) < 1:
            return self.stoploss

        last = dataframe.iloc[-1]
        atr = last.get('atr', 0)
        if atr > 0 and current_rate > 0:
            sl_distance = atr * self.atr_sl_multiplier.value
            sl_price = current_rate - sl_distance
            sl_pct = (sl_price / current_rate) - 1.0
            return max(sl_pct, self.stoploss)

        return self.stoploss

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Calculate z-scores for all possible lookback values
        for period in range(20, 101, 10):
            rolling_mean = dataframe['close'].rolling(window=period).mean()
            rolling_std = dataframe['close'].rolling(window=period).std()
            dataframe[f'zscore_{period}'] = (dataframe['close'] - rolling_mean) / rolling_std

        # Volume analysis
        dataframe['volume_mean_20'] = dataframe['volume'].rolling(window=20).mean()

        # ATR for dynamic stoploss
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)

        # RSI as secondary filter
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Snap lookback to nearest 10
        period = round(self.zscore_lookback.value / 10) * 10
        period = max(20, min(100, period))
        zscore_col = f'zscore_{period}'

        if zscore_col not in dataframe.columns:
            zscore_col = 'zscore_50'

        dataframe.loc[
            (
                (dataframe[zscore_col] < self.zscore_entry.value) &
                (dataframe['volume'] > dataframe['volume_mean_20'] * self.volume_multiplier.value) &
                (dataframe['rsi'] < 40) &  # Additional oversold confirmation
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        period = round(self.zscore_lookback.value / 10) * 10
        period = max(20, min(100, period))
        zscore_col = f'zscore_{period}'

        if zscore_col not in dataframe.columns:
            zscore_col = 'zscore_50'

        dataframe.loc[
            (
                (dataframe[zscore_col] > self.zscore_exit_mean.value) |
                (dataframe[zscore_col] > self.zscore_exit_overbought.value)
            ),
            'exit_long'] = 1

        return dataframe
