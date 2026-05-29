import logging
import pandas as pd
from binance import ThreadedWebsocketManager
from scripts.system_pipeline.pipeline import process_candle

logger = logging.getLogger(__name__)


def start_socket():
    twm = ThreadedWebsocketManager()
    twm.start()
    logger.info("WebSocket started...")

    # CALLBACK FUNCTION
    def handle(msg):
        try:
            # only process closed 1-minute candles
            if msg['e'] == 'kline' and msg['k']['x'] is True:

                candle = {
                    "open_time": pd.to_datetime(msg['k']['t'], unit='ms'),
                    "open": float(msg['k']['o']),
                    "high": float(msg['k']['h']),
                    "low": float(msg['k']['l']),
                    "close": float(msg['k']['c']),
                    "volume": float(msg['k']['v'])
                }

                live_candle = (
                    pd.DataFrame([candle])
                    .set_index("open_time")
                    .astype(float)
                )

                # SEND TO PIPELINE
                process_candle(live_candle)

        except Exception as e:
            logger.exception(f"WebSocket handler error: {e}")

    # START STREAM
    twm.start_kline_socket(
        callback=handle,
        symbol="BTCUSDT",
        interval="1m"
    )

    twm.join()