# ============================================================
# VALIDATION
# ============================================================

from src.signals import generate_signals
from src.backtest import (
    calculate_returns,
    run_backtest,
    calculate_equity,
)
from src.performance import calculate_performance
from src.trade_analysis import analyze_trades


# ============================================================
# OUT-OF-SAMPLE VALIDATION
# ============================================================

def run_out_of_sample_test(
    data,
    lookback,
    initial_capital,
    transaction_cost,
    slippage,
    train_ratio=0.70,
):

    split_index = int(
        len(data) * train_ratio
    )

    in_sample = data.iloc[
        :split_index
    ].copy()

    out_of_sample = data.iloc[
        split_index:
    ].copy()

    in_sample = generate_signals(
        in_sample,
        lookback=lookback,
    )

    in_sample = calculate_returns(
        in_sample
    )

    in_sample = run_backtest(
        in_sample,
        transaction_cost,
        slippage,
    )

    in_sample = calculate_equity(
        in_sample,
        initial_capital,
    )

    in_sample_performance = (
        calculate_performance(
            in_sample,
            initial_capital,
        )
    )

    in_sample_trades = analyze_trades(
        in_sample
    )

    out_of_sample = generate_signals(
        out_of_sample,
        lookback=lookback,
    )

    out_of_sample = calculate_returns(
        out_of_sample
    )

    out_of_sample = run_backtest(
        out_of_sample,
        transaction_cost,
        slippage,
    )

    out_of_sample = calculate_equity(
        out_of_sample,
        initial_capital,
    )

    out_of_sample_performance = (
        calculate_performance(
            out_of_sample,
            initial_capital,
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


# ============================================================
# WALK-FORWARD VALIDATION
# ============================================================

def run_walk_forward_test(
    data,
    lookback,
    initial_capital,
    transaction_cost,
    slippage,
    train_size=0.50,
    test_size=0.10,
    step_size=0.10,
):

    results = []

    total_rows = len(data)

    train_rows = int(
        total_rows * train_size
    )

    test_rows = int(
        total_rows * test_size
    )

    step_rows = int(
        total_rows * step_size
    )

    start = 0

    fold = 1

    while (
        start + train_rows + test_rows
        <= total_rows
    ):

        train_end = (
            start + train_rows
        )

        test_end = (
            train_end + test_rows
        )

        # ----------------------------------------------------
        # Training period
        # ----------------------------------------------------

        train_data = data.iloc[
            start:train_end
        ].copy()

        # ----------------------------------------------------
        # Test period
        # ----------------------------------------------------

        test_data = data.iloc[
            train_end:test_end
        ].copy()

        # ----------------------------------------------------
        # Run strategy on test period
        # ----------------------------------------------------

        test_data = generate_signals(
            test_data,
            lookback=lookback,
        )

        test_data = calculate_returns(
            test_data
        )

        test_data = run_backtest(
            test_data,
            transaction_cost,
            slippage,
        )

        test_data = calculate_equity(
            test_data,
            initial_capital,
        )

        performance = calculate_performance(
            test_data,
            initial_capital,
        )

        trades = analyze_trades(
            test_data
        )

        # ----------------------------------------------------
        # Store fold results
        # ----------------------------------------------------

        results.append(
            {
                "Fold": fold,
                "Train Start": train_data["time"].iloc[0],
                "Train End": train_data["time"].iloc[-1],
                "Test Start": test_data["time"].iloc[0],
                "Test End": test_data["time"].iloc[-1],
                "CAGR": performance["cagr"],
                "Sharpe": performance["sharpe"],
                "Max Drawdown": performance["max_drawdown"],
                "Trades": trades["completed_trades"],
            }
        )

        fold += 1

        start += step_rows

    return results