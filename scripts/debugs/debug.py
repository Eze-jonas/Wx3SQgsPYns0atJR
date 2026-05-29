from scripts.state.state import live_state


def update_debug(
    signal: float,
    action: str,
    momentum: float
):
    """
    Updates live debug state for dashboard.
    """

    # =========================
    # SAFETY NORMALIZATION
    # =========================
    if signal is None:
        signal = -1

    if action is None:
        action = "HOLD"

    if momentum is None:
        momentum = 0.0

    # =========================
    # STORE DEBUG STATE
    # =========================
    live_state["latest_debug"] = {
        "signal": float(signal),
        "action": action,
        "momentum": float(momentum)
    }