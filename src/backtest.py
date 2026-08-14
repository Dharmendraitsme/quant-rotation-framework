# ============================================================
# BACKTEST ENGINE
# ============================================================

import pandas as pd


def calculate_returns(data):
    """
    Calculate daily open-to-next-open returns.
    """

    data = data.copy()

    data["nifty_return"] = (
        data["open_nifty"].shift(-1)
        / data["open_nifty"]
        - 1
    )

    data["gold_return"] = (
        data["open_gold"].shift(-1)
        / data["open_gold"]
        - 1
    )

    return data


def run_backtest(
    data,
    transaction_cost=0.001,
    slippage=0.0005,
):
    """
    Run the rotation strategy including transaction costs
    and slippage.
    """

    data = data.copy()

    execution_cost = (
        transaction_cost + slippage
    )

    # --------------------------------------------------------
    # Actual held position
    # --------------------------------------------------------

    data["held_position"] = (
        data["position"]
        .shift(1)
        .fillna(0)
        .astype(int)
    )

    # --------------------------------------------------------
    # Position changes
    # --------------------------------------------------------

    data["held_position_change"] = (
        data["held_position"]
        .diff()
        .abs()
    )

    # --------------------------------------------------------
    # Transaction costs
    # --------------------------------------------------------

    data["cost"] = 0.0

    data.loc[
        data["held_position_change"] == 1,
        "cost"
    ] = execution_cost

    data.loc[
        data["held_position_change"] == 2,
        "cost"
    ] = execution_cost * 2

    # --------------------------------------------------------
    # Strategy return
    # --------------------------------------------------------

    data["strategy_return"] = 0.0

    data.loc[
        data["held_position"] == 1,
        "strategy_return"
    ] = data["nifty_return"]

    data.loc[
        data["held_position"] == -1,
        "strategy_return"
    ] = data["gold_return"]

    # --------------------------------------------------------
    # Return after costs
    # --------------------------------------------------------

    data["strategy_return_after_cost"] = (
        data["strategy_return"]
        - data["cost"]
    )

    return data


def calculate_equity(
    data,
    initial_capital=100_000,
):
    """
    Calculate strategy equity curve.
    """

    data = data.copy()

    data["equity"] = (
        initial_capital
        * (
            1
            + data["strategy_return_after_cost"]
        ).cumprod()
    )

    return data