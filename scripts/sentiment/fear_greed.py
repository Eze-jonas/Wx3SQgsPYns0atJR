import requests

def get_fear_greed():
    url = "https://api.alternative.me/fng/?limit=1&format=json"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        value = int(data["data"][0]["value"])
        label = data["data"][0]["value_classification"]

        return {
            "value": value,
            "label": label
        }

    except Exception as e:
        print("Fear & Greed fetch error:", e)
        return {
            "value": 50,
            "label": "Neutral"
        }