"""
Correlation Regime Strategy

Monitors BTC/ETH correlation to detect regime changes.
When correlation breaks down, trades the divergence.

High correlation (>0.7): trend-following mode (follow BTC direction)
Low correlation (<0.5): mean-reversion mode (trade relative strength)
"""

from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta
import numpy as np


class CorrelationRegimeStrategy(IStrategy):

    INTERFACE_VERSION = 3

    minimal_roi = {
        "0": 0.10,
        "60": 0.05,
        "180": 0.03,
        "360": 0.01,
    }

    stoploss = -0.08

    timeframe = '1h'
    startup_candle_count = 200

    # --- Hyperoptable parameters ---
    corr_lookback = IntParameter(12, 72, default=24, space='buy', optimize=True)
    corr_low_threshold = DecimalParameter(0.2, 0.7, default=0.5, decimals=1, space='buy', optimize=True)
    corr_high_threshold = DecimalParameter(0.6, 0.95, default=0.7, decimals=1, space='buy', optimize=True)
    relative_strength_period = IntParameter(6, 30, default=12, space='buy', optimize=True)
    atr_sl_multiplier = DecimalParameter(1.5, 4.0, default=2.5, decimals=1, space='buy', optimize=True)
    rsi_entry = IntParameter(20, 45, default=35, space='buy', optimize=True)
    rsi_exit = IntParameter(55, 80, default=65, space='sell', optimize=True)

    use_custom_stoploss = True

    def informative_pairs(self):
        """Get BTC/USDT data for correlation analysis."""
        return [("BTC/USDT", self.timeframe)]

    def custom_stoploss(self, pair: str, trade, current_time, current_rate, current_profit, **kwargs):
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

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        pair = metadata['pair']

        # Standard indicators on current pair
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        dataframe['ema_20'] = ta.EMA(dataframe, timeperiod=20)
        dataframe['ema_50'] = ta.EMA(dataframe, timeperiod=50)

        # Returns for correlation
        dataframe['returns'] = dataframe['close'].pct_change()

        # Get BTC data for correlation
        if pair != "BTC/USDT":
            btc_dataframe = self.dp.get_pair_dataframe("BTC/USDT", self.timeframe)
            if len(btc_dataframe) > 0:
                btc_dataframe = btc_dataframe.rename(columns={
                    'close': 'btc_close',
                    'volume': 'btc_volume',
                })
                btc_dataframe['btc_returns'] = btc_dataframe['btc_close'].pct_change()

                # Merge BTC data
                dataframe = dataframe.merge(
                    btc_dataframe[['date', 'btc_close', 'btc_returns']],
                    on='date', how='left'
                )

                # Rolling correlation for multiple lookbacks
                for period in [12, 18, 24, 36, 48, 72]:
                    dataframe[f'corr_{period}'] = (
                        dataframe['returns']
                        .rolling(window=period)
                        .corr(dataframe['btc_returns'])
                    )

                # Relative strength: pair performance vs BTC
                for period in [6, 12, 18, 24, 30]:
                    pair_perf = dataframe['close'].pct_change(period)
                    btc_perf = dataframe['btc_close'].pct_change(period)
                    dataframe[f'rel_strength_{period}'] = pair_perf - btc_perf

                # BTC trend
                dataframe['btc_ema_20'] = dataframe['btc_close'].ewm(span=20).mean()
                dataframe['btc_trend_up'] = (dataframe['btc_close'] > dataframe['btc_ema_20']).astype(int)
            else:
                # Fallback: no BTC data available
                for period in [12, 18, 24, 36, 48, 72]:
                    dataframe[f'corr_{period}'] = 0.5
                for period in [6, 12, 18, 24, 30]:
                    dataframe[f'rel_strength_{period}'] = 0
                dataframe['btc_close'] = dataframe['close']
                dataframe['btc_returns'] = 0
                dataframe['btc_trend_up'] = 1
        else:
            # Trading BTC itself — use EMA crossover as fallback
            for period in [12, 18, 24, 36, 48, 72]:
                dataframe[f'corr_{period}'] = 1.0
            for period in [6, 12, 18, 24, 30]:
                dataframe[f'rel_strength_{period}'] = 0
            dataframe['btc_close'] = dataframe['close']
            dataframe['btc_returns'] = dataframe['returns']
            dataframe['btc_trend_up'] = (dataframe['close'] > dataframe['ema_20']).astype(int)

        # Volume
        dataframe['volume_mean'] = dataframe['volume'].rolling(window=20).mean()

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Snap correlation lookback
        valid_periods = [12, 18, 24, 36, 48, 72]
        corr_period = min(valid_periods, key=lambda x: abs(x - self.corr_lookback.value))
        corr_col = f'corr_{corr_period}'

        rs_period = min([6, 12, 18, 24, 30], key=lambda x: abs(x - self.relative_strength_period.value))
        rs_col = f'rel_strength_{rs_period}'

        if corr_col not in dataframe.columns:
            corr_col = 'corr_24'
        if rs_col not in dataframe.columns:
            rs_col = 'rel_strength_12'

        # Low correlation regime: mean-reversion / relative strength
        low_corr_buy = (
            (dataframe[corr_col] < self.corr_low_threshold.value) &
            (dataframe[rs_col] > 0) &  # Pair outperforming BTC
            (dataframe['rsi'] < self.rsi_entry.value) &
            (dataframe['volume'] > 0)
        )

        # High correlation regime: trend-following
        high_corr_buy = (
            (dataframe[corr_col] > self.corr_high_threshold.value) &
            (dataframe['btc_trend_up'] == 1) &
            (dataframe['close'] > dataframe['ema_20']) &
            (dataframe['ema_20'] > dataframe['ema_50']) &
            (dataframe['rsi'] < 60) &
            (dataframe['volume'] > 0)
        )

        dataframe.loc[low_corr_buy | high_corr_buy, 'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        corr_period = min([12, 18, 24, 36, 48, 72], key=lambda x: abs(x - self.corr_lookback.value))
        corr_col = f'corr_{corr_period}'

        rs_period = min([6, 12, 18, 24, 30], key=lambda x: abs(x - self.relative_strength_period.value))
        rs_col = f'rel_strength_{rs_period}'

        if corr_col not in dataframe.columns:
            corr_col = 'corr_24'
        if rs_col not in dataframe.columns:
            rs_col = 'rel_strength_12'

        # Low correlation exit: relative strength fading
        low_corr_exit = (
            (dataframe[corr_col] < self.corr_low_threshold.value) &
            (dataframe[rs_col] < -0.01)
        )

        # High correlation exit: trend break
        high_corr_exit = (
            (dataframe[corr_col] > self.corr_high_threshold.value) &
            (
                (dataframe['close'] < dataframe['ema_50']) |
                (dataframe['rsi'] > self.rsi_exit.value)
            )
        )

        # General overbought exit
        overbought = dataframe['rsi'] > 75

        dataframe.loc[low_corr_exit | high_corr_exit | overbought, 'exit_long'] = 1

        return dataframe
