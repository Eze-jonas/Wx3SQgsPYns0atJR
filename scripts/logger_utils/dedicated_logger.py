import logging


def log_state(
    logger,
    live_state,
    latest_row,
    runtime_str,
    metrics
):

    # =========================
    # LIVE STATE
    # =========================
    logger.info("========== LIVE STATE ==========")
    logger.info(f"RUN TIME: {runtime_str}")

    # =========================
    # DEBUG PANEL
    # =========================
    debug_data = live_state.get("latest_debug", {})

    logger.info("========== DEBUG ==========")

    logger.info(f"Signal: {debug_data.get('signal', 'HOLD')}")
    logger.info(f"Momentum: {debug_data.get('momentum', None)}")
    logger.info(f"SMA %: {debug_data.get('sma_pct', None)}")
    logger.info(f"ATR %: {debug_data.get('atr_pct', None)}")
    logger.info(f"RSI %: {debug_data.get('rsi', None)}")

    # =========================
    # LIVE DASHBOARD
    # =========================
    logger.info("========== LIVE DASHBOARD ==========")

    for key, value in metrics.items():
        logger.info(f"{key}: {value}")