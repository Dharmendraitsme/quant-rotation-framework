# ============================================================
# RESEARCH VISUALIZATION
# ============================================================

from pathlib import Path

import matplotlib.pyplot as plt


RESULTS_DIR = Path("results")


def plot_equity_curves(
    strategy_equity,
    nifty_equity,
    gold_equity,
    balanced_equity,
):
    """
    Plot normalized equity curves.
    """

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.figure(figsize=(12, 6))

    plt.plot(
        strategy_equity.index,
        strategy_equity / strategy_equity.iloc[0],
        label="Rotation Strategy",
    )

    plt.plot(
        nifty_equity.index,
        nifty_equity / nifty_equity.iloc[0],
        label="NIFTYBEES",
    )

    plt.plot(
        gold_equity.index,
        gold_equity / gold_equity.iloc[0],
        label="GOLDBEES",
    )

    plt.plot(
        balanced_equity.index,
        balanced_equity / balanced_equity.iloc[0],
        label="50/50",
    )

    plt.title(
        "Strategy vs Benchmarks"
    )

    plt.xlabel("Date")
    plt.ylabel("Growth of ₹1")

    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        RESULTS_DIR / "equity_curves.png",
        dpi=150,
    )

    plt.close()


def plot_strategy_drawdown(
    strategy_equity,
):
    """
    Plot strategy drawdown.
    """

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    running_max = (
        strategy_equity.cummax()
    )

    drawdown = (
        strategy_equity
        / running_max
        - 1
    )

    plt.figure(figsize=(12, 5))

    plt.plot(
        drawdown.index,
        drawdown,
        label="Strategy Drawdown",
    )

    plt.title(
        "Strategy Drawdown"
    )

    plt.xlabel("Date")
    plt.ylabel("Drawdown")

    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        RESULTS_DIR / "strategy_drawdown.png",
        dpi=150,
    )

    plt.close()


def plot_robustness(
    robustness_results,
):
    """
    Plot CAGR across lookback parameters.
    """

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.figure(figsize=(10, 5))

    plt.plot(
        robustness_results["Lookback"],
        robustness_results["CAGR"],
        marker="o",
    )

    plt.title(
        "Parameter Robustness - CAGR"
    )

    plt.xlabel(
        "Lookback Period"
    )

    plt.ylabel(
        "CAGR"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        RESULTS_DIR / "parameter_robustness.png",
        dpi=150,
    )

    plt.close()