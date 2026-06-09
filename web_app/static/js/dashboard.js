// =========================
// START BOT
// =========================
console.log("🔥 DASHBOARD JS LOADED");

function setText(id, value) {

    const el = document.getElementById(id);

    if (el) {
        el.innerText = value ?? 0;
    }
}


// =========================
// START
// =========================
window.startBot = async function () {

    console.log("🔥 START CLICKED");

    try {

        const res = await fetch("/start", {
            method: "POST"
        });

        const data = await res.json();

        console.log("✅ RESPONSE:", data);

        setText("status", "Status: " + data.status);

    } catch (err) {

        console.error("❌ START ERROR:", err);

    }
};


// =========================
// STOP
// =========================
window.stopBot = async function () {

    console.log("🛑 STOP CLICKED");

    try {

        const res = await fetch("/stop", {
            method: "POST"
        });

        const data = await res.json();

        console.log("✅ RESPONSE:", data);

        setText("status", "Status: " + data.status);

    } catch (err) {

        console.error("❌ STOP ERROR:", err);

    }
};


// =========================
// WEBSOCKET
// =========================
const socket = new WebSocket("ws://127.0.0.1:8001/ws");

socket.onopen = function () {

    console.log("🟢 WebSocket Connected");

};


// =========================
// LIVE DATA
// =========================
socket.onmessage = function (event) {

    const data = JSON.parse(event.data);

    // console.log("📡 LIVE DATA:", data);

    // =========================
    // SAFE UI UPDATES
    // =========================
    setText("runtime", data.runtime ?? "00:00:00");

    setText("start-capital", data.start_capital);
    setText("invested", data.invested);
    setText("cash", data.cash);

    setText("btc-holdings", data.btc_holdings);
    setText("portfolio-value", data.portfolio_value);
    setText("current-price", data.current_price);

    setText("entering-price", data.entering_price);
    setText("exit-price", data.exit_price);

    setText("total-trades", data.total_trades);
    setText("wins", data.wins);
    setText("losses", data.losses);

    setText("total-profit", data.total_profit);
    setText("max-drawdown", data.max_drawdown);

    setText("candle-processed", data.candle_processed);
    setText("sharpe-ratio", data.sharpe_ratio);

    setText("cagr", data.cagr);
    setText("expectancy", data.expectancy);
    setText("profit-factor", data.profit_factor);
    setText("exposure", data.exposure);

    // =========================
    // DEBUG
    // =========================
    setText("momentum-value", data.momentum);
    setText("sma-pct-value", data.sma_pct);
    setText("atr-pct-value", data.atr_pct);
    setText("rsi-value", data.rsi);
    setText("signal-value", data.signal ?? "HOLD");


    // =========================
    // TRANSACTION TABLE UPDATE
    // =========================
    const tradeBody = document.getElementById("trade-table-body");

    if (!tradeBody) return;

    const trades = data.trades || [];

    //console.log("📊 TRADES RECEIVED:", trades);

    if (trades.length === 0) {

        tradeBody.innerHTML = `
            <tr>
                <td colspan="5" class="text-secondary">
                    No Transactions Yet
                </td>
            </tr>
        `;

        return;
    }

    tradeBody.innerHTML = trades
        .slice()
        .reverse()
        .map(t => {

            const pnl = t.pnl !== undefined
                ? Number(t.pnl).toFixed(2)
                : "-";

            const price = t.price !== undefined
                ? Number(t.price).toFixed(2)
                : "-";

            const qty = t.qty !== undefined
                ? Number(t.qty).toFixed(6)
                : "-";

            return `
                <tr>

                    <td style="
                        color:${t.type === "BUY" ? "#00ff88" : "#ff4d4d"};
                        font-weight:bold;
                    ">
                        ${t.type}
                    </td>

                    <td>${price}</td>

                    <td>${qty}</td>

                    <td style="
                        color:${Number(t.pnl) >= 0 ? "#00ff88" : "#ff4d4d"};
                    ">
                        ${pnl}
                    </td>

                    <td>${t.index ?? "-"}</td>

                </tr>
            `;
        })
        .join("");
};


// =========================
// SOCKET CLOSE
// =========================
socket.onclose = function () {

    console.log("🔴 WebSocket Disconnected");

};


// =========================
// SOCKET ERROR
// =========================
socket.onerror = function (error) {

    console.error("❌ WebSocket Error:", error);

};