# ============================================================
# MARKET REGIME ANALYSIS
# ============================================================

import pandas as pd


def classify_market_regime(data):
    """
    Classify the market environment using NIFTYBEES trend.

    Bull  -> NIFTYBEES above 200-day moving average
    Bear  -> NIFTYBEES below 200-day moving average
    """

    data = data.copy()

    data["nifty_ma_200"] = (
        data["close_nifty"]
        .rolling(200)
        .mean()
    )

    data["market_regime"] = "Bear"

    data.loc[
        data["close_nifty"]
        > data["nifty_ma_200"],
        "market_regime"
    ] = "Bull"

    return data


def analyze_regimes(data):
    """
    Calculate strategy performance by market regime.
    """

    results = []

    for regime in ["Bull", "Bear"]:

        regime_data = data[
            data["market_regime"] == regime
        ].copy()

        returns = (
            regime_data[
                "strategy_return_after_cost"
            ]
        )

        if returns.empty:
            continue

        volatility = (
            returns.std()
            * (252 ** 0.5)
        )

        sharpe = (
            returns.mean()
            / returns.std()
            * (252 ** 0.5)
            if returns.std() != 0
            else 0
        )

        cumulative_return = (
            (1 + returns).prod()
            - 1
        )

        results.append(
            {
                "Regime": regime,
                "Observations": len(regime_data),
                "Return": cumulative_return,
                "Volatility": volatility,
                "Sharpe": sharpe,
            }
        )

    return pd.DataFrame(results)