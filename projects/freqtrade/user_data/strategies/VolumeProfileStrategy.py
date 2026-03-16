"""Volume Profile Strategy - Order Flow analysis.

Identify high-volume price nodes (support/resistance), OBV trend,
VWAP + Volume weighted RSI. Buy at high-volume support with positive OBV divergence.
ATR-based dynamic stops.
"""

from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta
import numpy as np


class VolumeProfileStrategy(IStrategy):
    INTERFACE_VERSION = 3

    minimal_roi = {
        "0": 0.12,
        "90": 0.06,
        "240": 0.03,
        "480": 0.01
    }

    stoploss = -0.06
    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.05
    trailing_only_offset_is_reached = True

    timeframe = '1h'
    startup_candle_count = 60

    # Hyperoptable parameters
    buy_obv_lookback = IntParameter(5, 20, default=10, space='buy')
    buy_rsi = IntParameter(25, 50, default=45, space='buy')
    buy_vol_mult = DecimalParameter(0.5, 3.0, default=1.0, decimals=1, space='buy')
    sell_rsi = IntParameter(60, 80, default=70, space='sell')
    sell_obv_lookback = IntParameter(3, 15, default=5, space='sell')

    def _rolling_vwap(self, dataframe: DataFrame, window: int = 20):
        typical_price = (dataframe['high'] + dataframe['low'] + dataframe['close']) / 3
        tp_volume = typical_price * dataframe['volume']
        cum_tp_vol = tp_volume.rolling(window=window).sum()
        cum_vol = dataframe['volume'].rolling(window=window).sum()
        return cum_tp_vol / cum_vol

    def _volume_profile_support(self, dataframe: DataFrame, window: int = 40):
        """Identify high-volume price zones as support/resistance.
        Returns True when current price is near a high-volume node."""
        # Bin prices into ranges and find highest volume bins
        price_range = dataframe['close'].rolling(window).max() - dataframe['close'].rolling(window).min()
        # Simple proxy: price near VWAP with above-average volume = near a volume node
        vwap = self._rolling_vwap(dataframe, window)
        dist_from_vwap = (dataframe['close'] - vwap).abs() / vwap
        vol_above_avg = dataframe['volume'] > dataframe['volume'].rolling(window).mean()
        near_vwap = dist_from_vwap < 0.01  # Within 1% of VWAP
        return near_vwap & vol_above_avg

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # OBV
        dataframe['obv'] = ta.OBV(dataframe)
        dataframe['obv_ema'] = ta.EMA(dataframe['obv'], timeperiod=10)
        dataframe['obv_slope'] = dataframe['obv'].diff(self.buy_obv_lookback.value)

        # VWAP
        dataframe['vwap'] = self._rolling_vwap(dataframe, window=20)

        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # Volume-weighted RSI proxy: weight RSI by relative volume
        rel_vol = dataframe['volume'] / dataframe['volume'].rolling(20).mean()
        dataframe['vol_rsi'] = dataframe['rsi'] * rel_vol.clip(upper=2.0)

        # ATR
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)

        # Volume profile support
        dataframe['at_volume_support'] = self._volume_profile_support(dataframe)

        # Volume
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()

        # EMA for trend
        dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Near high-volume support zone
                (dataframe['at_volume_support'] | (dataframe['close'] <= dataframe['vwap'])) &
                # OBV rising (positive divergence)
                (dataframe['obv_slope'] > 0) &
                (dataframe['obv'] > dataframe['obv_ema']) &
                # RSI oversold
                (dataframe['rsi'] < self.buy_rsi.value) &
                # Above-average volume
                (dataframe['volume'] > dataframe['volume_mean'] * self.buy_vol_mult.value) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # RSI overbought
                (dataframe['rsi'] > self.sell_rsi.value) |
                # OBV declining
                (
                    (dataframe['obv'].diff(self.sell_obv_lookback.value) < 0) &
                    (dataframe['close'] > dataframe['vwap'])
                )
            ),
            'exit_long'] = 1
        return dataframe

    def custom_stoploss(self, pair: str, trade, current_time, current_rate, current_profit, **kwargs) -> float:
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        if len(dataframe) < 1:
            return self.stoploss
        last_candle = dataframe.iloc[-1]
        atr = last_candle.get('atr', 0)
        if atr > 0:
            atr_stop = -(atr * 2.0) / current_rate
            return max(atr_stop, self.stoploss)
        return self.stoploss
