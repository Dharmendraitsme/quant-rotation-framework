# ============================================================
# BENCHMARK ANALYSIS
# ============================================================

import pandas as pd


def calculate_single_asset_benchmark(
    returns,
    initial_capital,
    years,
):
    """
    Calculate a buy-and-hold benchmark.
    """

    equity = (
        initial_capital
        * (1 + returns).cumprod()
    )

    final_equity = equity.iloc[-2]

    cagr = (
        final_equity / initial_capital
    ) ** (1 / years) - 1

    volatility = (
        returns.std()
        * (252 ** 0.5)
    )

    drawdown = (
        equity
        / equity.cummax()
        - 1
    )

    max_drawdown = (
        drawdown.min()
    )

    sharpe = (
        returns.mean()
        / returns.std()
        * (252 ** 0.5)
    )

    downside = returns[
        returns < 0
    ]

    sortino = (
        returns.mean()
        / downside.std()
        * (252 ** 0.5)
    )

    return {
        "equity": equity,
        "final_equity": final_equity,
        "cagr": cagr,
        "volatility": volatility,
        "sharpe": sharpe,
        "sortino": sortino,
        "max_drawdown": max_drawdown,
    }


def calculate_50_50_benchmark(
    data,
    initial_capital,
    execution_cost,
):
    """
    Monthly-rebalanced 50/50 NIFTYBEES + GOLDBEES benchmark.

    Rebalancing costs include transaction cost + slippage.
    """

    data = data.copy()

    data["month"] = (
        data["time"]
        .dt.to_period("M")
    )

    nifty_value = (
        initial_capital * 0.50
    )

    gold_value = (
        initial_capital * 0.50
    )

    equity_values = []

    current_month = None

    for i in range(len(data)):

        row = data.iloc[i]

        if (
            pd.isna(row["nifty_return"])
            or pd.isna(row["gold_return"])
        ):
            break

        # ----------------------------------------------------
        # Monthly rebalance
        # ----------------------------------------------------

        if current_month != row["month"]:

            total_value = (
                nifty_value
                + gold_value
            )

            target_nifty = (
                total_value * 0.50
            )

            target_gold = (
                total_value * 0.50
            )

            nifty_trade = abs(
                target_nifty
                - nifty_value
            )

            gold_trade = abs(
                target_gold
                - gold_value
            )

            total_traded = (
                nifty_trade
                + gold_trade
            )

            if total_value > 0:

                rebalance_cost = (
                    total_traded
                    / total_value
                    * execution_cost
                )

            else:

                rebalance_cost = 0.0

            total_value_after_cost = (
                total_value
                * (1 - rebalance_cost)
            )

            nifty_value = (
                total_value_after_cost
                * 0.50
            )

            gold_value = (
                total_value_after_cost
                * 0.50
            )

            current_month = (
                row["month"]
            )

        # ----------------------------------------------------
        # Daily returns
        # ----------------------------------------------------

        nifty_value *= (
            1 + row["nifty_return"]
        )

        gold_value *= (
            1 + row["gold_return"]
        )

        equity_values.append(
            nifty_value + gold_value
        )

    balanced_equity = pd.Series(
        equity_values,
        index=data.index[
            :len(equity_values)
        ],
    )

    balanced_return = (
        balanced_equity.pct_change()
    )

    final_equity = (
        balanced_equity.iloc[-1]
    )

    years = (
        data["time"].iloc[-2]
        - data["time"].iloc[0]
    ).days / 365.25

    cagr = (
        final_equity / initial_capital
    ) ** (1 / years) - 1

    volatility = (
        balanced_return.std()
        * (252 ** 0.5)
    )

    sharpe = (
        balanced_return.mean()
        / balanced_return.std()
        * (252 ** 0.5)
    )

    downside = balanced_return[
        balanced_return < 0
    ]

    sortino = (
        balanced_return.mean()
        / downside.std()
        * (252 ** 0.5)
    )

    drawdown = (
        balanced_equity
        / balanced_equity.cummax()
        - 1
    )

    max_drawdown = (
        drawdown.min()
    )

    return {
        "equity": balanced_equity,
        "final_equity": final_equity,
        "cagr": cagr,
        "volatility": volatility,
        "sharpe": sharpe,
        "sortino": sortino,
        "max_drawdown": max_drawdown,
    }