from flask import Flask, jsonify
from flask_cors import CORS
import requests
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

MANSA_KEY = "mansa_live_sk_ljxlpzoi0arx74wr"
MANSA_BASE = "https://www.mansaapi.com/api/v1"
HEADERS = {"Authorization": f"Bearer {MANSA_KEY}"}

@app.route("/")
def home():
    return jsonify({"message": "FaidaAI API is running", "version": "1.0"})

@app.route("/stocks")
def get_stocks():
    try:
        res = requests.get(f"{MANSA_BASE}/stocks", params={"exchange": "NSE"}, headers=HEADERS, timeout=15)
        data = res.json()
        stocks = []
        for s in data.get("stocks", []):
            stocks.append({
                "symbol": s.get("ticker", ""),
                "name": s.get("name", ""),
                "price": str(s.get("price", "")),
                "change": str(s.get("change_pct", "")),
                "volume": str(s.get("volume", "")),
                "timestamp": datetime.now().isoformat()
            })
        return jsonify({
            "status": "success",
            "count": len(stocks),
            "data": stocks,
            "last_updated": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/stocks/<symbol>")
def get_stock(symbol):
    try:
        res = requests.get(f"{MANSA_BASE}/stocks/{symbol}", headers=HEADERS, timeout=15)
        data = res.json()
        stock = {
            "symbol": data.get("ticker", symbol),
            "name": data.get("name", ""),
            "price": str(data.get("price", "")),
            "change": str(data.get("change_pct", "")),
            "volume": str(data.get("volume", "")),
            "timestamp": datetime.now().isoformat()
        }
        return jsonify({"status": "success", "data": stock})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 404

@app.route("/movers")
def get_movers():
    try:
        res = requests.get(f"{MANSA_BASE}/movers/NSE", headers=HEADERS, timeout=15)
        data = res.json()
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)