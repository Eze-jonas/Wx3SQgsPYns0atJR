import requests
import json

from scripts.prompt_config.prompt import system_prompt
from scripts.momentum_classification.momentum_class import classify_momentum


class LLMWrapper:

    def __init__(self, model="llama3.2"):
        self.model = model
        self.url = "http://localhost:11434/api/chat"

    # -------------------------
    # PROMPT BUILDER
    # -------------------------
    def build_prompt(self, data):

        momentum = data.get("momentum", 0)
        btc_holdings = data.get("btc_holdings", 0)

        momentum_state = classify_momentum(momentum)

        print(
            f"MOMENTUM={momentum} | "
            f"STATE={momentum_state} | "
            f"HOLDINGS={btc_holdings}"
        )

        return f"""
INPUT STATE:
- btc_holdings: {btc_holdings}
- momentum_state: {momentum_state}
"""

    # -------------------------
    # SAFE JSON PARSER
    # -------------------------
    def extract_json(self, text):
        try:
            return json.loads(text)
        except:
            start = text.find("{")
            end = text.rfind("}")

            if start != -1 and end != -1:
                try:
                    return json.loads(text[start:end + 1])
                except:
                    pass

        return None

    # -------------------------
    # MAIN ENGINE
    # -------------------------
    def get_signal(self, data):

        user_prompt = self.build_prompt(data)

        print("\n" + "=" * 80)
        print("USER PROMPT")
        print("=" * 80)
        print(user_prompt)

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0
            }
        }

        try:

            response = requests.post(
                self.url,
                json=payload
            )

            response.raise_for_status()

            text = response.json()["message"]["content"]

            print("\n" + "=" * 80)
            print("RAW LLM RESPONSE")
            print("=" * 80)
            print(text)

            parsed = self.extract_json(text)

            print("\n" + "=" * 80)
            print("PARSED JSON")
            print("=" * 80)
            print(parsed)

            if not parsed:
                return {"signal": "HOLD"}

            signal = parsed.get(
                "signal",
                "HOLD"
            ).upper()

            if signal not in [
                "BUY",
                "SELL",
                "HOLD"
            ]:
                signal = "HOLD"

            print("\nFINAL SIGNAL:", signal)
            print("=" * 80 + "\n")

            return {
                "signal": signal
            }

        except Exception as e:

            print("LLM ERROR:", e)

            return {
                "signal": "HOLD"
            }