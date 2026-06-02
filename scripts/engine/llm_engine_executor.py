# scripts/engine/executor.py

import logging
from scripts.state.state import live_state
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
    # UPDATE LIVE STATE (CRITICAL FIX)
    # =========================
    live_state["momentum"] = momentum
    live_state["current_price"] = price

    # =========================
    # LLM SIGNAL (ANALYST ROLE)
    # =========================
    signal = llm.get_signal({
        "momentum": momentum,
        "price": price,
        "position": "LONG" if btc > 0 else "NONE",
    })["signal"]

    logger.info(f"LLM SIGNAL | momentum={momentum} | signal={signal}")

    live_state["last_signal"] = signal

    # =========================
    # PYTHON EXECUTION (TRADER ROLE)
    # =========================

    # BUY RULE (EXECUTOR CONTROL)
    if signal == "BUY" and btc == 0:

        invest = min(live_state["position_size"], cash)

        if invest > 0:

            qty = invest / price

            live_state["btc_holdings"] = qty
            live_state["cash"] -= invest
            live_state["entry_price"] = price

            live_state["trades"].append({
                "type": "BUY",
                "price": price,
                "qty": qty,
                "index": live_state["candle_count"]
            })

            logger.info(f"BUY EXECUTED | price={price} | qty={qty}")

    # SELL RULE (EXECUTOR CONTROL)
    elif signal == "SELL" and btc > 0:

        proceeds = btc * price
        entry = live_state.get("entry_price", price)

        pnl = (price - entry) * btc

        live_state["cash"] += proceeds
        live_state["btc_holdings"] = 0
        live_state["exit_price"] = price

        live_state["trades"].append({
            "type": "SELL",
            "price": price,
            "qty": btc,
            "pnl": pnl,
            "index": live_state["candle_count"]
        })

        logger.info(f"SELL EXECUTED | pnl={pnl}")

    else:
        live_state["last_action"] = "HOLD"

    # =========================
    # EQUITY UPDATE
    # =========================
    btc_value = live_state["btc_holdings"] * price
    equity = live_state["cash"] + btc_value

    live_state["equity_curve"].append(equity)

    # =========================
    # DRAWDOWN UPDATE
    # =========================
    peak = max(live_state["equity_curve"])
    drawdown = ((equity - peak) / peak) * 100 if peak > 0 else 0

    live_state["drawdown_curve"].append(drawdown)