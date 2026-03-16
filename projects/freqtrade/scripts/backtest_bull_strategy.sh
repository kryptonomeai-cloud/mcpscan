#!/usr/bin/env bash
# Backtest EMACrossBull strategy against BTC/USDT, ETH/USDT, SOL/USDT on 1h timeframe
# Compares against EMACrossOptimised (bear/sideways baseline)
#
# Usage: ./scripts/backtest_bull_strategy.sh [--download]
#
# Prerequisites:
#   - freqtrade installed and accessible
#   - Data downloaded for the pairs (use --download flag to fetch)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG="$PROJECT_DIR/user_data/config_backtest.json"
STRATEGY_DIR="$PROJECT_DIR/user_data/strategies"
RESULTS_DIR="$PROJECT_DIR/user_data/backtest_results"

# Backtest date range - use a bull-market period for meaningful comparison
# Adjust these dates to match available data
TIMERANGE="20250901-20260314"
TIMEFRAME="1h"

mkdir -p "$RESULTS_DIR"

echo "================================================"
echo "  EMACrossBull Backtest Suite"
echo "  Pairs: BTC/USDT, ETH/USDT, SOL/USDT"
echo "  Timeframe: $TIMEFRAME"
echo "  Range: $TIMERANGE"
echo "================================================"
echo ""

# Download data if requested
if [[ "${1:-}" == "--download" ]]; then
    echo "📥 Downloading market data..."
    freqtrade download-data \
        --config "$CONFIG" \
        --timeframe "$TIMEFRAME" \
        --timerange "$TIMERANGE" \
        --pairs BTC/USDT ETH/USDT SOL/USDT
    echo ""
fi

# Run backtest for EMACrossBull (new bull-market strategy)
echo "🐂 Backtesting EMACrossBull..."
echo "---"
freqtrade backtesting \
    --config "$CONFIG" \
    --strategy EMACrossBull \
    --strategy-path "$STRATEGY_DIR" \
    --timeframe "$TIMEFRAME" \
    --timerange "$TIMERANGE" \
    --enable-protections \
    2>&1 | tee "$RESULTS_DIR/EMACrossBull_results.txt"

echo ""
echo "================================================"
echo ""

# Run backtest for EMACrossOptimised (baseline comparison)
echo "📊 Backtesting EMACrossOptimised (baseline)..."
echo "---"
freqtrade backtesting \
    --config "$CONFIG" \
    --strategy EMACrossOptimised \
    --strategy-path "$STRATEGY_DIR" \
    --timeframe "$TIMEFRAME" \
    --timerange "$TIMERANGE" \
    --enable-protections \
    2>&1 | tee "$RESULTS_DIR/EMACrossOptimised_results.txt"

echo ""
echo "================================================"
echo "  Backtest Complete!"
echo "  Results saved to: $RESULTS_DIR/"
echo "================================================"
echo ""
echo "Compare the two strategies above."
echo "Key metrics to watch:"
echo "  - Total profit %"
echo "  - Win rate"
echo "  - Max drawdown"
echo "  - Profit factor"
echo "  - Number of trades (bull strategy should trade more)"
