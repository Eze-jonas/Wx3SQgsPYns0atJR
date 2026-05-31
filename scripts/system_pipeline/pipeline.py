import logging
import pandas as pd
import time

from data.data_loader import load_initial_data
from scripts.strategy.momentum import momentum
from scripts.engine.llm_engine_executor import execute_trade
from scripts.analytics.system_analytics import compute_metrics
from scripts.logger_utils.dedicated_logger import log_state
from scripts.state.state import live_state

logger = logging.getLogger(__name__)


# =========================
# INITIAL HISTORICAL DATA
# =========================
hd_df = load_initial_data()


# =========================
# SYSTEM START TIME
# =========================
start_time = time.time()


# =========================
# PROCESS LIVE CANDLE
# =========================
def process_candle(live_candle):

    global hd_df

    try:
        # =========================
        # INCREMENT CANDLE COUNT
        # =========================
        live_state["candle_count"] += 1

        # store start time once (safe reference)
        live_state["start_time"] = start_time

        # =========================
        # APPEND NEW CANDLE
        # =========================
        hd_df = pd.concat([hd_df, live_candle])

        # remove duplicates
        hd_df = hd_df[~hd_df.index.duplicated(keep="last")]

        # =========================
        # FEATURE ENGINEERING
        # =========================
        momentum_df = momentum(hd_df)
        

        # =========================
        # SIGNAL GENERATION
        # =========================
        latest_row = momentum_df.iloc[-1]
        execute_trade(latest_row)

        # =========================
        # EXECUTE TRADE
        # =========================
        execute_trade(latest_row)

        # =========================
        # UPDATE EXPOSURE HISTORY
        # =========================
        is_in_position = live_state["btc_holdings"] > 0
        live_state["exposure_history"].append(is_in_position)

        # =========================
        # COMPUTE METRICS
        # =========================
        metrics = compute_metrics(live_state)

        # store metrics for dashboard reuse
        live_state["metrics"] = metrics

        # =========================
        # RUNTIME STRING (REMOVED FROM HERE)
        # =========================

        # =========================
        # LOG SYSTEM STATE
        # =========================
        log_state(
            logger=logger,
            live_state=live_state,
            latest_row=latest_row,
            runtime_str=live_state.get("runtime", "00:00:00"),
            metrics=metrics
        )

    except Exception as e:
        logger.exception(f"Failed to process candle: {e}")