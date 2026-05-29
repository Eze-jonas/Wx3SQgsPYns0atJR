import threading
import time
import logging

from data.web_socket import start_socket
from scripts.state.state import live_state

logger = logging.getLogger(__name__)


# =========================
# SYSTEM FLAG
# =========================
system_running = False
ws_thread = None


# =========================
# START SYSTEM
# =========================
def start_live_system():

    global system_running, ws_thread

    if system_running:
        logger.warning("System already running")
        return

    system_running = True

    logger.info("STARTING LIVE TRADING SYSTEM")

    # =========================
    # FIX: INITIALISE RUNTIME CLOCK
    # =========================
    live_state["start_time"] = time.time()
    live_state["runtime"] = "00:00:00"

    def run_socket():

        try:
            start_socket()

        except Exception as e:
            logger.exception(f"WebSocket crashed: {e}")

    ws_thread = threading.Thread(
        target=run_socket,
        daemon=True
    )

    ws_thread.start()

    logger.info("WebSocket thread started")


# =========================
# STOP SYSTEM
# =========================
def stop_live_system():

    global system_running

    if not system_running:
        logger.warning("System already stopped")
        return

    system_running = False

    # reset state if needed
    live_state["last_action"] = "STOPPED"

    logger.info("LIVE SYSTEM STOPPED")


# =========================
# STATUS CHECK
# =========================
def get_system_status():

    return {
        "running": system_running,
        "cash": live_state["cash"],
        "btc": live_state["btc_holdings"],
        "last_price": live_state["current_price"],
        "last_action": live_state["last_action"],
        "runtime": live_state.get("runtime", "00:00:00")
    }