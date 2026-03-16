"""VWAP Scalper Strategy - Volume Weighted Average Price with deviation bands.

Buy when price touches lower VWAP band with RSI oversold confirmation.
Sell at VWAP mean or upper band. High frequency on 15m timeframe.
"""

from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta
import numpy as np


class VWAPScalperStrategy(IStrategy):
    INTERFACE_VERSION = 3

    minimal_roi = {
        "0": 0.03,
        "30": 0.02,
        "60": 0.01,
        "120": 0.005
    }

    stoploss = -0.02
    trailing_stop = True
    trailing_stop_positive = 0.005
    trailing_stop_positive_offset = 0.01
    trailing_only_offset_is_reached = True

    timeframe = '15m'
    startup_candle_count = 50

    # Hyperoptable parameters
    buy_rsi = IntParameter(15, 40, default=30, space='buy')
    buy_vwap_std = DecimalParameter(1.0, 3.0, default=2.0, decimals=1, space='buy')
    sell_rsi = IntParameter(60, 85, default=70, space='sell')
    sell_vwap_std = DecimalParameter(0.5, 2.0, default=1.0, decimals=1, space='sell')

    def _rolling_vwap(self, dataframe: DataFrame, window: int = 20) -> DataFrame:
        """Calculate rolling VWAP and standard deviation bands."""
        typical_price = (dataframe['high'] + dataframe['low'] + dataframe['close']) / 3
        tp_volume = typical_price * dataframe['volume']

        cum_tp_vol = tp_volume.rolling(window=window).sum()
        cum_vol = dataframe['volume'].rolling(window=window).sum()

        vwap = cum_tp_vol / cum_vol
        # Rolling std of typical price around VWAP
        vwap_std = typical_price.rolling(window=window).std()

        return vwap, vwap_std

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # VWAP
        vwap, vwap_std = self._rolling_vwap(dataframe, window=20)
        dataframe['vwap'] = vwap
        dataframe['vwap_std'] = vwap_std
        dataframe['vwap_upper_1'] = vwap + vwap_std
        dataframe['vwap_upper_2'] = vwap + 2 * vwap_std
        dataframe['vwap_lower_1'] = vwap - vwap_std
        dataframe['vwap_lower_2'] = vwap - 2 * vwap_std

        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # Volume confirmation
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()

        # ATR for custom stoploss
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        buy_std = self.buy_vwap_std.value
        lower_band = dataframe['vwap'] - buy_std * dataframe['vwap_std']

        dataframe.loc[
            (
                (dataframe['close'] <= lower_band) &
                (dataframe['rsi'] < self.buy_rsi.value) &
                (dataframe['volume'] > dataframe['volume_mean'] * 0.8) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        sell_std = self.sell_vwap_std.value
        upper_band = dataframe['vwap'] + sell_std * dataframe['vwap_std']

        dataframe.loc[
            (
                (dataframe['close'] >= upper_band) |
                (dataframe['rsi'] > self.sell_rsi.value) |
                (
                    (dataframe['close'] >= dataframe['vwap']) &
                    (dataframe['close'].shift(1) < dataframe['vwap'].shift(1))
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
            atr_stop = -(atr * 1.5) / current_rate
            return max(atr_stop, self.stoploss)
        return self.stoploss
