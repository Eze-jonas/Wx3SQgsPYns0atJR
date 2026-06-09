import pandas as pd

def add_sma(momentum_df, window=10):
    sma_df = momentum_df.copy()

    sma_df["sma"] = sma_df["close"].rolling(window=window).mean()

    ratio = sma_df["close"] / sma_df["sma"]
    sma_df["sma_pct"] = (ratio - 1) * 100

    return sma_df



def add_atr(sma_df, window=14):
    atr_df = sma_df.copy()

    # True Range components
    atr_df["prev_close"] = atr_df["close"].shift(1)

    atr_df["tr1"] = atr_df["high"] - atr_df["low"]
    atr_df["tr2"] = (atr_df["high"] - atr_df["prev_close"]).abs()
    atr_df["tr3"] = (atr_df["low"] - atr_df["prev_close"]).abs()

    atr_df["tr"] = atr_df[["tr1", "tr2", "tr3"]].max(axis=1)

    # ATR
    atr_df["atr"] = atr_df["tr"].rolling(window=window).mean()

    # ATR %
    atr_df["atr_pct"] = (atr_df["atr"] / atr_df["close"]) * 100

    return atr_df

def add_rsi(atr_df, window=14):
    rsi_df = atr_df.copy()

    delta = rsi_df["close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss

    rsi_df["rsi"] = 100 - (100 / (1 + rs))

    return rsi_df