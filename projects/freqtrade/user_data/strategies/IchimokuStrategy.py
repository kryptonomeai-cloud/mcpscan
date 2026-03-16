"""Ichimoku Cloud Strategy - Full Ichimoku Kinko Hyo system.

Buy: price above cloud, Tenkan crosses above Kijun, Chikou confirms.
Sell: price enters cloud or Tenkan crosses below Kijun.
Classic trend-following for all market conditions.
"""

from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta
import numpy as np


class IchimokuStrategy(IStrategy):
    INTERFACE_VERSION = 3

    minimal_roi = {
        "0": 0.15,
        "120": 0.08,
        "360": 0.04,
        "720": 0.02
    }

    stoploss = -0.08
    trailing_stop = True
    trailing_stop_positive = 0.03
    trailing_stop_positive_offset = 0.06
    trailing_only_offset_is_reached = True

    timeframe = '1h'
    startup_candle_count = 80  # Need 52 + 26 for Ichimoku lookback

    # Hyperoptable parameters
    buy_tenkan = IntParameter(7, 12, default=9, space='buy')
    buy_kijun = IntParameter(20, 30, default=26, space='buy')
    buy_senkou_b = IntParameter(45, 60, default=52, space='buy')
    buy_rsi_min = IntParameter(30, 55, default=40, space='buy')
    sell_rsi_max = IntParameter(65, 85, default=75, space='sell')

    def _ichimoku(self, dataframe: DataFrame, tenkan: int = 9, kijun: int = 26, senkou_b: int = 52) -> dict:
        """Calculate Ichimoku components manually."""
        high = dataframe['high']
        low = dataframe['low']

        # Tenkan-sen (Conversion Line)
        tenkan_sen = (high.rolling(window=tenkan).max() + low.rolling(window=tenkan).min()) / 2

        # Kijun-sen (Base Line)
        kijun_sen = (high.rolling(window=kijun).max() + low.rolling(window=kijun).min()) / 2

        # Senkou Span A (Leading Span A) - shifted forward 26 periods
        senkou_a = ((tenkan_sen + kijun_sen) / 2).shift(kijun)

        # Senkou Span B (Leading Span B) - shifted forward 26 periods
        senkou_b_val = ((high.rolling(window=senkou_b).max() + low.rolling(window=senkou_b).min()) / 2).shift(kijun)

        # Chikou Span (Lagging Span) - shifted back 26 periods
        chikou = dataframe['close'].shift(-kijun)

        return {
            'tenkan': tenkan_sen,
            'kijun': kijun_sen,
            'senkou_a': senkou_a,
            'senkou_b': senkou_b_val,
            'chikou': chikou,
            'cloud_top': np.maximum(senkou_a, senkou_b_val),
            'cloud_bottom': np.minimum(senkou_a, senkou_b_val),
        }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        ichi = self._ichimoku(
            dataframe,
            tenkan=self.buy_tenkan.value,
            kijun=self.buy_kijun.value,
            senkou_b=self.buy_senkou_b.value
        )

        dataframe['tenkan'] = ichi['tenkan']
        dataframe['kijun'] = ichi['kijun']
        dataframe['senkou_a'] = ichi['senkou_a']
        dataframe['senkou_b'] = ichi['senkou_b']
        dataframe['cloud_top'] = ichi['cloud_top']
        dataframe['cloud_bottom'] = ichi['cloud_bottom']

        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Price above cloud
                (dataframe['close'] > dataframe['cloud_top']) &
                # Tenkan crosses above Kijun (bullish TK cross)
                (dataframe['tenkan'] > dataframe['kijun']) &
                (dataframe['tenkan'].shift(1) <= dataframe['kijun'].shift(1)) &
                # RSI confirmation
                (dataframe['rsi'] > self.buy_rsi_min.value) &
                (dataframe['rsi'] < 70) &
                # Volume
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Price enters or goes below cloud
                (dataframe['close'] < dataframe['cloud_bottom']) |
                # Bearish TK cross
                (
                    (dataframe['tenkan'] < dataframe['kijun']) &
                    (dataframe['tenkan'].shift(1) >= dataframe['kijun'].shift(1))
                ) |
                # RSI overbought
                (dataframe['rsi'] > self.sell_rsi_max.value)
            ),
            'exit_long'] = 1
        return dataframe

    def custom_stoploss(self, pair: str, trade, current_time, current_rate, current_profit, **kwargs) -> float:
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        if len(dataframe) < 1:
            return self.stoploss
        last_candle = dataframe.iloc[-1]
        # Use Kijun-sen as dynamic stop
        kijun = last_candle.get('kijun', 0)
        if kijun > 0 and current_rate > 0:
            kijun_stop = (kijun - current_rate) / current_rate
            return max(kijun_stop, self.stoploss)
        return self.stoploss
