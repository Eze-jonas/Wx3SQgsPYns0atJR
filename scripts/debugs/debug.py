from scripts.state.state import live_state


def update_debug(
    action: str,
    momentum: float
):
    """
    Updates live debug state for dashboard.
    """

    # =========================
    # SAFETY NORMALIZATION
    # =========================
    if action is None:
        action = "HOLD"

    if momentum is None:
        momentum = 0.0

    # =========================
    # STORE DEBUG STATE
    # =========================
    live_state["latest_debug"] = {

        "action": action,

        "momentum": float(momentum)

    }