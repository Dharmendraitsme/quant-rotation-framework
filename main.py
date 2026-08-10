import pandas as pd
from src.data_loader import load_data


data = load_data()

transaction_cost = 0.001
slippage = 0.0005

data["ratio"] = data["close_nifty"] / data["close_gold"]

data["previous_20_high"] = (
    data["ratio"].rolling(20).max().shift(1)
)

data["previous_20_low"] = (
    data["ratio"].rolling(20).min().shift(1)
)

data["signal"] = 0

data.loc[
    data["ratio"] > data["previous_20_high"],
    "signal"
] = 1

data.loc[
    data["ratio"] < data["previous_20_low"],
    "signal"
] = -1

data["position"] = data["signal"].replace(0, pd.NA).ffill().fillna(0)

data["nifty_return"] = data["open_nifty"].shift(-1) / data["open_nifty"] - 1

data["gold_return"] = data["open_gold"].shift(-1) / data["open_gold"] - 1

data["held_position"] = (data["position"].shift(1).fillna(0).astype(int))

data["held_position_change"] = data["held_position"].diff().abs()

data["cost"] = 0.0

execution_cost = transaction_cost + slippage

data.loc[
    data["held_position_change"] == 1,
    "cost"
] = execution_cost

data.loc[
    data["held_position_change"] == 2,
    "cost"
] = execution_cost * 2

data["strategy_return"] = 0.0

data.loc[
    data["held_position"] == 1,
    "strategy_return"
] = data["nifty_return"]

data.loc[
    data["held_position"] == -1,
    "strategy_return"
] = data["gold_return"]

data["strategy_return_after_cost"] = (
    data["strategy_return"] - data["cost"]
)

initial_capital = 100_000

data["equity"] = (
    initial_capital
    * (1 + data["strategy_return_after_cost"]).cumprod()
)
start_value = data["equity"].iloc[0]
end_value = data["equity"].iloc[-2]

absolute_return = (end_value / initial_capital) - 1

start_date = data["time"].iloc[0]
end_date = data["time"].iloc[-2]

years = (end_date - start_date).days / 365.25

cagr = (end_value / initial_capital) ** (1 / years) - 1

drawdown = data["equity"] / data["equity"].cummax() - 1
max_drawdown = drawdown.min()

trades = data[
    data["position"].ne(data["position"].shift())
][
    [
        "time",
        "ratio",
        "signal",
        "position"
    ]
]

number_of_trades = (data["position"] != data["position"].shift()).sum() - 1

print(f"Number of Trades: {number_of_trades}")

print("\nPerformance")
print("--------------------")
print(f"Initial Capital : ₹{initial_capital:,.2f}")
print(f"Final Equity    : ₹{end_value:,.2f}")
print(f"Absolute Return : {absolute_return:.2%}")
print(f"CAGR            : {cagr:.2%}")
print(f"Max Drawdown    : {max_drawdown:.2%}")

