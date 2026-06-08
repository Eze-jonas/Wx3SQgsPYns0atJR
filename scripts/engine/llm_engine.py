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

        print(
            f"MOMENTUM={momentum} | "
            f"SMA_PCT={sma_pct}"
            )

        try:

            response = self.chain.invoke({
                "momentum": momentum,
                "sma_pct": sma_pct
            })

            signal = response.content.strip().upper()

            print("\nFINAL SIGNAL:", signal)
            print("=" * 80)

            if signal not in [
                "BUY",
                "SELL",
                "HOLD"
            ]:
                signal = "HOLD"

            return {
                "signal": signal
            }

        except Exception as e:

            print("LLM ERROR:", e)

            return {
                "signal": "HOLD"
            }