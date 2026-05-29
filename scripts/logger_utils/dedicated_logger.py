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
    debug_data = live_state["latest_debug"]

    logger.info("========== DEBUG ==========")

    logger.info(f"Momentum: {debug_data['momentum']}")
    logger.info(f"Signal: {debug_data['signal']}")
    logger.info(f"Action: {debug_data['action']}")

    # =========================
    # LIVE DASHBOARD
    # =========================
    logger.info("========== LIVE DASHBOARD ==========")

    for key, value in metrics.items():
        logger.info(f"{key}: {value}")

   