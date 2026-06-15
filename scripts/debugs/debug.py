from scripts.state.state import live_state


def update_debug(
    action: str,
    momentum: float,
    sma_pct: float = 0.0,
    rsi: float = 0.0,
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

    if rsi is None:
        rsi = 0.0

    # =========================
    # TRAILING STOP DEBUG
    # =========================
    highest_price = live_state.get("highest_price", 0.0)
    stop_loss = live_state.get("stop_loss", 0.0)

    risk_distance = (
        live_state.get("current_price", 0.0) - stop_loss
        if stop_loss > 0
        else 0.0
    )

    # =========================
    # FEAR & GREED DEBUG
    # =========================
    fear_greed = live_state.get("fear_greed", 50)
    fear_greed_label = live_state.get(
        "fear_greed_label",
        "Neutral"
    )

    # =========================
    # SAVE DEBUG STATE
    # =========================
    live_state["latest_debug"] = {
        "signal": action,
        "momentum": float(momentum),
        "sma_pct": float(sma_pct),
        "rsi": float(rsi),

        # FEAR & GREED
        "fear_greed": int(fear_greed),
        "fear_greed_label": fear_greed_label,

        # RISK MANAGEMENT
        "highest_price": float(highest_price),
        "stop_loss": float(stop_loss),
        "risk_distance": float(risk_distance),
    }