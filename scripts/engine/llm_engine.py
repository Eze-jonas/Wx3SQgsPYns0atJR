import requests
import json
import re


class LLMWrapper:

    def __init__(self, model="llama3.2"):
        self.model = model
        self.url = "http://localhost:11434/api/chat"

    # =========================
    # PROMPT
    # =========================
    def build_prompt(self, data):

        return f"""
You are a deterministic trading engine.

You are the ONLY decision maker.

INPUT DATA:
- momentum: {data.get("momentum")}
- price: {data.get("price")}
- position: {data.get("position")}

RULES:
- If momentum > 0 AND not in position → BUY
- If momentum < 0 AND in position → SELL
- Otherwise → HOLD

IMPORTANT:
- You MUST respect position state
- You MUST NOT guess
- You MUST return ONLY valid JSON

OUTPUT FORMAT:
{{"decision":"BUY|SELL|HOLD"}}
"""

    # =========================
    # JSON PARSER (SAFE)
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
    # MAIN DECISION CALL
    # =========================
    def get_decision(self, data):

        payload = {
            "model": self.model,
            "messages": [
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