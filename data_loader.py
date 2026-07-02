import pandas as pd
import logging
from binance.client import Client

logger = logging.getLogger(__name__)

client = Client()


def load_initial_data(
    symbol="BTCUSDT",
    interval=Client.KLINE_INTERVAL_1MINUTE,
    lookback="2 days ago UTC"
):

    try:
        logger.info("Loading historical data from Binance...")

        raw = client.get_historical_klines(
            symbol,
            interval,
            lookback
        )

        hd_df = pd.DataFrame(
            raw,
            columns=[
                "open_time", "open", "high", "low",
                "close", "volume",
                "close_time", "quote_asset_volume",
                "num_trades", "taker_buy_base",
                "taker_buy_quote", "ignore"
            ]
        )

        hd_df = hd_df[
            ["open_time", "open", "high", "low", "close", "volume"]
        ]

        hd_df["open_time"] = pd.to_datetime(
            hd_df["open_time"],
            unit="ms"
        )

        hd_df = hd_df.set_index("open_time").sort_index()

        hd_df = hd_df.astype(float)

        logger.info(f"Historical dataset ready: {hd_df.shape}")

        return hd_df

    except Exception as e:
        logger.exception("Failed to load historical data")
        raise