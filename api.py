from flask import Flask, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

def get_stocks_data():
    if os.path.exists("stocks_data.json"):
        with open("stocks_data.json", "r") as f:
            return json.load(f)
    return []

@app.route("/")
def home():
    return jsonify({"message": "FaidaAI API is running", "version": "1.0"})

@app.route("/stocks")
def get_stocks():
    stocks = get_stocks_data()
    return jsonify({
        "status": "success",
        "count": len(stocks),
        "data": stocks,
        "last_updated": datetime.now().isoformat()
    })

@app.route("/stocks/<symbol>")
def get_stock(symbol):
    stocks = get_stocks_data()
    stock = next((s for s in stocks if s["symbol"].upper() == symbol.upper()), None)
    if stock:
        return jsonify({"status": "success", "data": stock})
    return jsonify({"status": "error", "message": "Stock not found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)