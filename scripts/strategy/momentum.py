def momentum(hd_df):
    """
    Parameters: historical_df

    Returns: df with a momentum column.
    """
    momentum_df = hd_df.copy()
    
    momentum_df["momentum"] = momentum_df["close"].pct_change()
    
    return momentum_df