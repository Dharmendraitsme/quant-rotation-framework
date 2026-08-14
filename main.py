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


# ============================================================
# 1. LOAD DATA
# ============================================================

data = load_data()


# ============================================================
# 2. GENERATE SIGNALS
# ============================================================

data = generate_signals(
    data,
    lookback=LOOKBACK,
)


# ============================================================
# 3. CALCULATE ASSET RETURNS
# ============================================================

data = calculate_returns(
    data
)


# ============================================================
# 4. RUN BACKTEST
# ============================================================

data = run_backtest(
    data,
    transaction_cost=TRANSACTION_COST,
    slippage=SLIPPAGE,
)


# ============================================================
# 5. CALCULATE EQUITY
# ============================================================

data = calculate_equity(
    data,
    initial_capital=INITIAL_CAPITAL,
)


# ============================================================
# 6. STRATEGY PERFORMANCE
# ============================================================

performance = calculate_performance(
    data,
    initial_capital=INITIAL_CAPITAL,
)


# ============================================================
# 7. BENCHMARKS
# ============================================================

nifty_benchmark = (
    calculate_single_asset_benchmark(
        data["nifty_return"],
        INITIAL_CAPITAL,
        (
            data["time"].iloc[-2]
            - data["time"].iloc[0]
        ).days / 365.25,
    )
)

gold_benchmark = (
    calculate_single_asset_benchmark(
        data["gold_return"],
        INITIAL_CAPITAL,
        (
            data["time"].iloc[-2]
            - data["time"].iloc[0]
        ).days / 365.25,
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
# 8. TRADE ANALYSIS
# ============================================================

trades = analyze_trades(
    data
)


# ============================================================
# 9. POSITION CHANGES
# ============================================================

number_of_trades = (
    data["position"]
    .ne(data["position"].shift())
    .sum()
    - 1
)


# ============================================================
# 10. RESULTS
# ============================================================

print()
print("=" * 60)
print("NIFTYBEES vs GOLDBEES ROTATION STRATEGY")
print("=" * 60)


# ============================================================
# TRADING ASSUMPTIONS
# ============================================================

print()
print("Trading Assumptions")
print("--------------------")

print(
    f"Initial Capital       : "
    f"₹{INITIAL_CAPITAL:,.2f}"
)

print(
    f"Transaction Cost      : "
    f"{TRANSACTION_COST:.2%}"
)

print(
    f"Slippage              : "
    f"{SLIPPAGE:.2%}"
)

print(
    f"Total Execution Cost  : "
    f"{EXECUTION_COST:.2%}"
)

print(
    f"Position Changes      : "
    f"{number_of_trades}"
)


# ============================================================
# ROTATION STRATEGY
# ============================================================

print()
print("Rotation Strategy")
print("--------------------")

print(
    f"Final Equity          : "
    f"₹{performance['final_equity']:,.2f}"
)

print(
    f"Absolute Return       : "
    f"{performance['absolute_return']:.2%}"
)

print(
    f"CAGR                  : "
    f"{performance['cagr']:.2%}"
)

print(
    f"Annualized Volatility : "
    f"{performance['volatility']:.2%}"
)

print(
    f"Sharpe Ratio          : "
    f"{performance['sharpe']:.2f}"
)

print(
    f"Sortino Ratio         : "
    f"{performance['sortino']:.2f}"
)

print(
    f"Calmar Ratio          : "
    f"{performance['calmar']:.2f}"
)

print(
    f"Max Drawdown          : "
    f"{performance['max_drawdown']:.2%}"
)

print(
    f"Max Drawdown Duration : "
    f"{performance['max_drawdown_duration']} "
    f"trading days"
)


# ============================================================
# TRADE ANALYSIS
# ============================================================

print()
print("Trade Analysis")
print("--------------------")

print(
    f"Completed Trades      : "
    f"{trades['completed_trades']}"
)

print(
    f"Winning Trades        : "
    f"{trades['winning_trades']}"
)

print(
    f"Losing Trades         : "
    f"{trades['losing_trades']}"
)

print(
    f"Win Rate              : "
    f"{trades['win_rate']:.2%}"
)

print(
    f"Average Trade Return  : "
    f"{trades['average_trade_return']:.2%}"
)

print(
    f"Gross Profit          : "
    f"{trades['gross_profit']:.2%}"
)

print(
    f"Gross Loss            : "
    f"{trades['gross_loss']:.2%}"
)

print(
    f"Profit Factor         : "
    f"{trades['profit_factor']:.2f}"
)

print(
    f"Average Winning Trade : "
    f"{trades['average_winning_trade']:.2%}"
)

print(
    f"Average Losing Trade  : "
    f"{trades['average_losing_trade']:.2%}"
)

print(
    f"Trade Expectancy      : "
    f"{trades['expectancy']:.2%}"
)

print(
    f"Average Holding Period: "
    f"{trades['average_holding_period']:.1f} "
    f"calendar days"
)

print(
    f"Best Trade            : "
    f"{trades['best_trade']:.2%}"
)

print(
    f"Worst Trade           : "
    f"{trades['worst_trade']:.2%}"
)


# ============================================================
# ASSET TRADE ANALYSIS
# ============================================================

print()
print("Asset Trade Analysis")
print("--------------------")

print(
    f"NIFTYBEES Trades      : "
    f"{trades['nifty_trade_count']}"
)

print(
    f"NIFTYBEES Win Rate    : "
    f"{trades['nifty_win_rate']:.2%}"
)

print(
    f"NIFTYBEES Avg Return  : "
    f"{trades['nifty_average_trade']:.2%}"
)

print(
    f"NIFTYBEES Avg Holding : "
    f"{trades['average_nifty_holding']:.1f} days"
)

print()

print(
    f"GOLDBEES Trades       : "
    f"{trades['gold_trade_count']}"
)

print(
    f"GOLDBEES Win Rate     : "
    f"{trades['gold_win_rate']:.2%}"
)

print(
    f"GOLDBEES Avg Return   : "
    f"{trades['gold_average_trade']:.2%}"
)

print(
    f"GOLDBEES Avg Holding  : "
    f"{trades['average_gold_holding']:.1f} days"
)


# ============================================================
# BENCHMARKS
# ============================================================

print()
print("Benchmarks")
print("--------------------")

print(
    f"NIFTYBEES Final Equity : "
    f"₹{nifty_benchmark['final_equity']:,.2f}"
)

print(
    f"NIFTYBEES CAGR         : "
    f"{nifty_benchmark['cagr']:.2%}"
)

print(
    f"NIFTYBEES Volatility   : "
    f"{nifty_benchmark['volatility']:.2%}"
)

print(
    f"NIFTYBEES Sharpe       : "
    f"{nifty_benchmark['sharpe']:.2f}"
)

print(
    f"NIFTYBEES Sortino      : "
    f"{nifty_benchmark['sortino']:.2f}"
)

print(
    f"NIFTYBEES Max Drawdown : "
    f"{nifty_benchmark['max_drawdown']:.2%}"
)

print()

print(
    f"GOLDBEES Final Equity  : "
    f"₹{gold_benchmark['final_equity']:,.2f}"
)

print(
    f"GOLDBEES CAGR          : "
    f"{gold_benchmark['cagr']:.2%}"
)

print(
    f"GOLDBEES Volatility    : "
    f"{gold_benchmark['volatility']:.2%}"
)

print(
    f"GOLDBEES Sharpe        : "
    f"{gold_benchmark['sharpe']:.2f}"
)

print(
    f"GOLDBEES Sortino       : "
    f"{gold_benchmark['sortino']:.2f}"
)

print(
    f"GOLDBEES Max Drawdown  : "
    f"{gold_benchmark['max_drawdown']:.2%}"
)

print()

print(
    f"50/50 Final Equity     : "
    f"₹{balanced_benchmark['final_equity']:,.2f}"
)

print(
    f"50/50 CAGR             : "
    f"{balanced_benchmark['cagr']:.2%}"
)

print(
    f"50/50 Volatility       : "
    f"{balanced_benchmark['volatility']:.2%}"
)

print(
    f"50/50 Sharpe           : "
    f"{balanced_benchmark['sharpe']:.2f}"
)

print(
    f"50/50 Sortino          : "
    f"{balanced_benchmark['sortino']:.2f}"
)

print(
    f"50/50 Max Drawdown     : "
    f"{balanced_benchmark['max_drawdown']:.2%}"
)

print()
print("=" * 60)