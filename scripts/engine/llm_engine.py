import requests
import json
import re

from scripts.prompt_config.prompt import system_prompt


class LLMWrapper:

    def __init__(self, model="llama3.2"):
        self.model = model
        self.url = "http://localhost:11434/api/chat"

    # =========================
    # DATA ONLY PROMPT
    # =========================
    def build_prompt(self, data):

        return f"""
momentum: {data.get("momentum")}
price: {data.get("price")}
position: {data.get("position")}
"""

    # =========================
    # SAFE JSON PARSER
    # =========================
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

    # =========================
    # MAIN DECISION FUNCTION
    # =========================
    def get_decision(self, data):

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

            result_text = response.json()["message"]["content"]

            parsed = self.extract_json(result_text)

            if not parsed:
                return {"decision": "HOLD"}

            decision = parsed.get("decision", "HOLD").upper()

            if decision not in ["BUY", "SELL", "HOLD"]:
                decision = "HOLD"

            return {"decision": decision}

        except Exception as e:
            print("LLM ERROR:", e)
            return {"decision": "HOLD"}