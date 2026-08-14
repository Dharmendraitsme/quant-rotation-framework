# ============================================================
# RESEARCH REPORTING
# ============================================================

from pathlib import Path

import pandas as pd


RESULTS_DIR = Path("results")


def save_results(
    performance,
    trades,
    nifty_benchmark,
    gold_benchmark,
    balanced_benchmark,
    robustness_results,
    validation,
    regime_results,
):
    """Save research outputs to CSV files."""

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    pd.DataFrame(
        [performance]
    ).to_csv(
        RESULTS_DIR / "performance.csv",
        index=False,
    )

    pd.DataFrame(
        [trades]
    ).to_csv(
        RESULTS_DIR / "trade_analysis.csv",
        index=False,
    )

    benchmark_df = pd.DataFrame(
        [
            {
                "Benchmark": "NIFTYBEES",
                "Final Equity": nifty_benchmark["final_equity"],
                "CAGR": nifty_benchmark["cagr"],
                "Volatility": nifty_benchmark["volatility"],
                "Sharpe": nifty_benchmark["sharpe"],
                "Sortino": nifty_benchmark["sortino"],
                "Max Drawdown": nifty_benchmark["max_drawdown"],
            },
            {
                "Benchmark": "GOLDBEES",
                "Final Equity": gold_benchmark["final_equity"],
                "CAGR": gold_benchmark["cagr"],
                "Volatility": gold_benchmark["volatility"],
                "Sharpe": gold_benchmark["sharpe"],
                "Sortino": gold_benchmark["sortino"],
                "Max Drawdown": gold_benchmark["max_drawdown"],
            },
            {
                "Benchmark": "50/50",
                "Final Equity": balanced_benchmark["final_equity"],
                "CAGR": balanced_benchmark["cagr"],
                "Volatility": balanced_benchmark["volatility"],
                "Sharpe": balanced_benchmark["sharpe"],
                "Sortino": balanced_benchmark["sortino"],
                "Max Drawdown": balanced_benchmark["max_drawdown"],
            },
        ]
    )

    benchmark_df.to_csv(
        RESULTS_DIR / "benchmarks.csv",
        index=False,
    )

    robustness_results.to_csv(
        RESULTS_DIR / "robustness.csv",
        index=False,
    )

    validation_df = pd.DataFrame(
        [
            {
                "Period": "In-Sample",
                "CAGR": validation["in_sample"]["performance"]["cagr"],
                "Sharpe": validation["in_sample"]["performance"]["sharpe"],
                "Max Drawdown": validation["in_sample"]["performance"]["max_drawdown"],
                "Trades": validation["in_sample"]["trades"]["completed_trades"],
            },
            {
                "Period": "Out-of-Sample",
                "CAGR": validation["out_of_sample"]["performance"]["cagr"],
                "Sharpe": validation["out_of_sample"]["performance"]["sharpe"],
                "Max Drawdown": validation["out_of_sample"]["performance"]["max_drawdown"],
                "Trades": validation["out_of_sample"]["trades"]["completed_trades"],
            },
        ]
    )

    validation_df.to_csv(
        RESULTS_DIR / "validation.csv",
        index=False,
    )

    regime_results.to_csv(
        RESULTS_DIR / "regime_analysis.csv",
        index=False,
    )


def print_summary(
    performance,
    trades,
    nifty_benchmark,
    gold_benchmark,
    balanced_benchmark,
    initial_capital,
    transaction_cost,
    slippage,
    number_of_trades,
):
    """Print the main research summary."""

    execution_cost = (
        transaction_cost + slippage
    )

    print()
    print("=" * 60)
    print("NIFTYBEES vs GOLDBEES ROTATION STRATEGY")
    print("=" * 60)

    print()
    print("Trading Assumptions")
    print("--------------------")

    print(
        f"Initial Capital       : ₹{initial_capital:,.2f}"
    )

    print(
        f"Transaction Cost      : {transaction_cost:.2%}"
    )

    print(
        f"Slippage              : {slippage:.2%}"
    )

    print(
        f"Total Execution Cost  : {execution_cost:.2%}"
    )

    print(
        f"Position Changes      : {number_of_trades}"
    )

    print()
    print("Rotation Strategy")
    print("--------------------")

    print(
        f"Final Equity          : ₹{performance['final_equity']:,.2f}"
    )

    print(
        f"Absolute Return       : {performance['absolute_return']:.2%}"
    )

    print(
        f"CAGR                  : {performance['cagr']:.2%}"
    )

    print(
        f"Annualized Volatility : {performance['volatility']:.2%}"
    )

    print(
        f"Sharpe Ratio          : {performance['sharpe']:.2f}"
    )

    print(
        f"Sortino Ratio         : {performance['sortino']:.2f}"
    )

    print(
        f"Calmar Ratio          : {performance['calmar']:.2f}"
    )

    print(
        f"Max Drawdown          : {performance['max_drawdown']:.2%}"
    )

    print(
        f"Max Drawdown Duration : "
        f"{performance['max_drawdown_duration']} trading days"
    )

    print()
    print("Trade Analysis")
    print("--------------------")

    print(
        f"Completed Trades      : {trades['completed_trades']}"
    )

    print(
        f"Winning Trades        : {trades['winning_trades']}"
    )

    print(
        f"Losing Trades         : {trades['losing_trades']}"
    )

    print(
        f"Win Rate              : {trades['win_rate']:.2%}"
    )

    print(
        f"Average Trade Return  : {trades['average_trade_return']:.2%}"
    )

    print(
        f"Gross Profit          : {trades['gross_profit']:.2%}"
    )

    print(
        f"Gross Loss            : {trades['gross_loss']:.2%}"
    )

    print(
        f"Profit Factor         : {trades['profit_factor']:.2f}"
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
        f"Trade Expectancy      : {trades['expectancy']:.2%}"
    )

    print(
        f"Average Holding Period: "
        f"{trades['average_holding_period']:.1f} calendar days"
    )

    print(
        f"Best Trade            : {trades['best_trade']:.2%}"
    )

    print(
        f"Worst Trade           : {trades['worst_trade']:.2%}"
    )

    print()
    print("Asset Trade Analysis")
    print("--------------------")

    print(
        f"NIFTYBEES Trades      : {trades['nifty_trade_count']}"
    )

    print(
        f"NIFTYBEES Win Rate    : {trades['nifty_win_rate']:.2%}"
    )

    print(
        f"NIFTYBEES Avg Return  : {trades['nifty_average_trade']:.2%}"
    )

    print(
        f"NIFTYBEES Avg Holding : "
        f"{trades['average_nifty_holding']:.1f} days"
    )

    print()

    print(
        f"GOLDBEES Trades       : {trades['gold_trade_count']}"
    )

    print(
        f"GOLDBEES Win Rate     : {trades['gold_win_rate']:.2%}"
    )

    print(
        f"GOLDBEES Avg Return   : {trades['gold_average_trade']:.2%}"
    )

    print(
        f"GOLDBEES Avg Holding  : "
        f"{trades['average_gold_holding']:.1f} days"
    )

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