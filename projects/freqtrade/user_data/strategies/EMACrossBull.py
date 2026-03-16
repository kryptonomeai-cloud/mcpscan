from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta


class EMACrossBull(IStrategy):
    """Bull-market variant of EMACrossOptimised.

    Key changes from EMACrossOptimised (bear/sideways optimised):
    - Shorter EMA periods (5/21/100 vs 7/44/150) for faster trend following
    - Tighter ROI targets to capture gains more frequently
    - Less aggressive trailing stop (wider offset, gentler trail)
    - Volume confirmation filter (above-average volume required)
    - Higher RSI exit threshold (let momentum run in bulls)
    - ADX filter to confirm trend strength

    Designed for trending/bull market conditions.
    """

    INTERFACE_VERSION = 3

    # Tighter ROI - capture gains more frequently in bull runs
    minimal_roi = {
        "0": 0.15,       # 15% max target (was 49.1%)
        "120": 0.08,     # 8% after 2h (was 9.3% after 5.5h)
        "360": 0.04,     # 4% after 6h (was 6% after 17h)
        "720": 0.02,     # 2% after 12h
        "1440": 0        # breakeven after 24h
    }

    # Tighter stoploss - less tolerance needed in bull markets
    stoploss = -0.15  # was -0.252

    # Less aggressive trailing stop - let winners ride in uptrends
    trailing_stop = True
    trailing_stop_positive = 0.03      # trail at 3% (was 5.4%)
    trailing_stop_positive_offset = 0.06  # activate after 6% gain (was 13%)
    trailing_only_offset_is_reached = True

    timeframe = '1h'
    startup_candle_count = 200

    max_open_trades = 5

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Shorter EMAs for faster trend detection in bull markets
        dataframe['ema5'] = ta.EMA(dataframe, timeperiod=5)
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema100'] = ta.EMA(dataframe, timeperiod=100)

        # RSI for momentum
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # ADX for trend strength confirmation
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)

        # Volume analysis
        dataframe['volume_mean_20'] = dataframe['volume'].rolling(window=20).mean()
        dataframe['volume_mean_5'] = dataframe['volume'].rolling(window=5).mean()

        # MACD for momentum confirmation
        macd = ta.MACD(dataframe, fastperiod=12, slowperiod=26, signalperiod=9)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # EMA crossover (fast crosses above slow)
                (dataframe['ema5'] > dataframe['ema21']) &
                (dataframe['ema5'].shift(1) <= dataframe['ema21'].shift(1)) &

                # Price above long-term trend
                (dataframe['close'] > dataframe['ema100']) &

                # Trend strength: ADX > 20 confirms a real trend
                (dataframe['adx'] > 20) &

                # RSI in healthy range (not oversold, not overbought)
                (dataframe['rsi'] > 30) &
                (dataframe['rsi'] < 70) &

                # Volume confirmation: current vol above 20-period average
                # and short-term vol accelerating (5-bar avg > 20-bar avg)
                (dataframe['volume'] > dataframe['volume_mean_20'] * 1.2) &
                (dataframe['volume_mean_5'] > dataframe['volume_mean_20']) &

                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (
                    # EMA death cross
                    (dataframe['ema5'] < dataframe['ema21']) &
                    (dataframe['ema5'].shift(1) >= dataframe['ema21'].shift(1))
                ) |
                # RSI overbought - higher threshold for bull markets (was 62)
                (dataframe['rsi'] > 78) |
                # Price dropped below long-term trend (trend reversal)
                (
                    (dataframe['close'] < dataframe['ema100']) &
                    (dataframe['close'].shift(1) >= dataframe['ema100'].shift(1))
                )
            ),
            'exit_long'] = 1
        return dataframe
