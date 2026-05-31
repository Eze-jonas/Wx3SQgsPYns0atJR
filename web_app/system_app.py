import sys
import os
import asyncio
import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from scripts.state.state import live_state
from scripts.runtime.runtime_monitor import format_runtime
from scripts.engine.engine_controler import (
    start_live_system,
    stop_live_system,
    get_system_status
)

# FASTAPI APP
app = FastAPI(title="BTC Trading Bot API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates"))

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static")

# LOGGING
def setup_logger():

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s")

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)

    file = RotatingFileHandler(
        "bot.log",
        maxBytes=5_000_000,
        backupCount=3)

    file.setFormatter(formatter)
    logger.addHandler(console)
    logger.addHandler(file)
    return logger

logger = setup_logger()

# ROUTES
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )
    
@app.get("/test")
def test():
    return {"ok": True}

@app.post("/start")
def start():
    logger.info("START ENDPOINT CALLED")
    start_live_system()
    return {"status": "running"}

@app.post("/stop")
def stop():
    logger.info("STOP ENDPOINT CALLED")
    stop_live_system()
    return {"status": "stopped"}

# LIVE WEBSOCKET
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()
    print("DASHBOARD CONNECTED")

    try:
        while True:
            # TIME RUNTIME 
            start_time = live_state.get("start_time")

            if start_time:
                runtime = format_runtime(start_time)
                live_state["runtime"] = runtime
            else:
                runtime = "00:00:00"

            # READ STATE ONLY
            debug = live_state.get("latest_debug", {})
            metrics = live_state.get("metrics", {})
           
            payload = {

                # runtime
                "runtime": runtime,

                # capital
                "start_capital": live_state.get("starting_capital", 0),
                "invested": live_state.get("position_size", 0),

                # balances
                "cash": live_state.get("cash", 0),
                "btc_holdings": live_state.get("btc_holdings", 0),
                "portfolio_value": live_state.get("portfolio_value", 0),

                # prices
                "current_price": live_state.get("current_price", 0),
                "entering_price": live_state.get("entry_price", 0),
                "exit_price": live_state.get("exit_price", 0),

                # candles
                "candle_processed": live_state.get("candle_count", 0),

                # analytics
                **metrics,

                # debug
                 # debug
                "momentum": debug.get("momentum", 0),
                "action": debug.get("action", "HOLD"),

                # curves
                "equity_curve": live_state.get("equity_curve", []),
                "drawdown_curve": live_state.get("drawdown_curve", []),

                # trades
                "trades": live_state.get("trades", []),
            }
            await websocket.send_json(payload)
            await asyncio.sleep(1)

    except Exception as e:
        print("Dashboard disconnected:", e)

# HEALTH CHECK
@app.get("/health")
def health():
    return get_system_status()

# uvicorn web_app.system_app:app --port 8001