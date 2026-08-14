# ============================================================
# PARAMETER ROBUSTNESS ANALYSIS
# ============================================================

import pandas as pd


def run_robustness_test(
    data,
    lookback_periods,
    initial_capital,
    transaction_cost,
    slippage,
):
    """
    Test strategy performance across multiple
    breakout lookback periods.
    """

    from src.signals import generate_signals
    from src.backtest import (
        calculate_returns,
        run_backtest,
        calculate_equity,
    )
    from src.performance import (
        calculate_performance,
    )

    results = []

    for lookback in lookback_periods:

        test_data = generate_signals(
            data,
            lookback=lookback,
        )

        test_data = calculate_returns(
            test_data
        )

        test_data = run_backtest(
            test_data,
            transaction_cost=transaction_cost,
            slippage=slippage,
        )

        test_data = calculate_equity(
            test_data,
            initial_capital=initial_capital,
        )

        performance = (
            calculate_performance(
                test_data,
                initial_capital=initial_capital,
            )
        )

        results.append(
            {
                "Lookback": lookback,
                "CAGR": performance["cagr"],
                "Volatility": performance["volatility"],
                "Sharpe": performance["sharpe"],
                "Max Drawdown": performance["max_drawdown"],
            }
        )

    return pd.DataFrame(results)