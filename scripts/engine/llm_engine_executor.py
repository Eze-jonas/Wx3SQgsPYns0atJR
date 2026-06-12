import logging

from scripts.state.state import live_state
from scripts.debugs.debug import update_debug
from scripts.engine.llm_engine import LLMWrapper

logger = logging.getLogger(__name__)

llm = LLMWrapper(model="llama3.2")


def execute_trade(row):

    if row is None:
        return

    price = row.get("close")
    momentum = row.get("momentum")
    sma_pct = row.get("sma_pct")
    atr = row.get("atr") or live_state.get("atr", 0.0)         # raw ATR (NOT percentage)
    rsi = row.get("rsi")

    if price is None or price == 0:
        return

    # =========================
    # POSITION STATE
    # =========================
    btc_holdings = live_state["btc_holdings"]
    cash = live_state["cash"]

    is_flat = btc_holdings == 0
    is_long = btc_holdings > 0

    # =========================
    # LLM INPUT
    # =========================
    logger.info(
        f"LLM INPUT | momentum={momentum} | sma_pct={sma_pct} | atr={atr} | rsi={rsi}"
    )

    llm_result = llm.get_signal({
        "momentum": momentum,
        "sma_pct": sma_pct,
        "rsi": rsi
    })

    signal = llm_result["signal"]

    # =========================
    # SAFE GUARD
    # =========================
    if signal not in ["BUY", "SELL", "HOLD"]:
        signal = "HOLD"

    logger.info(f"LLM OUTPUT | signal={signal}")

    # =========================
    # POSITION VALIDATION
    # =========================
    if is_flat and signal == "SELL":
        logger.info("INVALID ACTION: SELL while FLAT -> HOLD")
        signal = "HOLD"

    if is_long and signal == "BUY":
        logger.info("INVALID ACTION: BUY while LONG -> HOLD")
        signal = "HOLD"

    # =========================
    # UPDATE MARKET STATE
    # =========================
    live_state["current_price"] = price
    live_state["last_llm_decision"] = signal
    live_state["atr"] = atr

    update_debug(signal, momentum, sma_pct, rsi)

    # =========================
    # TRAILING STOP LOGIC
    # =========================
    forced_sell = False

    if is_long:

        entry_price = live_state.get("entry_price", price)

        # initialize highest price if missing
        highest_price = live_state.get("highest_price", price)

        # update highest price
        highest_price = max(highest_price, price)
        live_state["highest_price"] = highest_price

        # ATR trailing stop (2x ATR)
        trailing_stop = highest_price - (2 * atr)
        live_state["stop_loss"] = trailing_stop

        # activate stop only AFTER position is in profit (important fix)
        if price <= trailing_stop:
            logger.info(
                f"ATR TRAILING STOP HIT | price={price:.2f} | stop={trailing_stop:.2f}"
            )
            forced_sell = True

    # =========================
    # SELL DECISION
    # =========================
    if signal == "SELL" and is_long:
        forced_sell = True

    # =========================
    # BUY LOGIC
    # =========================
    if signal == "BUY" and is_flat:

        invest = min(live_state["position_size"], cash)

        if invest > 0:

            qty = invest / price

            live_state["btc_holdings"] = qty
            live_state["cash"] -= invest

            live_state["entry_price"] = price
            live_state["highest_price"] = price
            live_state["stop_loss"] = price - (2 * atr)

            live_state["last_action"] = "BUY"

            live_state["trades"].append({
                "type": "BUY",
                "price": price,
                "qty": qty,
                "invest": invest,
                "index": live_state["candle_count"]
            })

            logger.info(f"BUY | price={price:.2f} | qty={qty:.6f}")

    # =========================
    # SELL EXECUTION
    # =========================
    if forced_sell and is_long:

        qty = btc_holdings
        proceeds = qty * price

        entry_price = live_state.get("entry_price", price)

        pnl = (price - entry_price) * qty

        live_state["cash"] += proceeds
        live_state["btc_holdings"] = 0

        live_state["exit_price"] = price

        # reset trailing state
        live_state["highest_price"] = 0
        live_state["stop_loss"] = 0

        live_state["last_action"] = "SELL"

        live_state["trades"].append({
            "type": "SELL",
            "price": price,
            "qty": qty,
            "proceeds": proceeds,
            "pnl": pnl,
            "index": live_state["candle_count"]
        })

        logger.info(f"SELL | pnl={pnl:.2f}")

    # =========================
    # HOLD STATE
    # =========================
    if not forced_sell:
        live_state["last_action"] = signal if signal in ["BUY", "HOLD"] else "HOLD"

    # =========================
    # EQUITY UPDATE
    # =========================
    btc_value = live_state["btc_holdings"] * price
    equity = live_state["cash"] + btc_value

    live_state["equity_curve"].append(float(equity))

    # =========================
    # DRAWDOWN UPDATE
    # =========================
    peak = max(live_state["equity_curve"])
    drawdown = ((equity - peak) / peak) * 100 if peak > 0 else 0

    live_state["drawdown_curve"].append(float(drawdown))

    # =========================
    # MEMORY LIMIT
    # =========================
    for key in ["equity_curve", "drawdown_curve"]:
        if len(live_state[key]) > 500:
            live_state[key] = live_state[key][-500:]

    if len(live_state["trades"]) > 500:
        live_state["trades"] = live_state["trades"][-500:]