from datetime import datetime, timedelta
from scripts.sentiment.fear_greed import get_fear_greed


fear_greed_cache = {
    "value": 50,
    "label": "Neutral",
    "last_update": datetime.min
}

CACHE_TTL = timedelta(minutes=30)


def get_cached_fear_greed():
    now = datetime.utcnow()

    if now - fear_greed_cache["last_update"] > CACHE_TTL:
        fg = get_fear_greed()

        fear_greed_cache["value"] = fg["value"]
        fear_greed_cache["label"] = fg["label"]
        fear_greed_cache["last_update"] = now

    return fear_greed_cache