import logging
import pandas as pd
import time

from data.data_loader import load_initial_data
from scripts.strategy.momentum import momentum
from scripts.engine.llm_engine_executor import execute_trade
from scripts.analytics.system_analytics import compute_metrics
from scripts.logger_utils.dedicated_logger import log_state
from scripts.state.state import live_state
from scripts.features.indicators import add_sma
from scripts.features.indicators import add_atr
from scripts.features.indicators import add_rsi
from scripts.sentiment.fear_greed_cache import get_cached_fear_greed


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
        sma_df = add_sma(momentum_df)
        atr_df = add_atr(sma_df)
        rsi_df = add_rsi(atr_df)

        # =========================
        # SIGNAL GENERATION
        # =========================
        clean_df = rsi_df.dropna()

        if clean_df.empty:
            return

        latest_row = clean_df.iloc[-1]

        # =========================
        # SENTIMENT UPDATE (FEAR & GREED)
        # =========================
        fg = get_cached_fear_greed()

        live_state["fear_greed"] = fg["value"]
        live_state["fear_greed_label"] = fg["label"]

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