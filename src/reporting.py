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
    """
    Save all major research outputs into CSV files.
    """

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Performance
    # --------------------------------------------------------

    performance_df = pd.DataFrame(
        [
            performance
        ]
    )

    performance_df.to_csv(
        RESULTS_DIR / "performance.csv",
        index=False,
    )

    # --------------------------------------------------------
    # Trade Analysis
    # --------------------------------------------------------

    trade_df = pd.DataFrame(
        [
            trades
        ]
    )

    trade_df.to_csv(
        RESULTS_DIR / "trade_analysis.csv",
        index=False,
    )

    # --------------------------------------------------------
    # Benchmarks
    # --------------------------------------------------------

    benchmark_df = pd.DataFrame(
        [
            {
                "Benchmark": "NIFTYBEES",
                "Final Equity":
                    nifty_benchmark["final_equity"],
                "CAGR":
                    nifty_benchmark["cagr"],
                "Volatility":
                    nifty_benchmark["volatility"],
                "Sharpe":
                    nifty_benchmark["sharpe"],
                "Sortino":
                    nifty_benchmark["sortino"],
                "Max Drawdown":
                    nifty_benchmark["max_drawdown"],
            },
            {
                "Benchmark": "GOLDBEES",
                "Final Equity":
                    gold_benchmark["final_equity"],
                "CAGR":
                    gold_benchmark["cagr"],
                "Volatility":
                    gold_benchmark["volatility"],
                "Sharpe":
                    gold_benchmark["sharpe"],
                "Sortino":
                    gold_benchmark["sortino"],
                "Max Drawdown":
                    gold_benchmark["max_drawdown"],
            },
            {
                "Benchmark": "50/50",
                "Final Equity":
                    balanced_benchmark["final_equity"],
                "CAGR":
                    balanced_benchmark["cagr"],
                "Volatility":
                    balanced_benchmark["volatility"],
                "Sharpe":
                    balanced_benchmark["sharpe"],
                "Sortino":
                    balanced_benchmark["sortino"],
                "Max Drawdown":
                    balanced_benchmark["max_drawdown"],
            },
        ]
    )

    benchmark_df.to_csv(
        RESULTS_DIR / "benchmarks.csv",
        index=False,
    )

    # --------------------------------------------------------
    # Parameter Robustness
    # --------------------------------------------------------

    robustness_results.to_csv(
        RESULTS_DIR / "robustness.csv",
        index=False,
    )

    # --------------------------------------------------------
    # Out-of-Sample Validation
    # --------------------------------------------------------

    validation_df = pd.DataFrame(
        [
            {
                "Period": "In-Sample",
                "CAGR":
                    validation[
                        "in_sample"
                    ]["performance"]["cagr"],
                "Sharpe":
                    validation[
                        "in_sample"
                    ]["performance"]["sharpe"],
                "Max Drawdown":
                    validation[
                        "in_sample"
                    ]["performance"]["max_drawdown"],
                "Trades":
                    validation[
                        "in_sample"
                    ]["trades"]["completed_trades"],
            },
            {
                "Period": "Out-of-Sample",
                "CAGR":
                    validation[
                        "out_of_sample"
                    ]["performance"]["cagr"],
                "Sharpe":
                    validation[
                        "out_of_sample"
                    ]["performance"]["sharpe"],
                "Max Drawdown":
                    validation[
                        "out_of_sample"
                    ]["performance"]["max_drawdown"],
                "Trades":
                    validation[
                        "out_of_sample"
                    ]["trades"]["completed_trades"],
            },
        ]
    )

    validation_df.to_csv(
        RESULTS_DIR / "validation.csv",
        index=False,
    )

    # --------------------------------------------------------
    # Regime Analysis
    # --------------------------------------------------------

    regime_results.to_csv(
        RESULTS_DIR / "regime_analysis.csv",
        index=False,
    )

    print()
    print("Research results saved to:")
    print(
        "results/"
    )