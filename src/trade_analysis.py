# ============================================================
# TRADE ANALYSIS
# ============================================================

import pandas as pd


def analyze_trades(data):
    """
    Calculate trade-level statistics.
    """

    trade_changes = data[
        data["held_position"].ne(
            data["held_position"].shift()
        )
    ].copy()

    trade_changes = trade_changes[
        trade_changes["held_position"] != 0
    ]

    trade_returns = []

    holding_periods = []

    nifty_trade_returns = []
    gold_trade_returns = []

    nifty_holding_periods = []
    gold_holding_periods = []

    for i in range(
        len(trade_changes) - 1
    ):

        start_index = (
            trade_changes.index[i]
        )

        end_index = (
            trade_changes.index[i + 1]
        )

        position = data.loc[
            start_index,
            "held_position"
        ]

        trade_return = (
            data.loc[
                start_index:end_index,
                "strategy_return_after_cost"
            ]
            + 1
        ).prod() - 1

        holding_days = (
            data.loc[end_index, "time"]
            - data.loc[start_index, "time"]
        ).days

        trade_returns.append(
            trade_return
        )

        holding_periods.append(
            holding_days
        )

        if position == 1:

            nifty_trade_returns.append(
                trade_return
            )

            nifty_holding_periods.append(
                holding_days
            )

        elif position == -1:

            gold_trade_returns.append(
                trade_return
            )

            gold_holding_periods.append(
                holding_days
            )

    trade_returns = pd.Series(
        trade_returns
    )

    nifty_trade_returns = pd.Series(
        nifty_trade_returns
    )

    gold_trade_returns = pd.Series(
        gold_trade_returns
    )

    # --------------------------------------------------------
    # Overall trade statistics
    # --------------------------------------------------------

    completed_trades = (
        len(trade_returns)
    )

    winning_trades = (
        trade_returns > 0
    ).sum()

    losing_trades = (
        trade_returns < 0
    ).sum()

    win_rate = (
        winning_trades
        / completed_trades
        if completed_trades > 0
        else 0
    )

    average_trade_return = (
        trade_returns.mean()
        if completed_trades > 0
        else 0
    )

    # --------------------------------------------------------
    # Profit factor
    # --------------------------------------------------------

    gross_profit = (
        trade_returns[
            trade_returns > 0
        ].sum()
    )

    gross_loss = abs(
        trade_returns[
            trade_returns < 0
        ].sum()
    )

    profit_factor = (
        gross_profit / gross_loss
        if gross_loss > 0
        else float("inf")
    )

    # --------------------------------------------------------
    # Expectancy
    # --------------------------------------------------------

    average_winning_trade = (
        trade_returns[
            trade_returns > 0
        ].mean()
    )

    average_losing_trade = (
        trade_returns[
            trade_returns < 0
        ].mean()
    )

    expectancy = (
        win_rate
        * average_winning_trade
        + (1 - win_rate)
        * average_losing_trade
    )

    # --------------------------------------------------------
    # Holding period
    # --------------------------------------------------------

    average_holding_period = (
        sum(holding_periods)
        / len(holding_periods)
        if holding_periods
        else 0
    )

    # --------------------------------------------------------
    # Best / worst trade
    # --------------------------------------------------------

    best_trade = (
        trade_returns.max()
        if not trade_returns.empty
        else 0
    )

    worst_trade = (
        trade_returns.min()
        if not trade_returns.empty
        else 0
    )

    # --------------------------------------------------------
    # NIFTYBEES
    # --------------------------------------------------------

    nifty_trade_count = (
        len(nifty_trade_returns)
    )

    nifty_win_rate = (
        (nifty_trade_returns > 0).mean()
        if nifty_trade_count > 0
        else 0
    )

    nifty_average_trade = (
        nifty_trade_returns.mean()
        if nifty_trade_count > 0
        else 0
    )

    average_nifty_holding = (
        sum(nifty_holding_periods)
        / len(nifty_holding_periods)
        if nifty_holding_periods
        else 0
    )

    # --------------------------------------------------------
    # GOLDBEES
    # --------------------------------------------------------

    gold_trade_count = (
        len(gold_trade_returns)
    )

    gold_win_rate = (
        (gold_trade_returns > 0).mean()
        if gold_trade_count > 0
        else 0
    )

    gold_average_trade = (
        gold_trade_returns.mean()
        if gold_trade_count > 0
        else 0
    )

    average_gold_holding = (
        sum(gold_holding_periods)
        / len(gold_holding_periods)
        if gold_holding_periods
        else 0
    )

    return {
        "completed_trades": completed_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "win_rate": win_rate,
        "average_trade_return": average_trade_return,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "profit_factor": profit_factor,
        "average_winning_trade": average_winning_trade,
        "average_losing_trade": average_losing_trade,
        "expectancy": expectancy,
        "average_holding_period": average_holding_period,
        "best_trade": best_trade,
        "worst_trade": worst_trade,

        "nifty_trade_count": nifty_trade_count,
        "nifty_win_rate": nifty_win_rate,
        "nifty_average_trade": nifty_average_trade,
        "average_nifty_holding": average_nifty_holding,

        "gold_trade_count": gold_trade_count,
        "gold_win_rate": gold_win_rate,
        "gold_average_trade": gold_average_trade,
        "average_gold_holding": average_gold_holding,
    }