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

    btc = live_state["btc_holdings"]
    cash = live_state["cash"]

    equity_curve = live_state.get("equity_curve", [])
    drawdown_curve = live_state.get("drawdown_curve", [])

    # =========================
    # LLM ONLY DECISION
    # =========================
    llm_result = llm.get_decision({
        "momentum": momentum,
        "price": price,
        "position": "LONG" if btc > 0 else "NONE",

        # OPTIONAL CONTEXT (helps stability)
        "equity": equity_curve[-1] if equity_curve else 0,
        "drawdown": drawdown_curve[-1] if drawdown_curve else 0
    })

    decision = llm_result["decision"]

    # =========================
    # UPDATE STATE
    # =========================
    live_state["current_price"] = price
    live_state["last_llm_decision"] = decision

    # DEBUG
    update_debug(decision, momentum)

    # =========================
    # BUY (NO HARD BLOCKING)
    # =========================
    if decision == "BUY":

        # prevent accidental over-buying (soft guard only)
        if btc == 0:

            invest = min(live_state["position_size"], cash)

            if invest > 0:

                btc_qty = invest / price

                live_state["btc_holdings"] = btc_qty
                live_state["cash"] -= invest
                live_state["entry_price"] = price
                live_state["highest_price"] = price
                live_state["last_action"] = "BUY"

                live_state["trades"].append({
                    "type": "BUY",
                    "price": price,
                    "qty": btc_qty,
                    "invest": invest,
                    "index": live_state["candle_count"]
                })

                logger.info(f"BUY | price={price:.2f} | qty={btc_qty:.6f}")

        else:
            live_state["last_action"] = "HOLD"

    # =========================
    # SELL
    # =========================
    elif decision == "SELL":

        if btc > 0:

            proceeds = btc * price
            entry_price = live_state.get("entry_price", price)

            pnl = (price - entry_price) * btc

            live_state["cash"] += proceeds
            live_state["btc_holdings"] = 0
            live_state["exit_price"] = price
            live_state["last_action"] = "SELL"

            live_state["trades"].append({
                "type": "SELL",
                "price": price,
                "qty": btc,
                "proceeds": proceeds,
                "pnl": pnl,
                "index": live_state["candle_count"]
            })

            logger.info(f"SELL | pnl={pnl:.2f}")

        else:
            live_state["last_action"] = "HOLD"

    # =========================
    # HOLD
    # =========================
    else:
        live_state["last_action"] = "HOLD"

    # =========================
    # EQUITY UPDATE
    # =========================
    btc_value = live_state["btc_holdings"] * price
    equity = live_state["cash"] + btc_value

    live_state["equity_curve"].append(float(equity))

    # =========================
    # SAFE DRAWDOWN CALC
    # =========================
    if len(live_state["equity_curve"]) > 0:
        peak = max(live_state["equity_curve"])
        drawdown = ((equity - peak) / peak) * 100 if peak > 0 else 0
    else:
        drawdown = 0

    live_state["drawdown_curve"].append(float(drawdown))

    # =========================
    # MEMORY LIMIT
    # =========================
    for key in ["equity_curve", "drawdown_curve"]:
        if len(live_state[key]) > 500:
            live_state[key] = live_state[key][-500:]

    if len(live_state["trades"]) > 500:
        live_state["trades"] = live_state["trades"][-500:]