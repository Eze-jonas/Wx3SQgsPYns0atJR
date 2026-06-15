from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama

from scripts.prompt_config.prompt import (
    system_prompt,
    user_prompt
)


class LLMWrapper:

    def __init__(self, model="llama3.2"):

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_prompt)
        ])

        self.llm = ChatOllama(
            model=model,
            temperature=0
        )

        self.chain = self.prompt | self.llm

    def get_signal(self, data):

        momentum = data.get("momentum", 0)
        sma_pct = data.get("sma_pct", 0)
        rsi = data.get("rsi", 0)

        # =========================
        # FEAR & GREED
        # =========================
        fear_greed = data.get("fear_greed", 50)
        fear_greed_label = data.get("fear_greed_label", "Neutral")

        print(
            f"MOMENTUM={momentum} | "
            f"SMA_PCT={sma_pct} | "
            f"RSI={rsi} | "
            f"FG={fear_greed} | "
            f"LABEL={fear_greed_label}"
        )

        try:

            response = self.chain.invoke({
                "momentum": momentum,
                "sma_pct": sma_pct,
                "rsi": rsi,

                # =========================
                # FEAR & GREED PASSED TO PROMPT
                # =========================
                "fear_greed": fear_greed,
                "fear_greed_label": fear_greed_label,
            })

            response_text = response.content.strip()

            print("\nRAW LLM RESPONSE:")
            print(response_text)
            print("=" * 80)

            response_upper = response_text.upper()

            if "SIGNAL: BUY" in response_upper:
                signal = "BUY"

            elif "SIGNAL: SELL" in response_upper:
                signal = "SELL"

            elif "SIGNAL: HOLD" in response_upper:
                signal = "HOLD"

            else:
                signal = "HOLD"

            print("\nPARSED SIGNAL:", signal)
            print("=" * 80)

            return {
                "signal": signal
            }

        except Exception as e:

            print("LLM ERROR:", e)

            return {
                "signal": "HOLD"
            }