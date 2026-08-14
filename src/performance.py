# ============================================================
# PERFORMANCE ANALYSIS
# ============================================================


def calculate_performance(
    data,
    initial_capital=100_000,
):
    """
    Calculate portfolio-level performance metrics.
    """

    end_value = data["equity"].iloc[-2]

    start_date = data["time"].iloc[0]
    end_date = data["time"].iloc[-2]

    years = (
        end_date - start_date
    ).days / 365.25

    absolute_return = (
        end_value / initial_capital
    ) - 1

    cagr = (
        end_value / initial_capital
    ) ** (1 / years) - 1

    # --------------------------------------------------------
    # Drawdown
    # --------------------------------------------------------

    running_max = (
        data["equity"].cummax()
    )

    drawdown = (
        data["equity"]
        / running_max
        - 1
    )

    max_drawdown = (
        drawdown.min()
    )

    # --------------------------------------------------------
    # Drawdown duration
    # --------------------------------------------------------

    in_drawdown = (
        drawdown < 0
    )

    groups = (
        ~in_drawdown
    ).cumsum()

    drawdown_duration = (
        data.loc[in_drawdown]
        .groupby(
            groups[in_drawdown]
        )
        .size()
    )

    max_drawdown_duration = (
        drawdown_duration.max()
        if not drawdown_duration.empty
        else 0
    )

    # --------------------------------------------------------
    # Volatility
    # --------------------------------------------------------

    returns = (
        data["strategy_return_after_cost"]
    )

    annualized_volatility = (
        returns.std()
        * (252 ** 0.5)
    )

    # --------------------------------------------------------
    # Sharpe
    # --------------------------------------------------------

    sharpe_ratio = (
        returns.mean()
        / returns.std()
        * (252 ** 0.5)
    )

    # --------------------------------------------------------
    # Sortino
    # --------------------------------------------------------

    downside_returns = data.loc[
        returns < 0,
        "strategy_return_after_cost"
    ]

    sortino_ratio = (
        returns.mean()
        / downside_returns.std()
        * (252 ** 0.5)
    )

    # --------------------------------------------------------
    # Calmar
    # --------------------------------------------------------

    calmar_ratio = (
        cagr / abs(max_drawdown)
    )

    return {
        "final_equity": end_value,
        "absolute_return": absolute_return,
        "cagr": cagr,
        "volatility": annualized_volatility,
        "sharpe": sharpe_ratio,
        "sortino": sortino_ratio,
        "calmar": calmar_ratio,
        "max_drawdown": max_drawdown,
        "max_drawdown_duration": max_drawdown_duration,
    }