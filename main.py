# ============================================================
# NIFTYBEES vs GOLDBEES ROTATION STRATEGY
# ============================================================

import pandas as pd

from src.data_loader import load_data


# ============================================================
# 1. SETTINGS
# ============================================================

initial_capital = 100_000

transaction_cost = 0.001       # 0.10%
slippage = 0.0005              # 0.05%

execution_cost = (
    transaction_cost + slippage
)


# ============================================================
# 2. LOAD DATA
# ============================================================

data = load_data()


# ============================================================
# 3. RATIO
# ============================================================

data["ratio"] = (
    data["close_nifty"]
    / data["close_gold"]
)


# ============================================================
# 4. 20-DAY BREAKOUT LEVELS
# ============================================================

data["previous_20_high"] = (
    data["ratio"]
    .rolling(20)
    .max()
    .shift(1)
)

data["previous_20_low"] = (
    data["ratio"]
    .rolling(20)
    .min()
    .shift(1)
)


# ============================================================
# 5. SIGNAL
# ============================================================

data["signal"] = 0

data.loc[
    data["ratio"] > data["previous_20_high"],
    "signal"
] = 1

data.loc[
    data["ratio"] < data["previous_20_low"],
    "signal"
] = -1


# ============================================================
# 6. POSITION
# ============================================================

data["position"] = (
    data["signal"]
    .replace(0, pd.NA)
    .ffill()
    .fillna(0)
    .astype(int)
)


# ============================================================
# 7. ASSET RETURNS
# ============================================================

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


# ============================================================
# 8. ACTUAL HELD POSITION
# ============================================================

data["held_position"] = (
    data["position"]
    .shift(1)
    .fillna(0)
    .astype(int)
)


# ============================================================
# 9. POSITION CHANGES
# ============================================================

data["held_position_change"] = (
    data["held_position"]
    .diff()
    .abs()
)


# ============================================================
# 10. TRANSACTION COST + SLIPPAGE
# ============================================================

data["cost"] = 0.0

data.loc[
    data["held_position_change"] == 1,
    "cost"
] = execution_cost

data.loc[
    data["held_position_change"] == 2,
    "cost"
] = execution_cost * 2


# ============================================================
# 11. STRATEGY RETURN
# ============================================================

data["strategy_return"] = 0.0

data.loc[
    data["held_position"] == 1,
    "strategy_return"
] = data["nifty_return"]

data.loc[
    data["held_position"] == -1,
    "strategy_return"
] = data["gold_return"]


# ============================================================
# 12. RETURN AFTER COST
# ============================================================

data["strategy_return_after_cost"] = (
    data["strategy_return"]
    - data["cost"]
)


# ============================================================
# 13. EQUITY CURVE
# ============================================================

data["equity"] = (
    initial_capital
    * (
        1
        + data["strategy_return_after_cost"]
    ).cumprod()
)

end_value = data["equity"].iloc[-2]


# ============================================================
# 14. CAGR
# ============================================================

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


# ============================================================
# 15. DRAWDOWN
# ============================================================

running_max = (
    data["equity"].cummax()
)

drawdown = (
    data["equity"]
    / running_max
) - 1

max_drawdown = (
    drawdown.min()
)


# ============================================================
# 16. DRAWDOWN DURATION
# ============================================================

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


# ============================================================
# 17. STRATEGY RISK METRICS
# ============================================================

annualized_volatility = (
    data["strategy_return_after_cost"].std()
    * (252 ** 0.5)
)

sharpe_ratio = (
    data["strategy_return_after_cost"].mean()
    / data["strategy_return_after_cost"].std()
    * (252 ** 0.5)
)

downside_returns = data.loc[
    data["strategy_return_after_cost"] < 0,
    "strategy_return_after_cost"
]

sortino_ratio = (
    data["strategy_return_after_cost"].mean()
    / downside_returns.std()
    * (252 ** 0.5)
)

calmar_ratio = (
    cagr / abs(max_drawdown)
)


# ============================================================
# 18. POSITION CHANGES
# ============================================================

number_of_trades = (
    data["position"]
    .ne(data["position"].shift())
    .sum()
    - 1
)


# ============================================================
# 19. NIFTYBEES BENCHMARK
# ============================================================

nifty_equity = (
    initial_capital
    * (1 + data["nifty_return"]).cumprod()
)

nifty_final_equity = (
    nifty_equity.iloc[-2]
)

nifty_cagr = (
    nifty_final_equity / initial_capital
) ** (1 / years) - 1

nifty_volatility = (
    data["nifty_return"].std()
    * (252 ** 0.5)
)


# ============================================================
# 20. GOLDBEES BENCHMARK
# ============================================================

gold_equity = (
    initial_capital
    * (1 + data["gold_return"]).cumprod()
)

gold_final_equity = (
    gold_equity.iloc[-2]
)

gold_cagr = (
    gold_final_equity / initial_capital
) ** (1 / years) - 1

gold_volatility = (
    data["gold_return"].std()
    * (252 ** 0.5)
)


# ============================================================
# 21. MONTHLY-REBALANCED 50/50 BENCHMARK
# ============================================================

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

balanced_equity_values = []

current_month = None


for i in range(len(data)):

    row = data.iloc[i]

    # Stop at final incomplete return
    if (
        pd.isna(row["nifty_return"])
        or pd.isna(row["gold_return"])
    ):
        break

    # --------------------------------------------------------
    # Monthly rebalance
    # --------------------------------------------------------

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
            target_nifty - nifty_value
        )

        gold_trade = abs(
            target_gold - gold_value
        )

        total_traded = (
            nifty_trade
            + gold_trade
        )

        # Rebalancing execution cost
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

    # --------------------------------------------------------
    # Daily asset returns
    # --------------------------------------------------------

    nifty_value *= (
        1 + row["nifty_return"]
    )

    gold_value *= (
        1 + row["gold_return"]
    )

    balanced_equity_values.append(
        nifty_value + gold_value
    )


balanced_equity = pd.Series(
    balanced_equity_values,
    index=data.index[
        :len(balanced_equity_values)
    ]
)

balanced_final_equity = (
    balanced_equity.iloc[-1]
)

balanced_cagr = (
    balanced_final_equity
    / initial_capital
) ** (1 / years) - 1

balanced_return = (
    balanced_equity.pct_change()
)

balanced_volatility = (
    balanced_return.std()
    * (252 ** 0.5)
)


# ============================================================
# 22. BENCHMARK DRAWDOWN
# ============================================================

nifty_drawdown = (
    nifty_equity
    / nifty_equity.cummax()
) - 1

gold_drawdown = (
    gold_equity
    / gold_equity.cummax()
) - 1

balanced_drawdown = (
    balanced_equity
    / balanced_equity.cummax()
) - 1

nifty_max_drawdown = (
    nifty_drawdown.min()
)

gold_max_drawdown = (
    gold_drawdown.min()
)

balanced_max_drawdown = (
    balanced_drawdown.min()
)


# ============================================================
# 23. BENCHMARK SHARPE RATIOS
# ============================================================

nifty_sharpe = (
    data["nifty_return"].mean()
    / data["nifty_return"].std()
    * (252 ** 0.5)
)

gold_sharpe = (
    data["gold_return"].mean()
    / data["gold_return"].std()
    * (252 ** 0.5)
)

balanced_sharpe = (
    balanced_return.mean()
    / balanced_return.std()
    * (252 ** 0.5)
)


# ============================================================
# 24. BENCHMARK SORTINO RATIOS
# ============================================================

nifty_downside = data.loc[
    data["nifty_return"] < 0,
    "nifty_return"
]

gold_downside = data.loc[
    data["gold_return"] < 0,
    "gold_return"
]

balanced_downside = (
    balanced_return[
        balanced_return < 0
    ]
)

nifty_sortino = (
    data["nifty_return"].mean()
    / nifty_downside.std()
    * (252 ** 0.5)
)

gold_sortino = (
    data["gold_return"].mean()
    / gold_downside.std()
    * (252 ** 0.5)
)

balanced_sortino = (
    balanced_return.mean()
    / balanced_downside.std()
    * (252 ** 0.5)
)


# ============================================================
# 25. TRADE ANALYSIS
# ============================================================

trade_changes = data[
    data["held_position"].ne(
        data["held_position"].shift()
    )
].copy()

trade_changes = trade_changes[
    trade_changes["held_position"] != 0
]

trade_returns = []

for i in range(
    len(trade_changes) - 1
):

    start_index = (
        trade_changes.index[i]
    )

    end_index = (
        trade_changes.index[i + 1]
    )

    trade_return = (
        data.loc[
            start_index:end_index,
            "strategy_return_after_cost"
        ]
        + 1
    ).prod() - 1

    trade_returns.append(
        trade_return
    )


trade_returns = pd.Series(
    trade_returns
)

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


# ============================================================
# 26. PROFIT FACTOR
# ============================================================

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


# ============================================================
# 27. TRADE EXPECTANCY
# ============================================================

winning_trade_returns = (
    trade_returns[
        trade_returns > 0
    ]
)

losing_trade_returns = (
    trade_returns[
        trade_returns < 0
    ]
)

average_winning_trade = (
    winning_trade_returns.mean()
    if not winning_trade_returns.empty
    else 0
)

average_losing_trade = (
    losing_trade_returns.mean()
    if not losing_trade_returns.empty
    else 0
)

expectancy = (
    win_rate
    * average_winning_trade
    + (1 - win_rate)
    * average_losing_trade
)


# ============================================================
# 28. AVERAGE HOLDING PERIOD
# ============================================================

holding_periods = []

for i in range(
    len(trade_changes) - 1
):

    start_index = (
        trade_changes.index[i]
    )

    end_index = (
        trade_changes.index[i + 1]
    )

    holding_days = (
        data.loc[end_index, "time"]
        - data.loc[start_index, "time"]
    ).days

    holding_periods.append(
        holding_days
    )

average_holding_period = (
    sum(holding_periods)
    / len(holding_periods)
    if holding_periods
    else 0
)


# ============================================================
# 29. NIFTYBEES vs GOLDBEES TRADE ANALYSIS
# ============================================================

nifty_trade_returns = []
gold_trade_returns = []

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

    if position == 1:

        nifty_trade_returns.append(
            trade_return
        )

    elif position == -1:

        gold_trade_returns.append(
            trade_return
        )


nifty_trade_returns = pd.Series(
    nifty_trade_returns
)

gold_trade_returns = pd.Series(
    gold_trade_returns
)


# NIFTYBEES

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


# GOLDBEES

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


# ============================================================
# 30. HOLDING PERIOD BY ASSET
# ============================================================

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

    holding_days = (
        data.loc[end_index, "time"]
        - data.loc[start_index, "time"]
    ).days

    if position == 1:

        nifty_holding_periods.append(
            holding_days
        )

    elif position == -1:

        gold_holding_periods.append(
            holding_days
        )


average_nifty_holding = (
    sum(nifty_holding_periods)
    / len(nifty_holding_periods)
    if nifty_holding_periods
    else 0
)

average_gold_holding = (
    sum(gold_holding_periods)
    / len(gold_holding_periods)
    if gold_holding_periods
    else 0
)


# ============================================================
# 31. BEST AND WORST TRADE
# ============================================================

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


# ============================================================
# 32. RESULTS
# ============================================================

print()
print("=" * 60)
print("NIFTYBEES vs GOLDBEES ROTATION STRATEGY")
print("=" * 60)


# ============================================================
# TRADING ASSUMPTIONS
# ============================================================

print()
print("Trading Assumptions")
print("--------------------")

print(
    f"Initial Capital       : "
    f"₹{initial_capital:,.2f}"
)

print(
    f"Transaction Cost      : "
    f"{transaction_cost:.2%}"
)

print(
    f"Slippage              : "
    f"{slippage:.2%}"
)

print(
    f"Total Execution Cost  : "
    f"{execution_cost:.2%}"
)

print(
    f"Position Changes      : "
    f"{number_of_trades}"
)


# ============================================================
# ROTATION PERFORMANCE
# ============================================================

print()
print("Rotation Strategy")
print("--------------------")

print(
    f"Final Equity          : "
    f"₹{end_value:,.2f}"
)

print(
    f"Absolute Return       : "
    f"{absolute_return:.2%}"
)

print(
    f"CAGR                  : "
    f"{cagr:.2%}"
)

print(
    f"Annualized Volatility : "
    f"{annualized_volatility:.2%}"
)

print(
    f"Sharpe Ratio          : "
    f"{sharpe_ratio:.2f}"
)

print(
    f"Sortino Ratio         : "
    f"{sortino_ratio:.2f}"
)

print(
    f"Calmar Ratio          : "
    f"{calmar_ratio:.2f}"
)

print(
    f"Max Drawdown          : "
    f"{max_drawdown:.2%}"
)

print(
    f"Max Drawdown Duration : "
    f"{max_drawdown_duration} trading days"
)


# ============================================================
# TRADE ANALYSIS
# ============================================================

print()
print("Trade Analysis")
print("--------------------")

print(
    f"Completed Trades      : "
    f"{completed_trades}"
)

print(
    f"Winning Trades        : "
    f"{winning_trades}"
)

print(
    f"Losing Trades         : "
    f"{losing_trades}"
)

print(
    f"Win Rate              : "
    f"{win_rate:.2%}"
)

print(
    f"Average Trade Return  : "
    f"{average_trade_return:.2%}"
)

print(
    f"Gross Profit          : "
    f"{gross_profit:.2%}"
)

print(
    f"Gross Loss            : "
    f"{gross_loss:.2%}"
)

print(
    f"Profit Factor         : "
    f"{profit_factor:.2f}"
)

print(
    f"Average Winning Trade : "
    f"{average_winning_trade:.2%}"
)

print(
    f"Average Losing Trade  : "
    f"{average_losing_trade:.2%}"
)

print(
    f"Trade Expectancy      : "
    f"{expectancy:.2%}"
)

print(
    f"Average Holding Period: "
    f"{average_holding_period:.1f} calendar days"
)

print(
    f"Best Trade            : "
    f"{best_trade:.2%}"
)

print(
    f"Worst Trade           : "
    f"{worst_trade:.2%}"
)


# ============================================================
# ASSET TRADE ANALYSIS
# ============================================================

print()
print("Asset Trade Analysis")
print("--------------------")

print(
    f"NIFTYBEES Trades      : "
    f"{nifty_trade_count}"
)

print(
    f"NIFTYBEES Win Rate    : "
    f"{nifty_win_rate:.2%}"
)

print(
    f"NIFTYBEES Avg Return  : "
    f"{nifty_average_trade:.2%}"
)

print(
    f"NIFTYBEES Avg Holding : "
    f"{average_nifty_holding:.1f} days"
)

print()

print(
    f"GOLDBEES Trades       : "
    f"{gold_trade_count}"
)

print(
    f"GOLDBEES Win Rate     : "
    f"{gold_win_rate:.2%}"
)

print(
    f"GOLDBEES Avg Return   : "
    f"{gold_average_trade:.2%}"
)

print(
    f"GOLDBEES Avg Holding  : "
    f"{average_gold_holding:.1f} days"
)


# ============================================================
# BENCHMARKS
# ============================================================

print()
print("Benchmarks")
print("--------------------")


# NIFTYBEES

print(
    f"NIFTYBEES Final Equity : "
    f"₹{nifty_final_equity:,.2f}"
)

print(
    f"NIFTYBEES CAGR         : "
    f"{nifty_cagr:.2%}"
)

print(
    f"NIFTYBEES Volatility   : "
    f"{nifty_volatility:.2%}"
)

print(
    f"NIFTYBEES Sharpe       : "
    f"{nifty_sharpe:.2f}"
)

print(
    f"NIFTYBEES Sortino      : "
    f"{nifty_sortino:.2f}"
)

print(
    f"NIFTYBEES Max Drawdown : "
    f"{nifty_max_drawdown:.2%}"
)


# GOLDBEES

print()

print(
    f"GOLDBEES Final Equity  : "
    f"₹{gold_final_equity:,.2f}"
)

print(
    f"GOLDBEES CAGR          : "
    f"{gold_cagr:.2%}"
)

print(
    f"GOLDBEES Volatility    : "
    f"{gold_volatility:.2%}"
)

print(
    f"GOLDBEES Sharpe        : "
    f"{gold_sharpe:.2f}"
)

print(
    f"GOLDBEES Sortino       : "
    f"{gold_sortino:.2f}"
)

print(
    f"GOLDBEES Max Drawdown  : "
    f"{gold_max_drawdown:.2%}"
)


# 50/50

print()

print(
    f"50/50 Final Equity     : "
    f"₹{balanced_final_equity:,.2f}"
)

print(
    f"50/50 CAGR             : "
    f"{balanced_cagr:.2%}"
)

print(
    f"50/50 Volatility       : "
    f"{balanced_volatility:.2%}"
)

print(
    f"50/50 Sharpe           : "
    f"{balanced_sharpe:.2f}"
)

print(
    f"50/50 Sortino          : "
    f"{balanced_sortino:.2f}"
)

print(
    f"50/50 Max Drawdown     : "
    f"{balanced_max_drawdown:.2%}"
)


# ============================================================
# END
# ============================================================

print()
print("=" * 60)