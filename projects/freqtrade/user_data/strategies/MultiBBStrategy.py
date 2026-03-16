"""Multi-Bollinger Bands Strategy - Inspired by Bandtastic.

4 levels of Bollinger Bands (1σ, 2σ, 3σ, 4σ) with MFI confirmation.
Scale entries at different band levels. Hyperoptable buy/sell triggers.
"""

from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta
import numpy as np


class MultiBBStrategy(IStrategy):
    INTERFACE_VERSION = 3

    minimal_roi = {
        "0": 0.10,
        "60": 0.05,
        "180": 0.03,
        "360": 0.01
    }

    stoploss = -0.10
    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.04
    trailing_only_offset_is_reached = True

    timeframe = '1h'
    startup_candle_count = 40

    # Hyperoptable parameters
    buy_bb_level = IntParameter(1, 4, default=2, space='buy')  # Which BB level triggers entry
    buy_mfi = IntParameter(10, 60, default=40, space='buy')
    buy_rsi = IntParameter(15, 50, default=40, space='buy')
    sell_bb_level = IntParameter(1, 3, default=2, space='sell')
    sell_mfi = IntParameter(60, 90, default=80, space='sell')

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Bollinger Bands at 4 sigma levels
        for std in [1.0, 2.0, 3.0, 4.0]:
            bb = ta.BBANDS(dataframe, timeperiod=20, nbdevup=std, nbdevdn=std, matype=0)
            std_int = int(std)
            dataframe[f'bb_upper_{std_int}'] = bb['upperband']
            dataframe[f'bb_mid'] = bb['middleband']  # Same for all
            dataframe[f'bb_lower_{std_int}'] = bb['lowerband']

        # MFI - Money Flow Index
        dataframe['mfi'] = ta.MFI(dataframe, timeperiod=14)

        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # ATR
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)

        # Volume
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()

        # BB width for volatility filter
        dataframe['bb_width'] = (dataframe['bb_upper_2'] - dataframe['bb_lower_2']) / dataframe['bb_mid']

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        level = self.buy_bb_level.value
        lower_key = f'bb_lower_{level}'

        dataframe.loc[
            (
                # Price at or below the selected BB level
                (dataframe['close'] <= dataframe[lower_key]) &
                # MFI oversold
                (dataframe['mfi'] < self.buy_mfi.value) &
                # RSI oversold
                (dataframe['rsi'] < self.buy_rsi.value) &
                # Minimum volatility (BB not too narrow)
                (dataframe['bb_width'] > 0.02) &
                # Volume
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        level = self.sell_bb_level.value
        upper_key = f'bb_upper_{level}'

        dataframe.loc[
            (
                # Price at or above the selected BB level
                (dataframe['close'] >= dataframe[upper_key]) |
                # MFI overbought
                (dataframe['mfi'] > self.sell_mfi.value)
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
