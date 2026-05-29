import logging
from scripts.state.state import live_state
from scripts.debugs.debug import update_debug

logger = logging.getLogger(__name__)

def execute_trade(row):
   
    momentum = row["momentum"]
    price = row["close"]
    
    signal = row["signal"]

    # UPDATE MARKET STATE
    live_state["current_price"] = price
    live_state["last_signal"] = signal
    

    cash = live_state["cash"]
    btc = live_state["btc_holdings"]

    # BUY
    if signal == 1 and btc == 0:

        invest = min(
            live_state["position_size"],cash)

        if invest > 0:
            btc_qty = invest / price

            # UPDATE STATE
            live_state["btc_holdings"] = btc_qty
            live_state["cash"] -= invest
            live_state["entry_price"] = price
            live_state["highest_price"] = price
            live_state["last_action"] = "BUY"

            # STORE TRADE
            live_state["trades"].append({
               
                "type": "BUY",

                "price": float(price),

                "qty": float(btc_qty),

                "invest": float(invest),

                "cash_after": float(
                    live_state["cash"]),

                # chart marker position
                "index": int(
                    live_state["candle_count"]),

                # preserve entry
                "entry_price": float(price)})

            # DEBUG
            update_debug(
                signal,
                "BUY",
                momentum)

            logger.info(
                f"BUY | price={price:.2f} "
                f"| qty={btc_qty:.6f}")

    # SELL
    elif signal == 0 and btc > 0:

        proceeds = btc * price

        # FIND LAST BUY ENTRY
        entry_price = None

        for trade in reversed(
            live_state["trades"]
        ):

            if trade["type"] == "BUY":

                entry_price = trade.get(
                    "entry_price",
                    trade["price"]
                )

                break

        if entry_price is None:

            entry_price = live_state.get(
                "entry_price",
                price
            )

        # PNL
        pnl = (
            (price - entry_price)
            * btc
        )

        # UPDATE STATE
        live_state["cash"] += proceeds

        live_state["btc_holdings"] = 0

        live_state["exit_price"] = price

        live_state["last_action"] = "SELL"

        # STORE TRADE
        live_state["trades"].append({

            "type": "SELL",

            "price": float(price),

            "qty": float(btc),

            "proceeds": float(proceeds),

            "pnl": float(pnl),

            "cash_after": float(
                live_state["cash"]),

            # chart marker position
            "index": int(
                live_state["candle_count"]),

            "entry_price": float(
                entry_price)})

        # RESET POSITION STATE
        live_state["entry_price"] = 0

        live_state["exit_price"] = price

        # DEBUG
        update_debug(
            signal,
            "SELL",
            momentum
        )

        logger.info(
            f"SELL | pnl={pnl:.2f}"
        )

    # HOLD
    else:

        live_state["last_action"] = "HOLD"

        update_debug(
            signal,
            "HOLD",
            momentum
        )

    # EQUITY UPDATE
    btc_value = (
        live_state["btc_holdings"] * price)

    equity = (
        live_state["cash"] + btc_value)

    live_state["equity_curve"].append(float(equity))

    # DRAWDOWN UPDATE
    equity_curve = live_state["equity_curve"]

    peak_equity = max(equity_curve)

    if peak_equity > 0:

        drawdown = (
            (equity - peak_equity)
            / peak_equity
        ) * 100

    else:
        drawdown = 0

    live_state["drawdown_curve"].append(float(drawdown))

    # KEEP LAST 500 POINTS
    for key in [
        "equity_curve",
        "drawdown_curve"
    ]:

        if len(live_state[key]) > 500:

            live_state[key] = (
                live_state[key][-500:]
            )

    # KEEP LAST 500 TRADES
    if len(live_state["trades"]) > 500:

        live_state["trades"] = (
            live_state["trades"][-500:]
        )