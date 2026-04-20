from flask import Flask, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "FaidaAI API is running", "version": "1.0"})

@app.route("/stocks")
def get_stocks():
    if os.path.exists("stocks_data.json"):
        with open("stocks_data.json", "r") as f:
            stocks = json.load(f)
        return jsonify({
            "status": "success",
            "count": len(stocks),
            "data": stocks,
            "last_updated": datetime.now().isoformat()
        })
    return jsonify({"status": "success", "count": 0, "data": [], "message": "No data yet"})

@app.route("/stocks/<symbol>")
def get_stock(symbol):
    if os.path.exists("stocks_data.json"):
        with open("stocks_data.json", "r") as f:
            stocks = json.load(f)
        stock = next((s for s in stocks if s["symbol"].upper() == symbol.upper()), None)
        if stock:
            return jsonify({"status": "success", "data": stock})
    return jsonify({"status": "error", "message": "Stock not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)