def add_sma(momentum_df, window=10):
    sma_df = momentum_df.copy()

    sma_df["sma"] = sma_df["close"].rolling(window=window).mean()

    ratio = sma_df["close"] / sma_df["sma"]
    sma_df["sma_pct"] = (ratio - 1) * 100

    return sma_df