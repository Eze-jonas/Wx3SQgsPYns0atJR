# BTC Trading Agent/Bot

## Project Overview

This project presents the design, implementation, and evaluation of an intelligent Bitcoin (BTC) trading agent capable of operating on both historical and live market data. The objective was to investigate the effectiveness of traditional rule-based trading strategies and compare them with an emerging Large Language Model (LLM)-driven trading approach.

The system was developed using historical and live market data obtained from the Binance cryptocurrency exchange. It integrates quantitative market indicators, automated portfolio management, live market streaming, and an interactive web dashboard to provide a complete end-to-end trading environment.

---

## Data Acquisition and Pre-processing

Historical Bitcoin market data was obtained from Binance in the form of two years of five-minute candlestick (kline) data. The following market variables were extracted:

* Open Time
* Open Price
* High Price
* Low Price
* Close Price
* Trading Volume

The raw dataset was converted into a Pandas DataFrame for further analysis and feature engineering. During preprocessing:

* The **Open Time** column was converted into a Python datetime object and used as the DataFrame index to preserve chronological ordering.
* The **Open**, **High**, **Low**, **Close**, and **Volume** columns were converted into floating-point values to enable numerical computation.
* The processed dataset served as the foundation for feature engineering, strategy development, and backtesting.

---

## Rule-Based Trading Agent

The first phase of the project focused on developing a deterministic rule-based Bitcoin trading agent.

A momentum-based strategy was implemented to generate trading signals. The trading pipeline consisted of three main components:

* Momentum-based market analysis
* Signal generation for entry (Buy) and exit (Sell)
* Average True Range (ATR) based stop-loss mechanism for risk management

To support these trading decisions, additional market indicators were computed and appended to the dataset, including:

* Momentum
* Trading Signals
* Average True Range (ATR)

A portfolio management system was also developed to simulate realistic trading by maintaining:

* Available cash
* Bitcoin holdings
* Portfolio valuation
* Trade execution history
* Performance statistics

The rule-based agent was evaluated using historical replay (backtesting), allowing its trading behaviour and financial performance to be analysed under historical market conditions.

---

## Live Trading System

Following successful backtesting, the trading engine was integrated with Binance's live streaming market data.

Incoming market data was continuously received, processed, and passed through the trading pipeline in real time.

To provide user interaction and monitoring capabilities, the system was deployed using FastAPI and connected to an interactive web dashboard.

---

## Interactive Dashboard
![Figure 1. Live Dashboard](images/live_dashboard.png)

The dashboard was implemented using HTML for structure, Bootstrap for responsive styling, and JavaScript for client-side interaction.

The interface provides users with complete visibility of the trading system while it is running.

The dashboard includes Start and Stop controls that allow users to initiate or terminate the trading process without restarting the application.

A runtime counter continuously displays the duration for which the trading agent has been active.

The dashboard consists of four primary components.

### 1. Debug Section

The debug section provides real-time visibility into the internal state of the trading system by displaying:

* Calculated indicators
* Current indicator values
* Trading signal status
* System diagnostic information

This component assists with monitoring and debugging the trading engine during execution.

### 2. Portfolio and Performance Metrics

A portfolio metrics section presents key financial information through summary cards, including:

* Initial capital
* Available cash
* Bitcoin holdings
* Current Bitcoin price
* Portfolio value
* Number of processed candles
* Number of executed trades
* Number of winning trades
* Number of losing trades
* Total profit
* Sharpe Ratio
* Maximum Drawdown

These metrics provide continuous evaluation of trading performance and portfolio health.

### 3. Transaction History

All executed trades are recorded within a transaction table displaying:

* Trade type (Buy or Sell)
* Entry price
* Quantity of Bitcoin purchased or sold
* Profit or loss
* Candle index corresponding to the execution point

This provides complete transparency of trading activity throughout system execution.

### 4. Performance Visualisations

The dashboard also contains graphical performance summaries including:

* An Equity Curve illustrating portfolio growth over time.
* A Pie Chart displaying the ratio of winning to losing trades.

These visualisations enable rapid assessment of overall trading performance.

---

## LLM-Based Trading Agent

The second phase of the project investigated the application of Large Language Models for trading decision making.

Rather than relying on manually designed trading rules, the rule-based signal generation layer was replaced with an LLM-based decision engine using the locally deployed Ollama implementation of Llama 3.1.

The LLM was responsible for analysing market information and determining trading actions without predefined entry and exit rules.

To improve decision quality, market indicators were progressively introduced into the LLM's input. Instead of exposing all indicators simultaneously, each indicator was incorporated incrementally, creating separate experimental versions of the trading agent.

Version control was maintained using Git, allowing each stage of development to be tracked and evaluated independently.

The indicators introduced during experimentation included:

* Momentum
* Simple Moving Average (SMA)
* Relative Strength Index (RSI)

In addition to technical indicators, Bitcoin market sentiment data based on the Fear and Greed Index was incorporated to provide the LLM with broader market context beyond price action alone.

The live dashboard was used throughout experimentation to monitor changes in portfolio performance, trading behaviour, profitability, and overall system performance as additional information became available to the LLM.

---

## System Architecture

The completed system combines several integrated components:

* Binance historical and live market data
* Data preprocessing and feature engineering
* Rule-based trading engine
* LLM-based trading engine
* Portfolio management module
* Risk management using ATR stop-loss
* FastAPI backend
* Interactive web dashboard
* Live market streaming
* Performance evaluation and visual analytics

This modular architecture enables future extension through additional indicators, alternative trading strategies, enhanced risk management techniques, or more advanced language models without requiring major structural modifications.


# Conclusion

This project successfully demonstrated the development of a complete Bitcoin trading system capable of operating on both historical and live market data. Beginning with a deterministic rule-based trading agent, the project established a reliable baseline using momentum-based signal generation and ATR-based risk management before progressing to a live trading environment with real-time market streaming and interactive performance monitoring.

The implementation of a FastAPI-powered dashboard provided continuous visibility into the internal state of the trading system through live portfolio metrics, transaction history, debugging information, and performance visualisations. This enabled effective monitoring, evaluation, and analysis of trading behaviour during both backtesting and live execution.

A significant contribution of this work was the exploration of Large Language Models as trading decision-makers. By replacing the rule-based signal generation layer with an Ollama-hosted Llama 3.1 model, the project investigated whether an LLM could make trading decisions based on progressively richer market information. Technical indicators such as Momentum, SMA, and RSI, together with the Bitcoin Fear and Greed Index, were incrementally incorporated into the model's context, allowing the impact of additional market information on trading behaviour to be observed and evaluated.

The project illustrates both the potential and the limitations of integrating LLMs into algorithmic trading systems. While deterministic rule-based strategies provide consistent and predictable execution, LLMs offer flexibility by reasoning over multiple market signals and qualitative information. However, effective deployment of LLMs requires careful prompt engineering, structured market context, and robust risk management to ensure reliable decision making.

Overall, the project demonstrates a practical hybrid framework that combines traditional quantitative trading techniques with modern artificial intelligence methods. The resulting architecture provides a scalable foundation for future enhancements, including additional technical indicators, multi-strategy portfolio management, reinforcement learning, autonomous agent frameworks, advanced risk management techniques, and integration with multiple financial markets. The modular design ensures that future improvements can be incorporated while preserving the robustness and extensibility of the overall trading system.
