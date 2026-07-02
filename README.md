#  BTC Trading Agent/Bot

An intelligent Bitcoin (BTC) trading system that combines **rule-based algorithmic trading**, **Large Language Models (LLMs)**, **live Binance market streaming**, **portfolio management**, and a **FastAPI dashboard** for real-time monitoring and evaluation.

---

##  Project Overview

This project presents the design, implementation, and evaluation of a complete Bitcoin trading agent capable of operating on both **historical** and **live market data**.

The objective was to investigate the effectiveness of traditional rule-based trading strategies and compare them with an emerging **LLM-driven trading approach** using **Ollama's Llama 3.1**.

The system integrates quantitative technical indicators, automated portfolio management, live market streaming, and an interactive web dashboard to provide an end-to-end cryptocurrency trading environment.
---
# ✨ Features

* Historical BTC data processing from Binance
* Live Binance WebSocket streaming
* Rule-based momentum trading strategy
* ATR-based stop-loss risk management
* Portfolio management system
* Historical replay (backtesting)
* Live trading dashboard
* Interactive Start/Stop controls
* Portfolio performance metrics
* Equity curve visualization
* Win/Loss distribution chart
* Trade history monitoring
* LLM-powered trading decisions
* Incremental feature engineering experiments
* Modular architecture for future strategy expansion

---

# 🛠 Technology Stack

### Programming

* Python

### Backend

* FastAPI

### Frontend

* HTML
* Bootstrap
* JavaScript

### Data Processing

* Pandas

### Data Source

* Binance Historical API
* Binance Live WebSocket Stream

### AI

* Ollama
* Llama 3.1

### Version Control

* Git

---
# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/<your-username>/btc_trading_agent.git
cd btc_trading_agent
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv BTC
BTC\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv BTC
source BTC/bin/activate
```

## 3. Install the required packages

```bash
pip install -r requirements.txt
```

## 4. Start Ollama

Make sure Ollama is installed and the Llama 3.1 model has been downloaded.

```bash
ollama pull llama3.1
```

Start the Ollama server:

```bash
ollama serve
```

## 5. Launch the FastAPI application

Start the trading dashboard by running:

```bash
uvicorn web_app.system_app:app --port 8001
```

Open your browser and navigate to:

```text
http://127.0.0.1:8001
```

The dashboard provides controls to:

* Start the trading bot
* Stop the trading bot
* Monitor live market data
* View portfolio metrics
* View transaction history
* Monitor the equity curve
* Monitor trading performance

---

# 📁 Project Structure

```text
btc_trading_agent/
│
├── scripts/
│   ├── features/
│   ├── logics/
│   ├── indicators/
│   ├── states/
│   ├── configurations/
│   └── ...
│
├── web_app/
│   ├── templates/
│   ├── static/
│   └── system_app.py
│
├── images/
│   └── live_dashboard.png
│
├── requirements.txt
├── README.md
└── .gitignore
```
---
# System Architecture

The completed trading system consists of the following modules:

```
Binance Historical Data
            │
            ▼
 Data Pre-processing
            │
            ▼
 Feature Engineering
(Momentum, SMA, RSI, ATR)
            │
            ▼
     Trading Engine
      ├─────────────┐
      │             │
      ▼             ▼
Rule-Based      LLM-Based
 Strategy        Strategy
      │             │
      └──────┬──────┘
             ▼
 Portfolio Manager
             ▼
      Performance Metrics
             ▼
      FastAPI Dashboard
             ▼
      Live Monitoring
```

The modular design allows additional indicators, strategies, and decision models to be integrated without significant architectural changes.

---

# 📊 Data Acquisition and Pre-processing

Historical Bitcoin market data was obtained from Binance using approximately **two years of five-minute candlestick (kline) data**.

The following fields were extracted:

* Open Time
* Open Price
* High Price
* Low Price
* Close Price
* Trading Volume

The raw data was converted into a Pandas DataFrame.

During preprocessing:

* **Open Time** was converted to a datetime object and used as the DataFrame index.
* **Open**, **High**, **Low**, **Close**, and **Volume** were converted into floating-point values.
* The processed dataset formed the foundation for feature engineering, strategy development, and backtesting.

---

# 📈 Phase 1 – Rule-Based Trading Agent

The first stage of the project focused on developing a deterministic rule-based trading system.

A momentum strategy was implemented to generate Buy and Sell signals.

The trading pipeline consisted of:

* Momentum-based market analysis
* Signal generation
* ATR-based stop-loss risk management

The following indicators were engineered:

* Momentum
* Trading Signal
* Average True Range (ATR)

The trading engine was integrated with a portfolio manager capable of tracking:

* Initial capital
* Available cash
* BTC holdings
* Portfolio value
* Trade history
* Trading performance

The strategy was evaluated using historical replay (backtesting).

---

# 📡 Phase 2 – Live Trading System

After validating the rule-based strategy, the trading engine was connected to Binance's live streaming market data.

Incoming candles were processed continuously in real time before being passed through the trading pipeline.

The system was deployed using **FastAPI**, allowing users to monitor the trading process through an interactive web dashboard.

---

# 🖥 Interactive Dashboard

The dashboard was implemented using:

* HTML
* Bootstrap
* JavaScript
* FastAPI

The interface provides complete visibility into the internal state of the trading system while running.

Users can:

* Start the trading bot
* Stop the trading bot
* Monitor runtime
* Observe portfolio performance in real time

---

## Debug Section

The debug panel provides real-time visibility into internal calculations by displaying:

* Technical indicators
* Indicator values
* Trading signal status
* Diagnostic information

This assists with debugging and monitoring the trading engine.

---

## Portfolio Metrics

The dashboard displays:

* Initial Capital
* Cash
* BTC Holdings
* Current BTC Price
* Portfolio Value
* Number of Candles
* Number of Trades
* Wins
* Losses
* Profit
* Sharpe Ratio
* Maximum Drawdown

These metrics provide continuous evaluation of trading performance.

---

## Transaction History

Every executed trade is recorded in a transaction table containing:

* Buy/Sell type
* Entry price
* BTC quantity
* Profit/Loss
* Candle index

This provides complete transparency of trading activity.

---

## Performance Visualizations

The dashboard includes:

* Equity Curve
* Win/Loss Pie Chart

These visualizations allow users to monitor trading performance throughout execution.

---

# 🤖 Phase 3 – LLM Trading Agent

The final stage of the project explored the use of **Large Language Models** for trading decision making.

Instead of relying on manually designed trading rules, the signal generation layer was replaced with an **LLM-based decision engine** powered by **Ollama Llama 3.1**.

The objective was to investigate whether an LLM could make trading decisions using progressively richer market information.

---

## Incremental Feature Engineering

Rather than exposing all indicators simultaneously, indicators were introduced incrementally.

Each addition produced a separate version of the trading bot, with Git used to maintain version history and enable comparison.

The indicators introduced included:

* Momentum
* Simple Moving Average (SMA)
* Relative Strength Index (RSI)

Finally, the **Bitcoin Fear & Greed Index** was incorporated to provide broader market sentiment beyond technical price movements.

The dashboard was continuously used to monitor changes in:

* Portfolio value
* Trading behaviour
* Profitability
* Overall strategy performance

---

# 📂 Project Workflow

```
Historical Binance Data
        │
        ▼
 Data Pre-processing
        │
        ▼
Feature Engineering
        │
        ▼
Rule-Based Trading Bot
        │
        ▼
Historical Backtesting
        │
        ▼
Live Binance Streaming
        │
        ▼
FastAPI Dashboard
        │
        ▼
LLM Trading Agent
        │
        ▼
Performance Evaluation
```

---

# 📈 Evaluation

The project evaluated both deterministic and AI-driven trading approaches.

The rule-based system established a stable baseline using momentum-based trading signals and ATR risk management.

The LLM implementation demonstrated the ability to reason over multiple technical indicators and market sentiment while making autonomous trading decisions.

Performance was continuously monitored through:

* Portfolio Value
* Profit
* Sharpe Ratio
* Maximum Drawdown
* Equity Curve
* Win/Loss Ratio
* Trade History

---

# 🎯 Conclusion

This project successfully demonstrated the development of a complete Bitcoin trading system capable of operating on both historical and live market data.

Beginning with a deterministic rule-based trading engine, the project established a reliable baseline using momentum-based signal generation and ATR-based risk management before progressing to a live trading environment with real-time monitoring through FastAPI.

A major contribution of the project was the exploration of Large Language Models as trading decision-makers. By replacing the traditional signal layer with **Ollama's Llama 3.1**, the project investigated how progressively richer market information—including Momentum, SMA, RSI, and the Bitcoin Fear & Greed Index—affected autonomous trading decisions.

The project highlights both the strengths and limitations of integrating LLMs into algorithmic trading systems. While deterministic strategies provide consistent execution, LLMs introduce greater flexibility by reasoning over multiple quantitative and qualitative market signals.

Overall, the project demonstrates a practical hybrid framework that combines traditional algorithmic trading with modern artificial intelligence techniques. The modular architecture provides a strong foundation for future work, including additional indicators, reinforcement learning, multi-strategy portfolio management, autonomous agent frameworks, advanced risk management, and support for multiple financial markets.
