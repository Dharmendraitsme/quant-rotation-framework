# ============================================================
# OUT-OF-SAMPLE VALIDATION
# ============================================================

from src.signals import generate_signals
from src.backtest import (
    calculate_returns,
    run_backtest,
    calculate_equity,
)
from src.performance import calculate_performance
from src.trade_analysis import analyze_trades


def run_out_of_sample_test(
    data,
    lookback,
    initial_capital,
    transaction_cost,
    slippage,
    train_ratio=0.70,
):
    """
    Split the historical data into:

    70% In-Sample
    30% Out-of-Sample
    """

    split_index = int(
        len(data) * train_ratio
    )

    in_sample = data.iloc[
        :split_index
    ].copy()

    out_of_sample = data.iloc[
        split_index:
    ].copy()

    # --------------------------------------------------------
    # Run strategy on In-Sample data
    # --------------------------------------------------------

    in_sample = generate_signals(
        in_sample,
        lookback=lookback,
    )

    in_sample = calculate_returns(
        in_sample
    )

    in_sample = run_backtest(
        in_sample,
        transaction_cost=transaction_cost,
        slippage=slippage,
    )

    in_sample = calculate_equity(
        in_sample,
        initial_capital=initial_capital,
    )

    in_sample_performance = (
        calculate_performance(
            in_sample,
            initial_capital=initial_capital,
        )
    )

    in_sample_trades = analyze_trades(
        in_sample
    )

    # --------------------------------------------------------
    # Run strategy on Out-of-Sample data
    # --------------------------------------------------------

    out_of_sample = generate_signals(
        out_of_sample,
        lookback=lookback,
    )

    out_of_sample = calculate_returns(
        out_of_sample
    )

    out_of_sample = run_backtest(
        out_of_sample,
        transaction_cost=transaction_cost,
        slippage=slippage,
    )

    out_of_sample = calculate_equity(
        out_of_sample,
        initial_capital=initial_capital,
    )

    out_of_sample_performance = (
        calculate_performance(
            out_of_sample,
            initial_capital=initial_capital,
        )
    )

    out_of_sample_trades = analyze_trades(
        out_of_sample
    )

    return {
        "in_sample": {
            "performance": in_sample_performance,
            "trades": in_sample_trades,
        },
        "out_of_sample": {
            "performance": out_of_sample_performance,
            "trades": out_of_sample_trades,
        },
    }