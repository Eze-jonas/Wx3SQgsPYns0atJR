from scripts.state.state import live_state


def update_debug(
    action: str,
    momentum: float,
    sma_pct: float = 0.0
):
    """
    Updates live debug state for dashboard.
    """

    if action is None:
        action = "HOLD"

    if momentum is None:
        momentum = 0.0

    if sma_pct is None:
        sma_pct = 0.0

    live_state["latest_debug"] = {
        "signal": action,
        "momentum": float(momentum),
        "sma_pct": float(sma_pct)
    }