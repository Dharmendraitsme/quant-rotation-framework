import pandas as pd
from src.data_loader import load_data


data = load_data()

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

data["held_position"] = data["position"].shift(1)

data["strategy_return"] = 0.0

data.loc[
    data["held_position"] == 1,
    "strategy_return"
] = data["nifty_return"]

data.loc[
    data["held_position"] == -1,
    "strategy_return"
] = data["gold_return"]

initial_capital = 100_000

data["equity"] = (
    initial_capital
    * (1 + data["strategy_return"]).cumprod()
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

print("\nPerformance")
print("--------------------")
print(f"Initial Capital : ₹{initial_capital:,.2f}")
print(f"Final Equity    : ₹{end_value:,.2f}")
print(f"Absolute Return : {absolute_return:.2%}")
print(f"CAGR            : {cagr:.2%}")
print(f"Max Drawdown    : {max_drawdown:.2%}")