"""
Adaptive RSI Strategy

RSI with dynamically adjusted lookback period based on market volatility.
High volatility → shorter RSI (more responsive)
Low volatility → longer RSI (smoother, fewer false signals)

Entry: adaptive RSI oversold + Chaikin Money Flow confirmation
Exit:  adaptive RSI overbought
"""

from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta
import numpy as np


class AdaptiveRSIStrategy(IStrategy):

    INTERFACE_VERSION = 3

    minimal_roi = {
        "0": 0.08,
        "60": 0.04,
        "180": 0.025,
        "360": 0.01,
    }

    stoploss = -0.08

    timeframe = '1h'
    startup_candle_count = 100

    # --- Hyperoptable parameters ---
    rsi_short_period = IntParameter(5, 14, default=7, space='buy', optimize=True)
    rsi_long_period = IntParameter(18, 40, default=28, space='buy', optimize=True)
    rsi_entry_threshold = IntParameter(20, 40, default=30, space='buy', optimize=True)
    rsi_exit_threshold = IntParameter(60, 85, default=70, space='sell', optimize=True)
    atr_pct_high = DecimalParameter(1.0, 5.0, default=3.0, decimals=1, space='buy', optimize=True)
    atr_pct_low = DecimalParameter(0.3, 2.0, default=1.0, decimals=1, space='buy', optimize=True)
    cmf_threshold = DecimalParameter(-0.2, 0.1, default=-0.05, decimals=2, space='buy', optimize=True)
    atr_sl_multiplier = DecimalParameter(1.5, 4.0, default=2.5, decimals=1, space='buy', optimize=True)

    use_custom_stoploss = True

    def custom_stoploss(self, pair: str, trade, current_time, current_rate, current_profit, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        if len(dataframe) < 1:
            return self.stoploss

        last = dataframe.iloc[-1]
        atr = last.get('atr', 0)
        if atr > 0 and current_rate > 0:
            sl_distance = atr * self.atr_sl_multiplier.value
            sl_pct = -sl_distance / current_rate
            return max(sl_pct, self.stoploss)

        return self.stoploss

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # ATR and ATR percentage (volatility measure)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        dataframe['atr_pct'] = (dataframe['atr'] / dataframe['close']) * 100
        dataframe['atr_pct_smooth'] = dataframe['atr_pct'].ewm(span=10).mean()

        # Pre-compute RSI for all possible periods
        for period in range(5, 41):
            dataframe[f'rsi_{period}'] = ta.RSI(dataframe, timeperiod=period)

        # Build adaptive RSI using vectorized approach
        rsi_short = self.rsi_short_period.value
        rsi_long = self.rsi_long_period.value
        atr_low = self.atr_pct_low.value
        atr_high = max(atr_low + 0.1, self.atr_pct_high.value)  # Ensure atr_high > atr_low

        # Ensure rsi_long > rsi_short
        if rsi_long <= rsi_short:
            rsi_long = rsi_short + 4

        # ATR ratio: 0 = low vol, 1 = high vol
        atr_ratio = (dataframe['atr_pct_smooth'] - atr_low) / (atr_high - atr_low)
        atr_ratio = atr_ratio.clip(0, 1).fillna(0.5)

        # High vol → short period, low vol → long period
        target_period = (rsi_long - atr_ratio * (rsi_long - rsi_short)).round().clip(5, 40).fillna(14).astype(int)

        # Select RSI value for each row based on target period
        adaptive_rsi = np.full(len(dataframe), np.nan)
        for period in range(5, 41):
            mask = (target_period == period).values
            if mask.any():
                adaptive_rsi[mask] = dataframe[f'rsi_{period}'].values[mask]

        dataframe['adaptive_rsi'] = adaptive_rsi

        # Chaikin Money Flow
        mfv = ((dataframe['close'] - dataframe['low']) - (dataframe['high'] - dataframe['close'])) / \
              (dataframe['high'] - dataframe['low'] + 1e-10) * dataframe['volume']
        dataframe['cmf'] = mfv.rolling(window=20).sum() / (dataframe['volume'].rolling(window=20).sum() + 1e-10)

        # Volume
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['adaptive_rsi'] < self.rsi_entry_threshold.value) &
                (dataframe['cmf'] > self.cmf_threshold.value) &
                (dataframe['volume'] > dataframe['volume_mean'] * 0.8) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['adaptive_rsi'] > self.rsi_exit_threshold.value)
            ),
            'exit_long'] = 1

        return dataframe
