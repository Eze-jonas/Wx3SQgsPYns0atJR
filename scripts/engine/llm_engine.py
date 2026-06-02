import requests
import json
import re

from scripts.prompt_config.prompt import system_prompt


class LLMWrapper:

    def __init__(self, model="llama3.2"):
        self.model = model
        self.url = "http://localhost:11434/api/chat"

    def build_prompt(self, data):

        return f"""
INPUT:
- momentum: {data.get("momentum")}
- price: {data.get("price")}
- position: {data.get("position")}

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

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": self.build_prompt(data)
                }
            ],
            "stream": False
        }

        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()

            text = response.json()["message"]["content"]
            parsed = self.extract_json(text)

            if not parsed:
                return {"signal": "HOLD"}

            signal = parsed.get("signal", "HOLD").upper()

            if signal not in ["BUY", "SELL", "HOLD"]:
                signal = "HOLD"

            return {"signal": signal}

        except Exception as e:
            print("LLM ERROR:", e)
            return {"signal": "HOLD"}