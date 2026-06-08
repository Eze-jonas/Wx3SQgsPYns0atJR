from scripts.state.state import live_state


def update_debug(
    action: str,
    momentum: float,
    sma_pct: float = 0.0,
    atr_pct: float = 0.0,
):
    """
    Updates live debug state for dashboard.
    """

    action = action or "HOLD"
    momentum = momentum or 0.0
    sma_pct = sma_pct or 0.0
    atr_pct = atr_pct or 0.0

    live_state["latest_debug"] = {
        "signal": action,
        "momentum": float(momentum),
        "sma_pct": float(sma_pct),
        "atr_pct": float(atr_pct),
    }