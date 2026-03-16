"""Funding Rate Arbitrage Strategy - Mean reversion proxy.

Since live funding rate data isn't available in spot backtesting,
this uses a proxy: extreme RSI + volume divergence + price deviation
from moving averages to simulate funding rate mean-reversion signals.

When market is extremely oversold (proxy for negative funding), go long.
When market is extremely overbought (proxy for positive funding), exit.
Combined with Bollinger Band squeeze detection.
"""

from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta
import numpy as np


class FundingRateStrategy(IStrategy):
    INTERFACE_VERSION = 3

    minimal_roi = {
        "0": 0.08,
        "60": 0.04,
        "180": 0.02,
        "480": 0.01
    }

    stoploss = -0.05
    trailing_stop = True
    trailing_stop_positive = 0.015
    trailing_stop_positive_offset = 0.03
    trailing_only_offset_is_reached = True

    timeframe = '1h'
    startup_candle_count = 50

    # Hyperoptable parameters - proxy thresholds for "funding rate"
    buy_rsi = IntParameter(10, 45, default=35, space='buy')
    buy_bb_std = DecimalParameter(1.5, 3.5, default=2.0, decimals=1, space='buy')
    buy_price_dev = DecimalParameter(0.005, 0.05, default=0.01, decimals=3, space='buy')
    sell_rsi = IntParameter(65, 85, default=75, space='sell')
    sell_price_dev = DecimalParameter(0.01, 0.05, default=0.02, decimals=2, space='sell')

    def _funding_rate_proxy(self, dataframe: DataFrame) -> DataFrame:
        """Create a proxy for funding rate based on:
        - Price deviation from long EMA (extreme deviation = extreme funding)
        - RSI extremes
        - Volume spike (panic selling/buying)
        Returns a synthetic 'funding_rate' between -1 and 1
        """
        ema50 = ta.EMA(dataframe, timeperiod=50)
        price_dev = (dataframe['close'] - ema50) / ema50

        rsi = dataframe['rsi']
        rsi_norm = (rsi - 50) / 50  # -1 to 1

        # Volume spike detection
        vol_ratio = dataframe['volume'] / dataframe['volume'].rolling(20).mean()
        vol_signal = vol_ratio.clip(upper=3.0) / 3.0  # 0 to 1

        # Combine: negative = oversold/negative funding, positive = overbought/positive funding
        funding_proxy = (price_dev * 10 + rsi_norm) / 2
        # Amplify when volume is high (more conviction)
        funding_proxy = funding_proxy * (0.5 + 0.5 * vol_signal)

        return funding_proxy.clip(-1, 1)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # Funding rate proxy
        dataframe['funding_proxy'] = self._funding_rate_proxy(dataframe)

        # Bollinger Bands for squeeze detection
        bb = ta.BBANDS(dataframe, timeperiod=20, nbdevup=2.0, nbdevdn=2.0)
        dataframe['bb_upper'] = bb['upperband']
        dataframe['bb_lower'] = bb['lowerband']
        dataframe['bb_mid'] = bb['middleband']
        dataframe['bb_width'] = (bb['upperband'] - bb['lowerband']) / bb['middleband']

        # Price deviation from EMA50
        dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)
        dataframe['price_dev'] = (dataframe['close'] - dataframe['ema50']) / dataframe['ema50']

        # ATR
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)

        # Volume
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()

        # MACD for trend confirmation
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macd_signal'] = macd['macdsignal']
        dataframe['macd_hist'] = macd['macdhist']

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Funding proxy negative (like negative funding = shorts paying longs)
                (dataframe['funding_proxy'] < -0.15) &
                # RSI oversold
                (dataframe['rsi'] < self.buy_rsi.value) &
                # Price below EMA
                (dataframe['price_dev'] < -self.buy_price_dev.value) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Funding proxy positive (like positive funding = longs paying shorts)
                (dataframe['funding_proxy'] > 0.3) |
                # RSI overbought
                (dataframe['rsi'] > self.sell_rsi.value) |
                # Price well above EMA
                (dataframe['price_dev'] > self.sell_price_dev.value) |
                # MACD bearish crossover
                (
                    (dataframe['macd_hist'] < 0) &
                    (dataframe['macd_hist'].shift(1) > 0)
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
