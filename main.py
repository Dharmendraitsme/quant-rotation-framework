# ============================================================
# NIFTYBEES vs GOLDBEES ROTATION STRATEGY
# ============================================================

import pandas as pd

from src.data_loader import load_data


# ============================================================
# 1. SETTINGS
# ============================================================

initial_capital = 100_000

transaction_cost = 0.001      # 0.10%
slippage = 0.0005             # 0.05%

execution_cost = transaction_cost + slippage


# ============================================================
# 2. LOAD DATA
# ============================================================

data = load_data()


# ============================================================
# 3. RATIO
# ============================================================

data["ratio"] = (
    data["close_nifty"] / data["close_gold"]
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
    data["held_position"].diff().abs()
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
    data["strategy_return"] - data["cost"]
)


# ============================================================
# 13. EQUITY CURVE
# ============================================================

data["equity"] = (
    initial_capital
    * (1 + data["strategy_return_after_cost"]).cumprod()
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

running_max = data["equity"].cummax()

drawdown = (
    data["equity"] / running_max
) - 1

max_drawdown = drawdown.min()


# ============================================================
# 16. DRAWDOWN DURATION
# ============================================================

in_drawdown = drawdown < 0

groups = (
    ~in_drawdown
).cumsum()

drawdown_duration = (
    data.loc[in_drawdown]
    .groupby(groups[in_drawdown])
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
# 21. RESULTS
# ============================================================

print()
print("============================================================")
print("NIFTYBEES vs GOLDBEES ROTATION STRATEGY")
print("============================================================")

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


print()
print("Benchmarks")
print("--------------------")

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

print("============================================================")