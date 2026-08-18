# ============================================================
# RESEARCH VISUALIZATION
# ============================================================

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


RESULTS_DIR = Path("results")


def _prepare_dates(dates, length):
    """Convert dates to datetime and align with equity length."""

    dates = dates.iloc[:length].copy()

    return dates


def _format_date_axis():
    """Format chart x-axis using readable calendar dates."""

    ax = plt.gca()

    ax.xaxis.set_major_locator(
        mdates.AutoDateLocator()
    )

    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%Y")
    )

    plt.xticks(rotation=45)


def plot_equity_curves(
    dates,
    strategy_equity,
    nifty_equity,
    gold_equity,
    balanced_equity,
):
    """
    Plot normalized equity curves using actual dates.
    """

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    length = min(
        len(dates),
        len(strategy_equity),
        len(nifty_equity),
        len(gold_equity),
        len(balanced_equity),
    )

    dates = _prepare_dates(
        dates,
        length,
    )

    plt.figure(figsize=(12, 6))

    plt.plot(
        dates,
        strategy_equity.iloc[:length]
        / strategy_equity.iloc[0],
        label="Rotation Strategy",
    )

    plt.plot(
        dates,
        nifty_equity.iloc[:length]
        / nifty_equity.iloc[0],
        label="NIFTYBEES",
    )

    plt.plot(
        dates,
        gold_equity.iloc[:length]
        / gold_equity.iloc[0],
        label="GOLDBEES",
    )

    plt.plot(
        dates,
        balanced_equity.iloc[:length]
        / balanced_equity.iloc[0],
        label="50/50",
    )

    plt.title(
        "Strategy vs Benchmarks"
    )

    plt.xlabel("Date")
    plt.ylabel("Growth of ₹1")

    _format_date_axis()

    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        RESULTS_DIR / "equity_curves.png",
        dpi=150,
    )

    plt.close()


def plot_strategy_drawdown(
    dates,
    strategy_equity,
):
    """
    Plot strategy drawdown using actual dates.
    """

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    length = min(
        len(dates),
        len(strategy_equity),
    )

    dates = _prepare_dates(
        dates,
        length,
    )

    equity = (
        strategy_equity.iloc[:length]
    )

    running_max = (
        equity.cummax()
    )

    drawdown = (
        equity
        / running_max
        - 1
    )

    plt.figure(figsize=(12, 5))

    plt.plot(
        dates,
        drawdown,
        label="Strategy Drawdown",
    )

    plt.title(
        "Strategy Drawdown"
    )

    plt.xlabel("Date")
    plt.ylabel("Drawdown")

    _format_date_axis()

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