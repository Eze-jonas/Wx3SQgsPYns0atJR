import numpy as np
import pandas as pd


def compute_metrics(live_state):

    # SAFE DEFAULTS
    starting_capital = live_state.get("starting_capital", 0)
    invested = live_state.get("position_size", 0)
    cash = live_state.get("cash", 0)
    current_price = live_state.get("current_price", 0)

    print("METRICS PRICE:", current_price)

    entry_price = live_state.get("entry_price", 0)
    exit_price = live_state.get("exit_price", 0)
    btc_holdings = live_state.get("btc_holdings", 0)

    trades = live_state.get("trades", [])
    equity_curve = live_state.get("equity_curve", [])

    # =========================
    # RISK MANAGEMENT FIELDS
    # =========================
    highest_price = live_state.get("highest_price", 0.0)
    stop_loss = live_state.get("stop_loss", 0.0)
    atr = live_state.get("atr", 0.0)
    

    risk_distance = (
        current_price - stop_loss
        if stop_loss > 0
        else 0.0
    )
    print(
    f"DEBUG | current_price={current_price} | "
    f"stop_loss={stop_loss} | "
    f"risk_distance={risk_distance}"
)

    portfolio_value = cash + (btc_holdings * current_price)

    # EARLY EXIT SAFETY
    if len(equity_curve) == 0:
        return {
            "starting_capital": starting_capital,
            "invested": invested,
            "cash": cash,
            "current_price": current_price,
            "btc_holdings": btc_holdings,
            "entry_price": entry_price,
            "exit_price": exit_price,
            "candle_count": live_state.get("candle_count", 0),
            "portfolio_value": round(portfolio_value, 2),

            # RISK METRICS (NEW)
            "highest_price": highest_price,
            "stop_loss": stop_loss,
            "atr": atr,
            "double_atr": atr * 2,
            "risk_distance": risk_distance,

            "total_trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0,
            "expectancy": 0,
            "total_profit": 0,
            "profit_factor": 0,
            "sharpe_ratio": 0,
            "max_drawdown": 0,
            "cagr": 0,
            "exposure": 0,

            "momentum": 0,
            "signal": "HOLD"
        }

    trades_df = pd.DataFrame(trades)

    sell_df = (
        trades_df[trades_df["type"] == "SELL"].copy()
        if len(trades_df)
        else pd.DataFrame()
    )

    total_trades = len(sell_df)

    wins = (
        (sell_df.get("pnl", pd.Series()) > 0).sum()
        if "pnl" in sell_df.columns
        else 0
    )

    losses = (
        (sell_df.get("pnl", pd.Series()) < 0).sum()
        if "pnl" in sell_df.columns
        else 0
    )

    win_rate = wins / total_trades if total_trades > 0 else 0

    expectancy = (
        sell_df["pnl"].mean()
        if total_trades > 0 and "pnl" in sell_df.columns
        else 0
    )

    total_profit = (
        sell_df["pnl"].sum()
        if "pnl" in sell_df.columns
        else 0
    )

    gross_profit = (
        sell_df.loc[sell_df["pnl"] > 0, "pnl"].sum()
        if "pnl" in sell_df.columns
        else 0
    )

    gross_loss = (
        abs(sell_df.loc[sell_df["pnl"] < 0, "pnl"].sum())
        if "pnl" in sell_df.columns
        else 0
    )

    profit_factor = (
        gross_profit / gross_loss
        if gross_loss != 0
        else 0
    )

    equity = pd.Series(equity_curve)

    returns = equity.pct_change().dropna()

    sharpe_ratio = (
        (returns.mean() / returns.std()) * np.sqrt(252)
        if len(returns) > 1 and returns.std() != 0
        else 0
    )

    rolling_max = equity.cummax()
    drawdown = (equity - rolling_max) / rolling_max
    max_drawdown = drawdown.min() if len(drawdown) > 0 else 0

    exposure_history = live_state.get("exposure_history", [])
    exposure = (
        sum(exposure_history) / len(exposure_history)
        if exposure_history
        else 0
    )

    start_value = equity.iloc[0]
    end_value = equity.iloc[-1]

    n_periods = max(len(equity), 1)

    cagr = (
        (end_value / start_value) ** (252 / n_periods) - 1
        if start_value > 0
        else 0
    )

    return {
        "starting_capital": starting_capital,
        "invested": invested,
        "cash": round(cash, 2),
        "current_price": round(current_price, 2),
        "btc_holdings": round(btc_holdings, 6),
        "portfolio_value": round(portfolio_value, 2),

        "entry_price": round(entry_price, 2),
        "exit_price": round(exit_price, 2),
        "candle_count": live_state.get("candle_count", 0),

        # RISK METRICS (NEW)
        "highest_price": round(highest_price, 2),
        "stop_loss": round(stop_loss, 2),
        "atr": round(atr, 2),
        "double_atr": round(atr * 2, 2),
        "risk_distance": round(risk_distance, 2),

        "total_trades": total_trades,
        "wins": int(wins),
        "losses": int(losses),
        "win_rate": round(win_rate * 100, 2),
        "expectancy": round(expectancy, 2),
        "total_profit": round(total_profit, 2),
        "profit_factor": round(profit_factor, 2),

        "sharpe_ratio": round(sharpe_ratio, 2),
        "max_drawdown": round(max_drawdown * 100, 2),
        "cagr": round(cagr * 100, 2),
        "exposure": round(exposure * 100, 2),

        "momentum": live_state.get("latest_debug", {}).get("momentum", 0),
        "signal": live_state.get("latest_debug", {}).get("signal", "HOLD")
    }