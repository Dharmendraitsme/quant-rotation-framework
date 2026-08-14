# ============================================================
# PARAMETER ROBUSTNESS ANALYSIS
# ============================================================

import pandas as pd

from src.signals import generate_signals
from src.backtest import (
    calculate_returns,
    run_backtest,
    calculate_equity,
)
from src.performance import calculate_performance
from src.trade_analysis import analyze_trades


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

    results = []

    for lookback in lookback_periods:

        # ----------------------------------------------------
        # Generate signals
        # ----------------------------------------------------

        test_data = generate_signals(
            data,
            lookback=lookback,
        )

        # ----------------------------------------------------
        # Calculate returns
        # ----------------------------------------------------

        test_data = calculate_returns(
            test_data
        )

        # ----------------------------------------------------
        # Run backtest
        # ----------------------------------------------------

        test_data = run_backtest(
            test_data,
            transaction_cost=transaction_cost,
            slippage=slippage,
        )

        # ----------------------------------------------------
        # Calculate equity
        # ----------------------------------------------------

        test_data = calculate_equity(
            test_data,
            initial_capital=initial_capital,
        )

        # ----------------------------------------------------
        # Performance
        # ----------------------------------------------------

        performance = calculate_performance(
            test_data,
            initial_capital=initial_capital,
        )

        # ----------------------------------------------------
        # Trade analysis
        # ----------------------------------------------------

        trades = analyze_trades(
            test_data
        )

        # ----------------------------------------------------
        # Store results
        # ----------------------------------------------------

        results.append(
            {
                "Lookback": lookback,
                "CAGR": performance["cagr"],
                "Volatility": performance["volatility"],
                "Sharpe": performance["sharpe"],
                "Max Drawdown": performance["max_drawdown"],
                "Trades": trades["completed_trades"],
                "Profit Factor": trades["profit_factor"],
            }
        )

    return pd.DataFrame(results)