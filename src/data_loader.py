import pandas as pd


def load_data():
    """Load NiftyBeES and GoldBeES data."""

    nifty = pd.read_csv("data/raw/NSE_NIFTYBEES.csv")
    gold = pd.read_csv("data/raw/NSE_GOLDBEES.csv")

    nifty["time"] = pd.to_datetime(
        nifty["time"],
        dayfirst=True
    )

    gold["time"] = pd.to_datetime(
        gold["time"],
        dayfirst=True
    )

    data = pd.merge(
        nifty[["time", "open", "close"]],
        gold[["time", "open", "close"]],
        on="time",
        how="inner",
        suffixes=("_nifty", "_gold")
    )

    return data