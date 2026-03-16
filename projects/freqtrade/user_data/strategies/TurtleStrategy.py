"""
Donchian Channel + Turtle Trading Strategy

Based on the legendary Turtle Trading system by Richard Dennis.
Entry: breakout above N-period Donchian high
Exit:  breakdown below shorter Donchian low
Pyramiding via adjust_trade_position

Periods are in candles (not days) for timeframe flexibility.
"""

from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta
import numpy as np


class TurtleStrategy(IStrategy):

    INTERFACE_VERSION = 3

    minimal_roi = {
        "0": 0.50,  # Let the Donchian exit manage exits
    }

    stoploss = -0.15  # Wide stop — trend following needs room

    timeframe = '1h'
    startup_candle_count = 500

    position_adjustment_enable = True

    # --- Hyperoptable parameters ---
    # Donchian periods in candles
    entry_period = IntParameter(48, 480, default=120, space='buy', optimize=True)  # ~5-20 days on 1h
    exit_period = IntParameter(24, 240, default=60, space='sell', optimize=True)   # ~1-10 days on 1h
    atr_period = IntParameter(10, 30, default=20, space='buy', optimize=True)
    atr_sl_multiplier = DecimalParameter(2.0, 6.0, default=3.0, decimals=1, space='buy', optimize=True)
    max_pyramid_units = IntParameter(1, 6, default=4, space='buy', optimize=True)
    pyramid_atr_step = DecimalParameter(0.3, 1.5, default=0.5, decimals=1, space='buy', optimize=True)

    use_custom_stoploss = True

    def custom_stoploss(self, pair: str, trade, current_time, current_rate, current_profit, **kwargs):
        """ATR-based trailing stop — wide for trend following."""
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

    def adjust_trade_position(self, trade, current_time, current_rate, current_profit,
                               min_stake, max_stake, current_entry_rate, current_exit_rate,
                               current_exit_profit, **kwargs):
        """Turtle pyramiding: add to winners."""
        if trade.nr_of_successful_entries >= self.max_pyramid_units.value:
            return None

        dataframe, _ = self.dp.get_analyzed_dataframe(trade.pair, self.timeframe)
        if len(dataframe) < 1:
            return None

        last = dataframe.iloc[-1]
        atr = last.get('atr', 0)
        if atr <= 0:
            return None

        if current_profit < 0.005:
            return None

        step = atr * self.pyramid_atr_step.value
        required_price = trade.open_rate + (step * trade.nr_of_successful_entries)

        if current_rate >= required_price:
            try:
                stake = trade.stake_amount / trade.nr_of_successful_entries
                stake = min(stake, max_stake)
                stake = max(stake, min_stake)
                return stake
            except Exception:
                return None

        return None

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Donchian channels for various candle periods
        for period in [24, 48, 72, 96, 120, 168, 240, 336, 480]:
            dataframe[f'dc_upper_{period}'] = dataframe['high'].rolling(window=period).max()
            dataframe[f'dc_lower_{period}'] = dataframe['low'].rolling(window=period).min()
            dataframe[f'dc_mid_{period}'] = (
                dataframe[f'dc_upper_{period}'] + dataframe[f'dc_lower_{period}']
            ) / 2

        # ATR
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=20)

        # Trend filter
        dataframe['ema_50'] = ta.EMA(dataframe, timeperiod=50)
        dataframe['ema_200'] = ta.EMA(dataframe, timeperiod=200)

        # Volume
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        entry_p = self.entry_period.value
        # Snap to nearest available period
        available = [24, 48, 72, 96, 120, 168, 240, 336, 480]
        entry_p = min(available, key=lambda x: abs(x - entry_p))
        upper_col = f'dc_upper_{entry_p}'

        # Breakout above previous Donchian high
        prev_upper = dataframe[upper_col].shift(1)

        dataframe.loc[
            (
                (dataframe['close'] > prev_upper) &
                (dataframe['volume'] > dataframe['volume_mean'] * 0.5) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        exit_p = self.exit_period.value
        available = [24, 48, 72, 96, 120, 168, 240, 336, 480]
        exit_p = min(available, key=lambda x: abs(x - exit_p))
        lower_col = f'dc_lower_{exit_p}'

        prev_lower = dataframe[lower_col].shift(1)

        dataframe.loc[
            (
                (dataframe['close'] < prev_lower)
            ),
            'exit_long'] = 1

        return dataframe
