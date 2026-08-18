# ============================================================
# NIFTYBEES vs GOLDBEES ROTATION STRATEGY
# ============================================================

from src.data_loader import load_data
from src.signals import generate_signals
from src.backtest import (
    calculate_returns,
    run_backtest,
    calculate_equity,
)
from src.performance import calculate_performance
from src.benchmarks import (
    calculate_single_asset_benchmark,
    calculate_50_50_benchmark,
)
from src.trade_analysis import analyze_trades
from src.robustness import run_robustness_test
from src.validation import (
    run_out_of_sample_test,
    run_walk_forward_test,
)
from src.regime import (
    classify_market_regime,
    analyze_regimes,
)
from src.reporting import (
    save_results,
    print_summary,
)
from src.visualization import (
    plot_equity_curves,
    plot_strategy_drawdown,
    plot_robustness,
)


# ============================================================
# SETTINGS
# ============================================================

INITIAL_CAPITAL = 100_000

TRANSACTION_COST = 0.001

SLIPPAGE = 0.0005

EXECUTION_COST = (
    TRANSACTION_COST + SLIPPAGE
)

LOOKBACK = 20

LOOKBACK_PERIODS = [
    10,
    15,
    20,
    30,
    40,
    60,
]

VALIDATION_LOOKBACK = 15

WALK_FORWARD_LOOKBACK = 15


# ============================================================
# DATA + STRATEGY
# ============================================================

data = load_data()

data = generate_signals(
    data,
    lookback=LOOKBACK,
)

data = calculate_returns(
    data
)

data = run_backtest(
    data,
    transaction_cost=TRANSACTION_COST,
    slippage=SLIPPAGE,
)

data = calculate_equity(
    data,
    initial_capital=INITIAL_CAPITAL,
)


# ============================================================
# PERFORMANCE
# ============================================================

performance = calculate_performance(
    data,
    initial_capital=INITIAL_CAPITAL,
)


# ============================================================
# BENCHMARKS
# ============================================================

years = (
    data["time"].iloc[-2]
    - data["time"].iloc[0]
).days / 365.25


nifty_benchmark = (
    calculate_single_asset_benchmark(
        data["nifty_return"],
        INITIAL_CAPITAL,
        years,
    )
)


gold_benchmark = (
    calculate_single_asset_benchmark(
        data["gold_return"],
        INITIAL_CAPITAL,
        years,
    )
)


balanced_benchmark = (
    calculate_50_50_benchmark(
        data,
        INITIAL_CAPITAL,
        EXECUTION_COST,
    )
)


# ============================================================
# TRADE ANALYSIS
# ============================================================

trades = analyze_trades(
    data
)

number_of_trades = (
    data["position"]
    .ne(data["position"].shift())
    .sum()
    - 1
)


# ============================================================
# PARAMETER ROBUSTNESS
# ============================================================

robustness_results = run_robustness_test(
    data,
    lookback_periods=LOOKBACK_PERIODS,
    initial_capital=INITIAL_CAPITAL,
    transaction_cost=TRANSACTION_COST,
    slippage=SLIPPAGE,
)


# ============================================================
# OUT-OF-SAMPLE VALIDATION
# ============================================================

validation = run_out_of_sample_test(
    data,
    lookback=VALIDATION_LOOKBACK,
    initial_capital=INITIAL_CAPITAL,
    transaction_cost=TRANSACTION_COST,
    slippage=SLIPPAGE,
    train_ratio=0.70,
)


# ============================================================
# WALK-FORWARD VALIDATION
# ============================================================

walk_forward_results = run_walk_forward_test(
    data,
    lookback=WALK_FORWARD_LOOKBACK,
    initial_capital=INITIAL_CAPITAL,
    transaction_cost=TRANSACTION_COST,
    slippage=SLIPPAGE,
)


# ============================================================
# MARKET REGIME
# ============================================================

regime_data = classify_market_regime(
    data
)

regime_results = analyze_regimes(
    regime_data
)


# ============================================================
# SAVE RESULTS
# ============================================================

save_results(
    performance=performance,
    trades=trades,
    nifty_benchmark=nifty_benchmark,
    gold_benchmark=gold_benchmark,
    balanced_benchmark=balanced_benchmark,
    robustness_results=robustness_results,
    validation=validation,
    regime_results=regime_results,
)


# ============================================================
# VISUALIZATION
# ============================================================

plot_equity_curves(
    dates=data["time"],
    strategy_equity=data["equity"],
    nifty_equity=nifty_benchmark["equity"],
    gold_equity=gold_benchmark["equity"],
    balanced_equity=balanced_benchmark["equity"],
)

plot_strategy_drawdown(
    dates=data["time"],
    strategy_equity=data["equity"],
)

plot_robustness(
    robustness_results=robustness_results,
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print_summary(
    performance=performance,
    trades=trades,
    nifty_benchmark=nifty_benchmark,
    gold_benchmark=gold_benchmark,
    balanced_benchmark=balanced_benchmark,
    initial_capital=INITIAL_CAPITAL,
    transaction_cost=TRANSACTION_COST,
    slippage=SLIPPAGE,
    number_of_trades=number_of_trades,
)