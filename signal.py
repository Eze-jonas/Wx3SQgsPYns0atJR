import pandas as pd

def generate_signal(momentum_df):
    """
    Generate trading signals from momentum.

    Parameters: momentum_df 

    Returns: signal column without nas
    """

    signal_df = momentum_df.copy()

    # initialize signal
    signal_df["signal"] = 0

    # BUY rule
    signal_df.loc[signal_df["momentum"] > 0, "signal"] = 1

    # SELL / FLAT rule
    signal_df.loc[signal_df["momentum"] <= 0, "signal"] = 0

    return signal_df.dropna()