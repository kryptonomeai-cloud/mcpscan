from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta


class MultiIndicatorStrategy(IStrategy):
    """Multi-confirmation strategy: RSI + MACD + Bollinger + EMA.

    Entry: At least 3 of 4 conditions met (relaxed from requiring all 4):
      1. RSI < 40 (approaching oversold)
      2. Price near or below lower BB (within 1%)
      3. MACD histogram positive or turning positive
      4. Price above EMA200 (uptrend filter)

    Exit: RSI > 70 OR price above upper BB OR trailing stop.
    Conservative position sizing (10% per trade, max 5 open trades).
    """

    INTERFACE_VERSION = 3

    minimal_roi = {
        "0": 0.10,     # 10% — let winners run
        "30": 0.03,    # 3% after 30 min
        "60": 0.02,    # 2% after 60 min
        "120": 0.01,   # 1% after 120 min
    }

    stoploss = -0.10

    trailing_stop = True
    trailing_stop_positive = 0.03
    trailing_stop_positive_offset = 0.08
    trailing_only_offset_is_reached = True

    timeframe = '1h'
    startup_candle_count = 200

    max_open_trades = 5

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # Bollinger Bands
        bollinger = ta.BBANDS(dataframe, timeperiod=20, nbdevup=2.0, nbdevdn=2.0)
        dataframe['bb_upper'] = bollinger['upperband']
        dataframe['bb_middle'] = bollinger['middleband']
        dataframe['bb_lower'] = bollinger['lowerband']

        # MACD
        macd = ta.MACD(dataframe, fastperiod=12, slowperiod=26, signalperiod=9)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']
        dataframe['macdhist_prev'] = dataframe['macdhist'].shift(1)

        # EMAs
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)

        # Volume
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()

        # Signal scoring: count how many conditions are met
        # Condition 1: RSI approaching oversold
        dataframe['sig_rsi'] = (dataframe['rsi'] < 40).astype(int)
        # Condition 2: Price near lower BB (within 1% above or below)
        dataframe['sig_bb'] = (dataframe['close'] <= dataframe['bb_lower'] * 1.01).astype(int)
        # Condition 3: MACD histogram positive or turning positive
        dataframe['sig_macd'] = (
            (dataframe['macdhist'] > 0) |
            ((dataframe['macdhist'] > dataframe['macdhist_prev']) & (dataframe['macdhist_prev'] < 0))
        ).astype(int)
        # Condition 4: Price above EMA200 (uptrend)
        dataframe['sig_ema'] = (dataframe['close'] > dataframe['ema200']).astype(int)

        dataframe['signal_score'] = (
            dataframe['sig_rsi'] + dataframe['sig_bb'] +
            dataframe['sig_macd'] + dataframe['sig_ema']
        )

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['signal_score'] >= 3) &    # At least 3 of 4 conditions
                (dataframe['volume'] > dataframe['volume_mean'] * 0.5) &  # Decent volume
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] > 70) |
                (dataframe['close'] >= dataframe['bb_upper'])
            ),
            'exit_long'] = 1
        return dataframe
