import logging
import numpy as np

from scripts.state.state import live_state
from scripts.debugs.debug import update_debug
from scripts.engine.llm_engine import LLMWrapper

logger = logging.getLogger(__name__)
llm = LLMWrapper(model="llama3.2")


def execute_trade(row):

    momentum = row["momentum"]
    price = row["close"]

    # =========================
    # POSITION STATE (FLAT / LONG)
    # =========================
    btc_holdings = live_state["btc_holdings"]

    is_flat = btc_holdings == 0
    is_long = btc_holdings > 0

    cash = live_state["cash"]

    # =========================
    # LLM INPUT
    # =========================
    logger.info(
        f"LLM INPUT | momentum={momentum} | btc_holdings={btc_holdings}"
    )

    llm_result = llm.get_signal({
        "momentum": momentum,
        "btc_holdings": btc_holdings
    })

    signal = llm_result["signal"]

    # =========================
    # SAFE GUARD ONLY
    # =========================
    if signal not in ["BUY", "SELL", "HOLD"]:
        signal = "HOLD"

    logger.info(f"LLM OUTPUT | signal={signal}")

    # =========================
    # POSITION VALIDATION LAYER
    # =========================

    if is_flat and signal == "SELL":
        logger.info("INVALID ACTION: SELL while FLAT → FORCED HOLD")
        signal = "HOLD"

    elif is_long and signal == "BUY":
        logger.info("INVALID ACTION: BUY while LONG → FORCED HOLD")
        signal = "HOLD"

    # =========================
    # STATE UPDATE
    # =========================
    live_state["current_price"] = price
    live_state["last_llm_decision"] = signal

    update_debug(signal, momentum)

    # =========================
    # BUY ONLY WHEN FLAT
    # =========================
    if signal == "BUY" and is_flat:

        invest = min(
            live_state["position_size"],
            cash
        )

        if invest > 0:

            qty = invest / price

            live_state["btc_holdings"] = qty
            live_state["cash"] -= invest
            live_state["entry_price"] = price
            live_state["highest_price"] = price
            live_state["last_action"] = "BUY"

            live_state["trades"].append({
                "type": "BUY",
                "price": price,
                "qty": qty,
                "invest": invest,
                "index": live_state["candle_count"]
            })

            logger.info(
                f"BUY | price={price:.2f} | qty={qty:.6f}"
            )

    # =========================
    # SELL ONLY WHEN LONG
    # =========================
    elif signal == "SELL" and is_long:

        qty = btc_holdings

        proceeds = qty * price

        entry_price = live_state.get(
            "entry_price",
            price
        )

        pnl = (
            (price - entry_price)
            * qty
        )

        live_state["cash"] += proceeds
        live_state["btc_holdings"] = 0

        live_state["exit_price"] = price
        live_state["last_action"] = "SELL"

        live_state["trades"].append({
            "type": "SELL",
            "price": price,
            "qty": qty,
            "proceeds": proceeds,
            "pnl": pnl,
            "index": live_state["candle_count"]
        })

        logger.info(
            f"SELL | pnl={pnl:.2f}"
        )

    else:
        live_state["last_action"] = "HOLD"

    # =========================
    # EQUITY UPDATE
    # =========================
    btc_value = (
        live_state["btc_holdings"]
        * price
    )

    equity = (
        live_state["cash"]
        + btc_value
    )

    live_state["equity_curve"].append(
        float(equity)
    )

    # =========================
    # DRAWDOWN
    # =========================
    if len(live_state["equity_curve"]) > 0:

        peak = max(
            live_state["equity_curve"]
        )

        drawdown = (
            ((equity - peak) / peak) * 100
            if peak > 0
            else 0
        )

    else:
        drawdown = 0

    live_state["drawdown_curve"].append(
        float(drawdown)
    )

    # =========================
    # MEMORY LIMIT
    # =========================
    for key in [
        "equity_curve",
        "drawdown_curve"
    ]:

        if len(live_state[key]) > 500:
            live_state[key] = (
                live_state[key][-500:]
            )

    if len(live_state["trades"]) > 500:
        live_state["trades"] = (
            live_state["trades"][-500:]
        )