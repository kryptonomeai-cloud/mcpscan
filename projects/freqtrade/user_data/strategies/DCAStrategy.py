from freqtrade.strategy import IStrategy, IntParameter, RealParameter
from freqtrade.persistence import Trade
from pandas import DataFrame
import talib.abstract as ta
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DCAStrategy(IStrategy):
    """Dollar Cost Averaging strategy.

    Entry: RSI oversold near Bollinger lower band.
    DCA:   Scale into positions at drawdown levels.
    Exit:  Take profit at mean reversion targets or trailing stop.
    """

    INTERFACE_VERSION = 3

    minimal_roi = {
        "0": 0.06,
        "60": 0.04,
        "120": 0.025,
        "240": 0.01,
    }

    stoploss = -0.15

    trailing_stop = True
    trailing_stop_positive = 0.015
    trailing_stop_positive_offset = 0.03
    trailing_only_offset_is_reached = True

    timeframe = '1h'
    startup_candle_count = 30

    position_adjustment_enable = True
    max_entry_position_adjustment = 3

    # Hyperopt params
    buy_rsi_threshold = IntParameter(20, 45, default=35, space='buy', optimize=True)
    buy_bb_offset = RealParameter(0.95, 1.02, default=1.0, decimals=2, space='buy', optimize=True)

    sell_rsi_threshold = IntParameter(55, 80, default=65, space='sell', optimize=True)

    # DCA levels
    dca_level_1 = RealParameter(-0.02, -0.05, default=-0.03, decimals=2, space='buy', optimize=True)
    dca_level_2 = RealParameter(-0.04, -0.08, default=-0.06, decimals=2, space='buy', optimize=True)
    dca_level_3 = RealParameter(-0.07, -0.12, default=-0.09, decimals=2, space='buy', optimize=True)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # Bollinger Bands
        bb = ta.BBANDS(dataframe, timeperiod=20, nbdevup=2.0, nbdevdn=2.0)
        dataframe['bb_upper'] = bb['upperband']
        dataframe['bb_middle'] = bb['middleband']
        dataframe['bb_lower'] = bb['lowerband']

        # EMA
        dataframe['ema20'] = ta.EMA(dataframe, timeperiod=20)

        # Volume
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] < self.buy_rsi_threshold.value) &
                (dataframe['close'] < dataframe['bb_lower'] * self.buy_bb_offset.value) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] > self.sell_rsi_threshold.value) |
                (dataframe['close'] > dataframe['bb_upper'])
            ),
            'exit_long'] = 1
        return dataframe

    def adjust_trade_position(self, trade: Trade, current_time: datetime,
                              current_rate: float, current_profit: float,
                              min_stake: float | None, max_stake: float | None,
                              current_entry_rate: float, current_exit_rate: float,
                              current_entry_profit: float, current_exit_profit: float,
                              **kwargs) -> float | None | tuple[float | None, str]:
        """Scale into position at defined DCA levels."""
        if current_profit > self.dca_level_1.value:
            return None

        filled_entries = trade.nr_of_successful_entries
        stake_amount = trade.stake_amount / filled_entries  # Original stake

        if filled_entries == 1 and current_profit <= self.dca_level_1.value:
            return stake_amount
        elif filled_entries == 2 and current_profit <= self.dca_level_2.value:
            return stake_amount * 1.5
        elif filled_entries == 3 and current_profit <= self.dca_level_3.value:
            return stake_amount * 2.0

        return None
