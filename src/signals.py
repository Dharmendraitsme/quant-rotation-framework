# ============================================================
# SIGNAL GENERATION
# ============================================================

import pandas as pd


def generate_signals(data, lookback=20):
    """
    Generate ratio-based breakout signals and positions.

    Signal:
        1  -> NIFTYBEES
       -1  -> GOLDBEES
        0  -> No new signal

    Position holds the previous signal until a new signal appears.
    """

    data = data.copy()

    # --------------------------------------------------------
    # Ratio
    # --------------------------------------------------------

    data["ratio"] = (
        data["close_nifty"]
        / data["close_gold"]
    )

    # --------------------------------------------------------
    # Previous breakout levels
    # --------------------------------------------------------

    data["previous_high"] = (
        data["ratio"]
        .rolling(lookback)
        .max()
        .shift(1)
    )

    data["previous_low"] = (
        data["ratio"]
        .rolling(lookback)
        .min()
        .shift(1)
    )

    # --------------------------------------------------------
    # Signal
    # --------------------------------------------------------

    data["signal"] = 0

    data.loc[
        data["ratio"] > data["previous_high"],
        "signal"
    ] = 1

    data.loc[
        data["ratio"] < data["previous_low"],
        "signal"
    ] = -1

    # --------------------------------------------------------
    # Position
    # --------------------------------------------------------

    data["position"] = (
        data["signal"]
        .replace(0, pd.NA)
        .ffill()
        .fillna(0)
        .astype(int)
    )

    return data