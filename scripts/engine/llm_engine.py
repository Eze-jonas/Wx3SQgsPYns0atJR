import requests
import json
import re

from scripts.prompt_config.prompt import system_prompt


class LLMWrapper:

    def __init__(self, model="llama3.2"):
        self.model = model
        self.url = "http://localhost:11434/api/chat"

    def build_prompt(self, data):

        momentum = data.get("momentum", 0)
        price = data.get("price", 0)
        position = data.get("position", 0)

        return f"""
INPUT:
- momentum: {momentum}
- price: {price}
- position: {position}

Return ONLY JSON:
{{"signal":"BUY|SELL|HOLD"}}
"""

    def extract_json(self, text):
        try:
            return json.loads(text)
        except:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except:
                    pass
        return None

    def get_signal(self, data):

        user_prompt = self.build_prompt(data)

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

            print("\n" + "=" * 80)
            print("SYSTEM PROMPT")
            print("=" * 80)
            print(system_prompt)

            print("\n" + "=" * 80)
            print("USER PROMPT")
            print("=" * 80)
            print(user_prompt)

            response = requests.post(self.url, json=payload)
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

            signal = parsed.get("signal", "HOLD").upper()

            if signal not in ["BUY", "SELL", "HOLD"]:
                signal = "HOLD"

            print("\nFINAL SIGNAL:", signal)
            print("=" * 80 + "\n")

            return {"signal": signal}

        except Exception as e:
            print("LLM ERROR:", e)
            return {"signal": "HOLD"}