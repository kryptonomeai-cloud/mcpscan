from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter, RealParameter
from pandas import DataFrame
import talib.abstract as ta


class MeanReversionStrategy(IStrategy):
    """Mean reversion using Bollinger Bands + RSI + Volume.

    Entry: Price touches lower BB, RSI oversold, volume spike.
    Exit:  Price reaches middle BB or RSI overbought.
    Works well in ranging/bear markets.
    """

    INTERFACE_VERSION = 3

    minimal_roi = {
        "0": 0.06,
        "30": 0.04,
        "60": 0.025,
        "120": 0.015,
        "240": 0.005,
    }

    stoploss = -0.07

    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.04
    trailing_only_offset_is_reached = True

    timeframe = '1h'
    startup_candle_count = 50

    # Hyperopt params
    buy_bb_period = IntParameter(14, 30, default=20, space='buy', optimize=True)
    buy_bb_std = RealParameter(1.5, 3.0, default=2.0, decimals=1, space='buy', optimize=True)
    buy_rsi_threshold = IntParameter(15, 40, default=30, space='buy', optimize=True)
    buy_volume_spike = RealParameter(1.0, 3.0, default=1.5, decimals=1, space='buy', optimize=True)

    sell_rsi_threshold = IntParameter(55, 80, default=70, space='sell', optimize=True)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Bollinger Bands for various periods
        for period in [14, 16, 18, 20, 22, 24, 26, 28, 30]:
            for std in [1.5, 2.0, 2.5, 3.0]:
                bb = ta.BBANDS(dataframe, timeperiod=period, nbdevup=std, nbdevdn=std)
                dataframe[f'bb_upper_{period}_{std}'] = bb['upperband']
                dataframe[f'bb_middle_{period}_{std}'] = bb['middleband']
                dataframe[f'bb_lower_{period}_{std}'] = bb['lowerband']
                dataframe[f'bb_width_{period}_{std}'] = (bb['upperband'] - bb['lowerband']) / bb['middleband']

        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # Volume
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()

        # ATR for volatility
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        period = self.buy_bb_period.value
        # Round to nearest even number for BB
        period = round(period / 2) * 2
        std = round(self.buy_bb_std.value * 2) / 2  # round to nearest 0.5

        lower_col = f'bb_lower_{period}_{std}'
        middle_col = f'bb_middle_{period}_{std}'

        # Fallback if column doesn't exist
        if lower_col not in dataframe.columns:
            lower_col = 'bb_lower_20_2.0'
            middle_col = 'bb_middle_20_2.0'

        dataframe.loc[
            (
                (dataframe['close'] <= dataframe[lower_col]) &
                (dataframe['rsi'] < self.buy_rsi_threshold.value) &
                (dataframe['volume'] > dataframe['volume_mean'] * self.buy_volume_spike.value) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        period = self.buy_bb_period.value
        period = round(period / 2) * 2
        std = round(self.buy_bb_std.value * 2) / 2

        middle_col = f'bb_middle_{period}_{std}'
        if middle_col not in dataframe.columns:
            middle_col = 'bb_middle_20_2.0'

        dataframe.loc[
            (
                (dataframe['close'] >= dataframe[middle_col]) |
                (dataframe['rsi'] > self.sell_rsi_threshold.value)
            ),
            'exit_long'] = 1
        return dataframe
